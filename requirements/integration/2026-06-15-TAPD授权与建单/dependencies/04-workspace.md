# 项目（Workspace）API

> 查询 TAPD 项目信息，用于本需求的四态判定和项目名获取。

---

## 1. get_granted_workspaces — 查询已授权项目列表

查询当前应用已授权安装的 TAPD 项目列表。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET |
| **请求 URL** | `http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces` |
| **认证方式** | **Basic Auth**（`client_id:client_secret`） |

### 请求参数（Query）

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `workspace_id` | 否 | integer | 项目 ID。传入则精确查询该项目是否已授权 |
| `type` | 否 | integer | 安装类型：`0`=应用商店安装，`1`=测试安装，`2`=插件安装 |
| `created` | 否 | datetime | 创建时间，支持时间查询 |
| `limit` | 否 | integer | 返回数量限制，默认 30，最大 200 |
| `page` | 否 | integer | 页码，默认 1 |
| `order` | 否 | string | 排序规则，如 `created%20desc`。需 URL encode |
| `fields` | 否 | string | 指定返回字段，多个字段用逗号隔开 |

### 请求示例（curl）

```bash
# 查询全部已授权项目（Basic Auth）
curl -u 'api_user:api_password' \
  'http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces'

# 查询指定项目是否已授权
curl -u 'api_user:api_password' \
  'http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces?workspace_id=10104801'
```

### 返回参数

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | integer | 1 = 成功 |
| `data.list` | array | 授权记录列表 |
| `data.list[].OpenOrganizationApp.workspace_id` | string | 项目 ID |
| `data.list[].OpenOrganizationApp.type` | string | 安装类型：`0`商店/`1`测试/`2`插件 |
| `data.list[].OpenOrganizationApp.created` | string | 授权时间 |
| `data.pager.count` | integer | 总记录数 |
| `data.pager.page` | integer | 当前页 |
| `data.pager.limit` | integer | 每页条数 |
| `info` | string | 提示信息 |

> 返回示例见原 `dependencies.md` §2.4 或官方文档。
> 本需求用途：B-07 查询 app 已授权项目，作为 `is_bound` 四态中 `bound`/`stale` 状态的判定源。

---

## 2. get_workspace_info — 获取项目详情

根据项目 ID 获取项目详细信息。

| 项目 | 内容 |
|------|------|
| **请求方式** | GET |
| **请求 URL** | `http://apiv2.tapd.woa.com/workspaces/get_workspace_info` |
| **认证方式** | **Basic Auth**（复用现网 `TapdAPIResource`） |

### 请求参数（Query）

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `workspace_id` | 是 | integer | 项目 ID |

### 返回关键字段（data.Workspace）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 项目 ID |
| `name` | string | 项目名称 |
| `pretty_name` | string | 项目英文昵称 |
| `status` | string | 项目状态：`normal`=正常，`closed`=关闭，`suspend`=挂起 |
| `creator` | string | 项目创建者 |
| `created` | string | 创建时间 |

> 本需求用途：B-03 应用态授权回调时，从 `resource["workspace_id"]` 获取 ID 后，调用本接口获取 `name`，写入 `TAPD_WORKSPACE_BINDING`。
> 现网已有封装：`bkmonitor/api/tapd/default.py` -> `TapdAPIResource`，设计应直接复用。
