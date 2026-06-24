---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-24
version: 2
tags: [integration, design, api, resource]
author: AI
document_type: design
---

# 内部 Resource 类

> 本节汇总新增和复用的后台 Resource 类，对应 design tree 的 B-02、B-04、B-05、B-06 节点。供 Stage 2 技术评审中后台人员直接定位实现。

---

## 枚举

| Resource 类 | 设计节点 | 类型 | 继承自 | 用途 |
|-------------|---------|------|--------|------|
| `TapdUserAPIResource` | B-06 | 新增 | `Resource`（基类） | 包装 TAPD 用户态 API（Bearer Token） |
| `GetGrantedWorkspacesResource` | B-02 | 新增 | `TapdAPIResource` | app 级 Basic Auth，获取已授权项目 |
| `GetWorkspaceInfoResource` | B-04 | 新增 | `TapdAPIResource` | app 级 Basic Auth，获取单个项目信息 |
| `RequestTokenResource` | B-05 | 新增 | `TapdAPIResource` | code 换 access_token（Basic Auth） |

---

## B-06: TapdUserAPIResource

### 类定义

```python
class TapdUserAPIResource(Resource):
    """
    调用 TAPD V2 用户态 API。

    提供 _get_user_token() 子类可覆盖获取当前请求用户的 access_token，
    自动注入到请求头：Authorization: Bearer {token}。
    """
    module_name = "tapd_user"
    base_url = fta_settings.TAPD_API_BASE_URL  # 如 https://api.tapd.woa.com
```

### 核心方法

| 方法 | 说明 |
|------|------|
| `_get_user_token()` | 从 Redis 读取 UAT 缓存并解密，返回值明文（含 access_token） |
| `get_headers()` | 自动注入 `Authorization: Bearer {access_token}` |
| `get_access_token()` | 供子类直接调用获取当前用户 token |

### get_access_token 时序

```
TapdUserAPIResource.get_access_token()
  → 1. 提取 request_user.username, bk_tenant_id
    → 2. Redis: get tapd_uat:{tenant}:{user}
      → 3. AESCipher.decrypt() → 明文 JSON
        → 4. 返回 {"access_token": "...", "tapd_user_id": "...", ...}
```

### self.client 通讯

```python
from bkmonitor.utils.http import BKMonitorSession

headers = self.get_headers()   # 含 Authorization: Bearer xxx
api_params = self.get_request_data()

self.client.fetch(
    url=f"{self.base_url}{self.action}",
    method=self.method,
    headers=headers,
    body=api_params,
)
```

### 子类示例

```python
class UserWorkspacesResource(TapdUserAPIResource):
    """获取用户可见的 TAPD 项目列表"""
    action = "/members/get_user_workspaces"
    method = "GET"
```

---

## B-02: GetGrantedWorkspacesResource

### 类定义

```python
class GetGrantedWorkspacesResource(TapdAPIResource):
    """
    查询 app 已授权的 TAPD 项目列表。
    使用 app 级 Basic Auth（client_id + client_secret）。
    """
    action = "/app_auth/get_granted_workspaces"
    method = "GET"
    cache_seconds = 60   # 短 TTL 缓存（秒），超时时使用缓存数据
```

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `client_id` | query | `string` | 是 | fta_settings.TAPD_APP_ID |
| `client_secret` | query | `string` | 是 | fta_settings.TAPD_APP_SECRET |
| `type` | query | `integer` | 否 | 0:应用商店, 1:测试, 2:插件 |
| `page` | query | `integer` | 否 | 页码，从 1 开始 |
| `limit` | query | `integer` | 否 | 每页数量，默认 200 |

### 返回示例

```json
{
  "status": 1,
  "data": [
    {
      "Workspace": {
        "id": "69990779",
        "name": "蓝鲸监控项目",
        "tapd_type": 0,
        "created": "2024-01-15T03:20:00Z"
      }
    }
  ],
  "info": "success"
}
```

### 返回字段（单层扁平化后）

| 字段 | 路径 | 类型 | 说明 |
|------|------|------|------|
| `workspace_id` | `Workspace.id` | `string` | TAPD 项目 ID |
| `workspace_name` | `Workspace.name` | `string` | 项目名称 |
| `tapd_type` | `Workspace.tapd_type` | `integer` | 安装类型 |
| `created` | `Workspace.created` | `string` | 创建时间 |

---

## B-04: GetWorkspaceInfoResource

### 类定义

```python
class GetWorkspaceInfoResource(TapdAPIResource):
    """
    查询单个 TAPD 项目信息。
    使用 app 级 Basic Auth。
    """
    action = "/workspaces/get_workspace_info"
    method = "GET"
```

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `client_id` | query | `string` | 是 | fta_settings.TAPD_APP_ID |
| `client_secret` | query | `string` | 是 | fta_settings.TAPD_APP_SECRET |
| `workspace_id` | query | `string` | 是 | TAPD 项目 ID |

### 返回示例

```json
{
  "status": 1,
  "data": [
    {
      "Workspace": {
        "id": "69990779",
        "name": "蓝鲸监控项目",
        "description": "蓝鲸监控 TAPD 项目"
      }
    }
  ],
  "info": "success"
}
```

### 返回字段

| 字段 | 路径 | 类型 | 说明 |
|------|------|------|------|
| `workspace_id` | `Workspace.id` | `string` | TAPD 项目 ID |
| `workspace_name` | `Workspace.name` | `string` | 项目名称 |
| `description` | `Workspace.description` | `string` | 项目描述（可选） |

---

## B-05: RequestTokenResource

### 类定义

```python
class RequestTokenResource(TapdAPIResource):
    """
    TAPD OAuth 请求令牌接口。
    使用 app 级 Basic Auth 调用。
    文档：https://tapd.woa.com/tapd_api/application_authorize/oauth.html
    """
    action = "/tokens/request_token"
    method = "POST"
```

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `client_id` | query | `string` | 是 | fta_settings.TAPD_APP_ID |
| `client_secret` | query | `string` | 是 | fta_settings.TAPD_APP_SECRET |
| `grant_type` | body | `string` | 是 | 固定为 `authorization_code` |
| `code` | body | `string` | 是 | OAuth redirect 时带回的授权码 |
| `redirect_uri` | body | `string` | 是 | 必须与注册 redirect_uri 完全一致 |

### 返回示例

```json
{
  "access_token": "access_token_abc123def456",
  "expires_in": 7200,
  "token_type": "Bearer",
  "scope": "user_space",
  "resource": {
    "user_id": "user123"
  }
}
```

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `access_token` | `string` | TAPD 用户态访问令牌 |
| `expires_in` | `integer` | 过期时间（秒，如 7200 = 2 小时） |
| `token_type` | `string` | 固定为 `Bearer` |
| `scope` | `string` | 授权范围（如 `user_space`） |
| `resource.user_id` | `string` | TAPD 用户唯一标识 |

### 异常处理

| 场景 | 行为 |
|------|------|
| code 已使用 | 报 401 `invalid_grant` |
| code 过期（10min） | 报 401 `invalid_grant` |
| redirect_uri 不匹配 | 报 400 `invalid_request` |

---

## 各 Resource 鉴权方式对比

| Resource | Auth 类型 | 认证信息 | 风险 |
|----------|-----------|----------|------|
| `TapdUserAPIResource` | Bearer Token | Redis 中缓存的用户 UAT | Token 泄露即有完整用户操作权限 |
| `GetGrantedWorkspacesResource` | Basic Auth | app_id + app_secret | 证书泄露即获取所有授权项目 |
| `GetWorkspaceInfoResource` | Basic Auth | app_id + app_secret | 同上 |
| `RequestTokenResource` | Basic Auth | app_id + app_secret | 无敏感用户数据，仅交换 code |

---

## 基类关系

```
Resource (bkmonitor.utils.http)
  ├── TapdAPIResource (api/tapd/default.py)
  │     ├── GetGrantedWorkspacesResource (B-02)
  │     ├── GetWorkspaceInfoResource (B-04)
  │     └── RequestTokenResource (B-05)
  └── TapdUserAPIResource (api/tapd/user.py, 新增 B-06)
        └── UserWorkspacesResource (子类)

IssueAPIResource / BKMonitorAPIResource (api/issue/default.py)
  └── IssueResource (fta_web/issue/resources.py)
        ├── ListUserVisibleTapdWorkspaceResource (B-01)
        ├── ListTapdWorkspaceResource (B-07)
        └── ... 现有 IssueResource ...
```

---

## 新文件清单

| 文件 | 内容 | 对应节点 |
|------|------|----------|
| `api/tapd/user.py` | `TapdUserAPIResource`、`UserWorkspacesResource` | B-06 |
| `api/tapd/default.py` | `GetGrantedWorkspacesResource`、`GetWorkspaceInfoResource`、`RequestTokenResource` | B-02, B-04, B-05 |
| `utils/tapd_auth.py` | `generate_auth_url`、`generate_install_url`、`generate_signed_state`、`verify_signed_state` | B-01, B-03 |

### 工具函数签名变更

#### `generate_auth_url`（B-01）

```python
# 变更前
def generate_auth_url(bk_biz_id: int, request) -> str:
    pass

# 变更后 — 增加 redirect_uri_real
from urllib.parse import quote

def generate_auth_url(
    bk_biz_id: int,
    redirect_uri_real: str,      # ← 前端传入：含 # 的真实地址（回调 302 用）
    request
) -> str:
    """生成 TAPD OAuth 授权 URL，state JSON 存入 Session"""
    nonce = f"{request.user.username}:{secrets.token_urlsafe(8)}"
    state_value = f"{nonce}:{bk_biz_id}"

    state_json = json.dumps({
        "nonce": nonce,
        "bk_biz_id": bk_biz_id,
        "redirect_uri_real": redirect_uri_real,
    })
    request.session[f"tapd_oauth_state_{bk_biz_id}"] = state_json

    return (
        f"https://tapd.woa.com/oauth/authorize"
        f"?client_id={settings.TAPD_APP_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri_verify}"  # ← 不含 #（TAPD 校验用）
        f"&scope=user_space"
        f"&state={state_value}"
    )
```

> `redirect_uri_verify` 由 B-01 请求参数传入。

#### `generate_install_url`（B-01）

```python
# 变更前 — 内部使用 settings.TAPD_OAUTH_CALLBACK_URL 构建 cb
def generate_install_url(bk_biz_id: int, signed_state: str) -> str:
    pass

# 变更后 — cb 中的 redirect_uri_verify 来自前端请求参数
def generate_install_url(
    bk_biz_id: int,
    signed_state: str,
    redirect_uri_verify: str,    # ← 前端传入：不含 # 的校验地址
) -> str:
    """生成 TAPD open_app_install URL"""
    cb = urllib.parse.quote(
        f"{redirect_uri_verify}/fta/issue/tapd/app_install_callback/?signed_state={signed_state}",
        safe=''
    )
    return (
        f"https://tapd.woa.com/oauth/open_app_install"
        f"?client_id={settings.TAPD_APP_ID}"
        f"&test=1"
        f"&cb={cb}"
        f"#selected_workspace_id={{workspace_id}}"
    )
```

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建 |
| 2 | 2026-06-24 | AI | `generate_auth_url` 增加 `redirect_uri_real` 参数；`generate_install_url` 增加 `redirect_uri_verify` 参数；新增工具函数签名变更说明 |
