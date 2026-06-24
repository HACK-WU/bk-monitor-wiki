#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BK-Monitor 接口测试器（api-tester）

在 Django 进程内直接调用 Resource 类，实现类似自动化 Postman 的接口测试：
  URL + Method → 解析出 Resource 类 → 自动提取参数 schema → 执行 / 校验

依赖 bkmonitor 的 Django 环境（脚本自动通过 hello.py 初始化）。
必须使用项目虚拟环境 Python 运行：
  /root/bk-monitor/bkmonitor/.venv/bin/python api_tester.py ...

子命令：
  inspect  <url> <method>            解析接口，输出 Resource 信息 + 参数 schema + 示例参数
  dry-run  <url> <method> -p JSON    仅校验请求参数，不执行 perform_request
  run      <url> <method> [-p JSON]  完整执行（非 GET 需 --confirm）

示例：
  api_tester.py inspect /rest/v2/data_explorer/get_graph_query_config/ POST
  api_tester.py run /rest/v2/duty_plan/preview_duty_rule_plan/ POST -p '{"days":7}' --confirm
"""
import os
import sys
import json
import time
import traceback

# --- 初始化 Django 环境（自动定位含 hello.py 的项目根目录）---
_BK_ROOT = os.environ.get("BK_MONITOR_ROOT")
if not _BK_ROOT:
    _p = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.exists(os.path.join(_p, "hello.py")):
            _BK_ROOT = _p
            break
        _p = os.path.dirname(_p)
if _BK_ROOT and _BK_ROOT not in sys.path:
    sys.path.insert(0, _BK_ROOT)
try:
    import hello  # noqa: F401  触发 django.setup()
except Exception as e:  # pragma: no cover
    print(json.dumps(
        {
            "status": "env_error",
            "message": f"初始化 Django 环境失败: {e}",
            "hint": "请用 bkmonitor 的 venv python 运行；如项目根非默认路径，设置 BK_MONITOR_ROOT 环境变量",
        },
        ensure_ascii=False,
    ))
    sys.exit(2)

from urllib.parse import urlparse

from django.urls import Resolver404, resolve
from rest_framework.fields import empty

from core.drf_resource.tools import get_serializer_fields
from core.drf_resource.viewsets import ResourceViewSet


def out(obj):
    """统一 JSON 输出（兜底 default=str 处理 datetime/Decimal 等非 JSON 类型）。"""
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def get_path(url):
    parsed = urlparse(url)
    path = parsed.path or url
    # 自动剥离 SITE_URL 前缀，支持用户直接粘贴浏览器完整路径（如 /o/bk_monitorv3/rest/...）
    from django.conf import settings

    site_url = getattr(settings, "SITE_URL", "/")
    if site_url and site_url != "/" and path.startswith(site_url):
        path = "/" + path[len(site_url):].lstrip("/")
    return path


def resolve_resource(url, method):
    """URL + Method → Resource 类。返回 (resource_cls, info_dict)。失败时 resource_cls 为 None。"""
    path = get_path(url)
    try:
        match = resolve(path)
    except Resolver404 as e:
        return None, {"error": "URL 未匹配到任何视图", "path": path, "detail": str(e)}

    view_func = match.func
    view_class = getattr(view_func, "view_class", None) or getattr(view_func, "cls", None)

    info = {
        "url": url,
        "path": path,
        "view_name": match.view_name,
        "view_module": getattr(view_func, "__module__", ""),
        "view_qualname": getattr(view_func, "__qualname__", ""),
        "view_class": f"{view_class.__module__}.{view_class.__name__}" if view_class else None,
        "args": match.args,
        "kwargs": match.kwargs,
    }

    if not (view_class and issubclass(view_class, ResourceViewSet)):
        return None, {**info, "error": "该视图不是 ResourceViewSet，不支持 Resource 直调测试"}

    actions = getattr(view_func, "actions", {}) or {}
    action_name = actions.get(method.lower(), "")
    view_set_path = f"{view_class.__module__}.{view_class.__name__}"
    if action_name:
        key = (method.upper(), f"{view_set_path}-{action_name}")
    else:
        key = (
            method.upper(),
            f"{view_set_path}-{ResourceViewSet.EMPTY_ENDPOINT_METHODS.get(method.upper(), '')}",
        )

    resource_cls = ResourceViewSet.resource_mapping.get(key)
    if not resource_cls:
        candidates = [
            {"key": list(k), "resource": str(v)}
            for k, v in ResourceViewSet.resource_mapping.items()
            if k[0] == method.upper() and k[1].startswith(view_set_path)
        ]
        return None, {
            **info,
            "error": "resource_mapping 中未找到对应 Resource",
            "method": method.upper(),
            "candidates": candidates,
        }

    info["action"] = action_name or "(default)"
    info["resource_class"] = str(resource_cls)
    info["resource_module"] = resource_cls.__module__
    info["resource_qualname"] = resource_cls.__qualname__
    return resource_cls, info


def schema_and_example(resource_cls):
    """提取参数 schema 与示例参数。返回 (schema, example, slz_info)。"""
    try:
        instance = resource_cls()
    except Exception as e:
        return None, None, {"error": f"实例化 Resource 失败: {type(e).__name__}: {e}"}

    slz_cls = instance.RequestSerializer
    if not slz_cls:
        return (
            None,
            {},
            {
                "has_request_serializer": False,
                "note": "该 Resource 无 RequestSerializer，可直接执行（无入参校验）",
            },
        )
    try:
        schema = get_serializer_fields(slz_cls)
    except Exception as e:
        return None, None, {"error": f"提取参数 schema 失败: {type(e).__name__}: {e}"}
    _clean_empty_defaults(schema)
    example = build_example(schema)
    return schema, example, {"has_request_serializer": True}


def _clean_empty_defaults(schema_list):
    """将 schema 中的 empty 哨兵值替换为 None，避免 JSON 序列化出类字符串。"""
    for field_schema in schema_list:
        if field_schema.get("default") is empty:
            field_schema["default"] = None
        items = field_schema.get("items")
        if isinstance(items, dict):
            _clean_empty_defaults([items])
        props = field_schema.get("properties")
        if isinstance(props, dict):
            _clean_empty_defaults(list(props.values()))


def build_example(schema_list):
    """根据 schema 列表生成示例参数 dict。"""
    example = {}
    for field_schema in schema_list:
        name = field_schema.get("name")
        if not name:
            continue
        example[name] = _example_for(field_schema)
    return example


def _example_for(field_schema):
    """根据单个字段 schema 生成示例值。"""
    default = field_schema.get("default")
    if default is not empty and default is not None:
        return default
    field_type = field_schema.get("type")
    if field_type == "Boolean":
        return False
    if field_type == "Integer":
        return 0
    if field_type == "Number":
        return 0
    if field_type == "Enum":
        choices = field_schema.get("choices") or []
        return choices[0] if choices else ""
    if field_type == "Array":
        items = field_schema.get("items") or {}
        return [_example_for(items)] if items.get("type") else []
    if field_type == "Object":
        props = field_schema.get("properties") or {}
        return {k: _example_for(v) for k, v in props.items()}
    return ""


def run(resource_cls, params):
    """实例化并执行 Resource.request。"""
    resource = resource_cls()
    start = time.time()
    try:
        result = resource.request(params)
        cost = time.time() - start
        return {"status": "success", "cost_seconds": round(cost, 3), "data": result}
    except Exception as e:
        cost = time.time() - start
        return {
            "status": "error",
            "cost_seconds": round(cost, 3),
            "exception_type": type(e).__name__,
            "exception_module": type(e).__module__,
            "exception_message": str(e),
            "traceback": traceback.format_exc(),
        }


def dry_run(resource_cls, params):
    """仅校验请求参数，不执行 perform_request。"""
    resource = resource_cls()
    try:
        validated = resource.validate_request_data(params)
        return {"status": "valid", "validated_data": validated}
    except Exception as e:
        return {
            "status": "invalid",
            "exception_type": type(e).__name__,
            "exception_message": str(e),
            "traceback": traceback.format_exc(),
        }


def parse_args(argv):
    if len(argv) < 2:
        return None
    cmd = argv[1]
    if cmd not in ("inspect", "dry-run", "run"):
        return None
    rest = argv[2:]
    url = rest[0] if len(rest) > 0 else None
    method = rest[1] if len(rest) > 1 else "GET"
    params_str = None
    confirm = False
    i = 2
    while i < len(rest):
        arg = rest[i]
        if arg in ("-p", "--params") and i + 1 < len(rest):
            params_str = rest[i + 1]
            i += 2
            continue
        if arg == "--confirm":
            confirm = True
        i += 1
    return cmd, url, method, params_str, confirm


def main():
    parsed = parse_args(sys.argv)
    if not parsed:
        out({
            "status": "usage_error",
            "usage": "api_tester.py <inspect|dry-run|run> <url> <method> [-p '{...json...}'] [--confirm]",
        })
        sys.exit(1)

    cmd, url, method, params_str, confirm = parsed
    if not url:
        out({"status": "usage_error", "message": "缺少 url 参数"})
        sys.exit(1)

    resource_cls, info = resolve_resource(url, method)
    if not resource_cls:
        out({"status": "resolve_failed", **info})
        sys.exit(3)

    schema, example, slz_info = schema_and_example(resource_cls)

    if cmd == "inspect":
        out({
            "status": "ok",
            "mode": "inspect",
            "method": method.upper(),
            "view": info,
            "request_serializer": slz_info,
            "param_schema": schema,
            "example_params": example,
        })
        return

    # dry-run / run 需要参数：优先用户传入，否则用自动生成的示例
    params = {}
    if params_str:
        try:
            params = json.loads(params_str)
        except json.JSONDecodeError as e:
            out({"status": "params_error", "message": f"参数 JSON 解析失败: {e}"})
            sys.exit(4)
    elif example:
        params = example

    if cmd == "dry-run":
        out({
            "status": "ok",
            "mode": "dry-run",
            "method": method.upper(),
            "view": info,
            "input_params": params,
            "result": dry_run(resource_cls, params),
        })
        return

    # run：非 GET 需显式确认，避免误触发写操作副作用
    if method.upper() != "GET" and not confirm:
        out({
            "status": "confirm_required",
            "message": f"非 GET 方法（{method.upper()}）可能产生副作用，确认后加 --confirm 再执行",
            "method": method.upper(),
            "view": info,
            "params": params,
        })
        sys.exit(5)

    out({
        "status": "ok",
        "mode": "run",
        "method": method.upper(),
        "view": info,
        "input_params": params,
        "result": run(resource_cls, params),
    })


if __name__ == "__main__":
    main()
