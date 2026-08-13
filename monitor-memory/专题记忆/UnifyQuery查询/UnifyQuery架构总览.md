---
groupPath: 专题记忆/UnifyQuery查询
relation: UnifyQuery架构总览
exportedAt: "2026-08-13T09:59:40.582Z"
---
UnifyQuery 是 BK-Monitor 查询体系的统一门面类，业务代码通过它执行时序/日志/维度查询，无需关心后端是统一查询HTTP服务还是各数据源原生查询。三层架构：load_data_source工厂→查询描述对象→UnifyQuery门面。

- 符号: `UnifyQuery`、`load_data_source`、`TimeSeriesDataSource`、`use_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`、`bkmonitor/bkmonitor/data_source/data_source/__init__.py`

三层查询架构:
1. 第一层 工厂函数 load_data_source((data_source_label, data_type_label))：返回 DataSource 子类本身（非实例），如 BkMonitorTimeSeriesDataSource
2. 第二层 查询描述对象：实例化 data_source_class(bk_biz_id, interval, metrics, table, group_by)，metrics 每项 {field, method, alias}
3. 第三层 统一查询门面 UnifyQuery：可包多个数据源，expression 是指标引用表达式（如 "a" 引用 alias=A），query_data() 执行时先由 use_unify_query() 判定走统一查询后端还是直连存储

表名与字段来源:
- ResultTable 模型: table_id（如 system.load）、label、schema_type、default_storage；命名规则 DB.TABLE_NAME
- ResultTableField 模型: table_id + field_name 联合唯一，tag 区分角色——metric=指标、dimension=维度、timestamp=时间
- DataSource 模型: bk_data_id、data_name、etl_config、source_label、type_label
- DataSourceResultTable 关系表: bk_data_id + table_id，一对多

关键发现:
- (BK_MONITOR_COLLECTOR, TIME_SERIES) 恒走统一查询后端分支，use_unify_query() 对其恒返回 True
- instant 查询行为与非 instant 完全不同：step强制1m、保留end_time边界点、仅返回单点
- query_dimensions 单数据源走维度端点，多数据源退化为全量拉取
- metrics 多指标展开为 query_list 多条，经 metric_merge 合成 PromQL

专家资产位置:
- 落盘: .module-experts/UnifyQuery查询专家/（契约层 C0~C2 + 实现层 01/02/03/05）