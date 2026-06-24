---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-23
version: 1
tags: [integration, design, api]
author: AI
document_type: design
---

# B-04 解绑 TAPD 项目

> 前端暴露接口，用于将已关联的 TAPD 项目与当前业务解绑。
> 仅删除本地 `TapdWorkspaceBinding`，不在 TAPD 侧撤回应用授权。
> 继承 `common.md` 中的所有公共约定。

---

## 基础信息

| 属性 | 值 |
|------|-----|
| **接口名称** | 解绑 TAPD 项目 |
| **端点** | `/fta/issue/tapd/workspace/unbind/` |
| **方法** | `POST` |
| **Resource 类** | `UnbindTapdWorkspaceResource` |
| **所在模块** | `fta_web/issue/tapd_auth_resources.py` |
| **权限** | `IAMPermission`（`ActionEnum.MANAGE_EVENT`） |
| **IAM Action** | `ActionEnum.MANAGE_EVENT` |

---

## Request

### Body 参数

| 字段 | 类型 | 必填 | 默认值 | 约束 |
|------|------|:----:|:------:|------|
| `bk_biz_id` | `integer` | 是 | — | 正整数 |
| `workspace_id` | `string` | 是 | — | 非空 |

### 请求示例

```http
POST /fta/issue/tapd/workspace/unbind/
Content-Type: application/json

{
  "bk_biz_id": 2,
  "workspace_id": "69990779"
}
```

---

## Response

### 成功（200）

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
  "data": {
    "success": true
  }
}
```

### 解绑成功（200）

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
  "data": {
    "success": true
  }
}
```

### 项目未关联（404）

```json
{
  "result": false,
  "code": 3300005,
  "message": "未找到",
  "data": "TAPD 项目 69990779 未与当前业务关联"
}
```

### 参数缺失（400）

```json
{
  "result": false,
  "code": 400,
  "message": "请求参数错误",
  "data": {
    "bk_biz_id": ["该字段是必填项。"]
  }
}
```

### 权限不足（403）

```json
{
  "result": false,
  "code": 403,
  "message": "权限不足"
}
```

---

## 内部调用链

```
前端 POST /fta/issue/tapd/workspace/unbind/
  → IssueViewSet
    → IAMPermission (MANAGE_EVENT) 校验
      → UnbindTapdWorkspaceResource.perform_request
        → 提取 bk_biz_id / workspace_id
        → space_uid = bk_biz_id_to_space_uid(bk_biz_id)
        → TapdWorkspaceBinding.objects.filter(
            bk_tenant_id=DEFAULT_TENANT_ID,
            space_uid=space_uid,
            bk_biz_id=bk_biz_id,
            tapd_workspace_id=workspace_id
          )
        → 不存在 → raise HTTP404Error
        → 存在 → delete() → 返回 {"success": true}
```

---

## 内部依赖

| 依赖 | 位置 | 说明 |
|------|------|------|
| `TapdWorkspaceBinding` | `bkmonitor/models/tapd.py` | Django Model，唯一约束 (bk_tenant_id, space_uid, tapd_workspace_id) |
| `bk_biz_id_to_space_uid` | `bkm_space.utils` | 业务 ID 转空间 UID |
| `HTTP404Error` | `core/errors/common.py` | 404 错误码 |

---

## 业务行为说明

### 范围约束

- 仅删除本地 `TapdWorkspaceBinding`，**不调用 TAPD API 撤回应用授权**
- 解绑后，该项目在 B-01 列表中显示为 `unbound` 或 `importable`（取决于 TAPD 侧是否仍授权了该应用）
- 解绑后，前端对应项目卡片恢复为「去关联」状态

### 幂等性

- 同一 `bk_biz_id` + `workspace_id` 多次解绑 → 第一次成功删除，后续返回 `HTTP404Error`（binding 不存在）
- 不存在时返回 404 而非 200，**非幂等**（区分成功和无效操作）

### 并发安全

- `TapdWorkspaceBinding` 有唯一约束 `(bk_tenant_id, space_uid, tapd_workspace_id)`
- delete() 操作在数据库层面是原子的，无并发数据竞争

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-23 | AI | 初始创建 |
