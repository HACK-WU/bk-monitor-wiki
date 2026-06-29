---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-22
updated: 2026-06-29
version: 2
tags: [integration, design, frontend, guide]
author: AI
document_type: frontend-guide
---

# 前端 API 集成指南：TAPD 授权与建单

> 基于 API 设计文档版本：v2（2026-06-29 修正版）
>
> 本指南面向前端开发者，描述如何在蓝鲸监控前端中集成 TAPD 项目关联授权流程。文档按用户操作场景拆分，不依赖后端设计文档，自包含完整。

---

## 1. API 清单

### 1.1 前端直接调用

| # | 接口 | 方法 | 路径 | 说明 | 详细文档 |
|---|------|------|------|------|----------|
| 1 | 查询用户可见 TAPD 项目列表 | `POST` | `/fta/issue/tapd/user_workspace/` | 冷启动去关联时展示 TAPD 项目及四态；Body 传 `bk_biz_id` + `success_url` + `error_url` | [load-tapd-workspaces.md](load-tapd-workspaces.md) |
| 2 | 解绑 TAPD 项目 | `POST` | `/fta/issue/tapd/workspace/unbind/` | 解除 TAPD 项目与当前业务的关联，仅删除本地 binding | [load-tapd-workspaces.md §解绑](load-tapd-workspaces.md) |

### 1.2 前端跳转（非 API 调用）

| # | 角色 | 说明 | 触发时机 |
|---|------|------|----------|
| 2 | OAuth 授权页 URL | 后端在 403 响应中返回的 `auth_url`，前端跳转即可 | 用户未授权 TAPD 或个人 Token 过期时 |
| 3 | 应用安装页 URL | 后端在 200 响应中返回的 `install_url`，前端替换占位符后跳转 | 用户点击「去授权」或「重新授权」按钮时 |

> 两个回调端点（TAPD 应用安装回调、TAPD OAuth 回调）均为 TAPD 调用后端，前端不直接调用，仅作为流程终点接收重定向。

---

## 2. 场景总览

| 场景 | 文档 | 前台角色 | 触发条件 | 核心动作 |
|------|------|---------|----------|---------|
| 加载 TAPD 项目列表 | [load-tapd-workspaces.md](load-tapd-workspaces.md) | 普通用户 | 进入去关联页面时页面加载 | 请求列表 → 按四态渲染 → 操作 |
| 解绑 TAPD 项目 | [load-tapd-workspaces.md](load-tapd-workspaces.md) | 有 MANAGE_EVENT 权限的用户 | 点击已关联项目的「解绑」按钮 | 发 POST 请求 → 后端删除本地 binding |
| TAPD 应用态授权安装 | [tapd-install-authorization.md](tapd-install-authorization.md) | 普通用户发起 / TAPD 管理员执行 | 列表中存在「未授权」或「授权失效」状态的项目 | 替换占位符 → `window.open` 打开安装页 → 管理员完成授权 → 页面回到监控 → 刷新列表 |
| TAPD 用户态 OAuth 授权 | [tapd-oauth-authorization.md](tapd-oauth-authorization.md) | 普通用户 | 列表接口返回 403，响应内含 `auth_url` | 跳转 TAPD OAuth → 回调后端 → 重定向到 success_url/error_url → 刷新列表 |

> 注意：以上三个场景在真实使用中可能交叉发生。例如冷启动加载列表时（场景一）可能同时触发 Token 过期（场景三），也可能触发应用态授权（场景二）。

---

## 3. 错误处理速查表

### 3.1 通用 HTTP 错误

| HTTP 状态码 | 触发场景 | 前端行为 |
|:----------:|----------|---------|
| 401 | 蓝鲸登录态过期 | 清除本地 token，跳转蓝鲸统一登录 |
| 403 | 未授权 TAPD（个人 Token 缺失或过期） | 显示授权引导弹窗，跳转 OAuth 授权页 |
| 403 | IAM 权限不足 | 提示「您没有权限访问该业务的 TAPD 关联功能」，禁用操作按钮 |
| 404 | 接口不存在 | 提示「功能正在升级，请稍后刷新」 |
| 429 | 请求过于频繁 | 提示「操作过于频繁，请稍后重试」 |
| 500 | TAPD API 异常或后端内部错误 | 提示「TAPD 服务暂时不可用，请稍后重试」，提供重试按钮 |

### 3.2 业务错误

| 错误场景 | HTTP 状态 | `message` | 前端行为 | 可恢复 |
|----------|----------|-----------|---------|-------|
| 个人 Token 缺失/过期 | 403 | "TAPD 用户态授权未生效" | 显示授权引导弹窗，跳转 `auth_url` 重走 OAuth | ✅ 是 |
| IAM 权限不足 | 403 | "权限不足" | 禁用所有操作，提示无权限 | ❌ 否 |
| TAPD API 异常 | 500 | "TAPD 服务暂时不可用，请稍后重试" | 显示错误提示 + 重试按钮 | ✅ 是 |
| 用户无 TAPD 项目 | 200 | "OK" | `items=[]`，显示空状态「暂无 TAPD 项目」 | ✅ 是 |

### 3.3 OAuth 回调处理

用户态授权回调重定向后，前端解析 URL query：

> **v2 变更**：B-05 OAuth 回调不再附加 `auth`/`reason` query 参数。成功时 302 重定向到 `success_url`（不含额外参数），失败时 302 重定向到 `error_url`（不含额外参数）。前端需**根据页面重新加载事件**（如 `window.onpageshow` / `document.visibilitychange`）判断是否需要刷新列表，而非解析 URL query。

用户态授权回调后，前端行为：

| 场景 | 前端表现 | 建议行为 |
|------|---------|---------|
| 页面加载且 URL 匹配 `success_url` | OAuth 成功结束 | 自动刷新项目列表 |
| 页面加载且 URL 匹配 `error_url` | OAuth 失败 | 提示「授权失败，请重试」并展示重试按钮 |

> 建议方式：在发起 OAuth 前将当前页面状态存入 sessionStorage（如 `{ oauthFlow: true, timestamp: Date.now() }`），页面从 `success_url` 或 `error_url` 返回时检测到该标记 + 时间戳在合理范围内（如 < 5 分钟），即可触发列表刷新。

应用态授权回调重定向后，前端解析 URL query：

| `tapd_bind` | `reason` | 含义 | 前端行为 |
|-------------|----------|------|---------|
| `success` | — | 应用安装成功，项目关联已写入数据库 | 提示「授权成功」，自动刷新项目列表 |
| `error` | `missing_resource` | 请求缺少项目信息 | 提示「授权信息不完整，请重试」 |
| `error` | `invalid_resource` | 项目 ID 无效 | 提示「项目不存在或已删除」 |
| `error` | `invalid_signed_state` | 授权链接的签名验证失败 | 提示「授权链接已失效，请重新获取」 |
| `error` | `signed_state_expired` | 授权链接签名已过期（超过 15 分钟） | 提示「授权链接已过期，请重新获取」 |
| `error` | `api_error` | TAPD API 异常 | 提示「TAPD 服务异常，请稍后重试」 |
| `error` | `db_error` | 数据库写入失败 | 提示「服务器内部错误，请稍后重试」 |

---

## 4. 关键数据结构

### 4.1 项目列表项

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `workspace_id` | `string` | 是 | TAPD 项目 ID |
| `workspace_name` | `string` | 是 | TAPD 项目名称 |
| `is_bound` | `string` | 是 | 四态标记：`bound` / `importable` / `stale` / `unbound` |

### 4.2 四态定义

| 状态值 | 含义 | 前端展示文案 | 颜色建议 | 可操作按钮               |
|--------|------|--------|---------|---------------------|
| `bound` | 该项目已关联监控业务，可直接建单 | 已关联    | 绿色 | 「已关联」（进入建单流程）       |
| `importable` | TAPD 已授权 · 后端自动关联中（若关联失败则返回此状态） | 去关联 | 蓝色 | 「去关联」（跳转应用安装页重新安装） |
| `stale` | TAPD 侧已解绑蓝鲸监控应用，关联已失效 | 去关联    | 橙色/黄色 | 「去关联」（跳转应用安装页重新安装）  |
| `unbound` | 该项目在 TAPD 上未授权蓝鲸监控 | 去关联    | 灰色 | 「去关联」（跳转应用安装页重新安装）  |

---

## 5. 注意事项

### 5.1 URL 编码规则

| 字段 | 编码责任方 | 前端操作 |
|------|-----------|---------|
| `auth_url` | 前端 | 后端返回裸字符串，直接跳转即可，浏览器自动处理编码 |
| `install_url` | 后端（`cb` 参数已编码）+ 前端（替换占位符） | `{workspace_id}` 占位符直接替换填入即可，无需额外编码处理 |

### 5.2 需要前端维护的本地状态

| 状态 | 位置建议 | 说明 |
|------|---------|------|
| `bk_biz_id` | URL query 或状态管理 | 当前业务 ID，所有列表请求必传 |
| `is_requesting` | 组件内部 | 请求中锁，防止重复请求 |
| `last_grant_time` | localStorage（可选） | 记录最后一次完成 OAuth 授权的时间戳，用于判断是否需要主动刷新 |

### 5.3 无 Token 异步刷新机制

一期**不实现**个人 Token 的异步后台刷新。Token 过期后由后端自动淘汰（Redis TTL），下次请求列表接口返回 403，前端引导用户重新走 OAuth 授权。评审结论：Token 刷新机制比例失衡，一次重定向成本低，无需复杂异步任务。

### 5.4 install_url 使用条件

`install_url` 仅在以下情况返回：列表中存在 `is_bound = stale` 或 `is_bound = unbound` 的项目。如果全部 `bound` / `importable`，该字段为空或不返回。

前端判断：遍历项目列表，若存在至少一个项目的 `is_bound` 为 `unbound` 或 `stale`，则需要展示授权引导。

### 5.5 跨浏览器/跨账号授权场景

管理员不一定在发起用户的浏览器中登录蓝鲸。`install_url` 中包含的签名状态串已内嵌真实发起人信息，即使管理员在别的浏览器或别的账号中完成应用安装授权，最终关联记录仍正确归属为原始发起人。前端只需正常跳转 `install_url`，无需额外处理。

---

## 6. 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建 |
| 2 | 2026-06-29 | AI | B-01 接口由 GET 改为 POST，参数改为 `success_url`/`error_url`；B-05 OAuth `state` 改用自包含 signed_state，回调不再附加 `auth`/`reason` 参数；新增 B-04 解绑接口；OAuth 错误处理改为 sessionStorage 标记判断 |
