---
groupPath: 关联关系/Issue
relation: IssueDocument-IssueActivityDocument
exportedAt: "2026-09-01T08:35:17.234Z"
---
[强关联] IssueDocument 状态机方法 与 IssueActivityDocument 活动日志
强度：必改——改 IssueActivityDocument 的字段定义/索引结构时，IssueDocument 状态机方法必须跟着改；改状态机方法的活动日志写入格式，ActivityDocument 不用管
原因：IssueDocument 所有状态机方法返回活动日志列表，活动日志写入 ES 索引 bkfta_fta_issue_act，字段结构变更级联影响所有状态流转

源端（状态机方法）：
- `IssueDocument.assign/reassign/resolve/archive/reopen/restore/rename/add_comment/update_priority` @ `bkmonitor/documents/issue.py`
- 每个方法返回 list[dict] 活动日志
- 活动类型: create/status_change/assignee_change/priority_change/name_change/comment/comment_edit/create_tapd/tapd_link

目标端（活动日志文档）：
- `IssueActivityDocument` @ `bkmonitor/documents/issue.py`
- ES 索引: `bkfta_fta_issue_act`
- 字段: issue_id / activity_type / operator / from_value / to_value / content
- 消费方: Issue 详情页活动流、审计查询、ListIssueActivitiesResource