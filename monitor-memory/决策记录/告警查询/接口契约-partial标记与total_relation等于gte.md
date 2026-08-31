---
groupPath: 决策记录/告警查询
relation: 接口契约-partial标记与total_relation等于gte
exportedAt: "2026-08-31T03:17:23.270Z"
---
【决策记录｜告警查询 结果不完整时用 partial 标记加 total_relation=gte 显式告知调用方】
- 分类：接口契约
- 动机：避坑（部分聚合失败时结果静默不完整，用户以为查全了）
- 决策：聚合或子流程失败时调用 _mark_partial(code=..., scopes=[...]) 记录不完整范围（如 aggs.notice_way）；响应中通过 get_partial_metadata 返回 partial_reasons；当 partial_reasons 中包含 total 时把 total_relation 从默认 eq 改为 gte（与 ES 的 track_total_hits 语义一致）
- 背景约束：告警查询由多个子流程拼装（主查询加 overview 加 aggs 加通知方式聚合），任一子流程失败都不应让整个查询失败，但必须让调用方知道结果不完整
- 被否决方案：子流程失败即整块失败或静默返回不完整结果，否决理由为前者可用性差、后者会静默误导；现状是继续返回加显式标记
- 已知代价：调用方必须检查 partial_reasons 才能知道数据是否可信；新增聚合路径时容易漏加 _mark_partial
- 重新评估触发条件：出现调用方未感知 partial 导致误判的反馈；或需要把不完整范围细化到字段级
- 关联代码：_mark_partial、get_partial_metadata、partial_reasons、_check_search_response_completeness @ packages/fta_web/alert/handlers/alert.py
- 证据来源：代码实现（total_relation = gte 分支、_mark_partial(code="notice_way_aggregation_failed", scopes=["aggs.notice_way"])）；commit 9ec2fc4119（告警通知方式查询部分结果缺少完整性标识）、a564b3f73c（命中 10000 上限时打 warning 日志便于排查 notice_way 过滤不完整问题）
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 5