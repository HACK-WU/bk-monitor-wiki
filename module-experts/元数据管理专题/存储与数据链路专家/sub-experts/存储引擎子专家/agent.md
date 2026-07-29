# 存储引擎子专家

> **父专家**: 存储与数据链路专家
> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28

---

## 一、子专家名片

| 属性 | 值 |
|------|-----|
| 名称 | 存储引擎子专家 |
| 职责 | 管理监控数据的存储引擎配置：InfluxDB/ES/Kafka/VM/Doris/Redis/Argus 存储模型、集群管理、ES 快照、VM 配置 |
| 目录 | `sub-experts/存储引擎子专家/` |

## 二、覆盖文件清单

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `models/storage.py` | 240 KB | ClusterInfo、InfluxDBStorage、ESStorage、KafkaStorage、RedisStorage、DorisStorage、ArgusStorage、BkDataStorage、StorageClusterRecord、SpaceRelatedStorageInfo |
| `models/es_snapshot.py` | 55 KB | EsSnapshot、EsSnapshotRepository、EsSnapshotIndice、EsSnapshotRestore |
| `models/influxdb_cluster.py` | 34 KB | InfluxDBTagInfo、InfluxDBClusterInfo、InfluxDBHostInfo、InfluxDBProxyStorage、InfluxDBTool |
| `models/vm/` | 6 文件 | BkDataClean、BkDataStorage、BkDataStorageWithDataID、AccessVMRecord、SpaceVMInfo、BkDataAccessor |

## 三、关键约束

- `storage.py` 240KB 是最大单文件，聚焦核心模型（ClusterInfo、InfluxDBStorage、ESStorage、KafkaStorage、DorisStorage），细节按需引用源码行号
- 不覆盖 `data_link/` 包（归数据链路子专家）
- 与元数据核心模型专家的边界：Storage 模型通过 `table_id` 关联 ResultTable，但不负责 ResultTable 本身的定义
