---
groupPath: 关联关系/数据源查询构造
relation: DataSource-to_unify_query_config-UnifyQuery
exportedAt: "2026-08-13T12:01:18.603Z"
---
[强关联] DataSource 查询描述对象 与 to_unify_query_config 拼装/UnifyQuery 门面
强度：必改——改 DataSource.to_unify_query_config 的 query_list 拼装逻辑或参数结构时，UnifyQuery 门面必须跟着改；改 data_source_class 实例化参数规范，to_unify_query_config 也要适配
原因：UnifyQuery 构造时依赖 data_source_class 实例化（传入 bk_biz_id/interval/metrics/table/group_by），执行时依赖 to_unify_query_config() 输出的 query_list 结构，参数拼装逻辑变更级联影响所有查询入口

源端（查询描述对象+拼装）:
- `DataSource` 基类 @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（实例化参数: bk_biz_id/interval/metrics/table/group_by）
- `TimeSeriesDataSource.to_unify_query_config` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（拼装 query_list: field_name/reference_name/time_aggregation/function/keep_columns）
- metrics 结构: {field, method, alias} → field_name/reference_name/聚合映射

目标端（UnifyQuery门面）:
- `UnifyQuery` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`（构造时接收 data_sources 列表）
- `UnifyQuery._query_unify_query` / `get_unify_query_params` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`（消费 query_list 拼装 HTTP 参数）
- `UnifyQuery.query_data` / `query_log` / `query_dimensions` 等公开入口依赖 to_unify_query_config 输出