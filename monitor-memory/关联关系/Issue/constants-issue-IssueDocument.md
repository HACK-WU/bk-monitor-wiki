---
groupPath: 关联关系/Issue
relation: constants-issue-IssueDocument
exportedAt: "2026-08-13T08:55:37.817Z"
---
[强关联] constants/issue.py 枚举常量 与 IssueDocument / Resource / Handler
强度：必改——改枚举值（状态/优先级/活动类型）时，所有引用方必须跟着改
原因：状态、优先级、活动类型枚举被 IssueDocument 状态机、Resource 层、查询处理器、活动日志等多处引用，枚举值变更级联影响全链路

源端（枚举定义）：
- 状态枚举: pending_review / unresolved / resolved / archived @ `constants/issue.py`
- 优先级枚举: P0 / P1 / P2 @ `constants/issue.py`
- 活动类型枚举: create / status_change / assignee_change / priority_change / name_change / comment / comment_edit / create_tapd / tapd_link @ `constants/issue.py`
- 活跃状态集合: ACTIVE_STATUSES @ `constants/issue.py`

目标端（引用方）：
- `IssueDocument` 状态机方法 @ `bkmonitor/documents/issue.py`
- `IssueAggregationProcessor` @ `alarm_backends/service/fta_action/issue_processor.py`（ACTIVE_STATUSES 查找活跃 Issue）
- `IssueQueryHandler` @ `bkmonitor/packages/fta_web/issue/handlers/issue.py`（虚拟状态转换）
- `IssueActivityDocument` @ `bkmonitor/documents/issue.py`（activity_type 字段）
- `sync_issue_alert_stats` @ `alarm_backends/service/fta_action/tasks/issue_tasks.py`（扫描活跃 Issue）