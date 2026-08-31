---
groupPath: 决策记录/告警查询
relation: 接口契约-issue_id合并成员展开用authorized_bizs
exportedAt: "2026-08-31T03:18:06.719Z"
---
【决策记录｜告警查询 issue_id 过滤自动展开合并成员，且必须用 authorized_bizs 而非原始 -1】
- 分类：接口契约
- 动机：避坑（按合并后主 Issue ID 过滤时被并入的告警不出现；全业务场景下展开失效）
- 决策：AlertQueryHandler 初始化内调用 _expand_merged_issue_conditions 原地改写 self.conditions，一处覆盖所有经 AlertQueryHandler 的路径（search、date_histogram、TopN）；展开时用已解析的 self.authorized_bizs 作为 biz 维度；关系层异常或无合并关系时 fail-open（保持原条件，体感等同无合并）
- 背景约束：全业务查询传 bk_biz_ids=[-1] 时 BaseBizQueryHandler 已把它解析为授权业务集；直接用 [-1] 查 IssueMergeRelation 不会有结果，会让全业务列表、TopN、histogram 的 issue_id 过滤漏掉 active members（docstring 原文）
- 被否决方案：在各 Resource 层分别展开，否决理由为需要覆盖 search、histogram、TopN 三条路径，分散展开易漏（docstring：可一处覆盖所有经 AlertQueryHandler 的查询路径）
- 已知代价：合并关系查询失败时静默退化为不展开（只记 warning），表现为按主 Issue 查不到被并入告警
- 重新评估触发条件：IssueMergeRelation 查询方式变化；或需要把展开失败暴露给调用方
- 关联代码：AlertQueryHandler._expand_merged_issue_conditions @ packages/fta_web/alert/handlers/alert.py；IssueMergeResolver @ bkmonitor/issue_merge/
- 证据来源：_expand_merged_issue_conditions 方法 docstring（biz 维度用已解析的 authorized_bizs 而非原始 bk_biz_ids；直接用 [-1] 查 IssueMergeRelation 无结果会让全业务列表漏掉 active members；fail-open 关系层异常或无合并关系时保持原条件）；C0 已知坑 3；commit bd7c598464
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 8