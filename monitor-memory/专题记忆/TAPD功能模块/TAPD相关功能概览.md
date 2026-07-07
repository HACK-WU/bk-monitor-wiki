---
groupPath: 专题记忆/TAPD功能模块
relation: TAPD相关功能概览
keywords: [TAPD, IssueViewSet, TapdAPIResource, OAuth, 用户态授权]
exportedAt: "2026-07-06T06:04:41.760Z"
---
### TAPD相关功能概览

#### 文件结构
- `bkmonitor/packages/fta_web/issue/resources.py` — TAPD相关Resource类（ListTapdWorkspaceResource等）
- `bkmonitor/packages/fta_web/issue/views.py` — IssueViewSet，定义TAPD_ENDPOINTS和权限控制
- `bkmonitor/packages/fta_web/issue/urls.py` — TAPD回调路由
- `bkmonitor/api/tapd/default.py` — TapdAPIResource基类及TAPD API封装

#### URL路由（urls.py）
- `tapd/oauth_callback/` → `tapd_user_oauth_callback`
- `tapd/app_install_callback/` → `tapd_app_install_callback`

#### 权限控制（views.py）
- `TAPDAuthPermission` — 校验TAPD用户态token（Redis tapd_uat:{tenant}:{user}）
- `TAPD_ENDPOINTS` — 所有TAPD相关端点列表
- 未授权时返回403 + auth_url引导授权

#### 主要Resource类（resources.py）
- `ListTapdWorkspaceResource` — 获取已授权TAPD项目列表
- `GetTapdFieldsResource` — 获取TAPD单据字段
- `SearchTAPDItemsResource` — 查询TAPD单据
- `CreateTAPDIssueResource` — 创建TAPD单据
- `LinkIssueToTAPDResource` — 关联Issue与TAPD单据
- `ListIssueTAPDRelationsResource` — 获取Issue关联的TAPD单据

#### TAPD API封装（default.py）
- `TapdAPIResource` — 基类，处理认证（Basic/Bearer）
- `GetGrantedWorkspacesResource` — 获取已授权项目
- `GetWorkspaceInfoResource` — 获取项目信息
- `AddStoryResource` — 创建需求
- `AddBugResource` — 创建缺陷
- `AddTaskResource` — 创建任务
- `UserOauthTokenResource` — OAuth换token

#### 关键逻辑
- 用户态授权：OAuth流程，code换token，存储在Redis
- 项目绑定：TapdWorkspaceBinding表记录绑定关系
- 回调处理：OAuth回调和应用安装回调
- 权限校验：所有TAPD接口需前置校验用户态token