---
groupPath: 关联关系/Issue
relation: IssueAggregationProcessor-AlertDocument-IssueDocument
exportedAt: "2026-09-01T08:35:17.234Z"
---
[强关联] IssueAggregationProcessor 与 AlertDocument / IssueDocument
强度：必改——改 AlertDocument.issue_id 字段定义或 IssueDocument 索引结构/缓存 key 时，聚合引擎必须跟着改；改聚合引擎的查找/创建逻辑，两个 Document 不用管
原因：聚合引擎直接读写两个 ES 文档模型——查/建 IssueDocument、UPSERT AlertDocument.issue_id、读写 Redis 缓存

源端（聚合引擎）：
- `IssueAggregationProcessor` @ `alarm_backends/service/fta_action/issue_processor.py`
- `gen_issue_fingerprint` @ `alarm_backends/service/fta_action/issue_processor.py`

目标端（ES 文档模型）：
- `IssueDocument` @ `bkmonitor/documents/issue.py`（查/建/缓存）
- `AlertDocument` @ `bkmonitor/documents/alert.py`（issue_id 字段 UPSERT）
- Redis 缓存 key: `issue_active_content:{fingerprint}`
- Redis 分布式锁: 按 fingerprint 粒度