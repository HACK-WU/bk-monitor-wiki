---
groupPath: 关联关系/Issue
relation: TAPD-MySQLModels
exportedAt: "2026-08-13T08:55:38.125Z"
---
[强关联] TAPD Resource 层 与 MySQL 模型（TapdWorkspaceBinding / IssueTapdRelation / TapdWorkspaceManualUnbind）
强度：必改——改 MySQL 模型字段定义/唯一键/表结构时，所有 TAPD Resource 必须跟着改；改 Resource 逻辑，模型结构不用管
原因：TAPD 操作直接读写三个 MySQL 关系表，模型结构变更级联影响绑定/解绑/重绑/创建/关联全链路

源端（TAPD Resource）：
- `CreateTapdResource` / `LinkIssueToTapdResource` / `ListIssueTapdRelationsResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- `UnbindTapdWorkspaceResource` / `RebindTapdWorkspaceResource` / `RevokeTapdUserAuthResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- `ListTapdWorkspaceResource` / `ListUserTapdWorkspaceResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- `_mark_bind_status` 五态查询逻辑（含 try_bind_importable）

目标端（MySQL 模型）：
- `TapdWorkspaceBinding` @ `bkmonitor_issue_tapd_workspace_binding` 表（工作区绑定）
- `IssueTapdRelation` @ `bkmonitor_issue_tapd_relation` 表（Issue ↔ TAPD 单据关联，含 link_mode/sync_status）
- `TapdWorkspaceManualUnbind` @ `bkmonitor_tapd_workspace_manual_unbind` 表（解绑 tombstone，唯一键 (bk_tenant_id, space_uid, tapd_workspace_id)）
- 解绑/重绑事务操作跨 TapdWorkspaceBinding + TapdWorkspaceManualUnbind 两表