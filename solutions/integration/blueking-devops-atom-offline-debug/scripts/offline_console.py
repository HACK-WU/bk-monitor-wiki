#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""蓝盾流水线插件「离线联调控制台」——本地模拟插件编排页 + mock 依赖接口 + 真跑插件。

用途
----
在没有蓝盾插件工作台权限（登不上 devops.oa.com）时，本地复刻插件编排页的行为：
按 ``task.json`` 动态渲染表单 -> 生成 ``input.json`` -> 真跑插件 -> 回显日志与输出。
同时把插件依赖的两个外部面 mock 掉：

* 前端面：``input.strategy_list.optionsConf.url``（selector 选项接口，浏览器侧）
* 进程面：``monitor_url`` 指向的 ``add_shield/`` / ``disable_shield/``（插件进程侧）

⚠️ 这是**本地模拟器，不是蓝盾前端的实现**。它按官方文档（插件配置规范 15009001、
开发规范 15009003、本地调试指引 17512739）复刻行为，用于自证「配置是否合法、mock 接口
是否符合 CORS 规范、插件与平台的数据契约是否对齐」。它**不能**证明蓝盾真实前端的
origin、附加请求头、渲染细节，这些必须在有权限后回平台实测。

SDK 契约（实证自 python_atom_sdk 1.2.19 源码，非推测）
-----------------------------------------------------
* 输入：``get_input()`` 读 ``$bk_data_dir/$bk_data_input``（默认 ``./input.json``）的 JSON
* 敏感配置：``get_sensitive_conf(key)`` 取 **input.json 里的 ``bkSensitiveConfInfo`` 字段**
* 流水线内置变量：同样来自 input.json（``BK_CI_START_USER_NAME`` / ``BK_CI_PIPELINE_UPDATE_USER``
  / ``BK_CI_PIPELINE_CREATE_USER`` ...）
* 输出：``set_output()`` 写 ``$bk_data_dir/$bk_data_output``（默认 ``./output.json``）
* 日志：``python_atom_sdk.log`` 走 stdout，带 ``##[level]`` 前缀
* ``.sdk.json`` 仅在调用 openapi（构件/通知）时才被读取，本插件不调，放一份只为保险

用法
----
    # 在插件工程内（脚本位于 <plugin>/devtools/）：
    python3 devtools/offline_console.py --listen 18081
    # 从别处运行副本时，显式指定插件工程根：
    python3 scripts/offline_console.py --repo /path/to/bk-monitor-shield --listen 18081

    浏览器打开 http://<本机地址>:18081/（console.html 需与脚本同目录）

路由
----
    GET  /                       模拟插件编辑页
    GET  /api/task-def           task.json + URL 改写表 + 运行环境信息
    GET  /api/requests           最近的请求日志（页面轮询）
    POST /api/run                按提交的 input 真跑插件（子进程）
    GET  /mock/strategy-list     模拟「接入网关后的第三方选项接口」
    POST /mock/add_shield/       模拟监控 add_shield
    POST /mock/disable_shield/   模拟监控 disable_shield
    GET  /health
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 插件工程根目录：默认取脚本上一级（脚本通常位于 <plugin>/devtools/）。
# 从 solution 目录运行副本时必须用 --repo 显式指定插件工程根。
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PAGE_FILE = os.path.join(SCRIPT_DIR, "console.html")
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
REQ_LOG_FILE = os.path.join(LOG_DIR, "requests.log")


def task_file():
    """task.json 路径随 REPO_ROOT 变化，故用函数而非模块常量。"""
    return os.path.join(REPO_ROOT, "task.json")

MAX_LOG_ENTRIES = 300

# 蓝盾请求可能携带的自定义头（官方 15009171 明确提到 x-devops-project-id）
CORS_ALLOW_HEADERS = (
    "Content-Type, X-Devops-Project-Id, X-Requested-With, "
    "Authorization, X-Bkapi-Authorization, X-Bkapi-Jwt"
)
CORS_ALLOW_METHODS = "GET, POST, PUT, PATCH, HEAD, DELETE, OPTIONS"

# mock 的策略列表：字段名与 task.json 的 optionsConf.paramId/paramName 对齐
MOCK_STRATEGIES = {
    "default": [
        {"optionId": "1540", "optionName": "CPU使用率过高（dev-mock）"},
        {"optionId": "1541", "optionName": "磁盘使用率过高（dev-mock）"},
        {"optionId": "1542", "optionName": "进程存活告警（dev-mock）"},
    ],
    "2": [
        {"optionId": "1540", "optionName": "CPU使用率过高（biz2-mock）"},
        {"optionId": "1541", "optionName": "磁盘使用率过高（biz2-mock）"},
    ],
    "3": [
        {"optionId": "9001", "optionName": "JVM GC 次数过高（biz3-mock）"},
    ],
}

# 进程面 mock：按接口分派的响应
MOCK_SHIELD_SEQ = {"value": 10000}

# --------------------------------------------------------------------------------------
# 屏蔽接口契约（源：monitor_web/shield/serializers.py + backend_resources.py，
# 以及 apigw resources yaml / compapi 的路径形态）
# --------------------------------------------------------------------------------------
SHIELD_CATEGORIES = ("scope", "strategy", "event", "alert", "dimension")
SHIELD_END_POLICIES = ("notify_once", "close")
# 源：bkmonitor/utils/range/__init__.py:24（含 include/exclude，没有 contain/not_contain）
SHIELD_METHODS = ("include", "exclude", "gt", "gte", "lt", "lte", "eq", "neq", "reg", "nreg")
SHIELD_CONDITIONS = ("or", "and")


def _as_int(value):
    """模拟 DRF IntegerField 的宽松转换：接受 int 或数字字符串（蓝盾页面传的是字符串）。"""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def _as_bool(value):
    """模拟 DRF BooleanField：接受 bool / 1 / 0 / 'true' / 'false'（大小写不敏感）。"""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, str)):
        lowered = str(value).strip().lower()
        if lowered in ("true", "1"):
            return True
        if lowered in ("false", "0"):
            return False
    return None


def _check_conditions(conditions, errors, path="dimension_config.dimension_conditions"):
    """校验维度条件列表（源：DimensionConditionSlz）。"""
    if not isinstance(conditions, list):
        errors.append("{} 必须是列表".format(path))
        return
    for idx, cond in enumerate(conditions):
        where = "{}[{}]".format(path, idx)
        if not isinstance(cond, dict):
            errors.append("{} 必须是对象".format(where))
            continue
        if not cond.get("key"):
            errors.append("{}.key 必填".format(where))
        value = cond.get("value")
        if not isinstance(value, list) or not value:
            errors.append("{}.value 必填且为非空列表".format(where))
        method = cond.get("method", "eq")
        if method not in SHIELD_METHODS:
            errors.append("{}.method={!r} 非法，合法值 {}".format(where, method, list(SHIELD_METHODS)))
        condition = cond.get("condition", "and")
        if condition not in SHIELD_CONDITIONS:
            errors.append("{}.condition={!r} 非法，合法值 {}".format(where, condition, list(SHIELD_CONDITIONS)))


def validate_shield_payload(body):
    """按真实后端序列化器校验新增屏蔽请求体，返回错误信息列表（空 = 合法）。

    刻意与 DRF **同等宽松**（不做比后端更严的校验），避免 mock 制造假失败；
    校验规则来源：BaseSerializer / ScopeSerializer / StrategySerializer / EventSerializer。
    """
    errors = []
    if _as_int(body.get("bk_biz_id")) is None:
        errors.append("bk_biz_id 必填且为整数")

    category = body.get("category")
    if category not in SHIELD_CATEGORIES:
        errors.append("category={!r} 非法，合法值 {}".format(category, list(SHIELD_CATEGORIES)))

    for field in ("begin_time", "end_time"):
        if not body.get(field):
            errors.append("{} 必填".format(field))

    if _as_bool(body.get("shield_notice")) is None:
        errors.append("shield_notice 必填且为布尔值")

    end_policy = body.get("end_policy", "notify_once")
    if end_policy not in SHIELD_END_POLICIES:
        errors.append("end_policy={!r} 非法，合法值 {}".format(end_policy, list(SHIELD_END_POLICIES)))
    elif end_policy == "close" and (category in ("event", "alert") or _as_bool(body.get("is_quick"))):
        # 源：serializers.py:55-60 BaseSerializer.validate
        errors.append("end_policy=close 不支持 event/alert 类或快捷屏蔽")

    cycle_config = body.get("cycle_config")
    if cycle_config is not None:
        if not isinstance(cycle_config, dict) or _as_int(cycle_config.get("type")) is None:
            errors.append("cycle_config.type 必填且为整数")

    dimension_config = body.get("dimension_config")
    if not isinstance(dimension_config, dict) or not dimension_config:
        errors.append("dimension_config 必填且为非空对象")
        return errors

    conditions = dimension_config.get("dimension_conditions")
    if category == "strategy":
        strategy_ids = dimension_config.get("id")
        if not isinstance(strategy_ids, list) or not strategy_ids:
            errors.append("dimension_config.id 必填且为非空列表（策略屏蔽）")
        elif any(_as_int(item) is None for item in strategy_ids):
            errors.append("dimension_config.id 元素必须为整数")
    elif category == "scope":
        if not dimension_config.get("scope_type"):
            errors.append("dimension_config.scope_type 必填（范围屏蔽）")
    elif category == "event":
        if not isinstance(dimension_config.get("id"), str) or not dimension_config.get("id"):
            errors.append("dimension_config.id 必填且为字符串（事件屏蔽）")
    elif category == "dimension":
        if not conditions:
            errors.append("dimension_config.dimension_conditions 必填（维度屏蔽）")
    elif category == "alert":
        match_keys = [k for k in dimension_config if not k.startswith("_") and k != "dimension_conditions"]
        if not match_keys and not conditions:
            errors.append("dimension_config 至少需要一个告警维度或 dimension_conditions（告警屏蔽）")

    if conditions is not None:
        _check_conditions(conditions, errors)
    return errors


def validate_disable_payload(body):
    """按 DisableShieldResource.RequestSerializer 校验解除屏蔽请求体。

    源的兼容点：`id` 声明为 list[int]，但 `to_internal_value` 会把非 list 标量包成单元素列表
    （backend_resources.py:607-613），因此插件直接传字符串 shield_id 也是合法的。
    """
    errors = []
    raw_id = body.get("id")
    if raw_id is None or raw_id == "" or raw_id == []:
        errors.append("id 必填（可为单个值或列表）")
    else:
        ids = raw_id if isinstance(raw_id, list) else [raw_id]
        if any(_as_int(item) is None for item in ids):
            errors.append("id 元素必须为整数（后端会先包成列表再用 IntegerField 转换）")
    if _as_bool(body.get("verify_user_permission")) and _as_int(body.get("bk_biz_id")) is None:
        errors.append("verify_user_permission=true 时 bk_biz_id 必填")
    return errors


def match_shield_action(path):
    """识别屏蔽接口（兼容三种真实路径族，便于验证任一种 monitor_url 形态）。

    * 插件原生后缀      : `.../add_shield/`、`.../disable_shield/`（推断为 compapi 形态）
    * compapi(ESB)      : `/api/c/compapi/v2/monitor_v3/add_shield/`
    * 蓝鲸网关 v4 对外   : `/app/shield/add/`、`/app/shield/disable/`
    """
    if path.endswith(("/add_shield", "/shield/add", "/v4/shield/add")):
        return "add_shield"
    if path.endswith(("/disable_shield", "/shield/disable", "/v4/shield/disable")):
        return "disable_shield"
    return None


# --------------------------------------------------------------------------------------
# 组件覆盖度（P0）：页面 console.html::buildControl 实际实现了哪些 type。
# 清单与页面的一致性由 selfcheck 用"grep 页面里的 type 分支"断言，防止两边漂移。
# --------------------------------------------------------------------------------------
EXPLICIT_TYPES = (
    "tips", "enum-input", "atom-checkbox", "selector",
    "select-input", "devops-select", "vuex-textarea",
)
# 与 fallback（单行文本框）语义等价，故页面故意不写专属分支
GENERIC_INPUT_TYPES = ("vuex-input",)
RENDERED_TYPES = EXPLICIT_TYPES + GENERIC_INPUT_TYPES
# 有专属语义但页面未实现 → 降级为单行文本框：不崩、但保真度不足
DEGRADED_TYPES = (
    "atom-checkbox-list", "atom-ace-editor", "time-picker", "cron-timer",
    "staff-input", "company-staff-input", "parameter",
    "dynamic-parameter", "dynamic-parameter-simple",
)


def task_renderer_coverage(task):
    """统计 task.json 用到的组件类型与页面实现清单的差距。"""
    used = sorted({(field or {}).get("type") for field in (task.get("input") or {}).values() if (field or {}).get("type")})
    return {
        "explicit": list(EXPLICIT_TYPES),
        "genericInput": list(GENERIC_INPUT_TYPES),
        "rendered": list(RENDERED_TYPES),
        "degraded": list(DEGRADED_TYPES),
        "used": used,
        "degradedInTask": [t for t in used if t in DEGRADED_TYPES],
        "unknown": [t for t in used if t not in RENDERED_TYPES and t not in DEGRADED_TYPES],
    }


# --------------------------------------------------------------------------------------
# 平台侧校验模拟（严格模式用）：rely 可见性 + required + rule（配置规范 15009001）
# --------------------------------------------------------------------------------------
def evaluate_rely(field, values):
    """复刻蓝盾 rely 显隐判定。

    ⚠️ 与 console.html::relySatisfied 是**同一条规则的两份实现**（有意重复）：页面要做即时
    显隐不能每次都请求服务端，服务端要做提交校验不能依赖浏览器。selfcheck 用
    AND/OR/NOT + value/regex 用例钉住本实现。
    """
    rely = (field or {}).get("rely")
    if not rely or not rely.get("expression"):
        return True
    results = []
    for expr in rely["expression"]:
        actual = values.get(expr.get("key"))
        if "regex" in expr:
            try:
                # JS 的 RegExp.test() 是"部分匹配"，故用 re.search 而非 fullmatch
                results.append(re.search(expr["regex"], "" if actual is None else str(actual)) is not None)
            except re.error:
                results.append(False)
        else:
            results.append(str(actual) == str(expr.get("value")))
    op = str(rely.get("operation", "AND")).upper()
    if op == "OR":
        return any(results)
    if op == "NOT":
        return not any(results)
    return all(results)


def validate_field_rule(field, value):
    """按 rule 校验单个字段（alpha/numeric/alpha_dash/alpha_num/min/max/regex）。"""
    rule = (field or {}).get("rule") or {}
    if not rule:
        return []
    text = "" if value is None else str(value)
    # 空值且非必填 → 跳过（平台对可选字段留空不做格式校验；必填缺失由 validate_input 报）
    if text == "" and not field.get("required"):
        return []

    errors = []
    if rule.get("alpha") and not text.isalpha():
        errors.append("只允许英文字符")
    if rule.get("numeric") and not text.isdigit():
        errors.append("只允许数字")
    if rule.get("alpha_dash") and re.fullmatch(r"[A-Za-z0-9_-]*", text) is None:
        errors.append("只允许英文、数字、下划线、中划线")
    if rule.get("alpha_num") and re.fullmatch(r"[A-Za-z0-9]*", text) is None:
        errors.append("只允许英文和数字")
    if isinstance(rule.get("min"), int) and len(text) < rule["min"]:
        errors.append("长度不能小于 {}".format(rule["min"]))
    if isinstance(rule.get("max"), int) and len(text) > rule["max"]:
        errors.append("长度不能大于 {}".format(rule["max"]))
    if rule.get("regex"):
        # 用 search 而非 fullmatch：配置规范 15009001 的示例是 `"regex": "^[0-9]"` +
        # "正则匹配以数字开头的字符串"，即**部分匹配**语义（fullmatch 会把 "1x" 误判为不合法）
        try:
            if re.search(rule["regex"], text) is None:
                errors.append("不匹配正则 {}".format(rule["regex"]))
        except re.error as exc:
            errors.append("rule.regex 非法：{}".format(exc))
    return errors


def validate_input(payload, task):
    """模拟平台提交前校验：只校验 **rely 可见** 字段的 required 与 rule。

    与平台的差异：官方文档未说明隐藏字段是否参与校验，此处按"仅校验可见字段"实现
    （这也让 `shield_mode=unshielded` 时隐藏的 `duration` 不再被误报）。
    """
    errors = []
    values = payload or {}
    for name, field in (task.get("input") or {}).items():
        if not evaluate_rely(field, values):
            continue
        value = values.get(name)
        if field.get("required") and (value is None or str(value) == ""):
            errors.append({"field": name, "message": "必填项未填写"})
            continue
        for message in validate_field_rule(field, value):
            errors.append({"field": name, "message": message})
    return errors

_request_log = deque(maxlen=MAX_LOG_ENTRIES)
_log_lock = threading.Lock()


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def record(kind, method, path, headers, body):
    """记录一次请求（内存环形缓冲 + 落盘），页面据此确认「谁在调、带了什么头」。"""
    entry = {
        "ts": _now(),
        "kind": kind,
        "method": method,
        "path": path,
        "origin": headers.get("Origin", ""),
        "project_id": headers.get("X-Devops-Project-Id", ""),
        "content_type": headers.get("Content-Type", ""),
        "user_agent": (headers.get("User-Agent", "") or "")[:120],
        "body": body,
    }
    with _log_lock:
        _request_log.append(entry)
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            with open(REQ_LOG_FILE, "a", encoding="utf-8") as fp:
                fp.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass
    print("[{ts}] {kind:<10} {method} {path} origin={origin!r} body={body}".format(
        ts=entry["ts"], kind=kind, method=method, path=path, origin=entry["origin"],
        body=(json.dumps(body, ensure_ascii=False)[:200] if body else "-")), flush=True)
    return entry


def load_task():
    with open(task_file(), "r", encoding="utf-8") as fp:
        return json.load(fp)


def build_task_def(port):
    """返回页面渲染所需的全部上下文。"""
    task = load_task()
    overrides = {}
    for name, field in (task.get("input") or {}).items():
        conf = field.get("optionsConf") or {}
        url = conf.get("url")
        if url:
            # 保留 {bk_biz_id} 占位符，演示平台的变量替换行为
            overrides[url] = "/mock/strategy-list/?bk_biz_id={bk_biz_id}"
    return {
        "task": task,
        "urlOverrides": overrides,
        "renderer": task_renderer_coverage(task),
        "mock": {
            "monitorUrl": "http://127.0.0.1:{}/mock/".format(port),
            "strategyList": "/mock/strategy-list/",
        },
        "runner": {
            "venvPython": venv_python(),
            "venvPythonExists": os.path.exists(venv_python()),
            "sdkInstalled": _sdk_installed(),
        },
    }


def venv_python():
    return os.path.join(REPO_ROOT, ".venv", "bin", "python")


def _sdk_installed():
    for candidate in (venv_python(), sys.executable):
        if not os.path.exists(candidate):
            continue
        probe = subprocess.run(
            [candidate, "-c", "import python_atom_sdk, ply; print('ok')"],
            capture_output=True, text=True,
        )
        if probe.returncode == 0:
            return True
    return False


def run_plugin(payload, timeout=90):
    """按 SDK 契约真跑插件：写 input.json -> 设 bk_data_* 环境变量 -> 子进程执行。"""
    python = venv_python() if os.path.exists(venv_python()) else sys.executable
    run_root = tempfile.mkdtemp(prefix="shield-offline-run-")
    data_dir = os.path.join(run_root, "data")
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, "input.json"), "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    # .sdk.json 仅 openapi 调用需要，放一份避免 SDK 提前退出
    sdk_json = {
        "buildType": "DOCKER", "projectId": "232", "agentId": "local-debug",
        "secretKey": "local-debug", "gateway": "127.0.0.1", "buildId": "local-debug",
        "vmSeqId": "local-debug",
    }
    with open(os.path.join(data_dir, ".sdk.json"), "w", encoding="utf-8") as fp:
        json.dump(sdk_json, fp, indent=2)

    env = os.environ.copy()
    env.update({
        "bk_data_dir": data_dir,
        "bk_data_input": "input.json",
        "bk_data_output": "output.json",
        "PYTHONPATH": REPO_ROOT + os.pathsep + env.get("PYTHONPATH", ""),
        "PYTHONIOENCODING": "utf-8",
    })

    started = time.time()
    try:
        proc = subprocess.run(
            [python, "-c", "from bk_monitor_shield.command_line import main; main()"],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=timeout,
        )
        returncode, stdout, stderr, timed_out = proc.returncode, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired as exc:
        returncode, timed_out = -9, True
        stdout = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = "TIMEOUT after {}s".format(timeout)

    output = None
    output_path = os.path.join(data_dir, "output.json")
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as fp:
                output = json.load(fp)
        except (OSError, ValueError) as exc:
            output = {"_parseError": str(exc)}

    return {
        "ok": returncode == 0,
        "returncode": returncode,
        "timedOut": timed_out,
        "duration": round(time.time() - started, 3),
        "python": python,
        "dataDir": data_dir,
        "stdout": stdout,
        "stderr": stderr,
        "output": output,
        "input": payload,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "BkAtomOfflineConsole/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # 静音默认访问日志，改用结构化记录
        return

    # ---------- CORS ----------

    def _cors_headers(self):
        origin = self.headers.get("Origin") or "*"
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": CORS_ALLOW_METHODS,
            "Access-Control-Allow-Headers": CORS_ALLOW_HEADERS,
            "Access-Control-Max-Age": "600",
            "Vary": "Origin",
        }

    def _send(self, status, body, content_type="application/json; charset=utf-8", extra=None):
        if isinstance(body, (dict, list)):
            raw = json.dumps(body, ensure_ascii=False, indent=2).encode("utf-8")
        elif isinstance(body, str):
            raw = body.encode("utf-8")
        else:
            raw = body
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        for key, val in (extra or {}).items():
            self.send_header(key, val)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return {"_raw": raw.decode("utf-8", "replace")}

    def _query(self):
        return parse_qs(urlparse(self.path).query)

    # ---------- HTTP verbs ----------

    def do_OPTIONS(self):
        # 真实网关当前对 OPTIONS 直接 404（实测 1640401 API not found），模拟器显式做对预检
        record("preflight", "OPTIONS", self.path, self.headers, None)
        self._send(204, b"", extra=self._cors_headers())

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            return self._serve_page()
        if path == "/health":
            return self._send(200, {"ok": True, "ts": _now()})
        if path == "/api/task-def":
            return self._send(200, build_task_def(self.server.server_port))
        if path == "/api/requests":
            with _log_lock:
                items = list(_request_log)
            return self._send(200, {"ok": True, "count": len(items), "items": items})
        if path == "/api/renderer-coverage":
            task = load_task()
            return self._send(200, task_renderer_coverage(task))
        if path.rstrip("/") == "/mock/strategy-list":
            return self._mock_strategy_list()
        # 便于浏览器直接点开时看到提示，而不是 404 空白
        return self._send(404, {"ok": False, "error": "not found", "path": path})

    def do_POST(self):
        path = urlparse(self.path).path.rstrip("/")
        if path == "/api/run":
            body = self._read_json_body() or {}
            payload = body.get("input") or {}
            record("run-plugin", "POST", self.path, self.headers, {"input": payload})
            try:
                result = run_plugin(payload, timeout=int(body.get("timeout") or 90))
            except OSError as exc:
                return self._send(500, {"ok": False, "error": "run failed: {}".format(exc)})
            return self._send(200, result)
        action = match_shield_action(path)
        if action:
            return self._mock_shield(action)
        if path == "/api/validate":
            # 严格模式下由页面调用；`task` 可覆盖（便于用合成定义自测校验器）
            body = self._read_json_body() or {}
            task = body.get("task") or load_task()
            payload = body.get("input") or {}
            errors = validate_input(payload, task)
            record("validate", "POST", self.path, self.headers, {"fieldCount": len(payload), "errorCount": len(errors)})
            return self._send(200, {"ok": not errors, "errors": errors})
        return self._send(404, {"ok": False, "error": "not found", "path": path})

    # ---------- handlers ----------

    def _serve_page(self):
        if not os.path.exists(PAGE_FILE):
            return self._send(500, {"ok": False, "error": "缺少 {}".format(PAGE_FILE)})
        with open(PAGE_FILE, "r", encoding="utf-8") as fp:
            html = fp.read()
        return self._send(200, html, content_type="text/html; charset=utf-8")

    def _mock_strategy_list(self):
        """模拟「第三方 API 接入蓝鲸网关」后的选项接口：{status, data, message}。"""
        params = self._query()
        biz_id = (params.get("bk_biz_id") or ["default"])[0]
        record("selector-options", "GET", self.path, self.headers, {"bk_biz_id": biz_id})
        data = MOCK_STRATEGIES.get(biz_id, MOCK_STRATEGIES["default"])
        return self._send(200, {"status": 0, "data": data, "message": ""},
                          extra=self._cors_headers())

    def _mock_shield(self, action):
        """按真实屏蔽接口契约 mock：先按序列化器校验，再返回 {result,code,message,data}。"""
        body = self._read_json_body() or {}
        record("monitor-api", "POST", self.path, self.headers, body)

        errors = validate_shield_payload(body) if action == "add_shield" else validate_disable_payload(body)
        if errors:
            # 与真实网关一致的失败形态：HTTP 400 + result=false（插件侧 deal_error 会按用户配置错误退出）
            return self._send(400, {
                "result": False, "code": 1640001, "code_name": "INVALID_ARGS",
                "message": "Parameters error [reason=\"{}\"]".format("; ".join(errors)),
                "data": None,
            }, extra=self._cors_headers())

        if action == "add_shield":
            MOCK_SHIELD_SEQ["value"] += 1
            # 契约：AddShieldResource 返回 {"id": int}；插件读 r.json()["data"]["id"]
            return self._send(200, {"result": True, "code": 0, "message": "mock ok",
                                    "data": {"id": MOCK_SHIELD_SEQ["value"]}},
                              extra=self._cors_headers())
        # 契约：DisableShieldResource 返回 "success"（插件只校验 result 为真）
        return self._send(200, {"result": True, "code": 0, "message": "mock ok", "data": "success"},
                          extra=self._cors_headers())


def main():
    parser = argparse.ArgumentParser(description="蓝盾插件离线联调控制台")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址（默认 0.0.0.0，便于端口转发访问）")
    parser.add_argument("--listen", "--port", dest="port", type=int, default=18081, help="监听端口")
    parser.add_argument(
        "--repo", default=None,
        help="插件工程根目录（默认取脚本上一级）。把本脚本拷贝到 solution/scripts/ 下运行时必须指定",
    )
    args = parser.parse_args()

    global REPO_ROOT
    if args.repo:
        REPO_ROOT = os.path.abspath(args.repo)

    if not os.path.exists(task_file()):
        print("找不到 task.json: {}（用 --repo 指定插件工程根）".format(task_file()), file=sys.stderr)
        return 1

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print("=" * 78)
    print("蓝盾插件离线联调控制台（本地模拟器，非蓝盾实现）")
    print("  插件工程 : {}".format(REPO_ROOT))
    print("  页面     : http://127.0.0.1:{}/".format(args.port))
    print("  运行解释器: {}{}".format(venv_python(), "" if os.path.exists(venv_python()) else "  ❌ 不存在"))
    print("  SDK/ply  : {}".format("已安装" if _sdk_installed() else "❌ 未安装（无法真跑插件）"))
    print("  请求日志 : {}".format(REQ_LOG_FILE))
    print("=" * 78, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    return 0


if __name__ == "__main__":
    sys.exit(main())
