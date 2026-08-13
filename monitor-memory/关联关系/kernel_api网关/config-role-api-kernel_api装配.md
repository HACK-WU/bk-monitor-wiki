---
groupPath: 关联关系/kernel_api网关
relation: config-role-api-kernel_api装配
exportedAt: "2026-08-13T09:11:41.731Z"
---
[强关联] config/role/api.py 角色配置 与 kernel_api 路由/中间件装配
强度：必改——改 config/role/api.py 的 INSTALLED_APPS/ROOT_URLCONF/MIDDLEWARE 时，kernel_api 路由注册与中间件链必须跟着改；改 kernel_api 内部路由逻辑，角色配置不用动
原因：api 角色的整个运行时装配（挂载哪些 app、URLConf 指向、中间件链顺序）都在 config/role/api.py 定义，是 kernel_api 能启动的前提契约

源端（角色配置）：
- `INSTALLED_APPS`（追加 kernel_api/bkmonitor/metadata/monitor_web/fta_web/apm/rum/core.drf_resource）@ `bkmonitor/config/role/api.py`
- `ROOT_URLCONF = "kernel_api.urls"` @ `bkmonitor/config/role/api.py`
- `MIDDLEWARE`（中间件链顺序）@ `bkmonitor/config/role/api.py`
- `REST_FRAMEWORK.EXCEPTION_HANDLER = "kernel_api.exceptions.api_exception_handler"` @ `bkmonitor/config/role/api.py`
- `SKIP_IAM_PERMISSION_CHECK=True` / `SESSION_COOKIE_AGE=60` / `MIGRATE_MONITOR_API=False` @ `bkmonitor/config/role/api.py`

目标端（kernel_api）：
- `register_url` / `register_v2` / `register_v3` / `register_v4` @ `bkmonitor/kernel_api/urls.py`
- `AuthenticationMiddleware` / `ApiTimeZoneMiddleware` / `ApiLanguageMiddleware` @ `bkmonitor/kernel_api/middlewares/`
- `api_exception_handler` @ `bkmonitor/kernel_api/exceptions.py`