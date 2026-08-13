---
groupPath: 关联关系/UnifyQuery查询
relation: DataSource-DataQueryHandler
exportedAt: "2026-08-13T10:01:26.063Z"
---
[强关联] DataSource 下推分支 与 DataQueryHandler 查询执行器路由
强度：必改——改 DataQueryHandler 的路由键/执行器注册方式时，DataSource._get_queryset 必须跟着改；改 DataSource 的下推逻辑，DataQueryHandler 不用管
原因：use_unify_query()==False 时 UnifyQuery 下推到 DataSource.query_data → _get_queryset → DataQueryHandler，按 (data_source_label, data_type_label) 路由到具体存储后端执行器

源端（下推分支）:
- `UnifyQuery._query_data_using_datasource` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `DataSource.query_data` / `_get_queryset` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

目标端（执行器路由）:
- `DataQueryHandler` @ `bkmonitor/bkmonitor/data_source/handler/__init__.py`
- 按 (data_source_label, data_type_label) 路由到存储后端执行器
- 最终落点: 多数走外部 API（metadata→ES / log_search / bkdata BKSQL）；FTA 事件/告警直连 ES