---
groupPath: 关联关系/外部API集成专题
relation: bk_login_cmdb-use_apigw-ENABLE_MULTI_TENANT_MODE
exportedAt: "2026-08-14T07:51:51.854Z"
---
[强关联] bk_login/cmdb use_apigw() 双模式 与 ENABLE_MULTI_TENANT_MODE 配置
强度：必改——改 use_apigw() 逻辑或 ENABLE_MULTI_TENANT_MODE 配置语义时，bk_login 和 cmdb 的 base_url/action 路径全变
原因：多租户模式下 apigw 与 compapi 路径完全不同，配置错误会导致请求 404

源端（配置开关）:
- `settings.ENABLE_MULTI_TENANT_MODE` @ Django settings
- cmdb 额外看 `settings.CMDB_USE_APIGW`

目标端（双模式系统）:
- `BkUserApiResource.use_apigw()` @ `bkmonitor/api/bk_login/default.py`
  - apigw 模式: base_url=`BK_USER_API_BASE_URL`，action 走 `/api/v3/open/...`
  - compapi 模式: base_url=`api/c/compapi/v2/usermanage/`，action 走旧路径
- `CMDBBaseResource.use_apigw()` @ `bkmonitor/api/cmdb/client.py`
  - apigw 模式: 走蓝鲸 API 网关路径
  - compapi 模式: 走组件 API 路径
- action 路径两套不同，切换时必须同步改