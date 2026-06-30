# 第三方依赖文档索引 — TAPD 开放平台 v2 API

> 需求：`REQ-20260615-001` TAPD 授权与建单
> 整理时间：2026-06-29（重构自原 `dependencies.md`）

---

## 快速导航

| 文档 | 内容 | 适用场景 |
|------|------|----------|
| [01-api-common.md](01-api-common.md) | 通用响应格式、认证方式、请求参数 | 接入任意 TAPD API 前必读 |
| [02-oauth-user.md](02-oauth-user.md) | 用户态 OAuth（授权码 → token） | B-05 用户态授权流程 |
| [03-oauth-app.md](03-oauth-app.md) | 应用态 OAuth（安装/卸载 URL） | B-01 install_url、B-03 回调、revoke_app_install |
| [04-workspace.md](04-workspace.md) | 项目查询 API | B-01 四态判定、B-03 获取项目名 |
| [05-error-codes.md](05-error-codes.md) | 全量错误码与排查建议 | 问题排查、日志设计 |
| [06-config.md](06-config.md) | 认证对照表、配置项清单 | 部署配置、安全审计 |
| [07-existing-code.md](07-existing-code.md) | 现网已有封装与复用建议 | 编码实施前必读 |

---

## 基地址速查

| 地址 | 说明 |
|------|------|
| API 基地址 | `http://apiv2.tapd.woa.com` |
| OAuth 基地址 | `https://tapd.woa.com/oauth/` |
| 开发者后台 | `https://o.tapd.woa.com/admin/myapps` |

---

## 认证方式速查

| 场景 | 认证方式 | 凭据 |
|------|----------|------|
| code 换 access_token（用户态） | Basic Auth | `client_id:client_secret` |
| 调用用户态 API | Bearer Token | `access_token` |
| 调用 app 级 API（workspace 相关） | Basic Auth | `client_id:client_secret` |

---

## 官方文档索引

| 文档 | 链接 |
|------|------|
| 用户态授权文档 | `https://o.tapd.woa.com/document/api-doc/next/api/API调用说明书/授权凭证/用户态.html` |
| 应用态授权文档 | `https://o.tapd.woa.com/document/api-doc/next/api/API调用说明书/授权凭证/应用态.html` |
| TAPD OAuth 接入文档 | `https://o.tapd.woa.com/document/api-doc/API文档/TAPD%20OAuth%20%E6%8E%A5%E5%85%A5%E6%96%87%E6%A1%A3/` |
| API 错误码 | `https://o.tapd.woa.com/document/api-doc/next/api/API错误码.html` |
