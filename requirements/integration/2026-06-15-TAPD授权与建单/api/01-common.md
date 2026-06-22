---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-22
version: 1
tags: [integration, design, api]
author: AI
document_type: design
---

# 公共约定

> 本文档定义 TAPD 授权与建单相关 API 的公共约定，包括：URL 编码规则、响应格式、鉴权机制、路由组织。所有接口文档均继承本文档约定。

---

## 一、URL 编码规则

### 1.1 核心约定

**后端返回的 URL 链接，参数不进行 URL 编码，前端自行处理编码。**

| 场景 | 规则 | 示例 |
|------|------|------|
| 后端返回 URL | **不编码**，直接返回原始字符串 | `https://tapd.woa.com/oauth/authorize?client_id=bkmonitor_tapd&redirect_uri=https://monitor.bk.example.com/api/v4/issue/tapd/oauth_callback/&state=nonce123:2&scope=user_space` |
| 前端使用 URL | **自行编码**后使用（如 `encodeURIComponent`、`encodeURI`） | `encodeURIComponent(state)` |
| URL 中占位符 | 用 `{变量名}` 标记，前端替换后编码 | `https://tapd.woa.com/oauth/open_app_install?cb=https://monitor.bk.example.com/api/v4/issue/tapd/app_install_callback/?state={state}&sig={sig}` |

### 1.2 特殊字符处理

若 URL 参数值中存在 `&`、`=`、`?`、`#` 等特殊字符，后端在生成 URL 时需避免直接拼接这些值，而是通过**占位符**让前端填充后再自行编码：

```
// 错误：直接拼接未编码的 redirect_uri（其中含 ? 和 &)
redirect_uri=https://monitor.bk.example.com/api/v4/issue/tapd/oauth_callback/?a=1&b=2

// 正确：使用占位符
redirect_uri={redirect_uri}
```

### 1.3 install_url 格式

`install_url` 为 TAPD 应用安装页面 URL，格式为：
```
https://tapd.woa.com/oauth/open_app_install?client_id={app_id}&test=1#selected_workspace_id={workspace_id}
```

- `client_id` 和 `test` 由后端预写固定值
- 仅 `#selected_workspace_id={workspace_id}` 需前端替换为实际项目 ID
- 使用 `#fragment` 方式传递，`workspace_id` 不含需 URL 编码的字符

### 1.4 代码示例

#### 后端（Python）：生成未编码 URL

```python
def generate_auth_url(bk_biz_id: int, request) -> str:
    """生成 TAPD OAuth 授权 URL，返回未编码格式"""
    nonce = f"{request.user.username}:{secrets.token_urlsafe(8)}"
    state = f"{nonce}:{bk_biz_id}"

    # state 存入 Session
    request.session[f"tapd_oauth_state_{bk_biz_id}"] = state

    # 使用字符串拼接，不进行 urlencode
    return (
        f"https://tapd.woa.com/oauth/authorize"
        f"?client_id={settings.TAPD_APP_ID}"
        f"&response_type=code"
        f"&redirect_uri={settings.TAPD_OAUTH_CALLBACK_URL}"
        f"&scope=user_space"
        f"&state={state}"
    )
```

#### 前端（JavaScript）：使用前自行编码

```javascript
// 后端返回的 auth_url（未编码）
const authUrl = 'https://tapd.woa.com/oauth/authorize?client_id=bkmonitor_tapd&redirect_uri=https://monitor.bk.example.com/api/v4/issue/tapd/oauth_callback/&state=nonce123:2&scope=user_space';

// 方式一：直接跳转（浏览器会自动处理大部分编码）
window.location.href = authUrl;

// 方式二：替换占位符后再编码（针对含特殊字符的场景）
function buildInstallUrl(template, { state, sig, workspaceId }) {
    const url = template
        .replace('{state}', encodeURIComponent(state))
        .replace('{sig}', encodeURIComponent(sig))
        .replace('{workspace_id}', encodeURIComponent(workspaceId));
    return url;
}
```

---

## 二、响应格式

### 2.1 蓝鲸标准 Response Envelope

所有前端暴露接口（通过 `ResourceViewSet`）统一返回：

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
  "data": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `result` | boolean | 是否成功 |
| `code` | integer | HTTP 状态码（200/403/500 等） |
| `message` | string | 提示信息 |
| `data` | object/array/null | 业务数据 |

### 2.2 回调接口响应

TAPD 回调接口（B-03、B-05）返回 `302 Found` 重定向，**无 JSON 响应体**。

---

## 三、鉴权机制

### 3.1 前端暴露接口

| 鉴权层 | 方式 | 说明 |
|--------|------|------|
| **IAM** | `IAMPermission` | 校验蓝鲸业务权限（VIEW_EVENT / MANAGE_EVENT） |
| **TAPD_REQUIRED** | 自定义 Permission | 校验 Redis 中是否存有有效用户态 token（仅 B-01） |

### 3.2 TAPD 回调接口

| 接口 | 鉴权方式 | 说明 |
|------|----------|------|
| B-03 | `login_exempt` + `csrf_exempt` + 请求来源校验 | 无会话鉴权，通过 `request.state_querystring` 中的上下文参数校验来源一致性 |
| B-05 | `login_exempt` + `csrf_exempt` + Session state | 无会话鉴权，通过 Django Session 中的 state 比对防 CSRF |

> `login_exempt` 和 `csrf_exempt` 是 Django 装饰器，意味着这些接口不校验蓝盾登录态和 CSRF token。

---

## 四、路由组织

### 4.1 接口类型与注册位置

| 接口类型 | 路由注册位置 | 基类/视图 | URL 前缀 |
|----------|-------------|-----------|----------|
| **前端暴露接口** | `fta_web/issue/views.py` | `ResourceViewSet` + `ResourceRoute` | `/fta/issue/{endpoint}` |
| **TAPD 回调接口** | `kernel_api/views/v4/issue/callbacks.py` | Django `View`（函数视图） | `/api/v4/issue/tapd/{callback_endpoint}` |
| **内部 Resource 类** | `bkmonitor/api/tapd/*.py` | 继承 `APIResource`/`TapdAPIResource` | 内部调用，无外部 URL |

### 4.2 URL 路由规则

```
前端暴露接口：
  POST /fta/issue/issue/search          # 现有
  GET  /fta/issue/issue/detail          # 现有
  GET  /fta/issue/tapd/workspace        # B-07（原 POST → 改为 GET）
  GET  /fta/issue/tapd/user_workspace   # B-01（新增）

TAPD 回调接口：
  GET /api/v4/issue/tapd/app_install_callback/   # B-03（新增）
  GET /api/v4/issue/tapd/oauth_callback/         # B-05（新增）
```

---

## 五、WorkspaceItem 数据结构（四态）

所有返回 TAPD 项目列表的接口，item 结构统一：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspace_id` | `string` | 是 | TAPD 项目 ID |
| `workspace_name` | `string` | 是 | TAPD 项目名称 |
| `is_bound` | `string` | 是 | `bound`/`stale`/`importable`/`unbound` |

### 四态定义

| 状态 | 本地 binding | TAPD 授权 | 前端语义 |
|------|:-----------:|:---------:|----------|
| `bound` | ✓ | ✓ | 已关联，可建单 |
| `stale` | ✓ | ✗ | TAPD 侧已解绑，需重关联 |
| `importable` | ✗ | ✓ | TAPD 已授权，可一键关联 |
| `unbound` | ✗ | ✗ | 未关联，提供去关联入口 |

---

## 六、错误处理

**不使用自定义错误码体系**，统一复用蓝鲸平台标准 HTTP status + message。

| HTTP Code | 含义 | 典型场景 |
|-----------|------|----------|
| 200 | 成功 | 正常返回 |
| 403 | 禁止访问 | 未授权 TAPD、Token 过期、IAM 权限不足 |
| 500 | 服务器错误 | TAPD API 异常、DB 写入失败 |
| 302 | 重定向 | 回调接口成功/失败均重定向 |

---

## 七、版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建 |
