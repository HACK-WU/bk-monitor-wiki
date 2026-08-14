---
groupPath: 关联关系/元数据管理
relation: 任务调度-模型层-Consul存储后端
exportedAt: "2026-08-14T01:46:33.763Z"
---
[强关联] Celery 任务调度 与 模型层/Consul/存储后端基础设施
强度：必改——改 DataSource/ResultTable/Storage/DataLink 模型或 Consul/ES/InfluxDB 接口时，task/ 任务必须跟着改；改任务逻辑，模型/基础设施不用管
原因：Celery 任务（tasks.py 86KB）操作元数据模型并刷新 Consul 配置、管理 ES/InfluxDB 索引、下发节点管理、接入计算平台，模型或基础设施变更级联影响所有后台任务

源端（任务调度）:
- `task/tasks.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/task/tasks.py`（86KB 核心 Celery 任务）
- `task/config_refresh.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/task/config_refresh.py`（Consul/ES/InfluxDB 配置刷新）
- `task/sync_space.py` / `bcs.py` / `bkbase.py` / `datalink.py` / `migrate.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/task/`
- `management/commands/` @ `bk-monitor-base/src/bk_monitor_base/metadata/management/commands/`（60+ 管理命令）

目标端（模型+基础设施）:
- `DataSource` / `ResultTable` / `Storage` / `DataLink` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/`
- Consul（配置刷新/分布式锁）
- ES/InfluxDB（索引轮转/清理）
- 节点管理（插件下发）
- 计算平台（元数据 Redis 监听同步）
- Redis（路由推送）