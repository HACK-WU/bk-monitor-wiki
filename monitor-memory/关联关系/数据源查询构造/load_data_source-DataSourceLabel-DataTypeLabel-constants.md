---
groupPath: 关联关系/数据源查询构造
relation: load_data_source-DataSourceLabel-DataTypeLabel-constants
exportedAt: "2026-08-13T12:01:18.603Z"
---
[强关联] load_data_source 工厂枚举 与 DataSourceLabel/DataTypeLabel 常量定义
强度：必改——改 DataSourceLabel/DataTypeLabel 枚举值或新增枚举项时，load_data_source 注册字典和所有引用枚举的代码必须跟着改；改注册字典 key，枚举不用管
原因：load_data_source 以 (DataSourceLabel.X, DataTypeLabel.Y) 元组为 key 查注册字典，枚举值变更直接导致字典查找失败返回错误

源端（工厂注册）:
- `load_data_source` 内部字典 @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（14 个 (label,type)→Class 映射）
- UnifyQueryDataSources / GrayUnifyQueryDataSources 常量列表 @ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`（以枚举元组为元素）

目标端（枚举常量）:
- `DataSourceLabel` 枚举 @ `bkmonitor/constants/data_source.py`（BK_MONITOR_COLLECTOR/CUSTOM/BK_DATA/BK_LOG_SEARCH/BK_FTA/BK_APM/PROMETHEUS）
- `DataTypeLabel` 枚举 @ `bkmonitor/constants/data_source.py`（TIME_SERIES/LOG/EVENT/ALERT）
- 枚举值变更影响: load_data_source 字典查找、UnifyQueryDataSources/GrayUnifyQueryDataSources 判定、所有调用方传参