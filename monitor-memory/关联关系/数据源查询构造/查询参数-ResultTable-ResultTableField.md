---
groupPath: 关联关系/数据源查询构造
relation: 查询参数-ResultTable-ResultTableField
exportedAt: "2026-08-13T12:01:18.603Z"
---
[强关联] 查询描述参数 与 ResultTable/ResultTableField 元数据模型
强度：必改——改 ResultTable.table_id 命名规则或 ResultTableField.tag 分类时，查询描述的 table/metrics[].field/group_by 构造必须跟着改；改 to_unify_query_config 的 table_id 拼装逻辑，元数据模型不用管
原因：查询描述的 table/metrics[].field/group_by 都来自元数据模型，table_id 命名规则和 field 的 tag 分类直接决定查询参数结构

源端（查询描述参数）:
- `data_source_class(bk_biz_id, interval, metrics, table, group_by)` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`
- `table` 参数 → to_unify_query_config 的 table_id（data_label 未传则 table.lower()）
- `metrics[].field` → query_list[].field_name（来自 ResultTableField tag=metric）
- `group_by` → query_list[].dimensions/function[0].dimensions/keep_columns（来自 ResultTableField tag=dimension）

目标端（元数据模型）:
- `ResultTable` @ `bkmonitor/metadata/models/result_table.py`（table_id 命名规则 DB.TABLE_NAME、label、schema_type、default_storage）
- `ResultTableField` @ `bkmonitor/metadata/models/result_table.py`（table_id + field_name 联合唯一，tag 区分 metric/dimension/timestamp）
- `DataSource` 模型 @ `bkmonitor/bkmonitor/models/base.py`（bk_data_id/data_name/source_label/type_label）
- `DataSourceResultTable` 关系表 @ `bkmonitor/bkmonitor/models/base.py`（bk_data_id + table_id 一对多）
- 初始化数据 `init_resulttable.json`（如 system.proc 含 display_name/pid 等维度与 cpu_usage_pct 等指标）