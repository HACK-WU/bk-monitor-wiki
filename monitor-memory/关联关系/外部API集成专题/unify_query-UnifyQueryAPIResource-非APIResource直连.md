---
groupPath: 关联关系/外部API集成专题
relation: unify_query-UnifyQueryAPIResource-非APIResource直连
exportedAt: "2026-08-14T07:52:30.763Z"
---
[强关联] unify_query UnifyQueryAPIResource 非APIResource直连 与空间路由机制
强度：必改——改 UnifyQueryAPIResource 的路由逻辑或请求头注入时，所有统一查询接口的路由全变
原因：unify_query 直接继承 Resource（非 APIResource），用 requests 调 unify-query 服务，按 space_uid 路由 + 注入空间/租户头

源端（非标准基类）:
- `UnifyQueryAPIResource(Resource)` @ `bkmonitor/api/unify_query/default.py`
- 非 `APIResource`——用 `requests` 直接 HTTP 调用 unify-query 服务
- `get_unify_query_url()`: 按 `space_uid` 经 `UNIFY_QUERY_ROUTING_RULES` 路由
- 请求头: `Bk-Query-Source` / `X-Bk-Scope-Space-Uid` / `X-Bk-Tenant-Id`
- 超时 60s
- 全量 18 类 Resource（QueryData/QueryRaw/QueryByPromql/GetDimensionData/GetTagKeys/QuerySeries 等）

目标端（路由配置与消费）:
- `settings.UNIFY_QUERY_ROUTING_RULES` — 路由规则配置
- 消费方: `api.unify_query.query_data({"bk_biz_ids": [2], "space_uid": "bkcc__2"})`