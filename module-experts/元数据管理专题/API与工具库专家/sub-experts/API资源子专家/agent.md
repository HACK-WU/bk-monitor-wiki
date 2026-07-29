# API资源子专家

> **父专家**: API与工具库专家
> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28

---

## 一、子专家名片

| 属性 | 值 |
|------|-----|
| 名称 | API资源子专家 |
| 职责 | 覆盖 metadata 模块的 Resource 层（8 个文件）和 Service 层（7 个文件），负责 API 接口定义、请求处理流程、服务层接口契约 |
| 目录 | `.module-experts/元数据管理专题/API与工具库专家/sub-experts/API资源子专家/` |

## 二、覆盖文件清单

### 2.1 Resource 层

| 文件 | 大小 | 核心内容 |
|------|------|---------|
| `resources/__init__.py` | 0 B | 空 |
| `resources/base.py` | 5.3 KB | `Resource` 抽象基类、`format_serializer_errors` |
| `resources/resources.py` | **152 KB** | 核心 Resource：数据源 CRUD、结果表 CRUD、字段管理、BCS 集成等 |
| `resources/cluster.py` | 18.4 KB | 集群管理：注册/查询/修改/删除 |
| `resources/bkdata_link.py` | 50.9 KB | 计算平台数据链路 Resource |
| `resources/datalink_operation.py` | 18.1 KB | 数据链路操作 Resource |
| `resources/entity_relation.py` | 20.7 KB | 实体关系声明式 API |
| `resources/log_datalink.py` | 39.1 KB | 日志数据链路 Resource |
| `resources/space.py` | 18.2 KB | 空间管理 Resource |
| `resources/vm.py` | 13.1 KB | VM 存储 Resource |

### 2.2 Service 层

| 文件 | 大小 | 核心内容 |
|------|------|---------|
| `service/__init__.py` | 0 B | 空 |
| `service/data_source.py` | 6.0 KB | 数据源服务 |
| `service/storage_details.py` | 17.9 KB | 存储详情服务 |
| `service/sync_metadata.py` | 12.1 KB | 元数据同步 |
| `service/space_redis.py` | 2.9 KB | 空间 Redis |
| `service/es_storage.py` | 2.6 KB | ES 存储 |
| `service/vm_storage.py` | 8.8 KB | VM 存储 |
| `service/influxdb_instance.py` | 1.5 KB | InfluxDB 实例 |

## 三、与其他子专家的关系

| 关系 | 对象 | 描述 |
|------|------|------|
| **上游依赖** | 专家1（元数据核心模型） | Resource 通过 Service 读写 DataSource、ResultTable |
| | 专家2（存储与数据链路） | Resource 通过 Service 配置存储引擎 |
| | 专家3（空间与自定义上报） | Resource 通过 Service 管理空间 |
| **同级** | BCS与工具库子专家 | 本子专家使用 utils/ 工具函数和 BCS 模型 |
| **契约边界** | service/ 接口契约归本子专家 | 实现细节归对应功能域子专家 |

## 四、关键约束

- `resources/resources.py`（152KB）是第二大单文件，聚焦核心 Resource 类而非全文
- `service/` 的接口契约归本子专家，实现细节归对应功能域子专家
- Resource 基类 `base.py` 定义了统一的请求处理模式
