---
groupPath: 最近需求
relation: "[2026-06-30] TAPD手动解绑持久化与重新关联：新增 TapdWorkspaceManualUnbind tombstone 表+显式重新关联接口+撤销用户授权接口（REQ-20260630-001）"
keywords: [TAPD, tombstone, rebind]
exportedAt: "2026-06-30T06:49:05.859Z"
---
## [2026-06-30] TAPD 手动解绑持久化与重新关联

**需求 ID**: REQ-20260630-001
**关联文档**: `bk-monitor-wiki/requirements/integration/2026-06-30-TAPD手动解绑持久化与重新关联/requirement.md`

### 问题背景
当前 `UnbindTapdWorkspaceResource`（B-04）仅删除 `TapdWorkspaceBinding`，但 B-01 列表查询时 `_mark_bind_status` 在 `in_app && !in_local` 场景下会静默调用 `try_bind_importable()` 重新创建 binding，导致"取消关联"形同虚设。

### 核心方案
1. **新增 `TapdWorkspaceManualUnbind` 表**：轻量 tombstone，唯一键 `(bk_tenant_id, space_uid, tapd_workspace_id)`
   - 文件：`bkmonitor/bkmonitor/models/tapd.py`（新增模型）
2. **解绑时写 tombstone**：`UnbindTapdWorkspaceResource.perform_request` 中删除 binding + 创建 tombstone（事务内）
3. **五态查询逻辑**：`_mark_bind_status` 增加 `manual_unbound` 判断
   - `in_app && in_local` → BOUND
   - `in_app && !in_local && manual_unbound` → MANUALLY_UNBOUND（不自动绑定）
   - `in_app && !in_local && !manual_unbound` → IMPORTABLE
   - `!in_app && in_local` → STALE
   - `!in_app && !in_local` → UNBOUND
4. **新增 `RebindTapdWorkspaceResource`**：POST `/fta/issue/tapd/workspace/rebind/`，校验 tombstone 存在 + TAPD app 授权有效，删除 tombstone + 创建 binding
5. **新增 `RevokeTapdUserAuthResource`**：POST `/fta/issue/tapd/user_auth/revoke/`，调用 `delete_tapd_token()` 清除 access_token

### 关键文件
- `bkmonitor/bkmonitor/models/tapd.py` — 新增 `TapdWorkspaceManualUnbind` 模型
- `bkmonitor/packages/fta_web/issue/resources.py` — 修改 `_mark_bind_status`、`UnbindTapdWorkspaceResource`；新增 `RebindTapdWorkspaceResource`、`RevokeTapdUserAuthResource`
- `bkmonitor/packages/fta_web/issue/utils/tapd.py` — `delete_tapd_token()` 已存在

### 依赖
- 依赖 REQ-20260615-001（TAPD 授权与建单）中已实现的 B-01/B-03/B-04 基础能力
