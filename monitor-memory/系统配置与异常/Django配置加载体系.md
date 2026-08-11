Django 配置加载体系（settings.py + config/）：settings.py 依次加载 config.default、blueapps.patch、config.{env}、config.role.{role}，形成环境（dev/stag/prod）与角色（web/api/worker）的交叉配置覆盖。

## 加载顺序

```
settings.py
├── config.default (基础配置，含 INSTALLED_APPS、MIDDLEWARE、DATABASES)
├── blueapps.patch (蓝鲸 PaaS 框架 patch)
├── config.{env} (dev/stag/prod 环境配置)
└── config.role.{role} (web/api/worker 角色配置)
```

## 环境与角色检测

- 环境变量优先级：`DJANGO_CONF_MODULE`（显式）→ 自动推导
- **ENVIRONMENT**：`BKPAAS_ENVIRONMENT` (V3) 或 `BK_ENV` (V2)
  - `development/dev` → `config.dev.py`（本地开发，本地 MySQL，Redis）
  - `testing/stag` → `config.stag.py`（预发布，几乎继承 default）
  - `production/prod` → `config.prod.py`（生产，继承 default）
- **ROLE**：从 `DJANGO_CONF_MODULE = "config.role.{ROLE}.{ENVIRONMENT}.{PLATFORM}"` 解析
  - `web` → `config.role.web.py`（前端 Web 应用，用户 + APIGW）
  - `api` → `config.role.api.py`（API 网关节点，其他系统调用）
  - `worker` → `config.role.worker.py`（后台异步任务，Celery Worker）

## 三种角色差异

| 角色 | URL路由 | INSTALLED_APPS | 特有功能 | 中间件 |
|------|---------|----------------|----------|--------|
| **web** | `urls.py`（含 kernel_api v2/v3/v4 + Grafana 等） | 全模块（含 monitor_web、fta_web、weixin） | 用户认证、前端路由、Session、CSRF、APIGW JWT | 最丰富，含 `ProfilerMiddleware`、`RequestProvider`、`TrackSiteVisitMiddleware`、`ParamInjectMiddleware` |
| **api** | `kernels_api/urls.py`（仅 v2/v3/v4，无前端路由） | 精简（无 monitor_web、weixin，额外 kafka） | JWT/Token 认证、ApiTokenAuthentication | 精简单 ，专精API认证 |
| **worker** | `alarm_backends/urls.py` | 后台模块（alarm_backends、core.drf_resource） | Celery Worker、无HTTP、后台告警检测 | 无 HTTP 中间件 |

## 环境变量覆盖规则

- `BKAPP_SETTINGS_*` 前缀的环境变量自动注入 settings（去掉前缀后转为大写）
- 例如：`BKAPP_LOG_LEVEL=DEBUG` → `LOG_LEVEL = "DEBUG"`

## 关键入口

- 位置: `config/tools/environment.py` — 环境/角色/platform 变量初始化
- 位置: `config/default.py` — 默认配置（含 INSTALLED_APPS、MIDDLEWARE、DATABASES、CACHES、加密、APIGW 等）
- 位置: `config/dev.py` — `RUN_MODE="DEVELOP"`，本地 MySQL(Root/空密码)、Redis、DEBUG=True
- 位置: `config/role/web.py` — web 角色加载（REST Framework、Swagger、前端中间件、全 INSTALLED_APPS）
- 位置: `config/role/api.py` — API 角色加载（精简 INSTALLED_APPS、Token 认证、JWT 中间件、独立日志）
- 位置: `config/role/worker.py` — Worker 角色加载（Celery、告警后端配置、无 Web 中间件）

## 重要：实际不是 3×3 完全交叉

每个角色都会先加载对应的 `NEW_ENV` 环境配置（dev/stag/prod），然后叠加角色配置。例如：

- `api + prod` → `config.prod.py` + `config.role.api.py`
- `web + dev` → `config.dev.py` + `config.role.web.py`
- `worker + stag` → `config.stag.py` + `config.role.worker.py`
