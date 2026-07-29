# BCS与工具库子专家

> **父专家**: API与工具库专家
> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28

---

## 一、子专家名片

| 属性 | 值 |
|------|-----|
| 名称 | BCS与工具库子专家 |
| 职责 | 覆盖 metadata 模块的 Utils 工具库（30+ 模块）和 BCS 模型（4 个文件），负责工具函数封装、BCS 集群模型与 K8S 资源管理 |
| 目录 | `.module-experts/元数据管理专题/API与工具库专家/sub-experts/BCS与工具库子专家/` |

## 二、覆盖文件清单

### 2.1 Utils 工具库（按功能分组）

| 功能组 | 文件 | 大小 | 核心内容 |
|--------|------|------|---------|
| 加密/哈希 | `cipher.py` | 1.0 KB | AES 加密（DataID → Token） |
| | `hash_util.py` | — | MD5 哈希（对象→哈希值） |
| | `hashring.py` | — | 一致性哈希环 |
| 时间 | `time_tools.py` | 11.8 KB | 时区转换/时间范围/格式化 |
| | `time_format.py` | — | 时间格式常量 |
| | `go_time.py` | — | Go 时间格式 |
| Redis | `redis_tools.py` | 5.0 KB | RedisTools 封装（Hash/Set/PubSub） |
| | `redis_client.py` | — | RedisClient 连接管理 |
| Consul | `consul.py` | — | BKConsul 客户端（TLS/HTTP 自适应） |
| | `consul_tools.py` | 4.6 KB | HashConsul（MD5 比对后写入） |
| 请求/上下文 | `request.py` | 5.0 KB | 请求获取/租户ID/用户名 |
| | `local.py` | — | 线程本地存储 |
| | `user.py` | — | 用户工具 |
| | `tenant.py` | 4.0 KB | 租户转换（space_uid↔bk_tenant_id） |
| 序列化 | `serializers.py` | 1.2 KB | TenantIdField（自动注入租户ID） |
| 并发/锁 | `lock.py` | 1.3 KB | share_lock 分布式锁装饰器 |
| 数据库 | `db.py` | — | 数据库工具 |
| ES | `es_tools.py` | — | ES 客户端 |
| | `es_curator.py` | — | ES 索引管理 |
| InfluxDB | `influxdb_tools.py` | — | InfluxDB 工具 |
| BCS/K8S | `bcs.py` | 11.0 KB | BCS 集群工具/DataID 查询 |
| | `k8s_metric.py` | — | K8S 内置指标 |
| 外部集成 | `bkbase.py` | — | 计算平台集成 |
| | `bk_collector_config.py` | — | 采集器配置 |
| | `gse.py` | — | GSE 集成 |
| | `data_link.py` | — | 数据链路工具 |
| | `dataflow_auth.py` | — | 数据流认证 |
| 通用 | `basic.py` | — | 基础工具 |
| | `tools.py` | — | 通用工具 |
| | `env.py` | — | 环境变量 |
| | `version.py` | — | 版本管理 |
| | `space.py` | — | 空间工具 |
| | `api_request.py` | — | API 请求工具 |

### 2.2 BCS 模型

| 文件 | 大小 | 核心内容 |
|------|------|---------|
| `models/bcs/__init__.py` | — | 导出 BCSClusterInfo, ServiceMonitorInfo, PodMonitorInfo, ReplaceConfig, LogCollectorInfo, BcsFederalClusterInfo |
| `models/bcs/cluster.py` | **29 KB** | BCSClusterInfo — K8S 集群信息（核心模型） |
| `models/bcs/resource.py` | 20 KB | BCSResource 抽象基类 → ServiceMonitorInfo, PodMonitorInfo, LogCollectorInfo |
| `models/bcs/replace.py` | — | ReplaceConfig — 替换配置 |
| `models/bcs/utils.py` | — | ensure_data_id_resource, is_equal_config |

## 三、与其他子专家的关系

| 关系 | 对象 | 描述 |
|------|------|------|
| **上游依赖** | 专家1（元数据核心模型） | BCS 模型依赖 DataSource、ResultTable、TimeSeriesGroup、EventGroup |
| **同级** | API资源子专家 | Resource 层通过 utils/ 工具函数和 BCS 模型完成业务逻辑 |
| **契约边界** | utils/ 工具函数归本子专家 | 函数签名与实现细节均归本子专家 |

## 四、关键约束

- `models/bcs/cluster.py`（29KB）是 BCS 核心模型，聚焦 `BCSClusterInfo.init_resource()` 和 DataID 创建流程
- `utils/bcs.py`（11KB）是 BCS 工具核心，聚焦 `get_bcs_dataids()` 和 `BcsKubeClient`
- 工具函数设计原则：无状态、单一职责、低耦合、可测试
- `HashConsul` 的 MD5 比对机制是减少 Consul 写入压力的关键设计
