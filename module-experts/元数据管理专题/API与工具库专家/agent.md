# API与工具库专家

> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28
> **最后更新**: 2026-07-28
> **批次**: Batch 2

---

## 一、专家名片

| 属性 | 值 |
|------|-----|
| 名称 | API与工具库专家 |
| 职责 | 管理元数据的 API 接口（Resource 层）、服务层接口契约、通用工具函数库、BCS 容器服务集成 |
| 目录 | `.module-experts/元数据管理专题/API与工具库专家/` |

## 二、覆盖文件清单

### 2.1 Resource 层（8 个文件）

| 文件 | 大小 | 内容 |
|------|------|------|
| `resources/__init__.py` | 0 B | 空文件 |
| `resources/base.py` | 5.3 KB | Resource 抽象基类：请求/响应校验、异常转换 |
| `resources/resources.py` | **152 KB** | 核心 Resource 类（~3495 行）：数据源 CRUD、结果表 CRUD、字段管理、BCS 集成等 |
| `resources/cluster.py` | 18.4 KB | 集群管理 Resource：注册/查询/修改/删除集群 |
| `resources/bkdata_link.py` | 50.9 KB | 计算平台数据链路 Resource |
| `resources/datalink_operation.py` | 18.1 KB | 数据链路操作 Resource |
| `resources/entity_relation.py` | 20.7 KB | 实体关系 Resource（声明式 API） |
| `resources/log_datalink.py` | 39.1 KB | 日志数据链路 Resource |
| `resources/space.py` | 18.2 KB | 空间相关 Resource |
| `resources/vm.py` | 13.1 KB | VM 存储相关 Resource |

### 2.2 Service 层（7 个文件）

| 文件 | 大小 | 内容 |
|------|------|------|
| `service/__init__.py` | 0 B | 空文件 |
| `service/data_source.py` | 6.0 KB | 数据源服务：Kafka 集群管理、启停数据源、数据源来源切换 |
| `service/storage_details.py` | 17.9 KB | 存储详情服务：结果表与数据源详情查询、集群详情 |
| `service/sync_metadata.py` | 12.1 KB | 元数据同步：Kafka/ES/VM 元数据同步 |
| `service/space_redis.py` | 2.9 KB | 空间 Redis 服务：空间配置缓存、ES 别名推送 |
| `service/es_storage.py` | 2.6 KB | ES 存储服务：索引查询、过期索引清理 |
| `service/vm_storage.py` | 8.8 KB | VM 存储服务：InfluxDB 路由切换、VM 链路查询 |
| `service/influxdb_instance.py` | 1.5 KB | InfluxDB 实例服务 |

### 2.3 Utils 工具库（34 个文件）

按功能分组：

| 分组 | 文件 | 说明 |
|------|------|------|
| **加密/哈希** | `cipher.py`, `hash_util.py`, `hashring.py` | AES 加密、MD5 哈希、一致性哈希环 |
| **时间** | `time_tools.py`, `time_format.py`, `go_time.py` | 时间转换、格式解析、时区处理 |
| **Redis** | `redis_tools.py`, `redis_client.py` | Redis 操作封装（Hash/Set/PubSub） |
| **Consul** | `consul.py`, `consul_tools.py` | Consul 客户端、哈希 Consul 工具 |
| **请求/上下文** | `request.py`, `local.py`, `user.py`, `tenant.py` | 请求获取、租户 ID、用户名、线程本地 |
| **序列化** | `serializers.py` | TenantIdField 自定义字段 |
| **并发/锁** | `lock.py` | 分布式锁装饰器 |
| **数据库** | `db.py` | 数据库工具 |
| **ES** | `es_tools.py`, `es_curator.py` | ES 客户端、索引管理 |
| **InfluxDB** | `influxdb_tools.py` | InfluxDB 工具 |
| **BCS/K8S** | `bcs.py`, `k8s_metric.py` | BCS 集群工具、K8S 指标 |
| **外部集成** | `bkbase.py`, `bk_collector_config.py`, `gse.py`, `data_link.py`, `dataflow_auth.py` | 计算平台、采集器、GSE、数据链路、数据流认证 |
| **通用** | `basic.py`, `tools.py`, `env.py`, `version.py`, `space.py`, `api_request.py` | 基础工具、环境变量、版本、空间 |

### 2.4 BCS 模型（4 个文件）

| 文件 | 大小 | 内容 |
|------|------|------|
| `models/bcs/__init__.py` | 0.3 KB | 导出 BCSClusterInfo, ServiceMonitorInfo, PodMonitorInfo, ReplaceConfig, LogCollectorInfo, BcsFederalClusterInfo |
| `models/bcs/cluster.py` | 28.9 KB | BCSClusterInfo 模型：集群注册、DataID 管理、资源初始化 |
| `models/bcs/resource.py` | 20.4 KB | BCSResource 抽象基类、ServiceMonitorInfo、PodMonitorInfo |
| `models/bcs/replace.py` | 6.4 KB | ReplaceConfig 替换配置模型 |
| `models/bcs/utils.py` | 2.7 KB | BCS 工具函数 |

## 三、子专家列表

| 子专家 | 覆盖范围 | 重点文件 |
|--------|---------|---------|
| API资源子专家 | resources/ 全包 + service/ 服务层 | `resources.py`(152KB), `cluster.py`, `entity_relation.py`, `bkdata_link.py` |
| BCS与工具库子专家 | models/bcs/ + utils/ 全包 | `bcs/cluster.py`(29KB), `utils/`(34文件) |

## 四、与其他专家的关系

| 关系 | 对象 | 描述 |
|------|------|------|
| **上游依赖** | 专家1（元数据核心模型） | Resource 层通过 Service 层读写 DataSource、ResultTable 等模型 |
| | 专家2（存储与数据链路） | Resource 层通过 Service 层配置存储引擎、管理数据链路 |
| | 专家3（空间与自定义上报） | Resource 层通过 Service 层管理空间、自定义上报 |
| **下游被依赖** | 外部 API 网关（`api/metadata/default.py`） | 将 Resource 暴露为 HTTP 端点 |
| | 内核 API（`kernel_api/`） | 内核直连 Resource |
| **契约边界** | service/ 接口契约归本专家 | 实现细节归对应功能域子专家（如 `space_redis.py` 实现归空间管理子专家） |
| **公共依赖** | `core/drf_resource/` | Resource 框架基类（外部框架） |
| | `models/constants.py` (139KB) | 全局常量（T0 统一索引） |
| | `models/serializers.py` | ModelSerializer（公共序列化器） |

## 五、关键约束

- `resources/resources.py` (152KB) 是第二大单文件，不要全文读取，聚焦核心 Resource 类
- `service/` 的接口契约归本专家，实现细节归对应功能域子专家
- `utils/` 30+ 工具模块按功能分组（加密/哈希/时间/并发/分页/Redis/上下文等）
- BCS 模型（`models/bcs/`）仅覆盖 metadata 侧模型定义，APM 层的 BCS 操作不在本专题范围
