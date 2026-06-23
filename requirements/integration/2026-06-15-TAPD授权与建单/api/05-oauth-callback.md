---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-22
version: 1
tags: [integration, design, api]
author: AI
document_type: design
---

# B-05 用户态授权回调

> TAPD 回调接口，用户完成 OAuth 授权后，TAPD 回调该接口，后端用 code 换取 access_token 并加密存入 Redis。
> 继承 `common.md` 中的所有公共约定。

---

## 基础信息

| 属性 | 值 |
|------|-----|
| **接口名称** | 用户态授权回调 |
    | **端点** | `/fta/issue/tapd/oauth_callback/` |
| **方法** | `GET` |
| **视图类型** | Django 函数视图 |
| **所在模块** | `kernel_api/views/v4/issue/callbacks.py` |
| **装饰器** | `@login_exempt` + `@csrf_exempt` |
| **鉴权** | Session state 比对（防 CSRF） |

---

## Request

### Query 参数

```
GET /fta/issue/tapd/oauth_callback/
  ?code=4f9b2fab25a7c69715d426295a66717769666a0c
  &state=nonce123:2
  &resource[type]=user
  &resource[user_id]=user123
```

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `code` | `string` | TAPD 注入 | 授权码（有效期 10min） |
| `state` | `string` | 后端生成，TAPD 带回 | 格式 `{nonce}:{bk_biz_id}` |
| `resource[type]` | `string` | TAPD 注入 | 固定为 `user` |
| `resource[user_id]` | `string` | TAPD 注入 | TAPD 用户 ID |

### state 格式

```
state = f"{nonce}:{bk_biz_id}"

示例："adminuser:randomstr123:2"
```

| 部分 | 说明 |
|------|------|
| `nonce` | `{username}:{随机串}`，用于防 CSRF |
| `bk_biz_id` | 蓝鲸业务 ID，用于从 Session 中定位 state |

### resource 结构

```json
{
  "type": "user",
  "user_id": "user123"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `string` | 固定为 `user` |
| `user_id` | `string` | TAPD 用户唯一标识 |

---

## Response

所有情况均返回 **302 重定向**，无 JSON 响应体。

### 成功

```http
HTTP/1.1 302 Found
Location: https://monitor.bk.example.com/tapd/workspace?auth=success
```

### 失败（重定向到错误页）

```http
HTTP/1.1 302 Found
Location: https://monitor.bk.example.com/tapd/workspace?auth=error&reason=state_mismatch
```

### 失败原因枚举

| `reason` | 含义 | 触发条件 |
|----------|------|----------|
| `state_mismatch` | Session state 不匹配 | Session 中无此 state 或 nonce 不匹配（CSRF 攻击或 Session 过期） |
| `code_invalid` | 授权码无效 | code 已使用或超过 10min 有效期 |
| `api_error` | TAPD API 异常 | `RequestTokenResource` 调用失败 |
| `storage_error` | Redis 写入失败 | `setex` 操作异常 |

---

## 内部调用链

```
TAPD 回调 GET /fta/issue/tapd/oauth_callback/?code=xxx&state=nonce123:2

  → 1. 从 request.GET 提取 code, state, resource（可选）
    → 2. 解析 state: nonce, bk_biz_id
      → 3. 从 Session 取出 request.session[f'tapd_oauth_state_{bk_biz_id}']
        → 比对 nonce 是否匹配
          → 不匹配 → 302 ?auth=error&reason=state_mismatch
          → 匹配 → del request.session[key]  # 比对成功后立即删除，防重放攻击
            → 4. RequestTokenResource(code) -- Basic Auth
              → POST http://apiv2.tapd.woa.com/tokens/request_token
                → 获取 {access_token, expires_in, token_type, scope, resource.user_id}
                  → 5. AESCipher 加密 access_token
                    → 6. Redis: setex tapd_uat:{tenant}:{user} TTL=expires_in
                        value = json.dumps({
                            "access_token": "密文",
                            "tapd_user_id": "user123",
                            "token_type": "Bearer",
                            "expires_at": "2024-01-15T12:00:00Z"
                        })
                      → 7. 302 ?auth=success
```

---

## Token 存储格式（Redis）

### Key 规范

```
Key    : tapd_uat:{bk_tenant_id}:{username}
TTL    : expires_in（秒，如 7200 = 2小时）
Value  : AESCipher 加密后的 JSON 串
```

### Value 明文结构（加密前）

```json
{
  "access_token": "access_token_abc123def456",
  "tapd_user_id": "user123",
  "token_type": "Bearer",
  "expires_at": "2024-01-15T12:00:00Z"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `access_token` | `string` | TAPD 用户态访问令牌 |
| `tapd_user_id` | `string` | TAPD 用户 ID（来自 resource.user_id） |
| `token_type` | `string` | 令牌类型（通常为 `Bearer`） |
| `expires_at` | `string` | ISO 8601 过期时间（当前时间 + expires_in） |

### AESCipher 加密

```python
from bkmonitor.utils.cipher import AESCipher

cipher = AESCipher(key=settings.SECRET_KEY)   # 不传 iv，每次随机生成
encrypted = cipher.encrypt(json.dumps(token_data))
decrypted = cipher.decrypt(encrypted)         # 从首块读回 IV
```

> **禁止传固定 IV**：`AESCipher(iv=xxx)` 会导致相同明文的密文相同，泄露相等性。

### Redis 操作

```python
# 写入（B-05）
redis_client.setex(
    f"tapd_uat:{bk_tenant_id}:{username}",
    expires_in,  # TTL 对齐 token 过期时间
    cipher.encrypt(json.dumps(token_data))
)

# 读取（B-01 的 TAPD_REQUIRED Permission）
encrypted = redis_client.get(f"tapd_uat:{bk_tenant_id}:{username}")
if encrypted:
    token_data = json.loads(cipher.decrypt(encrypted))
    # 校验 expires_at（TTL 到期自动淘汰，兜底检查）
```

---

## Session State 管理

### 写入（B-01 生成 auth_url 时）

```python
def generate_auth_url(bk_biz_id: int, request) -> str:
    """生成 TAPD OAuth 授权 URL，state 存入 Session"""
    nonce = f"{request.user.username}:{secrets.token_urlsafe(8)}"
    state = f"{nonce}:{bk_biz_id}"

    # 存入 Session，key 按 bk_biz_id 隔离
    request.session[f"tapd_oauth_state_{bk_biz_id}"] = state

    # 返回未编码 URL（前端自行处理）
    return (
        f"https://tapd.woa.com/oauth/authorize"
        f"?client_id={settings.TAPD_APP_ID}"
        f"&response_type=code"
        f"&redirect_uri={settings.TAPD_OAUTH_CALLBACK_URL}"
        f"&scope=user_space"
        f"&state={state}"
    )
```

### 读取与删除（B-05 回调时）

```python
@login_exempt
@csrf_exempt
def tapd_oauth_callback(request):
    state = request.GET.get("state", "")
    nonce, bk_biz_id = state.rsplit(":", 1)

    # 从 Session 读取
    session_key = f"tapd_oauth_state_{bk_biz_id}"
    expected_state = request.session.get(session_key)

    if not expected_state or expected_state != state:
        return redirect(f"{settings.FRONTEND_URL}/tapd/workspace?auth=error&reason=state_mismatch")

    # 比对成功后立即删除，防止重放攻击
    del request.session[session_key]

    # ... 继续 code 换 token ...
```

### Session Key 命名规范

```
tapd_oauth_state_{bk_biz_id}

示例：
- tapd_oauth_state_2     # bk_biz_id = 2
- tapd_oauth_state_100   # bk_biz_id = 100
```

> 按 `bk_biz_id` 隔离，支持同一用户在不同业务下独立授权。

---

## 与 B-03 的差异

| 维度 | B-03（应用态回调） | B-05（用户态回调） |
|------|-------------------|-------------------|
| **触发时机** | 管理员完成应用安装授权 | 用户完成 OAuth 授权 |
| **state 机制** | `request.state_querystring`（框架/中间件解析的上下文参数） | Session state（明文 nonce + bk_biz_id） |
| **鉴权方式** | 请求来源一致性校验 | Session 比对（防 CSRF） |
| **核心操作** | upsert binding（项目关联） | code 换 token → 加密存入 Redis |
| **返回字段** | `workspace_id`（重定向参数） | 无（仅成功/失败状态） |
| **失败处理** | `?tapd_bind=error&reason=xxx` | `?auth=error&reason=xxx` |
| **前端页面** | `/tapd/bind` | `/tapd/workspace` |

---

## 无刷新机制说明

一期**不实现 token 异步刷新**：

- token 过期后，Redis TTL 自动淘汰 key
- 用户再次调用 B-01 时，TAPD_REQUIRED Permission 发现 key 不存在，返回 403 + auth_url
- 用户重走 OAuth 授权（一次廉价重定向）

> 评审结论：token 刷新机制比例失衡，一次重定向成本低，无需复杂异步任务。

---

## 内部依赖

| 依赖 | 位置 | 说明 |
|------|------|------|
| `RequestTokenResource` | 新增 `api/tapd/oauth.py` | code 换 access_token（Basic Auth） |
| `AESCipher` | `utils/cipher.py` | 加密/解密 token |
| Django Session | 框架内置 | 读写 state（防 CSRF） |
| Redis | 缓存服务 | 存储加密后的 token |
| `generate_auth_url()` | 工具函数 | 生成未编码 OAuth URL |

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建 |
