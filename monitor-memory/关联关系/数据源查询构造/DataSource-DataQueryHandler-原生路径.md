---
groupPath: 关联关系/数据源查询构造
relation: DataSource-DataQueryHandler-原生路径
exportedAt: "2026-08-13T12:01:18.603Z"
---
[强关联] DataSource 原生路径下推 与 DataQueryHandler 执行器路由
强度：必改——改 DataQueryHandler 路由键或执行器注册方式时，DataSource._get_queryset 必须跟着改；改 DataSource 下推逻辑，DataQueryHandler 不用管
原因：use_unify_query()==False 时 UnifyQuery 下推到 DataSource.query_data → _get_queryset → DataQueryHandler，按 (data_source_label, data_type_label) 路由到具体存储后端执行器

源端（下推分支）:
- `UnifyQuery._query_data_using_datasource` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`（use_unify_query()==False 时进入）
- `DataSource.query_data` / `_get_queryset` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`
- 8 个 NATIVE 组合: (bk_apm,time_series)→metadata/ES、(bk_monitor,event/alert)→直连ES、(bk_fta,event/alert)→直连ES、(prometheus,time_series)→PromQL直查

目标端（执行器路由）:
- `DataQueryHandler` @ `bkmonitor/bkmonitor/data_source/handler/__init__.py`
- 按 (data_source_label, data_type_label) 路由到存储后端执行器
- 最终落点: FTA事件/告警直连ES；APM时序→metadata/ES；Prometheus→PromQL直查
- PrometheusTimeSeriesDataSource 恒走本分支但执行 PromQL（不经 _get_queryset/DataQueryHandler）