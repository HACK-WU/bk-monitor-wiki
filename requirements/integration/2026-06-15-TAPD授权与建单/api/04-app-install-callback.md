---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-22
version: 2
tags: [integration, design, api]
author: AI
document_type: design
---

# B-03 应用态授权回调

> TAPD 回调接口，当管理员在 TAPD 完成应用授权安装后，TAPD 系统自动回调该接口完成项目绑定。
> 继承 `01-common.md` 中的所有公共约定。
> 
> **鉴权方式**：从回调请求中解析 `workspace_id`，结合 `request.state_querystring` 中的上下文参数校验请求来源一致性。

---

## 基础信息

| 属性 | 值 |
|------|-----|
| **接口名称** | 应用态授权回调 |
| **端点** | `/api/v4/issue/tapd/app_install_callback/` |
| **方法** | `GET` |
| **视图类型** | Django 函数视图 |
| **所在模块** | `kernel_api/views/v4/issue/callbacks.py` |
| **装饰器** | `@login_exempt` + `@csrf_exempt` |
| **鉴权** | 请求来源一致性校验（`state_querystring` 参数比对） |

---

## Request

### Query 参数

TAPD 完成应用安装授权后，将 `code`、`resource` 等参数附加到回调 URL。

```
GET /api/v4/issue/tapd/app_install_callback/
  ?code=4f9b2fab25a7c69715d426295a66717769666a0c
  &resource[type]=workspace
  &resource[workspace_id]=69990779
```

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `code` | `string` | TAPD 注入 | 授权码 |
| `resource[type]` | `string` | TAPD 注入 | 固定为 `workspace` |
| `resource[workspace_id]` | `string` | TAPD 注入 | TAPD 项目 ID |

### resource 结构

```json
{
  "type": "workspace",
  "workspace_id": "69990779"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `string` | 固定为 `workspace` |
| `workspace_id` | `string` | TAPD 项目 ID |

---

## Response

所有情况均返回 **302 重定向**，无 JSON 响应体。

### 成功

```http
HTTP/1.1 302 Found
Location: https://monitor.bk.example.com/tapd/bind?tapd_bind=success&workspace_id=69990779
```

### 失败（重定向到错误页）

```http
HTTP/1.1 302 Found
Location: https://monitor.bk.example.com/tapd/bind?tapd_bind=error&reason=missing_resource
```

### 失败原因枚举

| `reason` | 含义 | 触发条件 |
|----------|------|----------|
| `missing_resource` | 缺少项目信息 | `resource` 为空或 `workspace_id` 缺失 |
| `invalid_resource` | 项目信息无效 | `workspace_id` 格式错误或不存在 |
| `api_error` | TAPD API 异常 | `get_workspace_info` 调用失败 |
| `db_error` | 数据库写入失败 | upsert binding 失败 |

---

## 请求来源校验（state_querystring）

TAPD 回调时可能会在 `request.state_querystring` 中携带额外的上下文参数（如发起绑定的业务标识）。

```python
def verify_callback_source(request):
    """
    校验回调请求来源。

    1. 从 request.state_querystring 提取 bk_biz_id / initiator 等上下文参数
    2. 与回调中解析的 workspace_id 做一致性校验
    3. 失败时抛出异常，由视图捕获后 302 重定向到错误页
    """
    state_params = request.state_querystring or {}
    # 校验逻辑：确保 state 中携带的上下文与当前回调匹配
    # 如 bk_biz_id 一致、发起人与回调来源一致等
    ...
```

> `state_querystring` 为框架或中间件解析的额外参数，用于补充回调中缺失的上下文信息。
> 具体校验规则取决于业务需求（如租户隔离、发起人审计等）。

---

## 内部调用链

```
TAPD 回调 GET /api/v4/issue/tapd/app_install_callback/
  ?code=xxx&resource=...

  → 1. 从 request.GET 提取 code, resource
    → 2. 从 resource 中解析 workspace_id
      → 3. request.state_querystring → 提取上下文参数（bk_biz_id, initiator 等）
          → 校验来源一致性
            → 失败 → 302 ?tapd_bind=error&reason=invalid_resource
      → 4. GetWorkspaceInfoResource(workspace_id) -- Basic Auth
        → 获取 workspace_name
          → 5. upsert TapdWorkspaceBinding
              (bk_tenant_id, space_uid, bk_biz_id,
               workspace_id, workspace_name,
               create_user = current_user, update_user = current_user)
            → 6. 302 ?tapd_bind=success&workspace_id=xxx
```

---

## 幂等性

`TapdWorkspaceBinding.upsert` 使用唯一约束 `(bk_tenant_id, space_uid, tapd_workspace_id)` + `INSERT ... ON DUPLICATE KEY UPDATE` 实现幂等：

```sql
INSERT INTO tapd_workspace_binding
  (bk_tenant_id, space_uid, bk_biz_id, tapd_workspace_id, tapd_workspace_name, create_user, update_user)
VALUES
  (%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
  tapd_workspace_name = VALUES(tapd_workspace_name),
  update_user = VALUES(update_user),
  update_time = NOW();
```

重复回调（如用户多次点击）无副作用，最终状态一致。

---

## 跨浏览器/跨账号场景

应用态授权的关键场景：**普通用户在蓝鲸列表中看到未授权项目，复制 install_url（或前端直接打开）给有 TAPD 管理员权限的用户/账号完成授权**。

```
普通用户 → 前端展示 install_url（含 selected_workspace_id）→ 管理员在任意浏览器打开
                                                                     ↓
                                                              TAPD 应用安装页面
                                                                     ↓
                                                              TAPD 回调 B-03
                                                                     ↓
                                                              后端解析 workspace_id → upsert binding
```

由于 `install_url` 为 TAPD 页面 URL，管理员在任意浏览器中打开均可完成授权，无需登录蓝鲸平台。回调中通过 `request.state_querystring` 或 `workspace_id` 归属关系确定绑定上下文。

---

## 内部依赖

| 依赖 | 位置 | 说明 |
|------|------|------|
| `GetWorkspaceInfoResource` | `api/tapd/default.py` | Basic Auth 获取项目信息 |
| `TapdWorkspaceBinding` | `fta_web/issue/models.py` | upsert 关联记录 |

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建（含 signed_state HMAC 验签） |
| 2 | 2026-06-22 | AI | 简化：移除 signed_state/HMAC，改用 request.state_querystring 校验 |
