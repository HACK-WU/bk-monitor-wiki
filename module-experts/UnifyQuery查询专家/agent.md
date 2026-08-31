# UnifyQuery 查询专家

## 一句话职责
负责 BK-Monitor **统一查询门面（UnifyQuery）**——Python 侧 `load_data_source` → 查询描述对象 → `UnifyQuery` 门面的全链路知识：入参如何拼装成统一查询后端 HTTP 参数、何时下推到各数据源原生查询、以及 `query_data` / `query_data_with_stat` / `query_reference` / `query_log` / `query_dimensions` 各公开入口的差异。

## 负责的功能域
- 统一查询门面：`UnifyQuery` 类，`query_data` 等公开入口 + 参数拼装 + 分流决策
- 数据源描述对象：`load_data_source` 工厂、`TimeSeriesDataSource.to_unify_query_config`、`DataQueryHandler`
- 两条总分支：统一查询后端 HTTP（`use_unify_query()==True`）vs 数据源原生查询（`_query_data_using_datasource`）

## 何时找这个专家
- 构造一个时序/日志/维度查询（不确定 `data_source_class`、`metrics`、`group_by`、`interval` 怎么填）
- 排查查询参数不对、返回为空、聚合函数不对（如 `AVG` 变成 `avg_over_time`）
- 理解 `query_data` 与 `query_log` / `query_dimensions` / `query_reference` 的差异与选型
- 诊断一条查询到底走了「统一查询后端」还是「数据源原生查询」
- 排查 instant 查询 `step` 被强制成 `1m`、时间对齐、租户/空间解析问题

## 契约层就绪
`C0 + C1 + C2 + C5` 就绪（C5 于 2026-08-31 补建，含 12 条有证据决策 + 1 条 `[推测]`）

## 包含的资产
### 契约层（使用文档）
- `C0-使用总览.md` — 能力清单、边界、已知问题
- `C1-能力契约.md` — `UnifyQuery` 公开方法契约、使用示例
- `C2-使用流程.md` — 四条常见使用流程 + 调用示例
- `C5-关键决策.md` — 13 条关键决策（数据源三级接入与灰度切换 / 黑名单豁免 / `_time` 虚拟排序字段 / instant 语义 / 时间对齐开关 / 两层聚合 / 失败不回退 / query_log 剥离聚合 / 多源维度退化兜底 / 返回结构三重兜底 / 租户注入 / 类 ORM Builder / is_es_batch opt-in）

### 实现层（代码导航）
- `implementation/01-架构.md` — 三层架构、表名字段来源、全查询链路索引
- `implementation/02-实现.md` — 参数拼接链路（`to_unify_query_config` → `_query_unify_query`）
- `implementation/03-数据流转.md` — 六个公开入口链路 + 两条总分支对照
- `implementation/05-接口.md` — 统一查询后端四个 API 资源契约

## 出处
- 生成日期：2026-07-27
- 知识来源：项目记忆 `专题记忆/数据源查询机制`
