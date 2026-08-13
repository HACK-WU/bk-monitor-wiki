---
groupPath: 关联关系/告警屏蔽
relation: AddShieldResource-AlertDocument-is_shielded
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] AddShieldResource 屏蔽创建 与 AlertDocument ES 状态同步
强度：必改——改 AlertDocument.is_shielded 字段语义或更新方式时，AddShieldResource.handle_alert / BulkAddAlertShieldResource.handle_alerts 必须跟着改；改 handle_alert 的维度提取逻辑，AlertDocument 不用管
原因：alert 类型屏蔽创建时立即更新 ES 中告警的 is_shielded=True，前端据此展示"已屏蔽"状态，ES 字段变更级联影响创建链路

源端（屏蔽创建）:
- `AddShieldResource.handle_alert` @ `bkmonitor/packages/monitor_web/shield/resources/backend_resources.py`（从 AlertDocument.get 提取维度 + 更新 is_shielded=True）
- `BulkAddAlertShieldResource.handle_alerts` @ `bkmonitor/packages/monitor_web/shield/resources/backend_resources.py`（AlertDocument.mget 批量 + bulk_create 更新 is_shielded）

目标端（ES 文档）:
- `AlertDocument` @ `bkmonitor/documents/alert.py`（is_shielded 字段，bool 类型）
- `AlertDocument.get` / `AlertDocument.mget` / `AlertDocument.bulk_create` @ `bkmonitor/documents/alert.py`
- 注意：quick_shield 走 handle 方法而非 handle_alert，不更新 ES is_shielded