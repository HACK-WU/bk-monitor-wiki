TAPD 相关功能概览，涵盖文件结构、URL 路由、权限控制、主要 Resource 类与 TAPD API 封装、以及用户态授权与项目绑定等关键逻辑。

## 文件结构

- 位置: `bkmonitor/packages/fta_web/issue/resources.py` — TAPD相关Resource类（ListTapdWorkspaceResource等）
- 位置: `bkmonitor/packages/fta_web/issue/views.py` — IssueViewSet，定义TAPD_ENDPOINTS和权限控制
- 位置: `bkmonitor/packages/fta_web/issue/urls.py` — TAPD回调路由
- 位置: `bkmonitor/api/tapd/default.py` — TapdAPIResource基类及TAPD API封装

## URL 路由（urls.py）

- `tapd/oauth_callback/` → `tapd_user_oauth_callback`
- `tapd/app_install_callback/` → `tapd_app_install_callback`

## 权限控制（views.py）

- 符号: `TAPDAuthPermission`
- 位置: `bkmonitor/packages/fta_web/issue/views.py`
- 校验 TAPD 用户态 token（Redis tapd_uat:{tenant}:{user}）
- `TAPD_ENDPOINTS` — 所有TAPD相关端点列表
- 未授权时返回403 + auth_url引导授权

## 主要 Resource 类（resources.py）

- 位置: `bkmonitor/packages/fta_web/issue/resources.py`
- `ListTapdWorkspaceResource` — 获取已授权TAPD项目列表
- `GetTapdFieldsResource` — 获取TAPD单据字段
- `SearchTAPDItemsResource` — 查询TAPD单据
- `CreateTAPDIssueResource` — 创建TAPD单据
- `LinkIssueToTAPDResource` — 关联Issue与TAPD单据
- `ListIssueTAPDRelationsResource` — 获取Issue关联的TAPD单据

## TAPD API 封装（default.py）

- 符号: `TapdAPIResource`
- 位置: `bkmonitor/api/tapd/default.py`
- 基类，处理认证（Basic/Bearer）
- `GetGrantedWorkspacesResource` — 获取已授权项目
- `GetWorkspaceInfoResource` — 获取项目信息
- `AddStoryResource` — 创建需求
- `AddBugResource` — 创建缺陷
- `AddTaskResource` — 创建任务
- `UserOauthTokenResource` — OAuth换token

## 关键逻辑

- 用户态授权：OAuth流程，code换token，存储在Redis
- 项目绑定：TapdWorkspaceBinding表记录绑定关系
- 回调处理：OAuth回调和应用安装回调
- 权限校验：所有TAPD接口需前置校验用户态token
