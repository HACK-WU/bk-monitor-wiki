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

# B-01 查询用户可见 TAPD 项目列表

> 前端暴露接口，用于冷启动去关联时展示用户有权限的 TAPD 项目。
> 继承 `common.md` 中的所有公共约定。

---

## 基础信息

| 属性 | 值 |
|------|-----|
| **接口名称** | 查询用户可见 TAPD 项目列表 |
| **端点** | `/fta/issue/tapd/user_workspace/` |
| **方法** | `GET` |
| **Resource 类** | `ListUserVisibleTapdWorkspaceResource` |
| **所在模块** | `fta_web/issue/resources.py` |
| **权限** | `permission_classes = [TAPD_REQUIRED, IAMPermission]` |
| **IAM Action** | `ActionEnum.VIEW_EVENT` |

---

## Request

### Query 参数

| 字段 | 类型 | 必填 | 默认值 | 约束 |
|------|------|------|--------|------|
| `bk_biz_id` | `integer` | 是 | — | 正整数 |
| `page` | `integer` | 否 | 1 | ≥ 1 |
| `page_size` | `integer` | 否 | 20 | 1~100 |

### 请求示例

```http
GET /fta/issue/tapd/user_workspace/?bk_biz_id=2&page=1&page_size=20
```

---

## 权限前置：TAPD_REQUIRED

```python
class TAPD_REQUIRED(BasePermission):
    """校验用户是否持有有效 TAPD 用户态 token"""

    def has_permission(self, request, view) -> bool:
        # 1. 从 request.user 提取 username，从 tenant 上下文提取 bk_tenant_id
        # 2. Redis: get tapd_uat:{bk_tenant_id}:{username}
        # 3. key 存在 → 解密 token → 校验过期时间 → True
        # 4. key 不存在或过期 → 内部生成 auth_url → raise PermissionDenied
        raise PermissionDenied(
            detail={
                "auth_url": generate_auth_url(bk_biz_id, request),
                "auth_method": "session"
            }
        )
```

### auth_url 生成规则

```
https://tapd.woa.com/oauth/authorize
  ?client_id={settings.TAPD_APP_ID}
  &response_type=code
  &redirect_uri={settings.TAPD_OAUTH_CALLBACK_URL}
  &scope=user_space
  &state={nonce}:{bk_biz_id}
```

- `redirect_uri` 和 `state` **不进行 URL 编码**，前端自行处理
- `state` 格式：`{username}:{随机串}:{bk_biz_id}`
- `state` 连同完整值存入 `request.session[f'tapd_oauth_state_{bk_biz_id}']`

---

## Response

### 成功（200）

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
        "workspace_name": "蓝鲸监控项目",
        "is_bound": "bound"
      },
      {
        "workspace_id": "69990780",
        "workspace_name": "运维自动化项目",
        "is_bound": "importable"
      },
      {
        "workspace_id": "69990781",
        "workspace_name": "测试项目",
        "is_bound": "stale"
      }
    ],
    "has_more": true,
    "install_url": "https://tapd.woa.com/oauth/open_app_install?client_id=bkmonitor_tapd&test=1&cb=https%3A%2F%2Fmonitor.bk.example.com%2Ffta%2Fissue%2Ftapd%2Fapp_install_callback%2F%3Fsigned_state%3DeyJia19iaXpfaWQiOjIsInRlbi4uLn0.WzG4x#selected_workspace_id={workspace_id}"
  }
}
```

#### data 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | `integer` | 项目总数（不分页统计） |
| `items` | `WorkspaceItem[]` | 项目列表（见下方结构） |
| `has_more` | `boolean` | 是否还有更多数据 |
| `install_url` | `string` | 当列表中存在 `unbound` 或 `stale` 项目时返回，前端替换占位符后使用 |
| `method` | `string` | `install_url` 的请求方式，固定 `GET` |

#### WorkspaceItem 结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `workspace_id` | `string` | TAPD 项目 ID |
| `workspace_name` | `string` | TAPD 项目名称 |
| `is_bound` | `string` | `bound`/`stale`/`importable`/`unbound`（四态） |

### 用户无 TAPD 项目（200）

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
  "data": {
    "total": 0,
    "items": [],
    "has_more": false
  }
}
```

> 前端展示空状态「暂无 TAPD 项目」。

### 未授权 / Token 过期（403）

```json
{
  "result": false,
  "code": 403,
  "message": "TAPD 用户态授权未生效",
  "data": {
    "auth_url": "https://tapd.woa.com/oauth/authorize?client_id=bkmonitor_tapd&response_type=code&redirect_uri=https://monitor.bk.example.com/fta/issue/tapd/oauth_callback/&scope=user_space&state=nonce123:2",
    "auth_method": "session"
  }
}
```

> 前端提取 `data.auth_url` 直接跳转授权页（可自行编码处理）。

### TAPD API 异常（500）

```json
{
  "result": false,
  "code": 500,
  "message": "TAPD 服务暂时不可用，请稍后重试",
  "data": null
}
```

---

## install_url 说明

### 格式

```
https://tapd.woa.com/oauth/open_app_install
  ?client_id=bkmonitor_tapd
  &test=1
  &cb=https%3A%2F%2Fmonitor.bk.example.com%2Ffta%2Fissue%2Ftapd%2Fapp_install_callback%2F%3Fsigned_state%3DeyJia19iaXpfaWQiOjIsInRlbi4uLn0.WzG4x
  #selected_workspace_id={workspace_id}
```

### 参数说明

| 参数 | 来源 | 说明 |
|------|------|------|
| `client_id` | 后端预写 | 固定值 `bkmonitor_tapd` |
| `test` | 后端预写 | `1`=测试应用，`0`=正式应用（上架后改） |
| `cb` | 后端生成 | 回跳 URL（**整体 URL 编码**，防止 query string 解析歧义），指向 B-03 回调端点，内嵌 `signed_state`。`#fragment` 中的 `{workspace_id}` 占位符**跳过编码** |
| `signed_state` | 后端生成 | HMAC 签名状态串（`base64url(json).hmac`），内嵌在编码后的 `cb` 中，TAPD 原样带回回调 URL，B-03 验签 |
| `selected_workspace_id` | 前端填入 | `#fragment` 参数，值为 `item.workspace_id` |

### 占位符

| 占位符 | 替换值 | 来源 |
|--------|--------|------|
| `{workspace_id}` | TAPD 项目 ID | 前端从列表项 `item.workspace_id` 填入 |

### 前端使用示例

```javascript
// 后端返回的 install_url（cb 已编码，{workspace_id} 占位符未编码）
const installUrl = data.install_url.replace('{workspace_id}', item.workspace_id);
// 结果: https://tapd.woa.com/oauth/open_app_install?...&cb=https%3A%2F%2F...%3Fsigned_state%3DeyJ4e...#selected_workspace_id=10104091
window.open(installUrl, '_blank');
```

### 使用条件

- 列表中存在 `is_bound = "unbound"` 或 `"stale"` 项目时，`install_url` 才返回
- 若列表中没有 `unbound` / `stale` 状态的项目（即全部 `bound` / `importable`），`install_url` 字段为空或不返回

---

## 四态标记逻辑

```python
def compute_bound_status(
    workspace_id: str,
    local_bindings: Set[str],
    granted_workspaces: Set[str]
) -> str:
    has_local = workspace_id in local_bindings
    has_tapd = workspace_id in granted_workspaces

    if has_local and has_tapd:
        return "bound"
    if has_local and not has_tapd:
        return "stale"
    if not has_local and has_tapd:
        return "importable"
    return "unbound"
```

---

## 内部调用链

```
前端 GET /fta/issue/tapd/user_workspace/?bk_biz_id=2
  → IssueViewSet
    → TAPD_REQUIRED Permission 检查
      → Redis: tapd_uat:{tenant}:{user}
        ├─ 不存在 → PermissionDenied 403 + auth_url
        └─ 存在 → AESCipher 解密 → 获取 access_token
          → TapdUserAPIResource → TAPD 用户态 API
            → 获取用户可见项目
              → 查本地 TapdWorkspaceBinding
                → 调 GetGrantedWorkspacesResource（Basic Auth，短缓存）
                  → 交叉标记四态
                    → 分页 → 返回 {total, items, has_more, install_url, method}
```

---

## 内部依赖

| 依赖 | 位置 | 说明 |
|------|------|------|
| `TapdUserAPIResource` | 新增 `api/tapd/user.py` | Bearer Token 调用 TAPD 用户态 API |
| `GetGrantedWorkspacesResource` | `api/tapd/default.py` | Basic Auth，取 app 已授权项目 |
| `generate_auth_url()` | 工具函数 | 生成未编码 OAuth URL |
| `generate_install_url()` | 工具函数 | `open_app_install` URL 模板（含 `#selected_workspace_id` 占位符） |
| `generate_signed_state()` | 工具函数 | 生成 HMAC 签名的 `signed_state`，含 `initiator` 和 `exp` |
| `compute_bound_status()` | 工具函数 | 本地 binding × TAPD 授权 → 四态 |
| `AESCipher` | `utils/cipher.py` | Token 解密 |

---

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1 | 2026-06-22 | AI | 初始创建 |
| 2 | 2026-06-22 | AI | 修复：`generate_auth_url` 签名增加 `request` 参数；`install_url` 条件补充 `stale` 状态；install_url 中 `state` 改 `signed_state` |
