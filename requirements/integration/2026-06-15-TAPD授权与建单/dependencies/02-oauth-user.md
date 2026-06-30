# 用户态 OAuth

> 用户态 OAuth 用于获取 per-user 的 access_token，本需求用于 B-05 流程。
> ⚠️ 一期不存储 refresh_token（评审结论 A1），token 过期后重走 OAuth（一次廉价重定向）。

---

## 1. 获取用户授权码

引导用户到 TAPD 授权页，获取一次性 code。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET（浏览器跳转） |
| **请求 URL** | `https://tapd.woa.com/oauth/` |

### 请求参数（Query）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `response_type` | 是 | string | 固定 `code` |
| `client_id` | 是 | string | 应用 ID（需从开放平台应用管理获取） |
| `redirect_uri` | 是 | string | 回调地址，**必须在白名单中，不能包含 #** |
| `scope` | 是 | string | 空格分隔的权限范围，例如 `story#read bug#read`。**需要 URL encode** |
| `state` | 是 | string | 防 CSRF 状态码，回调时原样带回；可携带自定义信息 |
| `auth_by` | 是 | string | 固定 `user` |

> **scope URL encode 示例**：`story#read bug#read` → `story%23read+bug%23read`

### 请求示例

```
GET https://tapd.woa.com/oauth/?
    response_type=code
    &client_id=JnKeFzm1
    &redirect_uri=http%3A%2F%2Flion.oa.com%2F~anyechen%2Fcode%2Fphp%2Foauth_demo%2Fhey.php
    &scope=story%23read+bug%23read
    &state=random_string
    &auth_by=user
```

### 授权流程

1. 用户在浏览器中打开上述 URL
2. 用户点击「同意授权」
3. TAPD 跳回 `redirect_uri`，携带以下 Query 参数：

| 返回参数 | 说明 |
|----------|------|
| `code` | 授权码，**有效期 5 分钟**，一次性使用 |
| `state` | 原样带回的透传参数 |
| `resource` | JSON 字符串，例如 `{"type":"user","user_id":"1001320052"}` |

### 回调示例 URL

```
http://lion.oa.com/~anyechen/code/php/oauth_demo/hey.php?
    code=e09881835fc0a44c3bdabbbc091a1aa3f189554b
    &state=random_string
    &resource=%7B%22type%22%3A%22user%22%2C%22user_id%22%3A%221001320052%22%7D
```

---

## 2. code 换取 access_token

使用授权码换取用户态 access_token。

| 项目 | 内容 |
|------|------|
| **请求方式** | POST |
| **请求 URL** | `http://apiv2.tapd.woa.com/tokens/request_token` |
| **认证方式** | **Basic Auth** — `Base64(client_id:client_secret)` |

### 请求参数（POST Body，application/x-www-form-urlencoded）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `grant_type` | 是 | string | 固定 `authorization_code` |
| `redirect_uri` | 是 | string | 必须**与授权链接中传的 redirect_uri 完全一致** |
| `code` | 是 | string | 从回调 URL 中提取的 code |

### 请求示例（curl）

```bash
curl -u "client_id:client_secret" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=http://lion.oa.com/~anyechen/code/php/oauth_demo/hey.php" \
  -d "code=e09881835fc0a44c3bdabbbc091a1aa3f189554b" \
  "http://apiv2.tapd.woa.com/tokens/request_token"
```

### 返回参数

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | integer | 1 = 成功 |
| `data.access_token` | string | 用户态访问令牌（约 40 位字符串） |
| `data.expires_in` | integer | 有效时长，**单位秒**，约 7200（2 小时） |
| `data.token_type` | string | 固定 `Bearer` |
| `data.scope` | string | 接口范围，如 `bug#read story#read` |
| `data.resource` | object | 授权用户信息，如 `{"type":"user","user_id":"..."}` |
| `data.now` | string | 服务器当前时间，格式 `YYYY-MM-DD HH:MM:SS` |
| `info` | string | 提示信息 |

### 返回示例

```json
{
    "status": 1,
    "data": {
        "access_token": "9f11dab4be3fed782d15b7cfzxc8d08c49792119",
        "expires_in": 7200,
        "token_type": "Bearer",
        "scope": "bug#read story#read",
        "resource": {
            "type": "user",
            "user_id": "1001320052"
        },
        "now": "2026-01-06 17:16:04"
    },
    "info": "success"
}
```
