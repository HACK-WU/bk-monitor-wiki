# 项目（Workspace）API

> 查询 TAPD 项目信息，用于本需求的四态判定、项目名获取、用户授权后展示可绑定项目列表。
> 涵盖应用态（Basic Auth）和用户态（Bearer Token）两种鉴权方式下的项目查询接口。

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

---

## 3. get_user_participant_projects — 获取当前用户参与的项目列表

获取当前用户（OAuth 授权用户）在 TAPD 中参与的所有项目列表。

> 📎 官方文档：`https://o.tapd.woa.com/document/api-doc/API文档/api_reference/user/get_user_participant_projects.html`

| 项目 | 内容 |
|------|------|
| **请求方式** | GET |
| **请求 URL** | `http://apiv2.tapd.woa.com/workspaces/get_participant_projects` |
| **认证方式** | **Bearer Token**（OAuth Access Token） |

### 特殊约束

- 仅支持用户态 OAuth Access Token 调用，**不支持 Basic Auth**。
- 无分页，一次返回所有符合条件的项目。

### 请求参数（Query）

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `status` | 否 | string | 项目状态过滤，多个状态用逗号隔开。例如 `normal,suspend`。不传则返回所有状态 |

### 请求示例（curl）

```bash
# 获取当前用户参与的全部项目（OAuth Access Token）
curl -H 'Authorization: Bearer ACCESS_TOKEN' \
  'http://apiv2.tapd.woa.com/workspaces/get_participant_projects'

# 仅获取正常和挂起状态的项目
curl -H 'Authorization: Bearer ACCESS_TOKEN' \
  'http://apiv2.tapd.woa.com/workspaces/get_participant_projects?status=normal,suspend'
```

### 返回参数

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | integer | 1 = 成功 |
| `data` | array | 项目列表，每项包含一个 `Workspace` 对象 |
| `info` | string | 提示信息 |

### 返回示例

```json
{
    "status": 1,
    "data": [
        {
            "Workspace": {
                "id": "755",
                "name": "TAPD平台",
                "pretty_name": "tapd",
                "category": "product",
                "status": "normal",
                "description": "研发管理平台",
                "begin_date": "2006-04-13",
                "end_date": "2017-09-27",
                "external_on": "1",
                "creator": "",
                "created": "2007-05-01 00:00:00"
            }
        },
        {
            "Workspace": {
                "id": "10022001",
                "name": "Demo项目",
                "pretty_name": "tapd_demo",
                "category": "product",
                "status": "normal",
                "description": "",
                "begin_date": "2015-07-04",
                "end_date": "2015-07-31",
                "external_on": "1",
                "creator": "",
                "created": "2010-04-19 18:46:30"
            }
        }
    ],
    "info": "success"
}
```

### Workspace 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 项目 ID |
| `name` | string | 项目名称 |
| `pretty_name` | string | 项目英文昵称 |
| `category` | string | 项目类别 |
| `status` | string | 项目状态：`normal`=正常，`closed`=关闭，`suspend`=挂起 |
| `description` | string | 项目描述 |
| `begin_date` | string | 开始时间 |
| `end_date` | string / null | 结束时间 |
| `external_on` | string | 是否开通外网：`1`=是，`0`=否 |
| `creator` | string | 项目创建者 |
| `created` | string | 项目创建时间 |

### 本需求用途

- **B-01 授权流程**：用户完成 OAuth 授权后，可调用本接口列出其在 TAPD 中参与的项目，供选择绑定。
- **与 `get_granted_workspaces` 的区别**：
  - `get_granted_workspaces` 返回**当前 app** 已获授权安装的项目（应用视角，需 Basic Auth）。
  - `get_user_participant_projects` 返回**当前用户**参与的所有项目（用户视角，需 Bearer Token），可用于判断用户是否有权限将某项目绑定到本系统。
