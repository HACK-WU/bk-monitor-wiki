---
groupPath: 专题记忆/Issue
relation: TAPD 集成核心
exportedAt: "2026-08-13T08:54:28.863Z"
---
TAPD 集成模块负责 Issue 与 TAPD 工作项的打通，包括用户态/应用态 OAuth 授权、工作区绑定/解绑/重绑、创建/关联 TAPD 单据。用户态 token 存 Redis（AES 加密），工作区绑定存 MySQL，解绑通过 tombstone 表阻断自动回绑。

## 关键文件
- 符号: TAPD Resource 类（CreateTapdResource / LinkIssueToTapdResource / UnbindTapdWorkspaceResource / RebindTapdWorkspaceResource / RevokeTapdUserAuthResource 等）
- 位置: `bkmonitor/packages/fta_web/issue/resources.py`（TAPD 部分）
- 符号: `TAPDAuthPermission` / `TAPD_ENDPOINTS`
- 位置: `bkmonitor/packages/fta_web/issue/views.py`（TAPD 端点注册+权限）
- 符号: `generate_auth_url` / `generate_install_url` / `save_tapd_token` / `get_tapd_token` / `delete_tapd_token`
- 位置: `bkmonitor/packages/fta_web/issue/utils/tapd.py`（12KB，TAPD 工具函数）
- OAuth 回调路由: `tapd/oauth_callback/`、`tapd/app_install_callback/`（csrf_exempt）

## 用户态授权
- token 存储: Redis `tapd_uat:{tenant}:{user}`，AES 加密（依赖 SECRET_KEY）
- generate_auth_url: 生成 OAuth 授权 URL，signed_state TTL 15 分钟
- scope 固定: story#read story#write bug#read bug#write
- TAPDAuthPermission: 所有 TAPD_ENDPOINTS 接口前置校验 token
- 未授权+携带 success_url（仅 tapd/user_workspace）: 返回 403 + auth_url
- 未授权+无 success_url: 返回 403 提示先授权
- token 失效(422): 自动清理并重新引导

## 应用态授权
- generate_install_url: 生成 open_app_install URL
- tapd_app_install_callback: 回调建立/更新 TapdWorkspaceBinding
- 以 workspace_id 为字符串写入模型

## 工作区五态
- bound: in_app && in_local
- importable: in_app && !in_local && !manual_unbound（会静默 try_bind_importable）
- manually_unbound: in_app && !in_local && manual_unbound（不自动绑定）
- stale: !in_app && in_local
- unbound: !in_app && !in_local

## 解绑/重绑（REQ-20260630-001）
- 解绑: 事务内删除 TapdWorkspaceBinding + 创建 TapdWorkspaceManualUnbind tombstone
- 重绑: 事务内删除 tombstone + 创建/复用 TapdWorkspaceBinding
- tombstone 阻断周期任务自动回绑
- 撤销授权: 仅清 Redis token，不删 binding 和 relation

## MySQL 模型
- `TapdWorkspaceBinding`: 工作区绑定
- `TapdWorkspaceManualUnbind`: 解绑 tombstone，唯一键 (bk_tenant_id, space_uid, tapd_workspace_id)
- `IssueTapdRelation`: Issue ↔ TAPD 单据关联（表 bkmonitor_issue_tapd_relation）

## 创建/关联 TAPD 单
- CreateTapdResource: 调 TAPD API 创建 → 写 IssueTapdRelation(link_mode=create) → 记 create_tapd 活动
- LinkIssueToTapdResource: 批量查重 → 写 IssueTapdRelation → 记 tapd_link 活动（仅新建的）
- bug 类型必填 te 字段
- Issue 合并冻结时拒绝创建（MERGE_FREEZE_VIOLATION）