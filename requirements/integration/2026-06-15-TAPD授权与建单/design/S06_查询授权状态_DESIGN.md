---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-15
version: 1
tags: [feat, integration, design, S06]
depends_on: [S01, S02]
author: AI
document_type: design
parent: DESIGN.md
---

# S-06 授权检查

> 状态：设计中

---

## ★ 1. 术语

| 术语 | 含义 | 引用 |
|------|------|------|
| `TAPD_REQUIRED` | DRF `Permission` 子类，校验用户是否持有有效的 `UserTapdToken` | — |
| `PermissionDenied` | DRF 标准异常，未通过授权检查时抛出；前端拦截其响应中的 `auth_url` 进行授权跳转 | — |

---

## ★ 3. 方案（TO-BE）

不新增独立查询接口。通过 **DRF Permission 类** 在请求入口处统一校验授权状态：

1. `TapdViewSet` 挂载 `TAPD_REQUIRED`
2. 请求到达时，Permission 检查当前 `bk_biz_id + user` 是否存在有效 Token（`now() < expires_at`）
3. **已授权** → 放行，后续接口正常执行
4. **未授权 / 已过期** → Permission 内部调用 `generate_auth_url(bk_biz_id)` 生成 `auth_url` → 抛出 `PermissionDenied(detail={"auth_url": auth_url})`
5. DRF 异常处理返回 **403**，前端拦截后跳转到 `auth_url`

---

## ★ 4a. 权限类设计

### `TAPD_REQUIRED`（Permission）

```python
class TAPD_REQUIRED(BasePermission):
    def has_permission(self, request, view):
        bk_biz_id = get_bk_biz_id(request, view)
        token = UserTapdToken.objects.filter(
            username=request.user.username,
            is_deleted=False, is_enabled=True
        ).first()

        if not token or timezone.now() >= token.expires_at:
            # 内部生成 auth_url：查询 USER_TAPD_TOKEN 取 tapd_user_id（如有），构造 nonce={user_name}:{tapd_user_id}:{random_str}，再构造 OAuth URL，state 写入 Session
            auth_url = generate_auth_url(bk_biz_id)
            raise PermissionDenied(detail={"auth_url": auth_url})

        return True
```

> **使用位置**：所有需要 TAPD 用户态授权的 ViewSet（如 `TapdViewSet`）的 `permission_classes` 中挂载即可。

---

## +6. 异常处理

| 场景 | 行为 | 是否对外暴露 |
|------|------|:----------:|
| Token 不存在 | `PermissionDenied` → 403 + `{"detail": {"auth_url": "..."}}` | 是 |
| Token 已过期 | 同上，前端完成授权后由 S-07 自动刷新 Token | 是 |

---

## +10. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| `fta_web/tapd/` | 新增权限类 | `TAPD_REQUIRED` Permission 类（DRF permission layer） | 否 |
| `urls.py` | 无 | 不新增 URL 路由（Permission 层拦截，不新增 Resource） | 否 |
| 前端页面 | 行为变更 | 统一拦截 403，提取 `detail.auth_url` 跳转授权 | 否 |
