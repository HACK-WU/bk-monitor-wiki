# 错误码与排查指南

> 本需求流程涉及的所有 TAPD API 工作出错码。

---

## 1. 通用 HTTP 错误

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

---

## 2. OAuth 专项高频错误

| 错误提示 | 原因 | 解决 |
|----------|------|------|
| `invalid scope` | scope 参数权限未在应用权限中勾选 | 在开放平台勾选对应权限后**发布**应用 |
| `参数state不能为空` | state 参数为空 | 填入 state 参数 |
| `redirect_uri mismatch` | redirect_uri 与白名单不一致 | 修改使其完全一致（不含 `#`） |
| `The redirect URI is missing or do not match` | code 换 token 时 redirect_uri 与授权链接不一致 | 保持两处 redirect_uri 完全一致 |
| `The authorization code has expired` | code 已过期（超过 5 分钟） | 重新获取 code |
