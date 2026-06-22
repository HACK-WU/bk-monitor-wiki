---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 实施中
created: 2026-06-15
updated: 2026-06-22
version: 1
tags: [integration, design, api]
author: AI
document_type: existing-api-note
---

# B-07 查询 app 已授权 TAPD 项目列表

> **状态：已有/已实现。** 现网已存在 `ListTapdWorkspaceResource`（`POST /fta/issue/tapd/workspace/`），本次迭代**不做任何改动**。
>
> **变更归属说明**：`is_bound` 四态标记归属于 **B-01**（`user_workspace` 接口），不在本接口增加。

---

## 现网实现

| 属性 | 值 |
|------|-----|
| **Resource 类** | `ListTapdWorkspaceResource` |
| **位置** | `fta_web/issue/resources.py:1302` |
| **端点** | `POST /fta/issue/tapd/workspace/` |
| **鉴权** | `IAMPermission`（`ActionEnum.VIEW_EVENT`） |

### 调用链

```
POST /fta/issue/tapd/workspace/
  → ListTapdWorkspaceResource.perform_request
    → api.tapd.get_granted_workspaces()          # Basic Auth
    → ThreadPoolExecutor 并发取各项目 WorkspaceInfo
    → 返回 [{workspace_id, workspace_name, pretty_name, created, creator, description, status, category}]
```

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `workspace_id` | `string` | TAPD 项目 ID |
| `workspace_name` | `string` | 项目名称 |
| `pretty_name` | `string` | 展示名称 |
| `created` | `string` | 创建时间 |
| `creator` | `string` | 创建人 |
| `description` | `string` | 项目描述 |
| `status` | `string` | 项目状态 |
| `category` | `string` | 项目分类 |

> **无 `is_bound` 字段。** 如需四态标记，调用 B-01（见 `02-user-workspace.md`）。

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 标记为现有接口，说明无变更、四态归属 B-01 |
