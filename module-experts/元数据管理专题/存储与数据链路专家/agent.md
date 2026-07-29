# 存储与数据链路专家

> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28
> **最后更新**: 2026-07-28
> **工作量**: 9 个核心文件，最大单文件 `storage.py` 240KB

---

## 一、专家名片

| 属性 | 值 |
|------|-----|
| 名称 | 存储与数据链路专家 |
| 职责 | 管理监控数据的存储引擎配置（InfluxDB/ES/Kafka/VM/Doris）、数据链路编排（清洗/汇聚/流转）、ES 快照、集群管理 |
| 目录 | `.module-experts/元数据管理专题/存储与数据链路专家/` |

## 二、覆盖文件清单

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `models/storage.py` | 240 KB | ClusterInfo、InfluxDBStorage、ESStorage、KafkaStorage、RedisStorage、DorisStorage、ArgusStorage、BkDataStorage、StorageClusterRecord、SpaceRelatedStorageInfo |
| `models/data_link/data_link.py` | 56 KB | DataLink 主模型、策略枚举、链路申请/删除/元数据同步 |
| `models/data_link/data_link_configs.py` | 42 KB | DataLinkResourceConfigBase 基类、DataIdConfig、ResultTableConfig、VMStorageBindingConfig、ESStorageBindingConfig、DorisStorageBindingConfig、DataBusConfig、ConditionalSinkConfig、ClusterConfig |
| `models/data_link/relation.py` | 18 KB | BKBase V4 组件关联关系重建 |
| `models/data_link/service.py` | 8 KB | apply_data_id_v2、get_data_id_v2、组件状态/配置查询 |
| `models/data_link/utils.py` | 10 KB | 命名规则、模板渲染、字段组装 |
| `models/data_link/constants.py` | 3.5 KB | DataLinkKind、DataLinkResourceStatus、命名空间常量 |
| `models/es_snapshot.py` | 55 KB | EsSnapshot、EsSnapshotRepository、EsSnapshotIndice、EsSnapshotRestore |
| `models/influxdb_cluster.py` | 34 KB | InfluxDBTagInfo、InfluxDBClusterInfo、InfluxDBHostInfo、InfluxDBProxyStorage |
| `models/vm/` | 6 文件 | BkDataClean、BkDataStorage、AccessVMRecord、SpaceVMInfo、BkDataAccessor |

## 三、子专家列表

| 子专家 | 覆盖范围 | 重点文件 | 目录 |
|--------|---------|---------|------|
| 存储引擎子专家 | storage + influxdb_cluster + vm + es_snapshot | `storage.py`(240KB), `es_snapshot.py`, `influxdb_cluster.py`, `vm/` | `sub-experts/存储引擎子专家/` |
| 数据链路子专家 | data_link 全包 | `data_link/`(6文件) | `sub-experts/数据链路子专家/` |

## 四、与其他专家的关系

| 关系 | 对方专家 | 说明 |
|------|---------|------|
| **上游依赖** | 元数据核心模型专家 | Storage 模型依赖 ResultTable（table_id 外键）、DataSource（bk_data_id）；DataLink 依赖 DataSource、DataSourceResultTable |
| **上游依赖** | 空间与自定义上报专家 | Space 隔离影响存储路由；SpaceTableIDRedis 刷新 ES 路由 |
| **下游消费** | 任务调度与运维专家 | task/ 调用 Storage 模型做索引轮转/清理/Consul 刷新 |
| **下游消费** | API与工具库专家 | resources/ 通过 service/ 调用 Storage CRUD |
| **跨模块** | APM 模块 | APM 引用 metadata 存储模型做拓扑构建；DataLink 模型定义在 metadata，操作服务在 APM（不在本专题范围） |

## 五、关键约束

- `storage.py` 240KB 是最大单文件，子专家需聚焦核心模型，细节按需引用源码行号
- 数据链路子专家仅覆盖 metadata 模型定义层，APM 层操作服务（`apm/views.py` 等）不在本专题范围
- 参考 Wiki：`bk-monitor-wiki/wiki/核心模块架构/元数据管理模块/元数据服务层/数据链路操作服务.md`（注意区分 metadata 模型 vs APM 操作服务）
