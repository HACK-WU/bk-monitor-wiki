---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-24
version: 4
tags: [integration, design, api]
author: AI
document_type: design
---

# B-03 应用态授权回调

> TAPD 回调接口，当管理员在 TAPD 完成应用授权安装后，TAPD 系统自动回调该接口完成项目绑定。
> 继承 `01-common.md` 中的所有公共约定。
>
> **鉴权方式**：`signed_state` HMAC 验签。`signed_state` 在 B-01 构建 install_url 时烘入 `cb` 参数，TAPD 回调时原样带回，后端用共享密钥验证签名和过期时间，确保回调来源可信，同时兼容跨浏览器/跨账号授权场景。

---

## 基础信息

| 属性 | 值 |
|------|-----|
| **接口名称** | 应用态授权回调 |
| **端点** | `/fta/issue/tapd/app_install_callback/` |
| **方法** | `GET` |
| **视图类型** | Django 函数视图 |
| **所在模块** | `kernel_api/views/v4/issue/callbacks.py` |
| **装饰器** | `@login_exempt` + `@csrf_exempt` |
| **鉴权** | `signed_state` HMAC 验签 + HMAC-SHA256 |

---

## Request

### Query 参数

TAPD 完成应用安装授权后，将 `code`、`resource`、`signed_state` 等参数附加到回调 URL。

```
GET /fta/issue/tapd/app_install_callback/
  ?code=4f9b2fab25a7c69715d426295a66717769666a0c
  &resource[type]=workspace
  &resource[workspace_id]=69990779
  &signed_state=eyJia19iaXpfaWQiOjIsInRlbi4uLn0.WzG4x...
```

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `code` | `string` | TAPD 注入 | 授权码 |
| `resource[type]` | `string` | TAPD 注入 | 固定为 `workspace` |
| `resource[workspace_id]` | `string` | TAPD 注入 | TAPD 项目 ID |
| `signed_state` | `string` | B-01 生成，TAPD 原样带回 | `base64url(json).hmac`，HMAC-SHA256 签名状态 |

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
Location: https://monitor.bk.example.com/tapd/bind?tapd_bind=error&reason=invalid_signed_state
```

### 失败原因枚举

| `reason` | 含义 | 触发条件 |
|----------|------|----------|
| `missing_resource` | 缺少项目信息 | `resource` 为空或 `workspace_id` 缺失 |
| `invalid_resource` | 项目信息无效 | `workspace_id` 格式错误或不存在 |
| `invalid_signed_state` | HMAC 验签失败 | `signed_state` 格式非法或签名不匹配（可能被篡改） |
| `signed_state_expired` | signed_state 过期 | `exp` 已超过当前时间 |
| `api_error` | TAPD API 异常 | `get_workspace_info` 调用失败 |
| `db_error` | 数据库写入失败 | upsert binding 失败 |

> 注：所有重定向地址均从 `signed_state.payload.redirect_uri_real` 获取，不依赖 `settings` 硬编码。

---

## signed_state 机制

### 格式

```
signed_state = base64url(json_payload).hmac_signature

# 其中: base64url(json_payload) = base64url(json_bytes, urlsafe=True, padding=False)
#       hmac_signature         = HMAC-SHA256(base64url_json, secret_key)[:16]（截断至16进制16字符）
```

### JSON Payload 结构

```json
{
  "bk_biz_id": 2,
  "bk_tenant_id": "default",
  "space_uid": "bkcc__2",
  "initiator": "artemis",
  "exp": 1719072000,
  "redirect_uri_real": "https://monitor.bk.example.com/#/tapd/bind"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `bk_biz_id` | `integer` | 蓝鲸业务 ID |
| `bk_tenant_id` | `string` | 蓝鲸租户 ID |
| `space_uid` | `string` | 蓝鲸空间唯一标识 |
| `initiator` | `string` | 关联动作的**真实发起人**（B-01 生成 install_url 时的当前登录用户 username） |
| `exp` | `integer` | 过期时间戳（Unix epoch，建议 TTL = 15min） |
| `redirect_uri_real` | `string` | 前端传入的真实重定向地址（含 `#`），B-03 回调成功后 302 跳转用。
                     由 B-01 在生成 install_url 时从前端 `redirect_uri_real` 参数写入。 |

### HMAC 签名算法

```python
import base64
import hashlib
import hmac
import json
import secrets

def generate_signed_state(
    bk_biz_id: int,
    bk_tenant_id: str,
    space_uid: str,
    initiator: str,
    secret_key: str,
    ttl_seconds: int = 900  # 15min
) -> str:
    """生成 signed_state，用于应用态授权回调"""
    payload = {
        "bk_biz_id": bk_biz_id,
        "bk_tenant_id": bk_tenant_id,
        "space_uid": space_uid,
        "initiator": initiator,
        "exp": int(time.time()) + ttl_seconds,
    }

    # Base64URL 编码 payload（无 padding）
    json_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    b64_payload = base64.urlsafe_b64encode(json_bytes).rstrip(b"=").decode("ascii")

    # HMAC-SHA256（截断至16进制16字符）
    signature = hmac.new(
        secret_key.encode("utf-8"),
        b64_payload.encode("ascii"),
        hashlib.sha256
    ).hexdigest()[:16]

    return f"{b64_payload}.{signature}"

def verify_signed_state(signed_state: str, secret_key: str) -> dict:
    """验证 signed_state，返回 payload dict 或抛出异常"""
    try:
        b64_payload, signature = signed_state.rsplit(".", 1)
    except ValueError:
        raise InvalidSignedStateError("格式非法")

    # 重新计算签名比对
    expected = hmac.new(
        secret_key.encode("utf-8"),
        b64_payload.encode("ascii"),
        hashlib.sha256
    ).hexdigest()[:16]

    if not hmac.compare_digest(expected, signature):
        raise InvalidSignedStateError("签名不匹配")

    # 还原 payload
    json_bytes = base64.urlsafe_b64decode(b64_payload + "==")
    payload = json.loads(json_bytes)

    # 校验过期时间
    if payload["exp"] < time.time():
        raise SignedStateExpiredError()

    return payload
```

> **密钥**：使用 Django `settings.SECRET_KEY` 作为 HMAC secret，与 AES 加密 Token 共用同一密钥源。
>
> **截断**：签名截断至 hex 16 字符（64bit），兼顾安全性与 URL 长度。

---

## 内部调用链

```
TAPD 回调 GET /fta/issue/tapd/app_install_callback/
  ?code=xxx&resource=...&signed_state=eyJ4e...WzG4x

  → 1. 从 request.GET 提取 code, resource, signed_state
    → 2. 解析 resource 获取 workspace_id
      → 3. verify_signed_state(signed_state, settings.SECRET_KEY)
        → 验签 & 验过期
          → 失败 → 302 ?tapd_bind=error&reason=invalid_signed_state / signed_state_expired
          → 成功 → 提取 payload: {bk_biz_id, bk_tenant_id, space_uid, initiator}
      → 4. GetWorkspaceInfoResource(workspace_id) -- Basic Auth
        → 获取 workspace_name
          → 5. upsert TapdWorkspaceBinding
              (bk_tenant_id, space_uid, bk_biz_id,
               workspace_id, workspace_name,
               create_user = initiator,       # ← 真实发起人
               update_user = initiator)       # 管理员在管理员端完成授权，不依赖管理员登录态
                → 6. 提取 payload.redirect_uri_real
        → 7. 302 {redirect_uri_real}?tapd_bind=success&workspace_id=xxx
```

> **关键设计**：`create_user` 和 `update_user` 使用 `initiator`（从 `signed_state` 提取的 B-01 发起用户），而非 `current_user`（回调时管理员可能不在蓝鲸登录态）。这确保了跨浏览器/跨账号场景下的审计链完整性。

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

应用态授权的**核心场景**：普通用户在蓝鲸列表中看到未授权项目，复制 install_url 给有 TAPD 管理员权限的用户/账号完成授权。

```
普通用户 artemis
  → 前端展示 install_url（含 signed_state=eyJia19iaXpfaWQ...）
    → 复制给管理员 Alice 或发到企业微信
      → 管理员 Alice 在任意浏览器打开
        → TAPD 应用安装页面（无需登录蓝鲸）
          → TAPD 回调 B-03
            → verify_signed_state
              → 验签通过 → upsert binding, create_user = artemis
                → 302 redirect
```

由于 `signed_state` 中包含 `initiator=artemis`，即使管理员 Alice 在另一个浏览器/另一个蓝鲸账号中完成授权，最终关联记录的 `create_user` 依然是真正的发起人 `artemis`，保证了审计追溯的准确性。

`signed_state` 同时防止了恶意伪造：
- 不知道 `SECRET_KEY` 的攻击者无法生成有效签名 → 验签失败
- 截获了别人的 install_url 但 `signed_state` 已过期 → `signed_state_expired`

---

## 内部依赖

| 依赖 | 位置 | 说明 |
|------|------|------|
| `GetWorkspaceInfoResource` | `api/tapd/default.py` | Basic Auth 获取项目信息 |
| `TapdWorkspaceBinding` | `fta_web/issue/models.py` | upsert 关联记录 |
| `generate_signed_state` | `utils/tapd_auth.py` | B-01 生成 install_url 时调用 |
| `verify_signed_state` | `utils/tapd_auth.py` | B-03 回调时验签 |

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建（含 signed_state HMAC 验签） |
| 2 | 2026-06-22 | AI | 简化：移除 signed_state/HMAC，改用 request.state_querystring 校验 |
| 3 | 2026-06-22 | AI | **恢复**：按评审结论 A2 恢复 `signed_state` HMAC 机制，增加 `initiator` 从 `signed_state` 中提取替代 `current_user` |
| 4 | 2026-06-24 | AI | signed_state payload 增加 `redirect_uri_real`，回调成功时 302 跳转到该地址（替代硬编码 `settings.FRONTEND_URL`） |
