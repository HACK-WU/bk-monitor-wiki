---
groupPath: 关联关系/外部API集成专题
relation: bkdata-UseSaaSAuthInfoMixin-SAAS认证注入
exportedAt: "2026-08-14T07:52:30.762Z"
---
[强关联] bkdata UseSaaSAuthInfoMixin SaaS认证注入 与 QueryDataResource token/user 双鉴权
强度：必改——改 UseSaaSAuthInfoMixin 的注入逻辑或 QueryDataResource 的鉴权模式时，bkdata 所有查询接口的认证全变
原因：bkdata 企业版后台 AppCode 独立于前台，需 SaaS 侧凭证注入；QueryDataResource 支持 token/user 两种鉴权模式

源端（认证注入）:
- `UseSaaSAuthInfoMixin` @ `bkmonitor/api/bkdata/default.py`
- `full_request_data()`: 注入 `bk_app_code=SAAS_APP_CODE`
- `get_headers()`: 注入 SaaS 凭证（`SAAS_APP_CODE`/`SAAS_SECRET_KEY`）
- 基类: `BkDataAPIGWResource`（TIMEOUT=300s） / `BkDataQueryAPIGWResource`（查询专用 base_url）

目标端（双鉴权查询）:
- `QueryDataResource` @ `bkmonitor/api/bkdata/default.py`
- token 模式: 需配置 `BKDATA_DATA_TOKEN`，走应用授权
- user 模式: `_user_request=True`，走 `COMMON_USERNAME` 用户身份
- DataAccessAPIResource: 注入 `_origin_user` + 默认 `bk_username=BK_DATA_PROJECT_MAINTAINER`