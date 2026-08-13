---
groupPath: 关联关系/UnifyQuery查询
relation: UnifyQuery-api.unify_query-resources
exportedAt: "2026-08-13T10:01:09.759Z"
---
[强关联] UnifyQuery 门面 与 api.unify_query 后端 Resource 类
强度：必改——改 Resource 的 RequestSerializer 字段定义/请求参数名时，UnifyQuery 的参数拼装必须跟着改；改 UnifyQuery 编排逻辑，Resource 不用管
原因：UnifyQuery._query_unify_query 等方法直接调用 api.unify_query.query_data/query_raw/query_reference/get_dimension_data，参数名必须与 Resource 的 Serializer 字段一一对应

源端（查询门面）:
- `UnifyQuery._query_unify_query` / `_query_log_using_unify_query` / `_query_reference_using_unify_query` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `InfluxdbDimensionFetcher.query_dimensions` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

目标端（后端 Resource）:
- `QueryDataResource`（POST /query/ts）@ `bkmonitor/api/unify_query/default.py`
- `QueryRawResource`（POST /query/ts/raw）@ `bkmonitor/api/unify_query/default.py`
- `QueryReferenceResource`（POST /query/ts/reference）@ `bkmonitor/api/unify_query/default.py`
- `GetDimensionDataResource`（POST /query/ts/info/tag_values）@ `bkmonitor/api/unify_query/default.py`