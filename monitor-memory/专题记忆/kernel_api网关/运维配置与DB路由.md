---
groupPath: 专题记忆/kernel_api网关
relation: 运维配置与DB路由
exportedAt: "2026-08-13T09:11:15.552Z"
---
kernel_api 运维配置与 DB 路由：config/role/api.py 承载角色配置（INSTALLED_APPS/MIDDLEWARE/REST_FRAMEWORK），中间件链以 Prometheus 指标 + 认证为关键节点，会话短生命周期（60s），KernelAPIRouter 把 monitor_api/metadata 路由到 backend 库。

## 角色配置（config/role/api.py）
- 继承链：`config.{env}` → `from config.role.web import *` + `from config.role.worker import *` → api 角色覆盖
- `INSTALLED_APPS` 追加：kernel_api/bkmonitor/metadata/monitor_web/fta_web/apm/rum/core.drf_resource 等（web+worker 全量）
- `ROOT_URLCONF = "kernel_api.urls"`
- `CACHES = worker.CACHES`（复用 worker 缓存配置）
- `SESSION_COOKIE_AGE = 60`（后台 API 无 session id，每次新建 session，只保留 1min）
- `MIGRATE_MONITOR_API = False`（monitor_api 表不做迁移，走 backend 库）

## 中间件链（顺序敏感）
```
corsheaders.CorsMiddleware
→ bkmonitor.prometheus.MetricsBeforeMiddleware（必须最前）
→ Session/Locale/Common/Csrf(注释掉)/Auth/Message/Security
→ blueapps.request_provider.RequestProvider
→ bkmonitor.request_middlewares.RequestProvider
→ kernel_api.ApiTimeZoneMiddleware        # 读取 HTTP_BLUEKING_TIMEZONE
→ kernel_api.ApiLanguageMiddleware        # 读取 HTTP_BLUEKING_LANGUAGE
→ kernel_api.authentication.AuthenticationMiddleware   # 认证核心
→ bkm_space.ParamInjectMiddleware         # 空间参数注入
→ bkmonitor.prometheus.MetricsAfterMiddleware（必须最后）
```

## 环境变量与开关
- `INSTALLED_APIS`（默认 `collector,meta,models,query`）：控制 v3 暴露哪些模块
- `ALLOW_EXTEND_API`（默认 True）：是否加载 extend_views 扩展点
- `SKIP_IAM_PERMISSION_CHECK`（默认 True）：api 角色跳过 IAM 权限中心检查
- `AUTHENTICATION_BACKENDS`：AppWhiteListModelBackend + UserBackend
- `ENABLE_MULTI_TENANT_MODE`：多租户开关，影响 JWT 租户头校验
- `FROM_APIGW_NAME`：apigw 名称列表，用于获取公钥
- `OPERATION_MCP_ENV`：运营指标环境门控（bkte/bkop/sg）

## DB 路由（dbroutors.py）
- 符号: `KernelAPIRouter`
- 位置: `bkmonitor/kernel_api/dbroutors.py`
- Django `DATABASE_ROUTERS`，把 `monitor_api`、`metadata` 两个 app_label 的模型路由到 `settings.BACKEND_DATABASE_NAME` 库，其余走 `default`
- 方法：`db_for_read` / `db_for_write` / `allow_relation` / `allow_migrate`
- `allow_migrate` 返回 `app_label not in routers`，即 backend 库不迁移这两个 app（迁移走主库）

## 日志与监控
- 日志文件：`{LOG_PATH}/kernel_api.log`（WatchedFileHandler）；`IS_CONTAINER_MODE` 或 dev 环境仅 console
- Prometheus 指标：`MetricsBeforeMiddleware`/`MetricsAfterMiddleware` 包裹全链路；MCP 认证上报 `MCP_REQUESTS_TOTAL`
- `LogExceptionMiddleware`：异常日志记录后原样抛出（`process_exception`）