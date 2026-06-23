---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-22
version: 1
tags: [integration, design, api]
author: AI
document_type: api-overview
---

# API 设计文档总览

> 所有后端 API 接口的入口索引。设计阶段产物，供 Stage 2 技术评审及开发时快速定位。
>
> 阅读前请先查看 `01-common.md`，其中包含 HTTP Method、URL 编码规则、响应格式等公共约定。

---

## 接口一览

| 编号 | 名称 | 文件 | 端点 | 方法   | 鉴权 | 用途 |
|------|------|------|------|------|------|------|
| B-01 | 查询用户可见 TAPD 项目列表 | [02-user-workspace.md](02-user-workspace.md) | `/fta/issue/tapd/user_workspace/` | GET  | `TAPD_REQUIRED` + IAM | 冷启动去关联下拉 |
| B-07 | 查询 app 已授权 TAPD 项目列表 | [03-granted-workspace.md](03-granted-workspace.md) | `/fta/issue/tapd/workspace/` | POST | 日常建单下拉（**已有/无变更**） |
| B-03 | 应用态授权回调 | [04-app-install-callback.md](04-app-install-callback.md) | `/fta/issue/tapd/app_install_callback/` | GET  | 请求来源校验 | 管理员安装后 TAPD 回调 |
| B-05 | 用户态授权回调 | [05-oauth-callback.md](05-oauth-callback.md) | `/fta/issue/tapd/oauth_callback/` | GET  | Session state | 用户 OAuth 后 TAPD 回调 |

> B-02 / B-04 / B-06 为后台内部 Resource 类定义，不在`.路由中暴露为独立端点，见 [06-resource-classes.md](06-resource-classes.md)。

---

## 文档文件映射

```
api/
├── 00-api-overview.md          # ← 本文档：总览索引
├── 01-common.md                 # 公共约定：URL编码、响应格式、鉴权、路由、四态
├── 02-user-workspace.md          # B-01 查询用户可见 TAPD 项目
├── 03-granted-workspace.md       # B-07 查询 app 已授权 TAPD 项目
├── 04-app-install-callback.md    # B-03 应用态授权回调
├── 05-oauth-callback.md          # B-05 用户态授权回调
└── 06-resource-classes.md        # B-02/B-04/B-05/B-06 内部 Resource 类定义
```

---

## 核心约束速查

| 约束项 | 规则 | 出处 |
|--------|------|------|
| **URL 编码** | 后端返回 URL 字符串**不进行编码**，前端自行处理 | 01-common.md |
| **错误码** | 不使用自定义 `error_code`，复用 HTTP status + `message`| 01-common.md |
| **install_url** | 后端预写固定 URL，仅 `#selected_workspace_id={workspace_id}` 需前端替换 | 02-user-workspace.md |
| **Session State** | OAuth `state` 存 Django Session，回调比对后删除防重放 | 05-oauth-callback.md |
| **Token 存储** | AESCipher 加密后存 Redis，key=`tapd_uat:{tenant}:{user}`，TTL=7200s | 05-oauth-callback.md |
| **IV 安全** | `AESCipher`**禁止传固定 IV**，每次随机生成 | 05-oauth-callback.md |
| **回调响应** | B-03 / B-05 均返回 **302 重定向**，无 JSON 响应体 | [04-app-install-callback.md](04-app-install-callback.md)、[05-oauth-callback.md](05-oauth-callback.md) |
| **四态标记** | `bound`/`stale`/`importable`/`unbound`，交叉查询本地 + TAPD | [02-user-workspace.md](02-user-workspace.md)、[03-granted-workspace.md](03-granted-workspace.md) |
| **鉴权方式** | B-03：`signed_state` HMAC 验签；B-05：Session 比对；B-07：仅 IAM | 各子文档 |

---

## 接口依赖关系

```
B-01 用户可见项目列表
  ├── Redis: tapd_uat:{tenant}:{user}（B-05 写入）
  ├── TapdUserAPIResource（B-06）→ Bearer Token 调用 TAPD 用户态 API
  ├── GetGrantedWorkspacesResource（B-02）→ Basic Auth 获取已授权项目
  └── compute_bound_status() → 交叉标记四态

B-07 app 已授权项目列表
  ├── GetGrantedWorkspacesResource（B-02）→ Basic Auth
  └── 查本地 TapdWorkspaceBinding → 标记四态

B-03 应用态授权回调
  ├── request.state_querystring → 提取上下文参数校验来源
  ├── GetWorkspaceInfoResource（B-04）→ Basic Auth 获取项目信息
  └── TapdWorkspaceBinding.upsert → 幂等写入

B-05 用户态授权回调
  ├── Session: tapd_oauth_state_{bk_biz_id}（B-01 写入）
  ├── RequestTokenResource（B-05）→ code 换 access_token
  ├── AESCipher → Token 加密
  └── Redis: setex tapd_uat:{tenant}:{user} → Token 存储
```

---

## 关键参数来源

| 参数 | 来源文件 | 获取方式 |
|------|----------|----------|
| `client_id` | `fta_settings.TAPD_APP_ID` | 配置项 |
| `client_secret` | `fta_settings.TAPD_APP_SECRET` | 配置项 |
| `SECRET_KEY` | Django `settings.SECRET_KEY` | AESCipher 密钥（B-05 Token 加密）|
| `redirect_uri` | `fta_settings.SAAS_OAUTH_CALLBACK_URL` | 配置项 |
| `bk_tenant_id` | `request.any_source("bk_tenant_id")` | 框架轮询获取 |

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建 |
