---
groupPath: 关联关系/Issue
relation: sync_issue_alert_stats-IssueDocument-AlertDocument
exportedAt: "2026-08-13T08:55:55.573Z"
---
[强关联] sync_issue_alert_stats 周期任务 与 IssueDocument / AlertDocument
强度：必改——改 IssueDocument/AlertDocument 的 ES 索引结构或 issue_id 字段时，周期任务必须跟着改；改周期任务逻辑，Document 不用管
原因：周期任务直接读写两个 ES 文档——扫描活跃 IssueDocument 更新统计、回填 AlertDocument.issue_id、重算 impact_scope

源端（周期任务）：
- `sync_issue_alert_stats` @ `alarm_backends/service/fta_action/tasks/issue_tasks.py`
- 队列: celery_action_cron
- backfill 优化: O(N+M) 一次 scan Issue + 一次 scan alerts + 内存分组匹配

目标端（ES 文档）：
- `IssueDocument` @ `bkmonitor/documents/issue.py`（扫描活跃 Issue，更新 alert_count/last_alert_time/impact_scope）
- `AlertDocument` @ `bkmonitor/documents/alert.py`（回填 issue_id 未写入的告警）
- ES 索引 `bkfta_issue` + AlertDocument 索引