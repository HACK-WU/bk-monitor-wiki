# 结果表管理子专家

> **父专家**: 元数据核心模型专家
> **类型**: 子专家
> **创建时间**: 2026-07-28
> **最后更新**: 2026-07-28

---

## 一、子专家名片

| 属性 | 值 |
|------|-----|
| **名称** | 结果表管理子专家 |
| **职责** | 管理监控系统的结果表（ResultTable）全生命周期——创建、修改、升级、字段管理、存储管理、数据链路应用 |
| **目录** | `.module-experts/元数据管理专题/元数据核心模型专家/sub-experts/结果表管理子专家/` |

## 二、覆盖范围

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `bk-monitor-base/src/bk_monitor_base/metadata/models/result_table.py` | 139 KB | ResultTable、ResultTableField、ResultTableOption、ResultTableFieldOption、CMDBLevelRecord 等 |

> ⚠️ **不覆盖**: `data_source.py`（归数据源管理子专家）、`common.py`（归数据源管理子专家）、`entity_relation.py`（已在父专家覆盖）、`constants.py`（全局常量，按需引用）

## 三、核心职责边界

### 3.1 本子专家负责

- **ResultTable 模型**：字段定义、Meta 配置、索引约束、存储映射
- **ResultTable 生命周期**：创建（`create_result_table`）、修改（`modify`）、升级为全业务（`upgrade_result_table`）
- **字段管理**：ResultTableField 的创建、批量创建、默认字段生成、保留字检查
- **存储管理**：默认存储设置、额外存储创建/删除、存储校验
- **数据链路**：`apply_datalink()` 决策树（V3/V4/日志V4/事件组V4）
- **选项配置**：ResultTableOption（分段查询、字段黑名单、V4链路开关等）
- **字段选项**：ResultTableFieldOption（ES 类型、ES 格式、ES include_in_all 等）
- **CMDB 层级拆分**：`set_metric_split()` / `clean_metric_split()`
- **空间路由**：结果表启用时推送 Redis 路由
- **序列化**：`to_json()` / `to_json_self_only()` / `batch_to_json()`

### 3.2 子专家不负责

- DataSource 的创建/更新/配置同步（归数据源管理子专家）
- 存储引擎的物理创建（归存储与数据链路专家）
- 数据链路的异步任务执行（归任务调度与运维专家）
- API Resource 层（归 API 与工具库专家）

## 四、与父专家其他子专家的关系

| 关系 | 子专家 | 交互内容 |
|------|--------|---------|
| 上游依赖 | 数据源管理子专家 | ResultTable 通过 `bk_data_id` 关联 DataSource，创建时校验数据源存在性 |
| 共享基础 | 数据源管理子专家 | 共用 `common.py` 中的 Label、OptionBase |

## 五、使用指南

### 5.1 何时查阅本子专家

- 需要了解 ResultTable 的创建流程、字段管理、存储创建逻辑
- 需要了解 `modify()` 的逐项更新流程和字段重建机制
- 需要了解 `upgrade_result_table()` 的升级步骤
- 需要了解 `apply_datalink()` 的链路选择决策树
- 需要了解 ResultTableField 的字段类型、标签、默认字段
- 需要了解 CMDB 层级拆分的实现
- 需要了解 ResultTableOption/ResultTableFieldOption 的选项类型

### 5.2 文档导航

| 文档 | 类型 | 说明 |
|------|------|------|
| [C0-使用总览.md](C0-使用总览.md) | 契约层 | 黑盒使用文档：ResultTable 能力概览、典型场景、快速上手 |
| [C1-能力契约.md](C1-能力契约.md) | 契约层 | ResultTable/ResultTableField/ResultTableOption 的完整 API 契约 |
| [implementation/01-架构.md](implementation/01-架构.md) | 实现层 | ResultTable 模型架构：类层次、继承关系、存储映射 |
| [implementation/02-实现.md](implementation/02-实现.md) | 实现层 | 核心实现：create_result_table 13 步流程、modify 逐项更新、upgrade |
| [implementation/03-数据流转.md](implementation/03-数据流转.md) | 实现层 | 数据链路：V3/V4 决策树、空间路由、ETL 配置刷新 |
| [implementation/04-模型.md](implementation/04-模型.md) | 实现层 | 数据模型：ResultTable/Field/Option/CMDBLevelRecord 字段定义 |
| [implementation/05-接口.md](implementation/05-接口.md) | 实现层 | 接口说明：所有方法签名、参数、返回值、属性 |

---

> **下一步**: 查阅 [C0-使用总览.md](C0-使用总览.md) 了解 ResultTable 的能力和典型使用场景。
