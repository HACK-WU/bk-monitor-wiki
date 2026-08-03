# INDEX — 元数据管理专题 全量文件索引

> **专题路径**: `.module-experts/元数据管理专题/`
> **生成时间**: 2026-07-29
> **状态**: ✅ 全部批次完成
> **总文档数**: 118 份

---

## 一、专题层（3 份）

| 文件 | 说明 |
|------|------|
| [topic.md](topic.md) | 专题名片：范围、专家列表、批次信息 |
| [T0-专题总览.md](T0-专题总览.md) | 跨专家架构图、依赖边界、constants.py 索引、数据流全景 |
| [PLAN.md](PLAN.md) | 分批创建计划、模块评估、产出统计、Wiki 参考索引 |

---

## 二、专家 1：元数据核心模型（24 份）

**路径**: `元数据核心模型专家/`
**覆盖**: `data_source.py`(62KB), `result_table.py`(139KB), `common.py`, `entity_relation.py`

### 2.1 专家层（8 份）

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](元数据核心模型专家/agent.md) | 4.85 KB | 专家名片 |
| [C0-使用总览.md](元数据核心模型专家/C0-使用总览.md) | 6.34 KB | 黑盒使用文档 |
| [C1-能力契约.md](元数据核心模型专家/C1-能力契约.md) | 13.08 KB | API 契约 |
| [implementation/01-架构.md](元数据核心模型专家/implementation/01-架构.md) | 8.19 KB | 模型层架构 |
| [implementation/02-实现.md](元数据核心模型专家/implementation/02-实现.md) | 7.53 KB | 核心实现 |
| [implementation/03-数据流转.md](元数据核心模型专家/implementation/03-数据流转.md) | 6.59 KB | 数据流转 |
| [implementation/04-模型.md](元数据核心模型专家/implementation/04-模型.md) | 8.99 KB | 数据模型 |
| [implementation/05-接口.md](元数据核心模型专家/implementation/05-接口.md) | 9.89 KB | 接口说明 |

### 2.2 数据源管理子专家（8 份）

**路径**: `元数据核心模型专家/sub-experts/数据源管理子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](元数据核心模型专家/sub-experts/数据源管理子专家/agent.md) | 4.06 KB | 子专家名片 |
| [C0-使用总览.md](元数据核心模型专家/sub-experts/数据源管理子专家/C0-使用总览.md) | 5.56 KB | 使用总览 |
| [C1-能力契约.md](元数据核心模型专家/sub-experts/数据源管理子专家/C1-能力契约.md) | 10.75 KB | 能力契约 |
| [implementation/01-架构.md](元数据核心模型专家/sub-experts/数据源管理子专家/implementation/01-架构.md) | 5.94 KB | 架构 |
| [implementation/02-实现.md](元数据核心模型专家/sub-experts/数据源管理子专家/implementation/02-实现.md) | 15.10 KB | 核心实现 |
| [implementation/03-数据流转.md](元数据核心模型专家/sub-experts/数据源管理子专家/implementation/03-数据流转.md) | 9.10 KB | 数据流转 |
| [implementation/04-模型.md](元数据核心模型专家/sub-experts/数据源管理子专家/implementation/04-模型.md) | 7.70 KB | 数据模型 |
| [implementation/05-接口.md](元数据核心模型专家/sub-experts/数据源管理子专家/implementation/05-接口.md) | 7.09 KB | 接口说明 |

### 2.3 结果表管理子专家（8 份）

**路径**: `元数据核心模型专家/sub-experts/结果表管理子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](元数据核心模型专家/sub-experts/结果表管理子专家/agent.md) | 4.22 KB | 子专家名片 |
| [C0-使用总览.md](元数据核心模型专家/sub-experts/结果表管理子专家/C0-使用总览.md) | 6.65 KB | 使用总览 |
| [C1-能力契约.md](元数据核心模型专家/sub-experts/结果表管理子专家/C1-能力契约.md) | 9.12 KB | 能力契约 |
| [implementation/01-架构.md](元数据核心模型专家/sub-experts/结果表管理子专家/implementation/01-架构.md) | 6.70 KB | 架构 |
| [implementation/02-实现.md](元数据核心模型专家/sub-experts/结果表管理子专家/implementation/02-实现.md) | 16.16 KB | 核心实现 |
| [implementation/03-数据流转.md](元数据核心模型专家/sub-experts/结果表管理子专家/implementation/03-数据流转.md) | 7.74 KB | 数据流转 |
| [implementation/04-模型.md](元数据核心模型专家/sub-experts/结果表管理子专家/implementation/04-模型.md) | 6.75 KB | 数据模型 |
| [implementation/05-接口.md](元数据核心模型专家/sub-experts/结果表管理子专家/implementation/05-接口.md) | 6.24 KB | 接口说明 |

---

## 三、专家 2：存储与数据链路（24 份）

**路径**: `存储与数据链路专家/`
**覆盖**: `storage.py`(240KB), `data_link/`(6文件), `es_snapshot.py`(55KB), `influxdb_cluster.py`(34KB), `vm/`

### 3.1 专家层（8 份）

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](存储与数据链路专家/agent.md) | 3.48 KB | 专家名片 |
| [C0-使用总览.md](存储与数据链路专家/C0-使用总览.md) | 5.50 KB | 黑盒使用文档 |
| [C1-能力契约.md](存储与数据链路专家/C1-能力契约.md) | 9.26 KB | API 契约 |
| [implementation/01-架构.md](存储与数据链路专家/implementation/01-架构.md) | 8.60 KB | 存储引擎架构 |
| [implementation/02-实现.md](存储与数据链路专家/implementation/02-实现.md) | 8.01 KB | 核心实现 |
| [implementation/03-数据流转.md](存储与数据链路专家/implementation/03-数据流转.md) | 6.05 KB | 数据流转 |
| [implementation/04-模型.md](存储与数据链路专家/implementation/04-模型.md) | 13.99 KB | 数据模型 |
| [implementation/05-接口.md](存储与数据链路专家/implementation/05-接口.md) | 11.62 KB | 接口说明 |

### 3.2 存储引擎子专家（8 份）

**路径**: `存储与数据链路专家/sub-experts/存储引擎子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](存储与数据链路专家/sub-experts/存储引擎子专家/agent.md) | 1.46 KB | 子专家名片 |
| [C0-使用总览.md](存储与数据链路专家/sub-experts/存储引擎子专家/C0-使用总览.md) | 2.43 KB | 使用总览 |
| [C1-能力契约.md](存储与数据链路专家/sub-experts/存储引擎子专家/C1-能力契约.md) | 4.76 KB | 能力契约 |
| [implementation/01-架构.md](存储与数据链路专家/sub-experts/存储引擎子专家/implementation/01-架构.md) | 4.70 KB | 架构 |
| [implementation/02-实现.md](存储与数据链路专家/sub-experts/存储引擎子专家/implementation/02-实现.md) | 4.06 KB | 核心实现 |
| [implementation/03-数据流转.md](存储与数据链路专家/sub-experts/存储引擎子专家/implementation/03-数据流转.md) | 2.82 KB | 数据流转 |
| [implementation/04-模型.md](存储与数据链路专家/sub-experts/存储引擎子专家/implementation/04-模型.md) | 8.61 KB | 数据模型 |
| [implementation/05-接口.md](存储与数据链路专家/sub-experts/存储引擎子专家/implementation/05-接口.md) | 5.92 KB | 接口说明 |

### 3.3 数据链路子专家（8 份）

**路径**: `存储与数据链路专家/sub-experts/数据链路子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](存储与数据链路专家/sub-experts/数据链路子专家/agent.md) | 1.99 KB | 子专家名片 |
| [C0-使用总览.md](存储与数据链路专家/sub-experts/数据链路子专家/C0-使用总览.md) | 2.92 KB | 使用总览 |
| [C1-能力契约.md](存储与数据链路专家/sub-experts/数据链路子专家/C1-能力契约.md) | 3.77 KB | 能力契约 |
| [implementation/01-架构.md](存储与数据链路专家/sub-experts/数据链路子专家/implementation/01-架构.md) | 2.81 KB | 架构 |
| [implementation/02-实现.md](存储与数据链路专家/sub-experts/数据链路子专家/implementation/02-实现.md) | 4.95 KB | 核心实现 |
| [implementation/03-数据流转.md](存储与数据链路专家/sub-experts/数据链路子专家/implementation/03-数据流转.md) | 3.49 KB | 数据流转 |
| [implementation/04-模型.md](存储与数据链路专家/sub-experts/数据链路子专家/implementation/04-模型.md) | 6.35 KB | 数据模型 |
| [implementation/05-接口.md](存储与数据链路专家/sub-experts/数据链路子专家/implementation/05-接口.md) | 5.15 KB | 接口说明 |

---

## 四、专家 3：空间与自定义上报（25 份）

**路径**: `空间与自定义上报专家/`
**覆盖**: `space/`(6文件), `custom_report/`(5文件), `record_rule/`(4文件)

### 4.1 专家层（9 份）

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](空间与自定义上报专家/agent.md) | 2.11 KB | 专家名片 |
| [C0-使用总览.md](空间与自定义上报专家/C0-使用总览.md) | 4.37 KB | 黑盒使用文档 |
| [C1-能力契约.md](空间与自定义上报专家/C1-能力契约.md) | 11.99 KB | API 契约 |
| [CHANGELOG.md](空间与自定义上报专家/CHANGELOG.md) | 3.36 KB | 变更日志 |
| [implementation/01-架构.md](空间与自定义上报专家/implementation/01-架构.md) | 8.39 KB | 空间与上报架构 |
| [implementation/02-实现.md](空间与自定义上报专家/implementation/02-实现.md) | 9.38 KB | 核心实现 |
| [implementation/03-数据流转.md](空间与自定义上报专家/implementation/03-数据流转.md) | 8.37 KB | 数据流转 |
| [implementation/04-模型.md](空间与自定义上报专家/implementation/04-模型.md) | 8.94 KB | 数据模型 |
| [implementation/05-接口.md](空间与自定义上报专家/implementation/05-接口.md) | 12.15 KB | 接口说明 |

### 4.2 空间管理子专家（8 份）

**路径**: `空间与自定义上报专家/sub-experts/空间管理子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](空间与自定义上报专家/sub-experts/空间管理子专家/agent.md) | 2.33 KB | 子专家名片 |
| [C0-使用总览.md](空间与自定义上报专家/sub-experts/空间管理子专家/C0-使用总览.md) | 4.46 KB | 使用总览 |
| [C1-能力契约.md](空间与自定义上报专家/sub-experts/空间管理子专家/C1-能力契约.md) | 14.07 KB | 能力契约 |
| [implementation/01-架构.md](空间与自定义上报专家/sub-experts/空间管理子专家/implementation/01-架构.md) | 9.14 KB | 架构 |
| [implementation/02-实现.md](空间与自定义上报专家/sub-experts/空间管理子专家/implementation/02-实现.md) | 9.76 KB | 核心实现 |
| [implementation/03-数据流转.md](空间与自定义上报专家/sub-experts/空间管理子专家/implementation/03-数据流转.md) | 8.46 KB | 数据流转 |
| [implementation/04-模型.md](空间与自定义上报专家/sub-experts/空间管理子专家/implementation/04-模型.md) | 8.53 KB | 数据模型 |
| [implementation/05-接口.md](空间与自定义上报专家/sub-experts/空间管理子专家/implementation/05-接口.md) | 9.27 KB | 接口说明 |

### 4.3 自定义上报子专家（8 份）

**路径**: `空间与自定义上报专家/sub-experts/自定义上报子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](空间与自定义上报专家/sub-experts/自定义上报子专家/agent.md) | 2.33 KB | 子专家名片 |
| [C0-使用总览.md](空间与自定义上报专家/sub-experts/自定义上报子专家/C0-使用总览.md) | 5.23 KB | 使用总览 |
| [C1-能力契约.md](空间与自定义上报专家/sub-experts/自定义上报子专家/C1-能力契约.md) | 11.86 KB | 能力契约 |
| [implementation/01-架构.md](空间与自定义上报专家/sub-experts/自定义上报子专家/implementation/01-架构.md) | 8.58 KB | 架构 |
| [implementation/02-实现.md](空间与自定义上报专家/sub-experts/自定义上报子专家/implementation/02-实现.md) | 10.07 KB | 核心实现 |
| [implementation/03-数据流转.md](空间与自定义上报专家/sub-experts/自定义上报子专家/implementation/03-数据流转.md) | 8.26 KB | 数据流转 |
| [implementation/04-模型.md](空间与自定义上报专家/sub-experts/自定义上报子专家/implementation/04-模型.md) | 8.81 KB | 数据模型 |
| [implementation/05-接口.md](空间与自定义上报专家/sub-experts/自定义上报子专家/implementation/05-接口.md) | 9.02 KB | 接口说明 |

---

## 五、专家 4：任务调度与运维（8 份）

**路径**: `任务调度与运维专家/`
**覆盖**: `task/`(17文件), `management/commands/`(60+), `tools/`, `data/`, `migrations/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](任务调度与运维专家/agent.md) | 7.08 KB | 专家名片 |
| [C0-使用总览.md](任务调度与运维专家/C0-使用总览.md) | 11.78 KB | 黑盒使用文档 |
| [C1-能力契约.md](任务调度与运维专家/C1-能力契约.md) | 10.64 KB | 能力契约 |
| [implementation/01-架构.md](任务调度与运维专家/implementation/01-架构.md) | 8.74 KB | 任务调度架构 |
| [implementation/02-实现.md](任务调度与运维专家/implementation/02-实现.md) | 12.00 KB | 核心实现 |
| [implementation/03-数据流转.md](任务调度与运维专家/implementation/03-数据流转.md) | 7.04 KB | 数据流转 |
| [implementation/04-模型.md](任务调度与运维专家/implementation/04-模型.md) | 7.13 KB | 数据模型 |
| [implementation/05-接口.md](任务调度与运维专家/implementation/05-接口.md) | 14.86 KB | 接口说明 |

---

## 六、专家 5：API与工具库（24 份）

**路径**: `API与工具库专家/`
**覆盖**: `resources/`(8文件), `service/`, `utils/`(30+), `models/bcs/`

### 6.1 专家层（8 份）

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](API与工具库专家/agent.md) | 5.76 KB | 专家名片 |
| [C0-使用总览.md](API与工具库专家/C0-使用总览.md) | 8.46 KB | 黑盒使用文档 |
| [C1-能力契约.md](API与工具库专家/C1-能力契约.md) | 13.29 KB | API 契约 |
| [implementation/01-架构.md](API与工具库专家/implementation/01-架构.md) | 10.41 KB | API与工具架构 |
| [implementation/02-实现.md](API与工具库专家/implementation/02-实现.md) | 8.78 KB | 核心实现 |
| [implementation/03-数据流转.md](API与工具库专家/implementation/03-数据流转.md) | 7.43 KB | 数据流转 |
| [implementation/04-模型.md](API与工具库专家/implementation/04-模型.md) | 8.88 KB | 数据模型 |
| [implementation/05-接口.md](API与工具库专家/implementation/05-接口.md) | 14.23 KB | 接口说明 |

### 6.2 API资源子专家（8 份）

**路径**: `API与工具库专家/sub-experts/API资源子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](API与工具库专家/sub-experts/API资源子专家/agent.md) | 2.66 KB | 子专家名片 |
| [C0-使用总览.md](API与工具库专家/sub-experts/API资源子专家/C0-使用总览.md) | 3.05 KB | 使用总览 |
| [C1-能力契约.md](API与工具库专家/sub-experts/API资源子专家/C1-能力契约.md) | 6.12 KB | 能力契约 |
| [implementation/01-架构.md](API与工具库专家/sub-experts/API资源子专家/implementation/01-架构.md) | 8.18 KB | 架构 |
| [implementation/02-实现.md](API与工具库专家/sub-experts/API资源子专家/implementation/02-实现.md) | 8.29 KB | 核心实现 |
| [implementation/03-数据流转.md](API与工具库专家/sub-experts/API资源子专家/implementation/03-数据流转.md) | 6.80 KB | 数据流转 |
| [implementation/04-模型.md](API与工具库专家/sub-experts/API资源子专家/implementation/04-模型.md) | 6.81 KB | 数据模型 |
| [implementation/05-接口.md](API与工具库专家/sub-experts/API资源子专家/implementation/05-接口.md) | 7.97 KB | 接口说明 |

### 6.3 BCS与工具库子专家（8 份）

**路径**: `API与工具库专家/sub-experts/BCS与工具库子专家/`

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](API与工具库专家/sub-experts/BCS与工具库子专家/agent.md) | 3.84 KB | 子专家名片 |
| [C0-使用总览.md](API与工具库专家/sub-experts/BCS与工具库子专家/C0-使用总览.md) | 5.74 KB | 使用总览 |
| [C1-能力契约.md](API与工具库专家/sub-experts/BCS与工具库子专家/C1-能力契约.md) | 9.91 KB | 能力契约 |
| [implementation/01-架构.md](API与工具库专家/sub-experts/BCS与工具库子专家/implementation/01-架构.md) | 7.30 KB | 架构 |
| [implementation/02-实现.md](API与工具库专家/sub-experts/BCS与工具库子专家/implementation/02-实现.md) | 8.34 KB | 核心实现 |
| [implementation/03-数据流转.md](API与工具库专家/sub-experts/BCS与工具库子专家/implementation/03-数据流转.md) | 6.80 KB | 数据流转 |
| [implementation/04-模型.md](API与工具库专家/sub-experts/BCS与工具库子专家/implementation/04-模型.md) | 5.16 KB | 数据模型 |
| [implementation/05-接口.md](API与工具库专家/sub-experts/BCS与工具库子专家/implementation/05-接口.md) | 8.82 KB | 接口说明 |

---

## 七、专家 6：元数据种子数据与数据字典（9 份）

**路径**: `元数据种子数据与数据字典专家/`
**覆盖**: `data/` 下 12 个种子数据文件 + 加载机制（Migration + 运行时）

| 文件 | 大小 | 说明 |
|------|------|------|
| [agent.md](元数据种子数据与数据字典专家/agent.md) | 5.77 KB | 专家名片 |
| [C0-使用总览.md](元数据种子数据与数据字典专家/C0-使用总览.md) | 6.05 KB | 黑盒使用文档 |
| [C1-能力契约.md](元数据种子数据与数据字典专家/C1-能力契约.md) | 17.32 KB | 种子数据文件结构契约 + 加载函数契约 + UnifyQuery 对接契约 |
| [implementation/01-架构.md](元数据种子数据与数据字典专家/implementation/01-架构.md) | 12.18 KB | 种子数据架构：三层映射、加载机制 |
| [implementation/02-实现.md](元数据种子数据与数据字典专家/implementation/02-实现.md) | 16.17 KB | 加载函数实现、格式转换、缓存机制 |
| [implementation/03-数据流转.md](元数据种子数据与数据字典专家/implementation/03-数据流转.md) | 12.96 KB | JSON→Model→DB→UnifyQuery 全链路 |
| [implementation/04-模型.md](元数据种子数据与数据字典专家/implementation/04-模型.md) | 19.79 KB | 12 种文件结构详解、tag 角色、label 体系 |
| [implementation/05-接口.md](元数据种子数据与数据字典专家/implementation/05-接口.md) | 11.59 KB | 加载函数接口签名、K8s 接口、调用关系 |
| [CHANGELOG.md](元数据种子数据与数据字典专家/CHANGELOG.md) | 2.23 KB | 变更日志 |

---

## 八、按文档类型分类

| 类型 | 数量 | 说明 |
|------|------|------|
| 专题层 | 3 | topic.md + T0-专题总览 + PLAN.md |
| 索引 | 1 | INDEX.md（本文件） |
| agent.md | 14 | 6 专家 + 8 子专家 |
| C0-使用总览 | 14 | 6 专家 + 8 子专家 |
| C1-能力契约 | 14 | 6 专家 + 8 子专家 |
| implementation/01-架构 | 14 | 6 专家 + 8 子专家 |
| implementation/02-实现 | 14 | 6 专家 + 8 子专家 |
| implementation/03-数据流转 | 14 | 6 专家 + 8 子专家 |
| implementation/04-模型 | 14 | 6 专家 + 8 子专家 |
| implementation/05-接口 | 14 | 6 专家 + 8 子专家 |
| CHANGELOG | 2 | 空间与自定义上报专家 + 种子数据专家 |

---

## 八、快速查询指南

### 按源码文件查文档

| 源码文件 | 对应专家/子专家 |
|---------|---------------|
| `models/data_source.py` | 元数据核心模型 → 数据源管理子专家 |
| `models/result_table.py` | 元数据核心模型 → 结果表管理子专家 |
| `models/entity_relation.py` | 元数据核心模型（专家层，跨模块标注） |
| `models/constants.py` | T0-专题总览（结构化索引，不归属单一专家） |
| `models/storage.py` | 存储与数据链路 → 存储引擎子专家 |
| `models/data_link/` | 存储与数据链路 → 数据链路子专家 |
| `models/es_snapshot.py` | 存储与数据链路 → 存储引擎子专家 |
| `models/influxdb_cluster.py` | 存储与数据链路 → 存储引擎子专家 |
| `models/vm/` | 存储与数据链路 → 存储引擎子专家 |
| `models/space/` | 空间与自定义上报 → 空间管理子专家 |
| `models/custom_report/` | 空间与自定义上报 → 自定义上报子专家 |
| `models/record_rule/` | 空间与自定义上报 → 自定义上报子专家 |
| `task/` | 任务调度与运维 |
| `management/commands/` | 任务调度与运维 |
| `resources/` | API与工具库 → API资源子专家 |
| `service/` | API与工具库（契约层）+ 各功能域子专家（实现层） |
| `utils/` | API与工具库 → BCS与工具库子专家 |
| `models/bcs/` | API与工具库 → BCS与工具库子专家 |
| `data/` 种子数据文件 | 元数据种子数据与数据字典专家 |
| `migrations/0002_initial_data.py` | 元数据种子数据与数据字典专家 |
| `utils/k8s_metric.py` | 元数据种子数据与数据字典专家 |

### 按问题域查文档

| 问题域 | 入口文档 |
|--------|---------|
| 整体架构 | [T0-专题总览.md](T0-专题总览.md) |
| 数据源怎么创建/管理 | [数据源管理子专家/C0-使用总览.md](元数据核心模型专家/sub-experts/数据源管理子专家/C0-使用总览.md) |
| 结果表怎么配置 | [结果表管理子专家/C0-使用总览.md](元数据核心模型专家/sub-experts/结果表管理子专家/C0-使用总览.md) |
| 存储引擎怎么选型 | [存储引擎子专家/C0-使用总览.md](存储与数据链路专家/sub-experts/存储引擎子专家/C0-使用总览.md) |
| 数据链路怎么编排 | [数据链路子专家/C0-使用总览.md](存储与数据链路专家/sub-experts/数据链路子专家/C0-使用总览.md) |
| 空间隔离怎么实现 | [空间管理子专家/C0-使用总览.md](空间与自定义上报专家/sub-experts/空间管理子专家/C0-使用总览.md) |
| 自定义上报怎么接入 | [自定义上报子专家/C0-使用总览.md](空间与自定义上报专家/sub-experts/自定义上报子专家/C0-使用总览.md) |
| 后台任务怎么调度 | [任务调度与运维专家/C0-使用总览.md](任务调度与运维专家/C0-使用总览.md) |
| API 接口怎么调用 | [API资源子专家/C0-使用总览.md](API与工具库专家/sub-experts/API资源子专家/C0-使用总览.md) |
| 工具函数有哪些 | [BCS与工具库子专家/C0-使用总览.md](API与工具库专家/sub-experts/BCS与工具库子专家/C0-使用总览.md) |
| 内置指标/数据源从哪来 | [元数据种子数据与数据字典专家/C0-使用总览.md](元数据种子数据与数据字典专家/C0-使用总览.md) |
| table/field/unit 映射关系 | [元数据种子数据与数据字典专家/C0-使用总览.md](元数据种子数据与数据字典专家/C0-使用总览.md) |

---

## 九、批次完成状态

| 批次 | 内容 | 文档数 | 状态 |
|------|------|--------|------|
| Batch 0 | 专题架构（topic + T0 + PLAN） | 3 | ✅ 已完成 |
| Batch 1 | 专家 1+2+3（含子专家） | 73 | ✅ 已完成 |
| Batch 2 | 专家 4+5（含子专家） | 32 | ✅ 已完成 |
| Batch 3 | INDEX.md 汇总 | 1 | ✅ 已完成 |
| Batch 4 | 专家 6：种子数据与数据字典 | 9 | ✅ 已完成 |

**总计**: 118 份文档，6 个专家 + 8 个子专家，覆盖率 100%。

---

> **维护说明**: 新增/修改/删除专家或子专家文档后，需同步更新本 INDEX.md 及 [T0-专题总览.md](T0-专题总览.md)。
