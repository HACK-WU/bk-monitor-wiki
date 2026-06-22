---
id: REQ-20260615-001
feature: TAPD授权与建单
created: 2026-06-22
version: 1
tags: [integration, design, frontend, guide]
author: AI
document_type: frontend-guide
---

# 场景：加载 TAPD 项目列表

> 所属功能：TAPD 授权与建单 —— 关联 TAPD 项目
> 角色：普通用户 / 蓝鲸监控业务管理员
> 前置条件：用户已在告警处理页点击「创建单据」→ 选择「TAPD 单据」，触发授权状态检查
>
> **对应 UI 设计稿**：见 [ui-mockup.md](../ui-design/ui-mockup.md) P-03「关联 TAPD 项目列表页」

---

## 简要的调用流程图

用户进入此页面前，授权状态检查可能已发现以下情况，但**本场景仅处理列表接口调用本身**：

```mermaid
flowchart TD
    A["页面加载<br>GET /fta/issue/tapd/user_workspace/"] --> B{HTTP 状态}

    B -->|200| C[渲染项目卡片列表]
        C --> D{is_bound}
        D -->|bound| E["展示 已关联<br>【查看】→ 进入建单"]
        D -->|importable| F["展示 TAPD 侧已安装应用，可一键导入<br>【一键导入】→ 走绑定+建单"]
        D -->|stale| G["展示 TAPD 侧已解绑，需重新关联<br>【重新关联】→ 打开 install_url"]
        D -->|unbound| H["展示 用户态授权已拉取，需完成蓝鲸监控关联项目授权<br>【去关联】→ 打开 install_url"]

    B -->|403 + auth_url| I["展示 OAuth 授权引导弹窗<br>跳转 TAPD OAuth 授权页"]
    B -->|403 + 无 auth_url| J["展示 权限不足 提示<br>禁用所有操作"]
    B -->|401| K["清除登录态<br>跳转蓝鲸统一登录"]
    B -->|500| L["展示 TAPD 服务异常<br>提供重试按钮"]
```

---

## 调用序列

### 步骤 1：页面加载，请求 TAPD 项目列表

→ 触发时机：去关联页面（P-03）生命周期挂载时
→ 调用接口：`GET /fta/issue/tapd/user_workspace/`
→ 请求参数：

```json
{
  "bk_biz_id": 2,
  "page": 1,
  "page_size": 20
}
```

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|:----:|:------:|------|
| `bk_biz_id` | `integer` | 是 | — | 蓝鲸业务 ID，从当前 URL 或状态管理中读取 |
| `page` | `integer` | 否 | 1 | 页码，必须 ≥ 1 |
| `page_size` | `integer` | 否 | 20 | 每页数量，范围 1~100 |

→ 成功响应（HTTP 200）：

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
  "data": {
    "total": 42,
    "items": [
      {
        "workspace_id": "69990779",
        "workspace_name": "IEG-登录服务",
        "is_bound": "bound"
      },
      {
        "workspace_id": "69990780",
        "workspace_name": "平台中台",
        "is_bound": "importable"
      },
      {
        "workspace_id": "69990781",
        "workspace_name": "游戏运营平台",
        "is_bound": "stale"
      },
      {
        "workspace_id": "69990782",
        "workspace_name": "新项目",
        "is_bound": "unbound"
      }
    ],
    "has_more": true,
    "install_url": "https://tapd.woa.com/oauth/open_app_install?client_id=bkmonitor_tapd&test=1&cb=https%3A%2F%2Fmonitor.example.com%2Fapi%2Fv4%2Fissue%2Ftapd%2Fapp_install_callback%2F%3Fsigned_state%3DeyJ4e...#selected_workspace_id={workspace_id}",
    "method": "GET"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | `integer` | 项目总数（不分页统计） |
| `items` | `WorkspaceItem[]` | 项目列表，按四态标记 |
| `has_more` | `boolean` | 是否还有更多数据 |
| `install_url` | `string`（可能缺失） | 当列表中存在 `stale` 或 `unbound` 项目时返回，否则为空或不返回 |
| `method` | `string` | `install_url` 的请求方式，固定为 `GET` |

→ 成功后：按 `is_bound` 四态渲染每个项目的操作按钮

→ 失败响应示例：

**403 — 个人 Token 缺失/过期（含 `auth_url`）**

```json
{
  "result": false,
  "code": 403,
  "message": "TAPD 用户态授权未生效",
  "data": {
    "auth_url": "https://tapd.woa.com/oauth/authorize?client_id=bkmonitor_tapd&response_type=code&redirect_uri=https%3A%2F%2Fmonitor.example.com%2Fapi%2Fv4%2Fissue%2Ftapd%2Foauth_callback%2F&scope=user_space&state=nonce123:2",
    "auth_method": "session"
  }
}
```
→ 含 `auth_url` 字段，前端需展示 OAuth 授权引导弹窗（见 ui-mockup.md P-02），点击跳转 `auth_url`。

**403 — IAM 权限不足（无 `auth_url`）**

```json
{
  "result": false,
  "code": 403,
  "message": "权限不足"
}
```
→ 无 `auth_url` 字段，前端展示「您没有权限访问该业务的 TAPD 关联功能」，禁用所有操作按钮。

**401 — 蓝鲸登录态过期**

```json
{
  "result": false,
  "code": 401,
  "message": "用户未登录或登录态已过期"
}
```
→ 清除本地 token，跳转蓝鲸统一登录页。

**500 — TAPD API 异常或后端内部错误**

```json
{
  "result": false,
  "code": 500,
  "message": "TAPD 服务暂时不可用，请稍后重试"
}
```
→ 展示错误提示 + [重试] 按钮。

> **关键：区分两种 403** —— 响应体中是否包含 `auth_url` 字段。含 `auth_url` = Token 过期需重新 OAuth；不含 `auth_url` = IAM 权限不足无操作权限。

---

### 步骤 2：按项目四态渲染可操作按钮

每个项目根据其 `is_bound` 值展示不同的**状态文案**和**操作按钮**。

状态文案与操作按钮严格对应 UI 设计稿 P-03：

| `is_bound` | 状态文案（灰色小字） | 操作按钮 | 按钮行为 | 对应 UI 设计稿 |
|------------|---------------------|---------|---------|--------------|
| `bound` | 已关联 | [查看] | 点击进入 TAPD 建单流程（调用已有接口，不在本文档范围内） | P-03 |
| `importable` | TAPD 侧已安装应用，可一键导入 | [一键导入] | 先完成绑定，再进入建单流程 ⚠️ **当前缺少绑定接口，见 [../TODO-待办事项.md](../TODO-待办事项.md)** | P-03 |
| `stale` | TAPD 侧已解绑，需重新关联 | [重新关联] | 打开 `install_url`（替换 `{workspace_id}` 后以新窗口打开），让 TAPD 管理员重新授权安装 | P-03 |
| `unbound` | 用户态授权已拉取 · 需完成蓝鲸监控关联项目授权 | [去关联] | 打开 `install_url`（替换 `{workspace_id}` 后以新窗口打开），让 TAPD 管理员完成首次授权安装 | P-03 |

→ 前端布局参考（来自设计稿）：

```

┌──────────────────────────────────────────┐
│  游戏运营平台                               │
│  用户态授权已拉取 · 需完成蓝鲸监控关联项目授权 │
│                                   [去关联]  │
└──────────────────────────────────────────┘

全部卡片以列表形式纵向排列，每项之间有间距。
```

→ 按钮显示条件：
- `stale` / `unbound` 的按钮仅在 `install_url` 字段存在时展示；若 `install_url` 不存在（全部项目都是 `bound` / `importable`），这两个状态的项目可仅显示文字提示，不提供跳转按钮
- `importable` 的 [一键导入] 按钮当前不可点击或点击后提示「功能开发中」，待绑定接口补充后再实现

---

## 空状态

| 条件 | 前端行为 | 对应 UI |
|------|---------|---------|
| `items` 为空数组 | 展示「暂无 TAPD 项目」 | P-03 空白态 |
| `install_url` 不存在 | 不展示「去关联」引导区（全部项目已处于 `bound` 或 `importable` 状态） | — |
| `total === 0` | 隐藏分页组件 | — |

---

## 失败态（参考 ui-mockup.md P-02）

| 场景 | 前端展示 | 交互 |
|------|---------|------|
| 403 + `auth_url` | 弹窗：「蓝鲸监控需要先拉取您在 TAPD 有权限的项目列表」+ [同意授权并拉取项目] [取消授权] | 点击主按钮跳转 TAPD OAuth |
| 403 + 无 `auth_url` | 页面内区域：「您没有权限访问该业务的 TAPD 关联功能」，所有卡片置灰，操作按钮禁用 | 用户无法继续操作 |
| 401 | 统一登录页 | 登录后返回 |
| 500 | 页面内区域：「TAPD 服务暂时不可用，请稍后重试」+ [重试] 按钮 | 点击重试重新请求列表 |

---

## 常见问题

### Q1：`importable` 状态的「一键导入」与 `bound` 状态的「查看」有什么区别？

`bound`：该项目已完成与当前蓝鲸监控业务的绑定，且 TAPD 侧应用授权有效，点击 [查看] 直接进入建单流程。

`importable`：TAPD 侧已授权蓝鲸监控应用，但本地 `TapdWorkspaceBinding` 表中没有与当前 `bk_biz_id` 的绑定记录。点击 [一键导入] 后需要先在本地创建绑定记录，然后再进入建单流程。

> ⚠️ **已知问题**：当前 API 设计中缺少独立的「创建绑定」接口。详见 [../TODO-待办事项.md](../TODO-待办事项.md) —— **待后续迭代补充绑定接口设计后，本文档将同步更新**。在前端预留 `importable` 状态的处理逻辑即可。

### Q2：为什么 `stale` / `unbound` 的项目按钮文案是「重新关联」/「去关联」，而不是「重新授权」/「去授权」？

这是 UI 设计稿中的统一用词。`stale` 的「重新关联」和 `unbound` 的「去关联」都指的是**在 TAPD 平台内完成应用安装授权**，让 TAPD 侧允许蓝鲸监控应用访问该项目。操作本身都是打开 `install_url` 跳转到 TAPD 安装页，由管理员完成。文案差异仅反映状态语义（首次关联 vs 重新关联）。

### Q3：`install_url` 什么时候有、什么时候没有？

当用户可见的 TAPD 项目列表中，包含至少一个 `stale` 或 `unbound` 状态的项目时，后端在响应中会返回 `install_url`。如果全部项目都是 `bound` 或 `importable` 状态，`install_url` 字段为空或不返回。

### Q4：列表加载后，用户点击 [重新关联] 或 [去关联]，授权完成后页面如何刷新？

安装授权完成后，TAPD 会回调后端，后端 302 重定向回到监控前端页面。前端页面加载时，应检测 URL 是否带有 `tapd_bind=success` 参数。若带此参数，说明授权刚完成，自动重新请求列表接口刷新状态。之前 `stale` / `unbound` 的项目应变为 `bound` 状态，按钮文案从 [重新关联]/[去关联] 变为 [查看]。
