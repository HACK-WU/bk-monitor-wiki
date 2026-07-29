# 元数据核心模型专家

> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28
> **最后更新**: 2026-07-28
> **类型**: 专家（含子专家）

---

## 一、专家名片

| 属性 | 值 |
|------|-----|
| **名称** | 元数据核心模型专家 |
| **职责** | 管理监控系统的核心元数据定义——数据源（DataSource）、结果表（ResultTable）、实体关系（EntityRelation）及公共基础模型 |
| **目录** | `.module-experts/元数据管理专题/元数据核心模型专家/` |

## 二、覆盖文件清单

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `bk-monitor-base/src/bk_monitor_base/metadata/models/data_source.py` | 62 KB | DataSource 模型、数据源 CRUD、连接管理、Consul/GSE 配置同步 |
| `bk-monitor-base/src/bk_monitor_base/metadata/models/result_table.py` | 139 KB | ResultTable、ResultTableField、ResultTableOption、CMDBLevelRecord 等 |
| `bk-monitor-base/src/bk_monitor_base/metadata/models/common.py` | 9 KB | Label 标签模型、OptionBase 基类、BaseModel/BaseModelWithTime 抽象基类 |
| `bk-monitor-base/src/bk_monitor_base/metadata/models/entity_relation.py` | 8 KB | EntityMeta 抽象基类、ResourceDefinition、RelationDefinition、CustomRelationStatus |

> ⚠️ **`models/constants.py`（139KB）不归属本专家**。该文件为全局常量，已在 T0-专题总览中做结构化索引，各子专家按需引用。

## 三、子专家列表

| 子专家 | 目录 | 覆盖范围 | 重点文件 |
|--------|------|---------|---------|
| 数据源管理子专家 | `sub-experts/数据源管理子专家/` | DataSource 全链路 + 公共模型 | `data_source.py`(62KB), `common.py` |
| 结果表管理子专家 | `sub-experts/结果表管理子专家/` | ResultTable + Field + Option + CMDBLevelRecord | `result_table.py`(139KB) |

## 四、与其他专家的关系

### 4.1 上游依赖

| 上游专家 | 依赖内容 | 用途 |
|---------|---------|------|
| 存储与数据链路专家 | `models/storage.py` 中的 ClusterInfo、ESStorage、InfluxDBStorage 等 | DataSource 的 MQ 集群配置、ResultTable 的存储创建与管理 |
| 空间与自定义上报专家 | `models/space/` 中的 Space、SpaceDataSource | DataSource 的空间归属、ResultTable 的空间路由 |

### 4.2 下游消费者

| 下游模块 | 引用方式 | 影响 |
|---------|---------|------|
| `alarm_backends/` | 引用 metadata 模型做告警计算 | 修改 DataSource/ResultTable 字段需评估告警影响 |
| `apm/` | 引用 metadata 模型做 APM 拓扑 | EntityRelation 被 APM 层消费 |
| `api/metadata/default.py` | 通过 API 网关暴露 | 模型变更影响外部 API |
| `kernel_api/` | 路由注册与直连 | 模型变更影响内核 API |

### 4.3 跨模块边界

- **entity_relation.py** 跨 metadata + APM + bkm_ipchooser 三个模块，本专家仅覆盖 metadata 侧模型定义
- **data_source.py** 中的 `register_to_bkbase` 方法涉及计算平台集成，数据链路细节由存储与数据链路专家覆盖

## 五、使用指南

### 5.1 何时查阅本专家

- 需要了解 DataSource 的创建流程、字段含义、配置同步机制
- 需要了解 ResultTable 的生命周期管理（创建/修改/升级/删除）
- 需要了解 ResultTableField 的字段类型、标签、默认字段创建逻辑
- 需要了解 Label 标签体系、OptionBase 选项机制
- 需要了解 EntityRelation 的实体元数据模型设计

### 5.2 文档导航

| 文档 | 类型 | 说明 |
|------|------|------|
| [C0-使用总览.md](C0-使用总览.md) | 契约层 | 黑盒使用文档：能力概览、典型场景、快速上手 |
| [C1-能力契约.md](C1-能力契约.md) | 契约层 | 核心 API 契约、字段说明、约束条件、高频常量 |
| [implementation/01-架构.md](implementation/01-架构.md) | 实现层 | 模型层架构：类层次、继承关系、模型间关系 |
| [implementation/02-实现.md](implementation/02-实现.md) | 实现层 | 核心实现：DataSource CRUD、ResultTable 管理逻辑 |
| [implementation/03-数据流转.md](implementation/03-数据流转.md) | 实现层 | 数据流转：数据源→结果表→存储引擎的数据链路 |
| [implementation/04-模型.md](implementation/04-模型.md) | 实现层 | 数据模型：字段定义、索引、约束、Django ORM 配置 |
| [implementation/05-接口.md](implementation/05-接口.md) | 实现层 | 接口说明：模型对外暴露的方法签名、参数、返回值 |

### 5.3 子专家导航

| 子专家 | 文档入口 |
|--------|---------|
| 数据源管理子专家 | [sub-experts/数据源管理子专家/agent.md](sub-experts/数据源管理子专家/agent.md) |
| 结果表管理子专家 | [sub-experts/结果表管理子专家/agent.md](sub-experts/结果表管理子专家/agent.md) |

---

> **下一步**: 查阅 [C0-使用总览.md](C0-使用总览.md) 了解本专家覆盖的能力和典型使用场景。
