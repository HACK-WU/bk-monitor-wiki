---
groupPath: 专题记忆/数据源查询机制
relation: UnifyQuery全查询链路调研索引
keywords: [统一查询参数拼接, query_data, 数据源查询机制, with_series_stat]
exportedAt: "2026-07-14T03:30:55.129Z"
---
# UnifyQuery 全查询链路调研 · 索引

> 背景：原 wiki「统一查询参数拼接链路」只覆盖 `query_data` 单链路 + `BK_MONITOR_COLLECTOR/TIME_SERIES` 单数据源。
> 本目录补齐 `UnifyQuery` 全部公开查询入口的参数拼装链路，每链路独立成文，供审核。
> 数据源聚焦：`BK_MONITOR_COLLECTOR / TIME_SERIES`（LOG 类差异在 `query_log.md` 中另作说明）。

## 文档清单

| 文件 | 链路 | HTTP 接口 | 与 query_data 的关系 |
|------|------|-----------|----------------------|
| unify_query_query_data.md | `query_data` | POST /query/ts | 基线篇（共享前置） |
| unify_query_query_data_with_stat.md | `query_data_with_stat` | POST /query/ts | **完全相同** params，仅 `with_series_stat=True` 开关 + 返回带 `series_stat` |
| unify_query_query_reference.md | `query_reference` | POST /query/ts/reference | 逐条 query 注入 `limit/from`，透传 `order_by`；无 `down_sample_range`（`not_time_align` 默认写入但 API 忽略）；不返回 `series_stat` |
| unify_query_query_log.md | `query_log` | POST /query/ts/raw | 逐条**剥离聚合**（function/field_name/time_aggregation 清空）；顶层 `limit/_from`；忽略 `instant`；返回 `(records, total)`（unify 路径 `total=0`） |
| unify_query_query_dimensions.md | `query_dimensions` | POST /query/ts/info/tag_values（单数据源，聚焦数据源） | **本质分叉**：单数据源不拼时序 params，改走 unify「维度值」接口（复用 `to_unify_query_config[0]`）；多数据源兜底复用 `query_data` |
| unify_query_query_data_using_datasource.md | `_query_data_using_datasource` | **无 HTTP**（走原生 `DataQueryHandler` → `api.metadata`/`api.bkdata`/`api.log_search` 或直连 ES） | **另一条总分支**：`use_unify_query()==False` 时，查询下推到各数据源 `query_data` → `DataQueryHandler`；最终落点多为外部 API（metadata/bkdata/log_search），FTA 事件/告警直连 ES，无直连数据库 |

## 关键差异速查

| 维度 | query_data | with_stat | reference | log | dimensions |
|------|-----------|-----------|-----------|-----|------------|
| 顶层 params 拼装 | ✅ | ✅ 同 | ✅（order_by 透传） | ✅（聚合剥离） | ⚠️（单数据源走 get_dimension_data，不拼时序 params） |
| 逐条 query 附加 | — | — | `limit`/`from` | `function=[]`等清空 | — |
| instant→step=1m | ✅ | ✅ | ✅ | ❌ | — |
| down_sample_range | ✅ | ✅ | ❌ | ❌ | — |
| series_stat | ❌ | ✅ | ❌ | ❌ | — |
| 返回 | list | {series,stat} | list | (list,total) | list |

## 审核要点建议

1. `query_data` 篇是否与现有 wiki 内容一致（本文为独立成篇的基线，细节以 wiki 原文为准）。
2. `query_log` 的"聚合剥离"是否覆盖你关心的 LOG 数据源类型。
3. `query_dimensions` 的"单数据源不走 unify params"是否符合你的预期（这是与 query_data 最大的结构性差异）。
4. 审核通过后，可将本目录内容沉淀进 wiki「数据源查询机制」Group（替换/补充原单链路文档）。