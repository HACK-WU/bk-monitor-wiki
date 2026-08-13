---
groupPath: 关联关系/数据源查询构造
relation: load_data_source-DataSource子类-use_unify_query
exportedAt: "2026-08-13T12:01:18.603Z"
---
[强关联] load_data_source 工厂 与 DataSource 子类注册表/use_unify_query 路径决策
强度：必改——改 load_data_source 注册字典或 DataSourceLabel/DataTypeLabel 枚举值时，所有 14 个 DataSource 子类和 use_unify_query 判定必须跟着改；改 use_unify_query 逻辑，子类不用管
原因：load_data_source 维护 (label,type)→DataSourceClass 映射，use_unify_query 取 data_source.id=(label,type) 查 UnifyQueryDataSources/GrayUnifyQueryDataSources 判定路径，注册表或枚举值变更级联影响所有数据源的路径决策

源端（工厂+枚举）:
- `load_data_source(data_source_label, data_type_label)` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（内部字典 14 组合）
- `DataSourceLabel` / `DataTypeLabel` 枚举 @ `bkmonitor/constants/data_source.py`
- `UnifyQueryDataSources` / `GrayUnifyQueryDataSources` 常量 @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

目标端（DataSource子类+路径决策）:
- `DataSource` 基类 + 14 个子类 @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（BkMonitorTimeSeriesDataSource/BkdataTimeSeriesDataSource/CustomTimeSeriesDataSource/...）
- `use_unify_query()` / `switch_unify_query(bk_biz_id)` @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（路径决策）
- 各子类实现各自的 switch_unify_query 灰度判定逻辑