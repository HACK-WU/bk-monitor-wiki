---
groupPath: 专题记忆/Issue
relation: IssueQueryHandler 查询处理器
exportedAt: "2026-08-13T08:53:25.497Z"
---
IssueQueryHandler 继承 BaseBizQueryHandler，提供 Issue 列表的高级查询能力（搜索/TopN/趋势）。IssueQueryTransformer 将前端查询参数转换为 ES DSL，负责字段映射和中文显示名翻译。查询支持虚拟状态、时间分片、结构化条件。

## 关键符号
- 符号: `IssueQueryHandler`
- 位置: `bkmonitor/packages/fta_web/issue/handlers/issue.py`
- 方法: `search(show_aggs, show_dsl, show_trend)` / `top_n(fields, size, translators)` / `get_alert_trend(issue_ids)`
- 符号: `IssueQueryTransformer`
- 位置: `bkmonitor/packages/fta_web/issue/handlers/issue.py`
- 方法: `transform_query_string` / `transform_condition_fields` / `transform_ordering_fields`（继承 BaseQueryTransformer）
- 符号: `SearchIssueResource` / `IssueTopNResource` / `IssueTrendResource`
- 位置: `bkmonitor/packages/fta_web/issue/resources.py`
- 注意: 源码实际类名为 SearchIssueResource（非 IssueSearchResource）

## 虚拟状态
- MY_ASSIGNEE: 当前用户负责 → assignee = request_username
- NO_ASSIGNEE: 未分派 → assignee 字段不存在
- 仅在 status 过滤参数中生效，不出现在真实值里

## 时间范围语义（与常规查询不同）
- end_time 约束 create_time（该时间前已创建）
- start_time 约束 resolved_time（在该时间之后才解决）
- 时间分片模式下按 resolved_time 唯一归属分片，避免重复计数
- end_time 超过当前时间会收敛到 now+60

## TopN 查询
- 时间跨度 > 7 天触发时间分片并行
- 入口统一去重 fields，防止分片合并时重复累加
- bk_biz_id 会补齐授权业务中 count 为 0 的桶
- size 最大 10000

## 趋势查询
- 按 status（active/resolved）与 priority 做基数/计数聚合
- 内置 _repair_missing_resolved_activity 修复逻辑
- 合并展开后 Issue 数量不能超过 1000
- member 趋势计入对应主 Issue

## 字段映射速查
- name → name.raw（terms/wildcard）
- strategy_name → strategy_name.raw
- fingerprint → fingerprint（term）
- impact_scope.{dim} → impact_scope.{dim}.instance_list.{id_field}（exists/terms）
- dimension_values.{key} → dimension_values.{key}（terms）
- impact_dimensions → 多维度 exists filters 聚合