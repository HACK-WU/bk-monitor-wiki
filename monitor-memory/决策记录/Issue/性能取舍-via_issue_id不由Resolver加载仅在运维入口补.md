---
groupPath: 决策记录/Issue
relation: 性能取舍-via_issue_id不由Resolver加载仅在运维入口补
exportedAt: "2026-09-01T07:21:15.265Z"
---
【决策记录｜via_issue_id 刻意不进入 IssueMergeResolver 的 hydrate 路径，只在运维取证入口按需补一次 SQL】
- 分类：性能取舍
- 动机：优化（该字段只服务运维溯源，进主链路会无谓扩大 per-request 合并上下文载荷）
- 决策：IssueMergeResolver 的 hydrate 刻意不加载 via_issue_id；仅 bkm_cli inspect-issue detail 这一运维取证入口通过 _inject_member_via_issue_ids 补一次 SQL，注入到 merge_status.active_members 每一项
- 背景约束：hydrate_aggregations 的结果会进入每个请求的合并上下文，字段「只增不用」会持续放大载荷；而运维取证是低频人工操作，多一次 SQL 可接受
- 被否决方案：无
- 已知代价与边界：除 bkm_cli detail 外的所有路径拿不到该字段（fta_web 的 ListMergeSourcesResource 是直查模型，属例外）；补注入失败时**fail-open**——保持原样缺该字段，仅记 warning 日志，不阻塞 detail 主路径
- 重新评估触发条件：产品侧要求在 Issue 详情/列表展示上一跳主（届时须把字段并入 Resolver 并评估载荷增量）
- 关联代码：_inject_member_via_issue_ids @ bkmonitor/kernel_api/rpc/functions/bkm_cli/issue.py；IssueMergeResolver @ bkmonitor/bkmonitor/issue_merge/
- 证据来源：函数 docstring（bkm_cli/issue.py 明写「IssueMergeResolver 刻意不加载该字段（hydrate 不消费它，避免扩大 per-request context 载荷），故只在本运维取证入口按需补一次 SQL」「fail-open：查询失败保持原样（缺该字段），不阻塞 detail 主路径」）；commit 438a146（PR#12234）