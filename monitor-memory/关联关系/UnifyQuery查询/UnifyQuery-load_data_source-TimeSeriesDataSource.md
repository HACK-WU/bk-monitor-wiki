---
groupPath: 关联关系/UnifyQuery查询
relation: UnifyQuery-load_data_source-TimeSeriesDataSource
exportedAt: "2026-08-13T10:00:54.589Z"
---
[强关联] UnifyQuery 门面类 与 load_data_source 工厂/TimeSeriesDataSource 查询描述对象
强度：必改——改 load_data_source 工厂签名或 TimeSeriesDataSource.to_unify_query_config 的参数拼装逻辑时，UnifyQuery 门面必须跟着改；改 UnifyQuery 门面的查询编排逻辑，工厂/描述对象不用管
原因：UnifyQuery 构造时依赖 data_source_class 实例化（传入 bk_biz_id/interval/metrics/table/group_by），执行时依赖 to_unify_query_config() 输出的 query_list 结构，参数拼装逻辑变更级联影响所有查询入口

源端（查询门面）:
- `UnifyQuery` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `UnifyQuery._query_unify_query` / `get_unify_query_params` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`

目标端（数据源工厂+描述对象）:
- `load_data_source` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`
- `TimeSeriesDataSource` / `to_unify_query_config` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`
- DataSourceLabel / DataTypeLabel 枚举 @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`