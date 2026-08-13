---
groupPath: 关联关系/kernel_api网关
relation: authentication-ApiAuthToken
exportedAt: "2026-08-13T09:11:53.305Z"
---
[强关联] 认证中间件 与 ApiAuthToken 数据模型
强度：必改——改 bkmonitor.models.ApiAuthToken 模型字段/唯一键/表结构时，认证中间件 + is_match_api_token 必须跟着改；改认证逻辑，模型结构不用动
原因：认证中间件直接读写 ApiAuthToken 记录做有效性/视图白名单/命名空间校验，模型结构变更级联影响整个认证链路

源端（认证中间件）：
- `AuthenticationMiddleware._handle_api_token_auth` @ `bkmonitor/kernel_api/middlewares/authentication.py`
- `is_match_api_token(request, bk_tenant_id, app_code)` @ `bkmonitor/kernel_api/middlewares/authentication.py`（读 APP_CODE_TOKENS 缓存，300s 刷新）
- `AppWhiteListModelBackend.authenticate`（自动建用户）@ `bkmonitor/kernel_api/middlewares/authentication.py`

目标端（数据模型）：
- `ApiAuthToken` @ `bkmonitor/bkmonitor/models.py`（AuthType.API 记录，含 namespaces `biz#all`/`biz#{id}`）
- `AuthType` 枚举 @ `bkmonitor/bkmonitor/models.py`
- admin RPC `admin.api_auth_token.*` 提供 CRUD（仅运维侧）