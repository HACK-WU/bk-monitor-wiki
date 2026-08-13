---
groupPath: 关联关系/UnifyQuery查询
relation: to_unify_query_config-ResultTable-ResultTableField
exportedAt: "2026-08-13T10:01:29.923Z"
---
[强关联] to_unify_query_config 参数拼装 与 ResultTable/ResultTableField 元数据模型
强度：必改——改 ResultTable/ResultTableField 模型的字段定义/命名规则时，to_unify_query_config 的 table_id/field_name 拼装必须跟着改；改参数拼装逻辑，模型不用管
原因：查询描述的 table/metrics[].field/group_by 都来自元数据模型，table_id 命名规则（DB.TABLE_NAME）和 field 的 tag 分类（metric/dimension/timestamp）直接决定查询参数结构

源端（参数拼装）:
- `TimeSeriesDataSource.to_unify_query_config` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`
- table_id = data_label or table.lower()；field_name 来自 metrics[].field

目标端（元数据模型）:
- `ResultTable` @ `bkmonitor/metadata/models/result_table.py`（table_id 命名规则 DB.TABLE_NAME、label、schema_type）
- `ResultTableField` @ `bkmonitor/metadata/models/result_table.py`（table_id + field_name 联合唯一，tag 区分 metric/dimension/timestamp）
- 初始化数据 init_resulttable.json（如 system.proc 含 display_name/pid 等维度与 cpu_usage_pct 等指标）