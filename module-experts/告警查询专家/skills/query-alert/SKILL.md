---
name: query-alert
description: 告警查询标准操作与排查技能。覆盖通过 alert/search、alert/date_histogram、alert/top_n 等接口查询告警列表/趋势/TopN 的标准步骤，以及"查不到数据/数量对不上/超时"的系统性排查路径。触发短语："查询告警"、"告警列表查不到"、"告警数量对不上"、"排查告警查询"、"alert/search 返回空"。
---

# 查询告警（query-alert）

## 适用场景
- 需要新增 / 修改告警查询条件、排序、聚合维度
- 排查告警列表 / 趋势 / TopN 查不出数据、数量不符、查询超时
- 理解 `query_string` / `conditions` 解析与 ES DSL 生成

## 核心入口
| 接口 | Resource | Handler |
|------|----------|---------|
| `POST alert/search` | `SearchAlertResource` | `AlertQueryHandler.search` |
| `POST alert/date_histogram` | `AlertDateHistogramResource` | `AlertQueryHandler.date_histogram` |
| `POST alert/top_n` | `AlertTopNResource` | `AlertQueryHandler.top_n` |
| `POST alert/export` | `ExportAlertResource` | `AlertQueryHandler.export_with_docs` |

所有查询经统一管线：`get_search_object → add_conditions → add_query_string → add_ordering → add_pagination →（add_overview/add_aggs）→ execute`。

## 标准查询步骤
1. 明确业务范围：`bk_biz_ids`（可含 `-1` 全业务）或 `space_uids`（自动转 `bk_biz_ids`）。
2. 设置时间窗：`start_time` / `end_time`（必填，单位秒）。
3. 组装过滤：`status`（含 `MINE`/`MY_ASSIGNEE`/`SHIELDED_ABNORMAL` 等语义）、`conditions`、`query_string`。
4. 分页与统计：`page` / `page_size`（≤5000）、`show_overview` / `show_aggs` / `show_dsl`（调试开 `show_dsl` 看生成 DSL）。
5. 调用 `resource.alert.search_alert(...)`，取 `alerts` / `total` / `overview` / `aggs`。

## 排查"查不到 / 数量对不上"的优先检查项
1. **`bk_biz_ids=-1` 是否展开**：未展开会直接查空（不存在 `bk_biz_id=-1` 的数据）。确认走 `authorized_bizs`。
2. **`issue_id` 合并展开**：按 Issue 过滤时需展开为「主 + active members」，否则漏掉被并入的告警。
3. **时间切片交叠**：`get_search_object` 用 `begin_time/end_time/create_time` 与查询窗交叠过滤，时间窗设错会漏数据。
4. **`query_string` 空串 / 裸词**：空串不加过滤；裸词走全字段模糊，词过短/过长且非枚举显示名会返回 `match_none`（查空）。
5. **状态语义**：`MINE` 等是组合语义，误用会导致过滤不符预期。
6. **`track_total_hits=10000`**：超 1 万的 `total` 不精确。

## 关键文件
- `bkmonitor/packages/fta_web/alert/resources.py` — Resource 入口
- `bkmonitor/packages/fta_web/alert/handlers/alert.py` — `AlertQueryHandler`
- `bkmonitor/packages/fta_web/alert/handlers/base.py` — `BaseQueryHandler` / `BaseBizQueryHandler`（查询构建、业务鉴权）
- `bkmonitor/packages/fta_web/alert/serializers.py` — `AlertSearchSerializer`

## 边界
- 本技能仅覆盖**查询（读）**路径；写操作（ack / 反馈 / 经验）不在范围。
- 修改查询管线前先确认 `06-测试.md` 中的 P0 单测缺口，建议补测后再改。
