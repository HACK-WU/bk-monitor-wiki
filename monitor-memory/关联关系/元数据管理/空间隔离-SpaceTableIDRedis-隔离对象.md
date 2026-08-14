---
groupPath: 关联关系/元数据管理
relation: 空间隔离-SpaceTableIDRedis-隔离对象
exportedAt: "2026-08-14T01:46:33.763Z"
---
[强关联] 空间隔离（Space）与 数据源/结果表/自定义上报/数据链路
强度：必改——改 Space 模型或 SpaceTableIDRedis 路由推送机制时，DataSource/ResultTable/CustomReport/DataLink 的空间隔离逻辑必须跟着改；改空间隔离作用对象，Space 不用管
原因：Space 隔离作用于 DataSource/ResultTable/CustomReport/DataLink，SpaceTableIDRedis 刷新 ES 路由，空间路由变更级联影响所有元数据隔离

源端（空间模型）:
- `Space` / `SpaceDataSource` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/space/`
- `SpaceTableIDRedis` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/space/space_table_id_redis.py`（74KB，Redis 路由推送）
- `service/space_redis.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/service/space_redis.py`（空间配置缓存、ES 别名推送）

目标端（被隔离对象）:
- `DataSource` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/data_source.py`（空间归属）
- `ResultTable` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/result_table.py`（空间路由）
- `CustomReport` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/custom_report/`（空间隔离）
- `DataLink` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/data_link/`（空间隔离）
- 四种空间类型: BKCC（业务）/BCS（容器）/BKCI（研发）/BKSAAS（SaaS）