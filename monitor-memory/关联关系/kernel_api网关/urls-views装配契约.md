---
groupPath: 关联关系/kernel_api网关
relation: urls-views装配契约
exportedAt: "2026-08-13T09:11:47.946Z"
---
[强关联] kernel_api.urls 路由注册 与 views/v4 视图模块导出
强度：必改——新增 v4 endpoint 必须同时改两边（views/v4/{module}.py 定义 ViewSet + views/v4/__init__.py 导出），漏任一处则路由不生效；改 register_url 装配机制则所有版本视图受影响
原因：register_url 通过 __import__ 导入视图模块并扫描 ResourceViewSet 子类，模块必须在 __init__.py 显式导出才会被扫描到，形成双向注册契约

源端（路由注册）：
- `register_url(prex, views_module_list, namespace)` @ `bkmonitor/kernel_api/urls.py`
- `register_v4()` → `/api/v4/`（视图模块 `views.v4`）@ `bkmonitor/kernel_api/urls.py`
- `register_v3()` → `/api/v3/{模块名}/`（按 INSTALLED_APIS 裁剪）@ `bkmonitor/kernel_api/urls.py`

目标端（v4 视图模块）：
- `views/v4/__init__.py`（必须含 `from .{module} import *` 导出）@ `bkmonitor/kernel_api/views/v4/__init__.py`
- `ResourceViewSet` 子类 + `resource_routes = [ResourceRoute("POST", XxxResource, endpoint="xxx")]` @ `bkmonitor/kernel_api/views/v4/{module}.py`
- 同理 `views/v2/__init__.py` / `views/v3/__init__.py`