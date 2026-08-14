---
groupPath: 关联关系/外部API集成专题
relation: tapd-TapdAPIResource-contextvar-access_token
exportedAt: "2026-08-14T07:52:30.762Z"
---
[强关联] tapd TapdAPIResource contextvar access_token 与 Basic/Bearer 双认证模式
强度：必改——改 TapdAPIResource 的认证逻辑（get_headers/perform_request/render_response_data）时，所有 tapd 接口的认证行为全变
原因：tapd 用 contextvar 管理 access_token，Basic（APP_ID:SECRET）与 Bearer（access_token）双模式，perform_request 会 pop access_token 仅用于认证头不污染 body

源端（认证基类）:
- `TapdAPIResource` @ `bkmonitor/api/tapd/default.py`
- `base_url = settings.TAPD_API_BASE_URL`
- `IS_STANDARD_FORMAT = False` — 响应非标准格式
- `get_headers()`: Basic Auth（client_id:client_secret Base64）或 Bearer（access_token）
- `perform_request()`: pop `access_token` 参数仅用于认证头，不传入上游 body
- `render_response_data()`: 适配 `{status, info, data}`，status!="1" 抛 BKAPIError

目标端（token 获取与消费）:
- `UserOauthTokenResource` @ `bkmonitor/api/tapd/default.py` — 用 OAuth code 换 access_token
- 所有需 Bearer 认证的 tapd Resource（GetParticipantProjects 等）依赖 contextvar 传入的 access_token