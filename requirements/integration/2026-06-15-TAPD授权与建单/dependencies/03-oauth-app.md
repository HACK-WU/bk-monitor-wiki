# 应用态 OAuth

> 应用态 OAuth 用于将开放平台应用安装到指定 TAPD 项目，获取 app 级 Basic Auth 权限。
> 与本需求相关：B-01 生成 `install_url`、B-03 应用态回调、`revoke_app_install` 卸载。

---

## 前置步骤

1. **创建开放平台应用**：在 [开发者后台](https://o.tapd.woa.com/admin/myapps) 创建应用，配置所需接口权限，获取 **应用 ID（`client_id`）** 和 **应用密钥（`client_secret`）**。
2. **配置 OAuth 跳转链接**：在开放平台应用「安全配置」→ 「三方应用数据授权」中添加回调 URL 白名单，可添加多个。**回调 URL 不能包含 `#`**。

---

## 1. open_app_install — 生成安装 URL

| 项目 | 内容 |
|------|------|
| **请求方式** | GET（浏览器跳转） |
| **请求 URL** | `https://tapd.woa.com/oauth/open_app_install` |

### 请求参数（Query）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `client_id` | 是 | string | 应用 ID（从开放平台应用管理获取） |
| `cb` | 是 | string | 回跳 URL，**必须在白名单中**，**不能包含 `#`**，需要 URL encode |
| `state` | 是 | string | 透传参数。授权完成后原样带到回跳 URL。本设计将 `signed_state`（HMAC 签名串）作为 state，解决管理员跨账号问题。 |
| `test` | 是 | integer | `1` = 测试应用（应用**未上架前**固定传 1）；`0` = 正式应用（上架后改为 0） |
| `show_installed` | 否 | integer | `0` 不显示已授权项目（默认）；`1` 显示已授权项目 |

### 请求示例

```
GET https://tapd.woa.com/oauth/open_app_install?
    test=1
    &client_id=oauth_demo
    &cb=http%3A%2F%2Flion.oa.com%2F%7Eanyechen%2Fcode%2Fphp%2Foauth_demo%2Fhey.php
    &show_installed=1
    &state=demo-product123
```

### 授权流程

1. 浏览器打开上述拼接好的 URL
2. 页面展示用户有权限的项目列表，用户选择目标项目，点击「下一步」
3. 应用安装成功后，跳回 `cb` 配置的回调 URL，携带以下 Query 参数：

| 返回参数 | 说明 |
|----------|------|
| `code` | 应用态授权码，**有效期 5 分钟**，一次性使用 |
| `state` | 原样带回的透传参数 |
| `resource` | JSON 字符串，格式 `{"type":"workspace","workspace_id":"69990779"}`。注意：返回的 `resource` 会带上本次授权的项目 ID `workspace_id` |

> ⚠️ **注意**：回调 URL 中 `resource` 参数可能出现重复（如 `resouce` 和 `resource` 同时出现），实际解析时取 `resource` 即可。

### 回调示例 URL

```
http://lion.oa.com/~anyechen/code/php/oauth_demo/hey.php?
    code=4f9b2fab25a7c69715d426295a66717769666a0c
    &state=demo-product123
    &resource=%7B%22type%22%3A%22workspace%22%2C%22workspace_id%22%3A%2269990779%22%7D
```

> ⚠️ **`cb` 参数注意**：`cb` 是整体 URL 编码后放入 query 的，参数本身也放在 query 而非 fragment 中，这样服务端能收到全部参数。

---

## 2. revoke_app_install — 取消应用授权（卸载）

> ⚠️ **来源说明**：本接口信息来自 FE 团队，尚未在 TAPD 官方文档中确认，**标记为待验证**。实施前需与 FE 对齐具体参数和返回结构。

> 本接口用于取消应用对指定 TAPD 项目的授权（即从项目中卸载应用），与 `open_app_install` 互为反向操作。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET（浏览器跳转） |
| **请求 URL** | `https://tapd.woa.com/oauth/revoke_app_install` |

### 请求参数（Query）

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `client_id` | 是 | string | 应用 ID |
| `cb` | 是 | string | 回跳 URL，**必须在白名单中**，**不能包含 `#** |
| `state` | 是 | string | 透传参数 |
| `test` | 是 | integer | `1` 测试应用 / `0` 正式应用（同 `open_app_install`） |
| `workspace_ids` | 否 | string | 要卸载的项目 ID 列表，多个用逗号分隔。不传则展示全部已授权项目供选择 |

### 预期回调

卸载完成后，TAPD 跳回 `cb` 地址，携带：

| 返回参数 | 说明 |
|----------|------|
| `state` | 原样带回 |
| `resource` | JSON 字符串，含 `type` 和 `workspace_id`，表示被卸载的项目 |

### 注意事项

- 卸载后，调用 `get_granted_workspaces` 应查询不到该项目，可作为验证手段。
- 卸载不影响本地 `TapdWorkspaceBinding` 记录，需要在回调中同步删除。
- **待确认项**：
  - `workspace_ids` 参数是否支持预填（不展示选择页直接卸载）
  - 卸载多项目时 `resource` 格式（单个 vs 数组）
  - 是否也返回 `code`（应用态授权码）还是仅返回操作结果

---

## 3. 授权成功后调用业务 API

应用态 OAuth 授权完成（获取 `code`）后，**后续调用所有业务 API 均使用 Basic Auth 认证**：

```bash
# 使用 client_id:client_secret 调用任意已授权项目的数据接口
curl -u 'client_id:client_secret' \
  'http://apiv2.tapd.woa.com/bugs/count?workspace_id=69990779'
```

| 阶段 | 认证方式 | 凭据 | 说明 |
|------|----------|------|------|
| 生成安装 URL / 回调 | 无（浏览器跳转） | — | 用户浏览器与 TAPD 交互 |
| 调用业务 API | **Basic Auth** | `client_id:client_secret` | 应用级凭证，与具体用户无关 |
