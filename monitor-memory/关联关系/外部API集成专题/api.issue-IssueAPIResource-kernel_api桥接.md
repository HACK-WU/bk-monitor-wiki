---
groupPath: 关联关系/外部API集成专题
relation: api.issue-IssueAPIResource-kernel_api桥接
exportedAt: "2026-08-14T07:53:01.837Z"
---
[强关联] api.issue IssueAPIResource 与 kernel_api Issue 专家外部桥
强度：必改——改 api.issue 的 IssueAPIResource 基类或 action 路径时，web 端 Issue 状态流转接口全变
原因：api.issue 是 Issue 专家（fta_web/issue）的外部桥，web 端 RenameIssueResource 等经 api.issue.rename 转发到 kernel_api

源端（外部桥）:
- `IssueAPIResource(KernelAPIResource)` @ `bkmonitor/api/issue/default.py`
- `base_url` 为 bk-monitor 自身网关
- `TIMEOUT = 300`
- 全量 12 类: Assign/Resolve/Reopen/Archive/Restore/UpdatePriority/Rename/AddFollowUp/EditFollowUp/Merge/Split/RegenerateTitle

目标端（web 端桥接与 kernel_api 执行）:
- `RenameIssueResource` @ `bkmonitor/packages/fta_web/issue/resources.py` — web 端转发到 `api.issue.rename`
- kernel_api 端执行实际逻辑（IssueDocument 状态流转）
- 参见 Issue 专家「API」子专家与「状态聚合」子专家
- 重名异常返回专有状态码 HTTP 409 + code=3327001（REQ-20260803-001）