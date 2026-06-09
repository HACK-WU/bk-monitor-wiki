import  hello # noqa
import sys
from urllib.parse import urlparse
from django.urls import Resolver404, resolve

TARGET_URL = "/rest/v2/data_explorer/get_graph_query_config/"
METHOD = "POST"


def get_request_path(url: str) -> str:
    """将完整 URL 或路径统一转换为 Django 可解析的 path。"""
    parsed = urlparse(url)
    return parsed.path or url


def print_resolved_view(url: str, method: str = "") -> None:
    """解析 URL 并输出最终命中的视图对象。"""
    path = get_request_path(url)

    try:
        match = resolve(path)
    except Resolver404 as error:
        print(f"URL 未匹配到任何视图: {path}")
        print(error)
        return

    view_func = match.func

    print(f"输入 URL: {url}")
    print(f"解析 Path: {path}")
    print(f"路由名称: {match.view_name}")
    print(f"最终视图对象: {view_func}")
    print(f"视图模块: {getattr(view_func, '__module__', '')}")
    print(f"视图限定名: {getattr(view_func, '__qualname__', '')}")

    # DRF 的 view_func 上可能有 view_class 或 cls 属性
    view_class = getattr(view_func, "view_class", None) or getattr(view_func, "cls", None)
    if view_class:
        print(f"视图类: {view_class.__module__}.{view_class.__name__}")

    if match.args:
        print(f"位置参数: {match.args}")

    if match.kwargs:
        print(f"关键字参数: {match.kwargs}")

    if not method:
        return

    print(f"\n--- HTTP {method.upper()} 处理链分析 ---")

    # 尝试通过 ResourceViewSet.resource_mapping 查找最终 Resource 类
    from core.drf_resource.viewsets import ResourceViewSet as _RVS
    if view_class and issubclass(view_class, _RVS):
        resource_mapping = _RVS.resource_mapping
        view_set_path = f"{view_class.__module__}.{view_class.__name__}"

        # 从 view_func.actions 获取 method → action_name 映射
        actions = getattr(view_func, "actions", {})
        action_name = actions.get(method.lower(), "") if actions else ""

        # 构造 resource_mapping 的 key
        if action_name:
            key = (method.upper(), f"{view_set_path}-{action_name}")
        else:
            empty_map = _RVS.EMPTY_ENDPOINT_METHODS
            key = (method.upper(), f"{view_set_path}-{empty_map.get(method.upper(), '')}")

        resource_cls = resource_mapping.get(key)
        if resource_cls:
            print(f"action: {action_name or '(default)'}")
            print(f"resource_mapping key: {key}")
            print(f"Resource 类: {resource_cls}")
            print(f"Resource 模块: {resource_cls.__module__}")
            print(f"Resource 限定名: {resource_cls.__qualname__}")
        else:
            print(f"resource_mapping 中未找到 key={key}")
            # 回退：遍历匹配
            for k, v in resource_mapping.items():
                if k[0] == method.upper() and k[1].startswith(view_set_path):
                    print(f"  候选: {k} -> {v}")
        return

    # 标准 DRF ViewSet：从 view_func.actions 获取 method → action 映射
    actions: dict = getattr(view_func, "actions", {})
    if actions and view_class:
        print(f"method→action 映射: {actions}")
        action_name = actions.get(method.lower())
        if action_name:
            handler = getattr(view_class, action_name, None)
            print(f"HTTP {method.upper()} 对应 action: {action_name}")
            print(f"最终处理方法: {handler}")
            print(f"处理方法模块: {getattr(handler, '__module__', '')}")
            print(f"处理方法限定名: {getattr(handler, '__qualname__', '')}")
        else:
            print(f"HTTP {method.upper()} 在 actions 映射中未找到对应 action")
        return

    # 普通 APIView / Django View：直接按 method 取方法
    if view_class:
        handler = getattr(view_class, method.lower(), None)
        if handler:
            print(f"HTTP {method.upper()} 对应处理方法: {handler}")
            print(f"处理方法限定名: {getattr(handler, '__qualname__', '')}")
        else:
            print(f"视图类 {view_class} 上未找到 {method.upper()} 方法")


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else TARGET_URL
    target_method = sys.argv[2] if len(sys.argv) > 2 else METHOD
    print_resolved_view(target_url, target_method)