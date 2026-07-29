# 数据源查询构造专家

## 一句话职责
负责 BK-Monitor **数据源系统的查询构造层**——`load_data_source` 工厂注册的所有 `(DataSourceLabel, DataTypeLabel)` 组合、每个组合对应的数据源类及其路径决策（统一查询后端 vs 原生查询）、查询描述对象的构造规范（`data_source_class(bk_biz_id, interval, metrics, table, group_by)`）、以及表名/字段的真实来源。

## 负责的功能域
- 数据源工厂：`load_data_source` 的 14 个注册组合、`DataSourceLabel` / `DataTypeLabel` 取值
- 路径决策：`UnifyQueryDataSources`（硬编码走 unify-query）vs `GrayUnifyQueryDataSources`（灰度）vs 原生路径
- 查询描述对象：`data_source_class(...)` 的参数规范、metrics 结构、方法映射
- 表名/字段来源：`ResultTable` / `ResultTableField` 模型、`init_resulttable.json` 初始化数据

## 何时找这个专家
- 不确定某个数据源该用什么 `(data_source_label, data_type_label)` 组合
- 想知道一条查询会走 unify-query 还是原生路径
- 构造查询时不清楚 `metrics` / `group_by` / `table` 等参数如何填写
- 需要了解有哪些可用的数据源类型（除了 BK_MONITOR_COLLECTOR 之外）
- 排查表名或字段名找不到对应的数据源

## 契约层就绪
`C0 + C1` 就绪

## 包含的资产
### 契约层（使用文档）
- `C0-使用总览.md` — 能力清单、边界、已知问题
- `C1-能力契约.md` — `load_data_source` 完整映射表、构造规范、路径决策矩阵

### 实现层（代码导航）
- `implementation/01-架构.md` — 数据源系统架构、14 个注册类、表名字段来源
- `implementation/02-实现.md` — `load_data_source` 注册机制、路径决策逻辑、metrics 拼装

## 出处
- 生成日期：2026-07-27
- 知识来源：项目记忆 `专题记忆/数据源查询机制` + 源码 `data_source/__init__.py` + `constants/data_source.py`
