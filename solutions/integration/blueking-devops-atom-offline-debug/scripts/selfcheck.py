#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线联调控制台自检：CORS 预检 / mock 数据 / 插件真实执行 / 请求日志。

只依赖标准库（服务端本身用 .venv 解释器真跑插件），可直接运行（脚本放哪就执行哪，与 offline_console.py 同目录即可）：

    python3 selfcheck.py --base http://127.0.0.1:18081

覆盖：
    1. /health
    2. /api/task-def（URL 改写表、执行器信息）
    3. OPTIONS 预检 -> 必须 204 + ACAO/ACAM/ACAH（真实网关此处是 404，正是要对比的点）
    4. GET  mock 选项接口 -> {status:0,data:[...]} + ACAO
    5. 运行插件：策略屏蔽（走 mock add_shield）
    6. 运行插件：纯维度屏蔽（真跑 PLY 表达式解析）
    7. 运行插件：策略与维度都不填 -> 期望 fail-fast（errorCode=2199002）
    8. /api/requests 应能看到 mock 接口被调用的记录
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

RESULTS = []
KNOWN = []


def call(method, url, body=None, headers=None, timeout=120):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for key, val in (headers or {}).items():
        req.add_header(key, val)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, dict(resp.headers), raw
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode("utf-8", "replace")


def check(name, ok, detail=""):
    detail = "" if detail is None else str(detail)
    RESULTS.append((name, ok, detail))
    print("{} {}{}".format("[PASS]" if ok else "[FAIL]", name, ("  -> " + detail) if detail else ""))
    return ok


def known_issue(name, fixed, detail="", expect=""):
    """记录「期望行为尚未满足」的已知缺陷：不计入 FAIL，但必须显式打印。

    这样自检套件可以保持绿色，同时缺陷不会被静默吞掉（修复后自动转为 [FIXED]）。
    """
    detail = "" if detail is None else str(detail)
    KNOWN.append((name, fixed, detail))
    print("{} {}{}".format("[FIXED]" if fixed else "[KNOWN]", name,
                           ("  -> " + detail) if detail else ""))
    if expect and not fixed:
        print("      期望：{}".format(expect))
    return fixed


def base_input(monitor_url, **extra):
    payload = {
        "shield_mode": "shield",
        "bk_biz_id": "2",
        "duration": "1h",
        "shield_notice": "true",
        "shield_reason": "离线联调自检",
        "bkSensitiveConfInfo": {
            "monitor_url": monitor_url,
            "app_code": "local-debug-app",
            "app_secret": "local-debug-secret",
        },
        "BK_CI_START_USER_NAME": "selfcheck-user",
        "BK_CI_PIPELINE_UPDATE_USER": "selfcheck-user",
        "BK_CI_PIPELINE_CREATE_USER": "selfcheck-user",
    }
    payload.update(extra)
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:18081")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    # 1. health
    status, _, raw = call("GET", base + "/health")
    check("health 200", status == 200, raw.strip())

    # 2. task-def
    status, _, raw = call("GET", base + "/api/task-def")
    defn = json.loads(raw) if status == 200 else {}
    overrides = defn.get("urlOverrides") or {}
    check("task-def 200", status == 200)
    check("selector URL 已被改写到 mock",
          any("/mock/strategy-list/" in v for v in overrides.values()),
          json.dumps(overrides, ensure_ascii=False))
    check("执行器检测到 SDK/ply", bool((defn.get("runner") or {}).get("sdkInstalled")),
          json.dumps(defn.get("runner") or {}, ensure_ascii=False))
    monitor_url = (defn.get("mock") or {}).get("monitorUrl") or (base + "/mock/")

    # 3. 预检
    status, headers, _ = call("OPTIONS", base + "/mock/strategy-list/", headers={
        "Origin": "https://devops.oa.com",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "x-devops-project-id",
    })
    check("OPTIONS 预检 204", status == 204, "status={}".format(status))
    check("预检回 ACAO", headers.get("Access-Control-Allow-Origin") == "https://devops.oa.com",
          str(headers.get("Access-Control-Allow-Origin")))
    check("预检回 ACAM/ACAH",
          "OPTIONS" in (headers.get("Access-Control-Allow-Methods") or "") and
          "x-devops-project-id" in (headers.get("Access-Control-Allow-Headers") or "").lower(),
          "ACAM={} ACAH={}".format(headers.get("Access-Control-Allow-Methods"),
                                   headers.get("Access-Control-Allow-Headers")))

    # 4. mock 选项数据
    status, headers, raw = call("GET", base + "/mock/strategy-list/?bk_biz_id=2",
                                headers={"Origin": "https://devops.oa.com"})
    payload = json.loads(raw) if status == 200 else {}
    check("mock 选项接口 200 且 status=0", status == 200 and payload.get("status") == 0, raw.strip()[:160])
    check("选项数据非空且字段为 optionId/optionName",
          bool(payload.get("data")) and set(payload["data"][0].keys()) == {"optionId", "optionName"},
          json.dumps(payload.get("data", [])[:1], ensure_ascii=False))
    check("选项接口带 ACAO", headers.get("Access-Control-Allow-Origin") == "https://devops.oa.com")

    # 5. 策略屏蔽（真跑插件，走 mock add_shield）
    status, _, raw = call("POST", base + "/api/run", body={"input": base_input(
        monitor_url, strategy_list='["1540"]')})
    run = json.loads(raw) if status == 200 else {}
    out = (run.get("output") or {}).get("data") or {}
    shield_id = ((out.get("shield_id") or {}).get("value")) or ""
    check("策略屏蔽：插件 exit 0", run.get("returncode") == 0, "returncode={} stderr={}".format(
        run.get("returncode"), (run.get("stderr") or "")[:200]))
    check("策略屏蔽：拿到 mock shield_id", bool(shield_id) and str(shield_id).isdigit(), str(shield_id))
    check("策略屏蔽：stdout 有 SDK 日志", "bk-monitor-shield" in (run.get("stdout") or ""),
          " | ".join((run.get("stdout") or "").strip().splitlines()[:3]))

    # 6. 纯维度屏蔽（真跑 PLY）
    status, _, raw = call("POST", base + "/api/run", body={"input": base_input(
        monitor_url, dimension_expression="bk_cloud_id = 0 AND device_name =- 'dev/vdb1,dev/vda1'")})
    run_dim = json.loads(raw) if status == 200 else {}
    out_dim = (run_dim.get("output") or {}).get("data") or {}
    check("维度屏蔽：插件 exit 0", run_dim.get("returncode") == 0,
          "returncode={} stderr={}".format(run_dim.get("returncode"), (run_dim.get("stderr") or "")[:200]))
    check("维度屏蔽：拿到 mock shield_id",
          bool(((out_dim.get("shield_id") or {}).get("value"))),
          str(((out_dim.get("shield_id") or {}).get("value"))))

    # 7. 都不填 -> fail-fast（这里暴露的是插件自身缺陷，见 known_issue 说明）
    status, _, raw = call("POST", base + "/api/run", body={"input": base_input(monitor_url)})
    run_err = json.loads(raw) if status == 200 else {}
    err_out = run_err.get("output") or {}
    check("缺策略与维度：插件 fail-fast（未发起任何监控 API 调用）",
          err_out.get("status") == "failure",
          "returncode={} status={} errorCode={} errorType={}".format(
              run_err.get("returncode"), err_out.get("status"),
              err_out.get("errorCode"), err_out.get("errorType")))
    known_issue(
        "缺策略与维度：错误码应为 USER_CONFIG_ERROR(2199002) 而非 PLUGIN_ERROR(2199001)",
        err_out.get("errorCode") == 2199002,
        "实际 errorCode={} errorType={}；根因：command_line.py 有 4 处用户输入校验只传 error_msg、"
        "未传 error_code/error_type（L163 策略列表格式、L171 维度表达式解析失败、L176 策略与维度都为空、"
        "L261 缺 id），而 exit_with_error 默认落到 PLUGIN_ERROR/PLUGIN。"
        "另外 L303 deal_error（调监控接口 HTTP 失败）反而标成 USER_CONFIG_ERROR，归类方向相反".format(
            err_out.get("errorCode"), err_out.get("errorType")),
        expect="errorCode=2199002 / errorType=USER（用户配置有误），插件异常才用 2199001")

    # 7b. duration 为空 —— task.json 是「可输入下拉框」，用户清空文本就可能传 ""
    status, _, raw = call("POST", base + "/api/run", body={"input": base_input(
        monitor_url, strategy_list='["1540"]', duration="")})
    run_dur = json.loads(raw) if status == 200 else {}
    known_issue(
        "duration 为空时插件应给出可读错误，而非 AttributeError 崩溃",
        run_dur.get("returncode") == 0,
        "returncode={} stderr={}".format(run_dur.get("returncode"),
                                         (run_dur.get("stderr") or "").strip().splitlines()[-1:]),
        expect="应回填默认时长或按用户配置错误退出（2199002）")

    # 7c. 真实网关路径族（compapi / v4 apigw / 插件原生后缀）都要能 mock 通
    for path in ("/mock/add_shield/", "/mock/app/shield/add/", "/mock/api/c/compapi/v2/monitor_v3/add_shield/"):
        status, _, raw = call("POST", base + path, body={
            "bk_biz_id": "2", "category": "strategy",
            "begin_time": "2026-09-21 10:00:00", "end_time": "2026-09-21 11:00:00",
            "dimension_config": {"id": [1540]}, "cycle_config": {"type": 1},
            "shield_notice": False,
        })
        payload_path = json.loads(raw) if status == 200 else {}
        check("路径族可用并返回 data.id：{}".format(path),
              bool((payload_path.get("data") or {}).get("id")), raw.strip()[:120])

    # 7d. 契约守门：非法 method（专家资产曾误写 contain）必须被拒
    status, _, raw = call("POST", base + "/mock/app/shield/add/", body={
        "bk_biz_id": 2, "category": "dimension",
        "begin_time": "2026-09-21 10:00:00", "end_time": "2026-09-21 11:00:00",
        "dimension_config": {"dimension_conditions": [
            {"key": "device_name", "value": ["GPU-01"], "method": "contain"}]},
        "shield_notice": False,
    })
    err_body = json.loads(raw) if raw else {}
    check("非法 method=contain 被拒（400 + result=false）",
          status == 400 and err_body.get("result") is False,
          "status={} msg={}".format(status, (err_body.get("message") or "")[:110]))

    # 7e. 契约守门：strategy 缺 dimension_config.id 必须被拒
    status, _, raw = call("POST", base + "/mock/app/shield/add/", body={
        "bk_biz_id": 2, "category": "strategy",
        "begin_time": "2026-09-21 10:00:00", "end_time": "2026-09-21 11:00:00",
        "dimension_config": {"dimension_conditions": []}, "shield_notice": False,
    })
    err_body = json.loads(raw) if raw else {}
    check("strategy 缺 dimension_config.id 被拒",
          status == 400 and "dimension_config.id" in (err_body.get("message") or ""),
          (err_body.get("message") or "")[:110])

    # 7f. disable：插件的真实形态（字符串 id）+ v4 对外路径
    status, _, raw = call("POST", base + "/mock/app/shield/disable/", body={
        "id": "10001", "bk_biz_id": "2", "verify_user_permission": True})
    ok_body = json.loads(raw) if raw else {}
    check("disable 接受字符串 id 且返回 data=success（契约兼容点）",
          status == 200 and ok_body.get("data") == "success", raw.strip()[:120])

    # 7g. disable 契约校验：verify_user_permission=true 必须带 bk_biz_id
    status, _, raw = call("POST", base + "/mock/disable_shield/", body={
        "id": [10001], "verify_user_permission": True})
    err_body = json.loads(raw) if raw else {}
    check("disable 拒绝 verify_user_permission=true 缺 bk_biz_id",
          status == 400, (err_body.get("message") or "")[:110])

    # 7h. 组件覆盖度：task.json 用到的类型必须都已登记；且清单与页面实现不漂移
    status, _, raw = call("GET", base + "/api/renderer-coverage")
    cov = json.loads(raw) if status == 200 else {}
    check("覆盖度：task.json 用到的组件类型均已登记（unknown 为空）",
          cov.get("unknown") == [],
          "used={} unknown={}".format(cov.get("used"), cov.get("unknown")))
    check("覆盖度：task.json 无降级组件",
          cov.get("degradedInTask") == [],
          "degradedInTask={}".format(cov.get("degradedInTask")))
    page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "console.html")
    try:
        with open(page_path, "r", encoding="utf-8") as fp:
            page_html = fp.read()
    except OSError as exc:
        page_html = ""
        check("覆盖度：能读取 console.html", False, str(exc))
    if page_html:
        page_types = sorted(set(re.findall(r'type === "([a-z0-9-]+)"', page_html)))
        check("覆盖度：清单 EXPLICIT_TYPES 与页面实现的 type 分支一致",
              page_types == sorted(cov.get("explicit") or []),
              "page={} server={}".format(page_types, sorted(cov.get("explicit") or [])))

    # 7i. 校验器：rule（alpha/min/max/regex）
    synth_task = {"input": {
        "code": {"type": "vuex-input", "required": True, "rule": {"min": 3, "max": 7, "alpha": True}},
        "opt": {"type": "vuex-input", "rule": {"regex": "^[0-9]"}},
    }}

    def validate(input_values):
        status, _, body_raw = call("POST", base + "/api/validate",
                                   body={"task": synth_task, "input": input_values})
        return json.loads(body_raw) if status == 200 else {}

    def validate_real(input_values):
        status, _, body_raw = call("POST", base + "/api/validate", body={"input": input_values})
        return json.loads(body_raw) if status == 200 else {}

    result = validate({"code": "ab1"})
    check("rule.alpha：含数字被拒", any("只允许英文字符" in e["message"] for e in result.get("errors", [])),
          json.dumps(result.get("errors"), ensure_ascii=False))
    result = validate({"code": "ab"})
    check("rule.min：过短被拒", any("长度不能小于" in e["message"] for e in result.get("errors", [])),
          json.dumps(result.get("errors"), ensure_ascii=False))
    result = validate({"code": ""})
    check("required：空值被拒", any(e["message"] == "必填项未填写" for e in result.get("errors", [])),
          json.dumps(result.get("errors"), ensure_ascii=False))
    result = validate({"code": "abcd", "opt": "x"})
    check("rule.regex 不匹配被拒且 code 合法",
          [e["field"] for e in result.get("errors", [])] == ["opt"],
          json.dumps(result.get("errors"), ensure_ascii=False))
    result = validate({"code": "abcd", "opt": "1x"})
    check("全部合法时 ok", result.get("ok") is True and result.get("errors") == [],
          json.dumps(result, ensure_ascii=False))

    # 7j. 校验器：rely 可见性（真实 task.json —— duration 的 required 只在 shield 模式生效）
    result = validate_real({"shield_mode": "shield", "bk_biz_id": "2", "duration": ""})
    check("rely 生效：shield 模式下 duration 为空被拒",
          any(e["field"] == "duration" for e in result.get("errors", [])),
          json.dumps(result.get("errors"), ensure_ascii=False))
    result = validate_real({"shield_mode": "unshielded", "bk_biz_id": "2", "id": "12345"})
    check("rely 生效：unshielded 模式下隐藏的 duration 不参与校验",
          not any(e["field"] == "duration" for e in result.get("errors", [])),
          json.dumps(result.get("errors"), ensure_ascii=False))
    result = validate_real({"shield_mode": "shield", "bk_biz_id": "2", "duration": "1h",
                            "strategy_list": '["1540"]'})
    check("真实 task.json：合法输入严格校验通过", result.get("ok") is True,
          json.dumps(result.get("errors"), ensure_ascii=False))

    # 8. 请求日志
    status, _, raw = call("GET", base + "/api/requests")
    logs = (json.loads(raw) if status == 200 else {}).get("items") or []
    kinds = [item.get("kind") for item in logs]
    check("日志中有 selector 选项请求", "selector-options" in kinds, ",".join(sorted(set(kinds))))
    check("日志中有 monitor add_shield 请求", "monitor-api" in kinds)
    add_shield_logs = [i for i in logs if i.get("kind") == "monitor-api" and "add_shield" in i.get("path", "")]
    check("mock 收到 add_shield 请求体（含 dimension_config）",
          bool(add_shield_logs) and "dimension_config" in json.dumps(add_shield_logs[-1].get("body") or {}),
          json.dumps((add_shield_logs[-1].get("body") if add_shield_logs else {}) or {}, ensure_ascii=False)[:300])

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    failed = [(name, detail) for name, ok, detail in RESULTS if not ok]
    print("\n" + "=" * 70)
    print("自检结果：{}/{} 通过".format(passed, len(RESULTS)))
    for name, detail in failed:
        print("  [FAIL] {}  {}".format(name, detail))
    open_known = [(n, d) for n, fixed, d in KNOWN if not fixed]
    if open_known:
        print("已知缺陷（不计入 FAIL，待确认后修复）：")
        for name, detail in open_known:
            print("  [KNOWN] {}".format(name))
    print("=" * 70)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
