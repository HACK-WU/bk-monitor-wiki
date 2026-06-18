---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-17
version: 2
tags: [feat, integration, design, S06]
depends_on: [S01, S02]
author: AI
document_type: design
parent: DESIGN.md
---

# S-06 授权检查

> 状态：已按设计评审结论（v1，2026-06-17）修订。
>
> **评审核心结论**：Token 从 DB → Redis。`TapdRequiredPermission` 校验 Redis key 是否存在且有效。

---

## ★ 1. 术语

| 术语 | 含义 | 引用 |
|------|------|------|
| `TapdRequiredPermission` | DRF `Permission` 子类，校验用户 Redis 中是否存在有效 token | — |
| `PermissionDenied` | DRF 标准异常，未通过授权检查时抛出；前端拦截其响应中的 `auth_url` 进行授权跳转 | — |
| `bk_tenant_id` | 蓝鲸租户 ID，用于构造 Redis key | S-01 §1 |

---

## ★ 3. 方案（TO-BE）

不新增独立查询接口。通过 **DRF Permission 类** 在请求入口处统一校验授权状态：

1. `TapdViewSet` 挂载 `TapdRequiredPermission`
2. 请求到达时，Permission **从 Redis 检查**当前 `bk_tenant_id + user` 是否存在有效 token（`tapd_uat:{tenant}:{user}` key 存在）
3. **已授权**（Redis key 存在）→ 放行，后续接口正常执行
4. **未授权 / 已过期**（Redis key 不存在或已过期）→ Permission 内部调用 `generate_auth_url(bk_biz_id)` 生成 `auth_url` → 抛出 `PermissionDenied(detail={"auth_url": auth_url})`
5. DRF 异常处理返回 **403**，前端拦截后跳转到 `auth_url`

> **【评审后变更】**：
> - 校验逻辑从查 DB（`UserTapdToken.objects.filter(...)`）→ 查 Redis（`redis_client.exists(key)`）
> - 删除 S-07 异步刷新的引用（已整套删除）
> - Token 过期不再「自动刷新」，而是返回 403 + auth_url，引导用户重走 OAuth

---

## ★ 4a. 权限类设计

### `TapdRequiredPermission`（Permission）

```python
class TapdRequiredPermission(BasePermission):
    def has_permission(self, request, view):
        bk_biz_id = get_bk_biz_id(request, view)
        bk_tenant_id = get_bk_tenant_id(request)  # 从请求上下文获取
        
        # 【评审后】从 Redis 检查 token
        redis_key = f"tapd_uat:{bk_tenant_id}:{request.user.username}"
        token_data = redis_client.get(redis_key)
        
        if not token_data:
            # Token 不存在或已过期，生成 auth_url
            auth_url = generate_auth_url(bk_biz_id)
            raise PermissionDenied(detail={"auth_url": auth_url})

        return True
```

> **使用位置**：所有需要 TAPD 用户态授权的 ViewSet（如 `TapdViewSet`）的 `permission_classes` 中挂载即可。

### `auth_url` 示例

`auth_url` 是**跳转用户授权**的链接地址。当 `TapdRequiredPermission` 检测到用户未授权或 Token 已过期时，生成此 URL 并随 `PermissionDenied` 返回给前端，前端通过 `window.location.href = auth_url` 或 `window.open(auth_url)` 跳转至 TAPD OAuth 授权页面，用户完成授权后由 TAPD 重定向回回调地址。

```
https://tapd.woa.com/oauth/?response_type=code&client_id=bkmonitor_tapd&redirect_uri=https%3A%2F%2Fmonitor.bk.example.com%2Fapi%2Ftapd%2Fcallback&scope=story%23read+story%23write&state=admin%3A12345678%3Aabc123def%3A2&auth_by=user
```

**参数说明**：

| 参数 | 值 | 说明 |
|------|------|------|
| `response_type` | `code` | 固定，OAuth 2.0 授权码模式 |
| `client_id` | `bkmonitor_tapd` | TAPD 应用 Client ID，由系统配置 |
| `redirect_uri` | `https://monitor.bk.example.com/api/tapd/callback` | 后端回调地址，需与 TAPD 应用配置完全一致 |
| `scope` | `story%23read+story%23write` | 授权范围，URL 编码后的 scope（如 `story#read` → `story%23read`） |
| `state` | `{nonce}:{bk_biz_id}` | 防 CSRF 参数，`nonce={user_name}:{random_str}` |
| `auth_by` | `user` | 固定，标识用户态授权 |

> **参考实现**：`tapd_oauth_demo.py` 中 `_generate_auth_url()` 函数，使用 `urllib.parse.urlencode` 拼接参数后返回完整 URL。

---

## +6. 异常处理

| 场景 | 行为 | 是否对外暴露 |
|------|------|:----------:|
| Token 不存在 | `PermissionDenied` → 403 + `{"detail": {"auth_url": "..."}}` | 是 |
| Token 已过期 | 同上，**不再自动刷新**（S-07 已删除），重走 OAuth | 是 |

---

## +10. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| `fta_web/tapd/` | 新增权限类 | `TapdRequiredPermission` Permission 类（DRF permission layer） | 否 |
| `urls.py` | 无 | 不新增 URL 路由（Permission 层拦截，不新增 Resource） | 否 |
| 前端页面 | 行为变更 | 统一拦截 403，提取 `detail.auth_url` 跳转授权 | 否 |

---

## +11. 待定问题

（无）
