# 数据源管理子专家

> **父专家**: 元数据核心模型专家
> **类型**: 子专家
> **创建时间**: 2026-07-28
> **最后更新**: 2026-07-28

---

## 一、子专家名片

| 属性 | 值 |
|------|-----|
| **名称** | 数据源管理子专家 |
| **职责** | 管理监控系统的数据源（DataSource）全生命周期——创建、更新、配置同步、MQ 管理、空间归属 |
| **目录** | `.module-experts/元数据管理专题/元数据核心模型专家/sub-experts/数据源管理子专家/` |

## 二、覆盖范围

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `bk-monitor-base/src/bk_monitor_base/metadata/models/data_source.py` | 62 KB | DataSource 模型、DataSourceOption、DataSourceResultTable、CRUD、配置同步 |
| `bk-monitor-base/src/bk_monitor_base/metadata/models/common.py` | 9 KB | Label 标签模型、OptionBase 选项基类 |

> ⚠️ **不覆盖**: `result_table.py`（归结果表管理子专家）、`entity_relation.py`（已在父专家覆盖）、`constants.py`（全局常量，按需引用）

## 三、核心职责边界

### 3.1 本子专家负责

- **DataSource 模型**：字段定义、Meta 配置、索引约束
- **DataSource 生命周期**：创建（`create_data_source`）、更新（`update_config`）、序列化（`to_json`）
- **配置同步**：Consul 配置刷新（`refresh_consul_config`）、GSE 路由同步（`refresh_gse_config`）、外部配置统一入口（`refresh_outer_config`）
- **MQ 管理**：Kafka 集群分配、MQ 配置创建、懒加载属性
- **空间归属**：空间类型/UID 管理、授权空间、SpaceDataSource 关系
- **DataID 分配**：自增分配、GSE 申请、计算平台（BkData）申请
- **DataSourceOption**：数据源级别选项配置
- **DataSourceResultTable**：数据源与结果表的 N:1 映射
- **公共基础模型**：Label 标签体系、OptionBase 选项基类

### 3.2 子专家不负责

- ResultTable 的创建/修改/升级（归结果表管理子专家）
- 存储引擎配置（归存储与数据链路专家）
- 数据链路操作（归存储与数据链路专家）
- 后台任务调度（归任务调度与运维专家）
- API Resource 层（归 API 与工具库专家）

## 四、与父专家其他子专家的关系

| 关系 | 子专家 | 交互内容 |
|------|--------|---------|
| 下游消费者 | 结果表管理子专家 | DataSource 创建后，ResultTable 通过 `bk_data_id` 关联数据源 |
| 共享基础 | 结果表管理子专家 | 共用 `common.py` 中的 Label、OptionBase |

## 五、使用指南

### 5.1 何时查阅本子专家

- 需要了解 DataSource 的创建流程、DataID 分配策略、Kafka 集群选择逻辑
- 需要了解 Consul/GSE 配置同步的触发时机和同步内容
- 需要了解 DataSourceOption 的选项类型和使用方式
- 需要了解 Label 标签体系和 OptionBase 选项机制
- 需要了解数据源的空间归属和授权空间管理

### 5.2 文档导航

| 文档 | 类型 | 说明 |
|------|------|------|
| [C0-使用总览.md](C0-使用总览.md) | 契约层 | 黑盒使用文档：DataSource 能力概览、典型场景、快速上手 |
| [C1-能力契约.md](C1-能力契约.md) | 契约层 | DataSource/DataSourceOption/Label 的完整 API 契约 |
| [implementation/01-架构.md](implementation/01-架构.md) | 实现层 | DataSource 模型架构：类层次、继承关系、设计模式 |
| [implementation/02-实现.md](implementation/02-实现.md) | 实现层 | 核心实现：create_data_source 7 步流程、update_config 逐项更新 |
| [implementation/03-数据流转.md](implementation/03-数据流转.md) | 实现层 | 配置同步：Consul 推送、GSE 路由、空间路由 |
| [implementation/04-模型.md](implementation/04-模型.md) | 实现层 | 数据模型：DataSource/DataSourceOption/DataSourceResultTable 字段定义 |
| [implementation/05-接口.md](implementation/05-接口.md) | 实现层 | 接口说明：所有方法签名、参数、返回值、属性 |

---

> **下一步**: 查阅 [C0-使用总览.md](C0-使用总览.md) 了解 DataSource 的能力和典型使用场景。
