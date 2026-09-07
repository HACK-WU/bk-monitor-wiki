# Issue API 子专家

> 契约层就绪：C0-使用总览、C1-能力契约、C2-使用流程、C4-数据流向与消费
> 实现层就绪：implementation/01-实现
> 父专家：[Issue 专家](../agent.md)
> 覆盖范围：RESTful 接口层、权限控制、序列化、路由
> 最后更新：2026-08-03

## 测试状态

- **测试位置**：`packages/fta_web/tests/issue/test_issue_resources.py`（21 用例）、`tests/api/fta/test_issue_activities_contract.py`（7 用例，AST 契约）、`kernel_api/tests/test_issue_v4.py`
- **测试可执行性**：✅ 可跑（web/worker 角色），详见 [父专家 06-测试.md](../../implementation/06-测试.md)
- **已知失败**：[父专家 test/known-failures.md](../../test/known-failures.md)

## 覆盖文件

| 文件 | 大小 | 职责 |
|------|------|------|
| `resources.py` | 142KB | 所有 Resource 类实现（CRUD、批量操作、TAPD、趋势等） |
| `views.py` | 13KB | `IssueViewSet` 注册 + 权限配置 + TAPD 端点注册 |
| `serializers.py` | 1.6KB | 请求序列化器；当前仅 `IssueSearchSerializer`，其他参数校验多在 Resource 内完成 |
| `urls.py` | 1.2KB | URL 路由配置 |

## 端点总览

### 只读接口（VIEW_EVENT）

| 方法 | 路径 | Resource 类 | 说明 |
|------|------|-------------|------|
| POST | `/issue/search` | `SearchIssueResource` | Issue 列表查询（分页、过滤、排序、时间分片） |
| POST | `/issue/top_n` | `IssueTopNResource` | TopN 统计聚合 |
| GET | `/issue/detail` | `IssueDetailResource` | Issue 详情 |
| GET | `/issue/activities` | `ListIssueActivitiesResource` | 活动日志查询 |
| GET | `/issue/history` | `ListIssueHistoryResource` | 同策略历史 Issue |
| POST | `/issue/alert_enrich` | `AlertIssueEnrichResource` | 告警 enrich |
| POST | `/issue/log_content` | `IssueLogContentResource` | 日志内容批量查询 |
| GET | `/issue/merge_sources` | `ListMergeSourcesResource` | 合并来源列表（2026-08-31 起条目新增 `via_issue_id` 上一跳主溯源字段；2026-09-07 起条目新增 `first_alert_time`/`last_alert_time` 成员自身告警时间，秒级时间戳，缺失兜底 0） |
| POST | `/issue/export` | `ExportIssueResource` | 导出 Issue 列表 |
| POST | `/issue/recent_assignees` | `ListRecentAssigneesResource` | 最近使用负责人 |
| POST | `/issue/trend` | `IssueTrendResource` | Issue 趋势统计 |
| POST | `/issue/get_tapd_fields` | `GetTapdFieldsResource` | TAPD 字段定义 |
| POST | `/issue/search_tapd_items` | `SearchTAPDItemsResource` | 搜索 TAPD 项 |
| POST | `/issue/tapd_relations` | `ListIssueTapdRelationsResource` | TAPD 关联列表 |
| POST | `/tapd/workspace` | `ListTapdWorkspaceResource` | TAPD 项目列表（应用态） |
| POST | `/tapd/user_workspace` | `ListUserTapdWorkspaceResource` | 用户可见 TAPD 项目（用户态） |

### 写操作（MANAGE_EVENT）

| 方法 | 路径 | Resource 类 | 说明 |
|------|------|-------------|------|
| POST | `/issue/assign` | `AssignIssueResource` | 指派/改派负责人（批量） |
| POST | `/issue/resolve` | `ResolveIssueResource` | 标记已解决（批量） |
| POST | `/issue/reopen` | `ReopenIssueResource` | 重新打开 |
| POST | `/issue/archive` | `ArchiveIssueResource` | 归档 |
| POST | `/issue/restore` | `RestoreIssueResource` | 恢复归档 |
| POST | `/issue/update_priority` | `UpdateIssuePriorityResource` | 修改优先级（批量） |
| POST | `/issue/rename` | `RenameIssueResource` | 重命名 |
| POST | `/issue/add_follow_up` | `AddIssueFollowUpResource` | 添加跟进评论（批量） |
| POST | `/issue/edit_follow_up` | `EditIssueFollowUpResource` | 编辑跟进评论 |
| POST | `/issue/merge` | `MergeIssueResource` | 将多个 Issue 合并到主 Issue |
| POST | `/issue/split` | `SplitIssueResource` | 将子 Issue 从主 Issue 拆分恢复为独立 Issue |
| POST | `/issue/create_tapd` | `CreateTapdResource` | 创建 TAPD 单并关联 |
| POST | `/issue/link_tapd` | `LinkIssueToTapdResource` | 关联已有 TAPD 单 |
| POST | `/tapd/unbind_workspace` | `UnbindTapdWorkspaceResource` | 手动解绑工作区 |
| POST | `/tapd/rebind_workspace` | `RebindTapdWorkspaceResource` | 重新关联工作区 |
| POST | `/tapd/revoke_auth` | `RevokeTapdUserAuthResource` | 撤销用户授权 |

## 权限体系

### IssueBusinessActionPermission

自定义权限校验器，处理 `bk_biz_id` 的三种来源：
1. `body.issues[*].bk_biz_id` — 批量写操作
2. `body.bk_biz_ids` — issue/search 查询
3. `request.biz_id` — URL/GENU/POST/JSON body

### 无需业务 ID 的接口

`NO_BIZ_REQUIRED_ENDPOINTS`：`issue/search`、`issue/top_n`、`issue/recent_assignees`

### TAPD 用户态授权

`TAPD_ENDPOINTS` 中接口（`tapd/workspace`、`tapd/user_workspace`、`tapd/unbind_workspace`、`tapd/rebind_workspace`、`issue/get_tapd_fields`、`issue/search_tapd_items`、`issue/create_tapd`、`issue/link_tapd`）额外由 `TAPDAuthPermission` 前置校验 Redis `tapd_uat:{tenant}:{user}` token。`tapd/revoke_auth` 与 `issue/tapd_relations` 不在该列表中。

## 批量操作框架

`_run_batch(issues, action_fn, max_workers=10)`：
- 并发模型：ThreadPoolExecutor，每条 Issue 一个任务
- 错误隔离：单条失败不影响其他条目
- 返回格式：`{"succeeded": [...], "failed": [{"bk_biz_id", "issue_id", "message"}]}`

## API Gateway 接口

`api/issue/default.py` 定义了通过蓝鲸 API Gateway 访问的 Issue 操作接口，超时 300 秒。

## bkm-cli RPC 接口

`kernel_api/rpc/functions/bkm_cli/issue.py` 提供 4 种只读 operation：
- `detail`：查询单个 Issue 详情
- `list_by_strategy`：按策略 ID 列出 Issue
- `list_by_fingerprint`：按 fingerprint 列出 Issue
- `list_activities`：查询 Issue 活动日志

## 新增端点指南

1. 在 `resources.py` 中创建 Resource 类
2. 在 `views.py` 的 `READ_ONLY_ENDPOINTS` 或 `NO_BIZ_REQUIRED_ENDPOINTS` 中注册
3. 在 `urls.py` 中添加路由
4. 如需序列化器，在 `serializers.py` 中添加

## 包含的资产

| 资产文件 | 说明 |
|----------|------|
| [agent.md](./agent.md) | 子专家入口：覆盖范围、端点总览、权限体系、批量框架 |
| [C0-使用总览.md](./C0-使用总览.md) | 能力清单、边界、已知坑、兄弟子专家导航 |
| [C1-能力契约.md](./C1-能力契约.md) | 公开 Resource 与权限的行为语义、参数、返回、真实代码示例 |
| [C2-使用流程.md](./C2-使用流程.md) | Issue 列表查询、批量解决、创建 TAPD 单并关联三条使用流程 |
| [C4-数据流向与消费.md](./C4-数据流向与消费.md) | 数据实体来源、去向、消费方与业务用途 |
| [implementation/01-实现.md](./implementation/01-实现.md) | 实现层：文件结构、ViewSet 注册、批量框架、新增端点模板 |
