# 任务调度与运维专家

> **专题**: 元数据管理专题
> **目录**: `.module-experts/元数据管理专题/任务调度与运维专家/`
> **创建时间**: 2026-07-28
> **最后更新**: 2026-07-28

---

## 一、专家名片

| 属性 | 值 |
|------|-----|
| **名称** | 任务调度与运维专家 |
| **职责** | 管理元数据相关的后台 Celery 任务调度、Django 管理命令、Redis 分布式锁等运维工具、种子数据加载、数据库迁移 |
| **子专家** | 无（功能内聚，直接产出全部文档） |

---

## 二、覆盖文件清单

### 2.1 task/ — Celery 任务调度（19 个文件）

| 文件 | 大小 | 职责 |
|------|------|------|
| `task/__init__.py` | 75 B | 导出 config_refresh 和 custom_report 模块 |
| `task/tasks.py` | **86 KB** | 核心 Celery 异步任务定义（@app.task 装饰器） |
| `task/config_refresh.py` | 22 KB | Consul/ES/InfluxDB 配置刷新与存储管理 |
| `task/custom_report.py` | 12 KB | 自定义上报配置下发、事件维度同步、日志配置刷新 |
| `task/sync_space.py` | 39 KB | 空间同步（BKCC/BCS/BKCI 空间创建与维护） |
| `task/bcs.py` | 27 KB | BCS 集群监控信息刷新（ServiceMonitor/PodMonitor） |
| `task/bkbase.py` | 26 KB | 计算平台元数据 Redis 监听与同步 |
| `task/migrate.py` | 12 KB | 日志纳秒结果表迁移 |
| `task/datalink.py` | 11 KB | 日志 V4 数据链路创建/更新 |
| `task/auto_deploy_proxy.py` | 9 KB | 代理自动部署（节点管理插件下发） |
| `task/tenant.py` | 9 KB | 租户初始化（Kafka/InfluxDB 集群、系统数据链路） |
| `task/ping_server.py` | 8 KB | Ping Server 配置下发至节点管理 |
| `task/sync_cmdb_relation.py` | 7 KB | CMDB 关系数据同步至 Redis |
| `task/entity_relation.py` | 4 KB | 实体关系定义全量刷新至 Redis |
| `task/vm.py` | 4 KB | VM 接入检测与重试 |
| `task/constants.py` | 3 KB | 计算平台 V4 链路 KIND-STORAGE 映射配置 |
| `task/refresh_data_link.py` | 1 KB | 数据链路状态刷新入口 |
| `task/refresh_default_rp.py` | 1 KB | InfluxDB 默认 RP 策略刷新 |
| `task/utils.py` | 1 KB | 批量操作工具函数（bulk_handle、chunk_list） |

核心文件路径：`bk-monitor-base/src/bk_monitor_base/metadata/task/`

### 2.2 management/commands/ — Django 管理命令（60 个文件）

| 分类 | 代表命令 | 数量 |
|------|---------|------|
| **空间管理** | `sync_cmdb_space`, `sync_bcs_space`, `init_space_data`, `init_space_type`, `query_space` | 8 |
| **数据源/结果表** | `access_bkdata_vm`, `switch_kafka_for_data_id`, `query_data_id_by_mq`, `modify_data_source_space_type` | 10 |
| **集群/存储** | `sync_cluster_config`, `check_bcs_cluster_status`, `init_influxdb_proxy_storage`, `switch_vm_cluster` | 6 |
| **数据链路** | `check_datalink_health`, `create_shortcut_data_link`, `sync_bklog_es_router` | 4 |
| **指标/维度** | `add_bkci_metrics_and_dimensions`, `add_extend_dimensions`, `check_ts_metrics`, `refresh_ts_metric` | 6 |
| **运维/清理** | `clean_old_consul_config`, `delete_data_source_consul_config`, `delete_gse_router`, `query_disabled_data_id` | 8 |
| **初始化** | `init_redis_data`, `init_tenant`, `enable_global_biz` | 4 |
| **迁移** | `migrate_nano_log`, `switch_data_id_from_influxdb_to_bkbase_v4` | 4 |
| **其他** | `deploy_official_plugin`, `modify_kafka_cluster`, `query_es_index` 等 | 10 |

核心文件路径：`bk-monitor-base/src/bk_monitor_base/metadata/management/commands/`

### 2.3 tools/ — 运维工具

| 文件 | 大小 | 职责 |
|------|------|------|
| `tools/redis_lock.py` | 2.5 KB | Redis 分布式锁（DistributedLock） |

核心文件路径：`bk-monitor-base/src/bk_monitor_base/metadata/tools/`

### 2.4 data/ — 种子数据

| 文件 | 大小 | 内容 |
|------|------|------|
| `data/init_data.json` | 177 KB | 内置结果表、字段、存储配置 |
| `data/init_resulttable.json` | 209 KB | 结果表初始化数据 |
| `data/init_datasource.json` | 11 KB | 数据源初始化数据 |
| `data/init_label.json` | 4 KB | 标签初始化数据 |
| `data/init_cluster_info.json` | 666 B | 集群信息初始化 |
| `data/init_storage.json` | 753 B | 存储初始化 |
| `data/init_ts_or_event_group.json` | 2 KB | 时序/事件组初始化 |
| `data/description_unit.json` | 98 KB | 单位描述 |
| `data/bkci_data.json` | 6 KB | BKCI 数据 |
| `data/k8s_events.json` | 6 KB | K8s 事件 |
| `data/k8s_metrics/` (24 YAML) | — | K8s 指标定义（apiserver/etcd/kubelet/node 等） |
| `data/metadata_resulttablefield.txt` | 5 KB | 结果表字段文本 |

核心文件路径：`bk-monitor-base/src/bk_monitor_base/metadata/data/`

### 2.5 migrations/ — 数据库迁移

| 文件 | 大小 | 内容 |
|------|------|------|
| `migrations/0001_initial.py` | 115 KB | 初始模型迁移 |
| `migrations/0002_initial_data.py` | 7 KB | 初始数据加载（label/cluster/datasource/resulttable/storage） |
| `migrations/0003_init_storage_backend_info.py` | 3 KB | 存储后端信息初始化 |
| `migrations/0004_*.py` | 4 KB | DataBusConfig/DataIdConfig 变更 |
| `migrations/0005_*.py` | 16 KB | RelationDefinition/ResourceDefinition 新增 |

核心文件路径：`bk-monitor-base/src/bk_monitor_base/metadata/migrations/`

---

## 三、与其他专家的关系

| 关系 | 专家 | 说明 |
|------|------|------|
| **上游依赖** | 元数据核心模型专家 | 任务操作 DataSource/ResultTable/EventGroup 等模型 |
| **上游依赖** | 存储与数据链路专家 | 任务操作 ESStorage/InfluxDBStorage/DataLink 等模型 |
| **上游依赖** | 空间与自定义上报专家 | 任务操作 Space/SpaceTableIDRedis/CustomReport 等模型 |
| **上游依赖** | API与工具库专家 | 任务使用 utils/ 工具函数、service/ 服务层 |
| **被调用** | 全部专家 | 管理命令可被其他模块通过 `call_command` 调用 |

---

## 四、使用指南

### 4.1 何时查阅本专家

- 需要了解 Celery 任务的定义、调度策略、重试机制
- 需要执行 Django 管理命令进行运维操作
- 需要使用 Redis 分布式锁
- 需要了解种子数据加载机制
- 需要了解数据库迁移策略

### 4.2 文档导航

| 文档 | 内容 | 阅读顺序 |
|------|------|---------|
| `agent.md` | 本文件 | 1 |
| `C0-使用总览.md` | 黑盒使用：Celery 任务体系、管理命令清单、运维工具 | 2 |
| `C1-能力契约.md` | 能力契约：任务签名、命令参数、锁 API、种子数据格式 | 3 |
| `implementation/01-架构.md` | 任务调度架构 | 4 |
| `implementation/02-实现.md` | 核心实现逻辑 | 5 |
| `implementation/03-数据流转.md` | 数据流转链路 | 6 |
| `implementation/04-模型.md` | 数据模型与迁移策略 | 7 |
| `implementation/05-接口.md` | 接口签名与参数 | 8 |

### 4.3 不负责范围

- 具体模型定义（DataSource/ResultTable/ESStorage 等）→ 元数据核心模型专家 / 存储与数据链路专家
- API Resource 层（resources/）→ API与工具库专家
- 服务层业务逻辑（service/）→ API与工具库专家
- 工具函数实现（utils/）→ API与工具库专家
- BCS 模型定义（models/bcs/）→ API与工具库专家
