# 第三方依赖文档 — TAPD 开放平台 v2 API

> 需求：`REQ-20260615-001` TAPD 授权与建单
> 整理时间：2026-06-18
> 文档性质：技术设计前置依赖参考
> 
> ⚠️ **安全声明**：本文档不包含任何 client_id、client_secret、access_token、密钥等敏感信息。所有示例中的凭据均为占位符。

---

## 依赖总览

| 依赖名称 | 类型 | 在本需求中的用途 |
|----------|------|-----------------|
| TAPD 开放平台 v2 | 第三方 OAuth + REST API | 用户态 OAuth、应用态 OAuth、业务数据查询 |

| API 基地址 | `http://apiv2.tapd.woa.com` |
| OAuth 基地址 | `https://tapd.woa.com/oauth/` |
| 开发者后台 | `https://o.tapd.woa.com/admin/myapps` |

---

## 1. API 通用规范

### 1.1 通用响应格式

所有 TAPD API v2 使用统一响应结构：

```json
{
    "status": 1,
    "data": { ... },
    "info": "success"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | integer | 1 = 成功，其他 = 失败 |
| `data` | object | 响应数据体，各接口结构不同 |
| `info` | string | 提示信息 |

> 失败时 `status != 1`，可能伴随更详细的错误信息（常见 HTTP 状态码见 §5）。

### 1.2 认证方式

| 认证方式 | 场景 |
|----------|------|
| **Basic Auth** | app 级 API（`get_granted_workspaces`、`get_workspace_info`、建单）；`request_token` 接口本身也使用 Basic Auth |
| **Bearer Token** | 用户态 API（获取用户可见项目列表等） |

**Basic Auth 构造方法**：
```
1. 拼接: client_id + ":" + client_secret
2. BASE64 编码
3. 写入 Header: Authorization: Basic {base64_str}
```

> curl 简写: `curl -u 'client_id:client_secret' URL`

**Bearer Token 使用方法**：
```
Header: Authorization: Bearer {access_token}
```

### 1.3 通用请求参数（可选）

部分列表接口支持以下分页/过滤参数：

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `limit` | 否 | integer | 返回数量限制，默认 30，最大 200 |
| `page` | 否 | integer | 当前页码，默认 1 |
| `order` | 否 | string | 排序规则，如 `created%20desc` |
| `fields` | 否 | string | 指定返回字段，多个用逗号分隔 |

---

## 2. 接口详表

### 2.1 用户态 OAuth — 获取用户授权码

用于引导用户到 TAPD 授权页，获取一次性 code。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET（浏览器跳转） |
| **请求 URL** | `https://tapd.woa.com/oauth/` |

#### 请求参数（Query）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `response_type` | 是 | string | 固定 `code` |
| `client_id` | 是 | string | 应用 ID（需从开放平台应用管理获取） |
| `redirect_uri` | 是 | string | 回调地址，**必须在开放平台安全设置的白名单中，不能包含 #** |
| `scope` | 是 | string | 空格分隔的权限范围，例如 `story#read bug#read`。**需要 URL encode** |
| `state` | 是 | string | 防 CSRF 状态码，回调时原样带回；可携带自定义信息 |
| `auth_by` | 是 | string | 固定 `user` |

> **scope URL encode 示例**：`story#read bug#read` → `story%23read+bug%23read`

#### 请求示例

```
GET https://tapd.woa.com/oauth/?
    response_type=code
    &client_id=JnKeFzm1
    &redirect_uri=http%3A%2F%2Flion.oa.com%2F~anyechen%2Fcode%2Fphp%2Foauth_demo%2Fhey.php
    &scope=story%23read+bug%23read
    &state=random_string
    &auth_by=user
```

#### 授权流程

1. 用户在浏览器中打开上述 URL
2. 用户点击「同意授权」
3. TAPD 跳回 `redirect_uri`，携带以下 Query 参数：

| 返回参数 | 说明 |
|----------|------|
| `code` | 授权码，**有效期 5 分钟**，一次性使用 |
| `state` | 原样带回的透传参数 |
| `resource` | JSON 字符串，例如 `{"type":"user","user_id":"1001320052"}` |

#### 回调示例 URL

```
http://lion.oa.com/~anyechen/code/php/oauth_demo/hey.php?
    code=e09881835fc0a44c3bdabbbc091a1aa3f189554b
    &state=random_string
    &resource=%7B%22type%22%3A%22user%22%2C%22user_id%22%3A%221001320052%22%7D
```

---

### 2.2 用户态 OAuth — code 换取 access_token

使用授权码换取用户态 access_token。

| 项目 | 内容 |
|------|------|
| **请求方式** | POST |
| **请求 URL** | `http://apiv2.tapd.woa.com/tokens/request_token` |
| **认证方式** | **Basic Auth** — `Base64(client_id:client_secret)` |

#### 请求参数（POST Body，application/x-www-form-urlencoded）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `grant_type` | 是 | string | 固定 `authorization_code` |
| `redirect_uri` | 是 | string | 必须**与授权链接中传的 redirect_uri 完全一致** |
| `code` | 是 | string | 从回调 URL 中提取的 code |

#### 请求示例（curl）

```bash
curl -u "client_id:client_secret" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=http://lion.oa.com/~anyechen/code/php/oauth_demo/hey.php" \
  -d "code=e09881835fc0a44c3bdabbbc091a1aa3f189554b" \
  "http://apiv2.tapd.woa.com/tokens/request_token"
```

#### 返回参数

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

#### 返回示例

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

> ⚠️ **一期不存储 refresh_token**（评审结论 A1）。token 过期后重走 OAuth（一次廉价重定向）。

---

### 2.3 应用态 OAuth — 生成安装 URL（open_app_install）

引导用户到 TAPD 把应用安装到指定项目。对应本需求 B-01（生成 install_url）。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET（浏览器跳转） |
| **请求 URL** | `https://tapd.woa.com/oauth/open_app_install` |

#### 请求参数（Query）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `client_id` | 是 | string | 应用 ID |
| `cb` | 是 | string | 回跳 URL，需 URL encode，**必须在开放平台安全配置的三方应用数据授权白名单中，不含 #** |
| `state` | 是 | string | 透传参数。授权完成后原样带到回跳 URL。本设计将 `signed_state`（HMAC 签名串）作为 state，解决管理员跨账号问题。 |
| `test` | 是 | integer | 是否测试应用：`1` = 测试（应用未上架前），`0` = 正式（上架后） |
| `show_installed` | 否 | integer | `0` 不显示已授权项目（默认）；`1` 显示已授权项目 |

#### 请求示例

```
GET https://tapd.woa.com/oauth/open_app_install?
    test=1
    &client_id=oauth_demo
    &cb=http%3A%2F%2Flion.oa.com%2F%7Eanyechen%2Fcode%2Fphp%2Foauth_demo%2Fhey.php
    &show_installed=1
    &state=demo-product123
```

#### 授权流程

1. 浏览器打开上述 URL
2. 用户选择 TAPD 项目，点击「下一步」
3. 应用安装成功后，跳回 `cb` URL，携带以下参数：

| 返回参数 | 说明 |
|----------|------|
| `code` | 应用态授权码，**有效期 5 分钟** |
| `state` | 原样带回的透传参数 |
| `resource` | JSON 字符串，格式 `{"type":"workspace","workspace_id":"69990779"}` |

#### 回调示例 URL

```
http://lion.oa.com/~anyechen/code/php/oauth_demo/hey.php?
    code=4f9b2fab25a7c69715d426295a66717769666a0c
    &state=demo-product123
    &resource=%7B%22type%22%3A%22workspace%22%2C%22workspace_id%22%3A%2269990779%22%7D
```

> ⚠️ **注意**：`cb` 参数是整体 URL 编码后放入 query 的，参数本身也放在 query 而非 fragment 中，这样服务端能收到全部参数。

---

### 2.4 应用态 API — get_granted_workspaces

查询当前应用已授权安装的 TAPD 项目列表。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET |
| **请求 URL** | `http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces` |
| **认证方式** | **Basic Auth**（`client_id:client_secret`） |

#### 请求参数（Query）

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `workspace_id` | 否 | integer | 项目 ID。传入则精确查询该项目是否已授权 |
| `type` | 否 | integer | 安装类型：`0`=应用商店安装，`1`=测试安装，`2`=插件安装 |
| `created` | 否 | datetime | 创建时间，支持时间查询 |
| `limit` | 否 | integer | 返回数量限制，默认 30，最大 200 |
| `page` | 否 | integer | 页码，默认 1 |
| `order` | 否 | string | 排序规则，如 `created%20desc`。需 URL encode |
| `fields` | 否 | string | 指定返回字段，多个字段用逗号隔开 |

#### 请求示例（curl）

```bash
# 查询全部已授权项目（Basic Auth）
curl -u 'api_user:api_password' \
  'http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces'

# 查询指定项目是否已授权
curl -u 'api_user:api_password' \
  'http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces?workspace_id=10104801'
```

#### 返回参数

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | integer | 1 = 成功 |
| `data.list` | array | 授权记录列表 |
| `data.list[].OpenOrganizationApp.workspace_id` | string | 项目 ID |
| `data.list[].OpenOrganizationApp.type` | string | 安装类型：`0`商店/`1`测试/`2`插件 |
| `data.list[].OpenOrganizationApp.created` | string | 授权时间 `YYYY-MM-DD HH:MM:SS` |
| `data.pager.count` | integer | 总记录数 |
| `data.pager.page` | integer | 当前页 |
| `data.pager.limit` | integer | 每页条数 |
| `info` | string | 提示信息 |

#### 返回示例（全部）

```json
{
    "status": 1,
    "data": {
        "list": [
            {
                "OpenOrganizationApp": {
                    "workspace_id": "10104801",
                    "type": "1",
                    "created": "2024-04-02 16:10:30"
                }
            },
            {
                "OpenOrganizationApp": {
                    "workspace_id": "10093721",
                    "type": "1",
                    "created": "2023-06-15 20:00:15"
                }
            },
            {
                "OpenOrganizationApp": {
                    "workspace_id": "10028191",
                    "type": "1",
                    "created": "2023-06-15 20:00:13"
                }
            }
        ],
        "pager": {
            "count": 3,
            "page": 1,
            "limit": 30
        }
    },
    "info": "success"
}
```

#### 返回示例（单个项目）

```json
{
    "status": 1,
    "data": {
        "list": [
            {
                "OpenOrganizationApp": {
                    "workspace_id": "10104801",
                    "type": "1",
                    "created": "2024-04-02 16:10:30"
                }
            }
        ],
        "pager": {
            "count": 1,
            "page": 1,
            "limit": 30
        }
    },
    "info": "success"
}
```

> 💡 **本需求用途**：B-07 查询 app 已授权项目，作为 `is_bound` 四态中 `bound`/`stale` 状态的判定源。

---

### 2.5 业务 API — get_workspace_info

根据项目 ID 获取项目详细信息。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET |
| **请求 URL** | `http://apiv2.tapd.woa.com/workspaces/get_workspace_info` |
| **认证方式** | **Basic Auth**（复用现网 `TapdAPIResource`） |

#### 请求参数（Query）

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `workspace_id` | 是 | integer | 项目 ID |

#### 请求示例（curl）

```bash
curl -u 'api_user:api_password' \
  'http://apiv2.tapd.woa.com/workspaces/get_workspace_info?workspace_id=10104801'
```

#### 返回参数（data.Workspace 字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 项目 ID |
| `name` | string | 项目名称 |
| `pretty_name` | string | 项目英文昵称 |
| `category` | string | 项目类别 |
| `status` | string | 项目状态：`normal`=正常，`closed`=关闭，`suspend`=挂起 |
| `description` | string | 项目描述 |
| `begin_date` | string | 开始时间 |
| `end_date` | string | 结束时间 |
| `closed` | string | 关闭时间 |
| `external_on` | string | 是否开通外网 |
| `creator` | string | 项目创建者 |
| `created` | string | 创建时间 |
| `product_type` | string | 产品类型 |
| `platform_type` | string | 平台类型 |
| `is_self_development` | string | 是否自研：`1`=自研，`0`=合作 |
| `objective` | string | 项目目标 |
| `secrecy` | string | 是否保密：`1`=保密，`0`=非保密 |
| `schedule` | string | 项目进度 |
| `milestone` | string | 里程碑 |
| `risk` | string | 项目总体风险 |

#### 返回示例

```json
{
    "status": 1,
    "data": {
        "Workspace": {
            "id": "10104801",
            "name": "TAPD 乌云",
            "pretty_name": "tapd_security",
            "category": "product",
            "status": "normal",
            "description": "",
            "begin_date": null,
            "end_date": null,
            "external_on": "0",
            "creator": "",
            "created": "2015-03-27 16:02:02"
        }
    },
    "info": "success"
}
```

> 💡 **本需求用途**：B-03 应用态授权回调时，从 `resource["workspace_id"]` 获取 ID 后，调用本接口获取 `name`，写入 `TAPD_WORKSPACE_BINDING`。

> ⚠️ **注意**：本接口在现网已有封装（`bkmonitor/api/tapd/default.py` → `TapdAPIResource`），硬编码 app 级 Basic Auth，**设计应直接复用**。

---

### 2.6 用户态 API — 获取用户可见项目列表（推测）

> 本接口在现网已有封装（`fta_web/issue/resources.py:1302` → `ListTapdWorkspaceResource`），但官方文档未直接提供详情页。下面是根据现网代码和设计推断的规范。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET |
| **请求 URL** | `http://apiv2.tapd.woa.com/workspaces`（推测） |
| **认证方式** | **Bearer** `Authorization: Bearer {access_token}` |

#### 请求参数（Query，推测）

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `limit` | 否 | integer | 分页限制 |
| `page` | 否 | integer | 页码 |
| `order` | 否 | string | 排序规则 |

#### 返回值（推测）

| 字段 | 说明 |
|------|------|
| `status` | 1 = 成功 |
| `data.list` | 项目列表，包含 `Workspace` 对象 |
| `Workspace.id` | 项目 ID |
| `Workspace.name` | 项目名称 |
| `Workspace.pretty_name` | 英文昵称 |
| `Workspace.status` | 项目状态 |

> ⚠️ **实施前需与现网 `ListTapdWorkspaceResource` 代码对账确认**实际请求 URL、参数和返回字段。

> 💡 **本需求用途**：B-01 查询用户可见 TAPD 项目列表，返回 `install_url` + `is_bound` 四态标记。

---

## 3. 全量错误码

本需求流程涉及的所有 TAPD API 工作出错码：

| 错误码/HTTP状态 | 说明 | 排查建议 |
|----------------|------|----------|
| `401 Unauthorized` | 1. 未传账号密码 2. 账号密码错误 3. 代码问题 | 检查是否传了账号密码，核实是否正确 |
| `404 workspace 1010480 not existed` | 项目 ID 不存在或错误 | 核实项目 ID 是否正确和存在 |
| `403 api account xxx not allowed to access project 755` | 当前账号无权限访问项目 | 需要在开放平台中授权该项目 |
| `422` | 参数错误或必填参数未填写 | 参考提示语解决 |
| `429 To many requests` | 超过请求频率限制。默认 `6000req/10min`（约 25req/s） | 降低请求频率，增加缓存 |
| `500` | 服务器报错，通常由超大量请求超频引起 | 减少请求频率 |
| `502` | 1. 并发请求量太多 2. 单次返回数据量超大 | 问题1：降低并发。问题2：传 `limit` 分页 |
| `timeout` | 服务器请求超时 / 网络不通，常见于 IDC 机器 | 配置 host 解决；IDC 可用 `oss.apiv2.tapd.woa.com` 或指定 IP + Host header |

### OAuth 专项高频错误

| 错误提示 | 原因 | 解决 |
|----------|------|------|
| `invalid scope` | scope 参数权限未在应用权限中勾选 | 在开放平台勾选对应权限后**发布**应用 |
| `参数state不能为空` | state 参数为空 | 填入 state 参数 |
| `redirect_uri mismatch` | redirect_uri 与白名单不一致 | 修改使其完全一致（不含 `#`） |
| `The redirect URI is missing or do not match` | code 换 token 时 redirect_uri 与授权链接不一致 | 保持两处 redirect_uri 完全一致 |
| `The authorization code has expired` | code 已过期（超过 5 分钟） | 重新获取 code |

---

## 4. 认证与配置

### 4.1 认证方式对照表

| 场景 | 认证方式 | 凭据来源 | 说明 |
|------|----------|----------|------|
| code 换 access_token（用户态） | **Basic Auth** | `client_id:client_secret` | 应用级别凭证 |
| 调用用户态 API（如获取用户项目列表） | **Bearer Token** | `access_token`（用户态） | 每个用户独立 |
| 调用 app 级 API（`get_granted_workspaces` / `get_workspace_info`） | **Basic Auth** | `client_id:client_secret` | 应用级别，与用户无关 |

### 4.2 配置项（从环境变量 / 配置中心读取）

| 配置项 | 说明 | 是否敏感 |
|--------|------|:--------:|
| `TAPD_CLIENT_ID` | TAPD 应用 ID | 是 |
| `TAPD_CLIENT_SECRET` | TAPD 应用密钥 | 是 |
| `TAPD_OAUTH_BASE_URL` | OAuth 基地址，默认 `https://tapd.woa.com/oauth/` | 否 |
| `TAPD_API_BASE_URL` | API 基地址，默认 `http://apiv2.tapd.woa.com` | 否 |
| `TAPD_REDIRECT_URI` | OAuth 回调地址（白名单中） | 否 |

> **安全要求**：`TAPD_CLIENT_ID` 和 `TAPD_CLIENT_SECRET` 从环境变量或 Django settings（`local_settings` / 配置中心）读取，**禁止硬编码于代码中**。

---

## 5. 注意事项

### 5.1 限流策略

| 项目 | 说明 |
|------|------|
| `get_granted_workspaces` 分页 | 默认 30 条/页，最大 200 条/页，可传 `page` 翻页 |
| 全局限流 | 默认 `6000req/10min`（约 25req/s），超频返回 429/500 |
| 建议 | 实现侧加指数退避重试 + 本地缓存（`get_granted_workspaces` 缓存 TTL 建议 1-5 分钟） |

### 5.2 版本兼容性

| 项目 | 说明 |
|------|------|
| API 版本 | v2（`apiv2.tapd.woa.com`） |
| OAuth 版本 | TAPD 自定义 OAuth，非标准 RFC 6749 完整实现 |
| 注意点 | `request_token` 路径为 `/tokens/request_token`，非标准 `/token`；返回含外层 `status`/`data`/`info` |

### 5.3 回调安全

| 项目 | 说明 |
|------|------|
| redirect_uri 白名单 | 必须在 TAPD 开放平台「安全配置」中预先配置，**不支持 wildcard** |
| state 参数 | 用户态必填（防 CSRF）；应用态透传（本设计将 HMAC 签名串作为 state 解决跨浏览器问题） |
| code 有效期 | 5 分钟，一次性使用，过期需重新获取 |

### 5.4 风险点

| 风险 | 等级 | 说明 | 缓解措施 |
|------|------|------|----------|
| TAPD OAuth 服务不可用 | 中 | 外部服务，超时/拒绝服务 | 业务接口加 3-5s 超时 → 返回友好错误提示 → 记录日志 |
| token 有效期短（约 2h） | 低 | 用户态 token 过期频繁 | 删除 refresh_token 方案，过期重走 OAuth（一次廉价重定向） |
| client_secret 泄露 | 高 | Basic Auth 凭证被窃取 | 仅服务端使用；日志脱敏；配置中心存储 |
| API 返回字段变更 | 低 | 接口升级导致字段变动 | 防御性解析；关注官方文档 |
| 用户权限不足 | 低 | 用户无 TAPD 项目 | 返回空列表，前端友好提示 |

---

## 6. 现网已有封装（需复用）

| 现网文件 | 封装内容 | 复用建议 |
|----------|----------|----------|
| `bkmonitor/api/tapd/default.py` → `TapdAPIResource` | app 级 Basic Auth 客户端，含 `get_granted_workspaces`、`get_workspace_info`、建单资源 | **直接复用** `get_workspace_info` 和 `get_granted_workspaces`；新增接口可复用同一基类 |
| `fta_web/issue/resources.py:1302` → `ListTapdWorkspaceResource` | 用户态项目列表查询（B-01 前身） | **改名区分**：拆分为 `ListUserVisibleTapdWorkspaceResource`（Bearer）和 `ListGrantedTapdWorkspaceResource`（Basic） |

---

## 7. DEMO 验证（可选）

### 前置条件

```bash
# 1. 设置环境变量
export TAPD_CLIENT_ID="your_app_id"
export TAPD_CLIENT_SECRET="your_app_secret"
export TAPD_REDIRECT_URI="https://your-callback.com/callback"

# 2. 安装依赖
pip install requests
```

### 验证脚本模板

```python
# dependencies/verify/verify_tapd_api.py
import os
import base64
import requests

CLIENT_ID = os.environ.get("TAPD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TAPD_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("请设置 TAPD_CLIENT_ID 和 TAPD_CLIENT_SECRET 环境变量")

# 构造 Basic Auth headers
credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}

# 验证1: get_granted_workspaces
def test_get_granted_workspaces():
    url = "http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get("status") == 1:
            print(f"✅ get_granted_workspaces: {len(data['data']['list'])} 个已授权项目")
            return True
    except Exception as e:
        print(f"❌ get_granted_workspaces 失败: {e}")
        return False

# 验证2: get_workspace_info (需配置一个已知的 workspace_id)
def test_get_workspace_info(workspace_id=""):
    if not workspace_id:
        print("⚠️ 跳过 get_workspace_info（未提供 workspace_id）")
        return True
    url = f"http://apiv2.tapd.woa.com/workspaces/get_workspace_info?workspace_id={workspace_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get("status") == 1:
            print(f"✅ get_workspace_info: {data['data']['Workspace']['name']}")
            return True
    except Exception as e:
        print(f"❌ get_workspace_info 失败: {e}")
        return False

if __name__ == "__main__":
    print("🔍 TAPD API 连通性测试")
    test_get_granted_workspaces()
```

---

## 8. 官方文档索引

> 以下链接用于在需要时跳转到官方最新文档页，防止本归档内容过时。本文件以离线完整参考为主。

| 文档 | 链接 |
|------|------|
| 用户态授权文档 | `https://o.tapd.woa.com/document/api-doc/next/api/API调用说明书/授权凭证/用户态.html` |
| 应用态授权文档 | `https://o.tapd.woa.com/document/api-doc/next/api/API调用说明书/授权凭证/应用态.html` |
| TAPD OAuth 接入文档 | `https://o.tapd.woa.com/document/api-doc/API文档/TAPD%20OAuth%20%E6%8E%A5%E5%85%A5%E6%96%87%E6%A1%A3/` |
| get_granted_workspaces | `https://o.tapd.woa.com/document/api-doc/API文档/api_reference/workspace/get_granted_workspaces.html` |
| get_workspace_info | `https://o.tapd.woa.com/document/api-doc/API文档/api_reference/workspace/get_workspace_info.html` |
| API 错误码 | `https://o.tapd.woa.com/document/api-doc/next/api/API错误码.html` |
