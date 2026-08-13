---
groupPath: 关联关系/Issue
relation: IssueDocument-WebAPI
exportedAt: "2026-08-13T08:55:30.413Z"
---
[强关联] IssueDocument 状态机 与 Web API Resource 层
强度：必改——改 IssueDocument 状态机方法签名/返回语义/前置条件时，所有 Resource 必须跟着改；改 Resource 的调用方式，IssueDocument 不用管
原因：状态机方法（assign/resolve/archive/reopen/restore/rename/add_comment/update_priority）被 Resource 层直接调用，签名或行为变更会级联影响所有写操作端点

源端（IssueDocument 状态机）：
- `IssueDocument` @ `bkmonitor/documents/issue.py`
  - assign / reassign / resolve / archive / reopen / restore / rename / add_comment / update_priority
  - get_issue_or_raise / to_cache_dict
- 异常类: IssueNotFoundError / IssueFrozenError / IssueNameDuplicatedError

目标端（Web API Resource）：
- `AssignIssueResource` / `ResolveIssueResource` / `ArchiveIssueResource` / `ReopenIssueResource` / `RestoreIssueResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- `RenameIssueResource` / `AddIssueFollowUpResource` / `EditIssueFollowUpResource` / `UpdateIssuePriorityResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- `MergeIssueResource` / `SplitIssueResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- `_run_batch` 批量框架直接调用状态机方法