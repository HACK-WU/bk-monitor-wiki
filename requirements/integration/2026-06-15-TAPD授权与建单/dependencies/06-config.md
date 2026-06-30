# 认证与配置

## 1. 认证方式对照表

| 场景 | 认证方式 | 凭据来源 | 说明 |
|------|----------|----------|------|
| code 换 access_token（用户态） | **Basic Auth** | `client_id:client_secret` | 应用级别凭证 |
| 调用用户态 API（如获取用户项目列表） | **Bearer Token** | `access_token`（用户态） | 每个用户独立 |
| 调用 app 级 API（`get_granted_workspaces` / `get_workspace_info`） | **Basic Auth** | `client_id:client_secret` | 应用级别，与用户无关 |

---

## 2. 配置项（从环境变量 / 配置中心读取）

| 配置项 | 说明 | 是否敏感 |
|--------|------|:--------:|
| `TAPD_CLIENT_ID` | TAPD 应用 ID | 是 |
| `TAPD_CLIENT_SECRET` | TAPD 应用密钥 | 是 |
| `TAPD_OAUTH_BASE_URL` | OAuth 基地址，默认 `https://tapd.woa.com/oauth/` | 否 |
| `TAPD_API_BASE_URL` | API 基地址，默认 `http://apiv2.tapd.woa.com` | 否 |
| `TAPD_REDIRECT_URI` | OAuth 回调地址（白名单中） | 否 |

> **安全要求**：`TAPD_CLIENT_ID` 和 `TAPD_CLIENT_SECRET` 从环境变量或 Django settings（`local_settings` / 配置中心）读取，**禁止硬编码于代码中**。

---

## 3. 限流策略

| 项目 | 说明 |
|------|------|
| `get_granted_workspaces` 分页 | 默认 30 条/页，最大 200 条/页，可传 `page` 翻页 |
| 全局限流 | 默认 `6000req/10min`（约 25req/s），超频返回 429/500 |
| 建议 | 实现侧加指数退避重试 + 本地缓存（`get_granted_workspaces` 缓存 TTL 建议 1-5 分钟） |

---

## 4. 版本兼容性

| 项目 | 说明 |
|------|------|
| API 版本 | v2（`apiv2.tapd.woa.com`） |
| OAuth 版本 | TAPD 自定义 OAuth，非标准 RFC 6749 完整实现 |
| 注意点 | `request_token` 路径为 `/tokens/request_token`，非标准 `/token`；返回含外层 `status`/`data`/`info` |

---

## 5. 回调安全

| 项目 | 说明 |
|------|------|
| redirect_uri 白名单 | 必须在 TAPD 开放平台「安全配置」中预先配置，**不支持 wildcard** |
| state 参数 | 用户态必填（防 CSRF）；应用态透传（本设计将 HMAC 签名串作为 state 解决跨浏览器问题） |
| code 有效期 | 5 分钟，一次性使用，过期需重新获取 |

---

## 6. 风险点

| 风险 | 等级 | 说明 | 缓解措施 |
|------|------|------|----------|
| TAPD OAuth 服务不可用 | 中 | 外部服务，超时/拒绝服务 | 业务接口加 3-5s 超时 -> 返回友好错误提示 -> 记录日志 |
| token 有效期短（约 2h） | 低 | 用户态 token 过期频繁 | 删除 refresh_token 方案，过期重走 OAuth（一次廉价重定向） |
| client_secret 泄露 | 高 | Basic Auth 凭证被窃取 | 仅服务端使用；日志脱敏；配置中心存储 |
| API 返回字段变更 | 低 | 接口升级导致字段变动 | 防御性解析；关注官方文档 |
| 用户权限不足 | 低 | 用户无 TAPD 项目 | 返回空列表，前端友好提示 |
