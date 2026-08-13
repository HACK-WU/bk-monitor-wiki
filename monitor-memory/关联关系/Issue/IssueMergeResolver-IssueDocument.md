---
groupPath: 关联关系/Issue
relation: IssueMergeResolver-IssueDocument
exportedAt: "2026-08-13T08:55:36.466Z"
---
[强关联] IssueMergeResolver 与 IssueDocument 状态机
强度：必改——改 IssueDocument 状态机的级联逻辑或冻结守卫时，MergeResolver 必须跟着改；改 MergeResolver 的合并/拆分逻辑，状态机方法本身不用改（但级联效果依赖状态机）
原因：合并/拆分直接修改 IssueDocument 状态，主 Issue 状态变更会级联同步所有 active member 的 ES status，冻结守卫（IssueFrozenError）在状态机方法中检查

源端（合并/拆分）：
- `IssueMergeResolver.merge` / `IssueMergeResolver.split` @ `bkmonitor/issue_merge.py`
- MySQL 模型: `IssueMergeRelation` @ `bkmonitor_issue_merge_relation` 表
- Web 层: `MergeIssueResource` / `SplitIssueResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- API 层: `MergeResource` / `SplitResource` @ `kernel_api/views/v4/issue.py`

目标端（状态机）：
- `IssueDocument` 状态机方法（resolve/archive/reopen/restore 均含级联同步 active member 逻辑）@ `bkmonitor/documents/issue.py`
- `IssueFrozenError` 异常（合并 member 不可操作）@ `bkmonitor/documents/issue.py`
- 查询路径: display_id 折叠、member 排除、聚合数据 union