# TAPD 集成子专家

> 父专家：[Issue 专家](../agent.md)
> 覆盖范围：TAPD 关联管理、OAuth 授权、工作区解绑/重绑
> 最后更新：2026-08-03
> 契约层：就绪
> 实现层：就绪

## 测试状态

- **测试位置**：无直接单测（TAPD OAuth/工作区绑定逻辑未被测试覆盖，`test_bkm_cli_inspect_issue.py` 仅覆盖 bkm-cli 诊断入口）
- **测试可执行性**：该子专家无直接测试；间接相关用例见 [父专家 06-测试.md](../../implementation/06-测试.md)
- **测试缺口**：TAPD OAuth 回调、token 加解密、工作区绑定/解绑/重绑、tombstone 阻断逻辑需补单测

## 包含的资产

| 类型 | 文件 | 说明 |
|------|------|------|
| 使用总览 | [C0-使用总览.md](./C0-使用总览.md) | 能力清单、边界、已知问题 |
| 能力契约 | [C1-能力契约.md](./C1-能力契约.md) | 公开能力、参数、返回、异常、真实代码示例 |
| 使用流程 | [C2-使用流程.md](./C2-使用流程.md) | 用户态授权、创建 TAPD 单、解绑/重绑 |
| 数据流向与消费 | [C4-数据流向与消费.md](./C4-数据流向与消费.md) | token、binding、tombstone、关联、活动日志 |
| 实现-实现 | [implementation/01-实现.md](./implementation/01-实现.md) | 用户态授权、回调、创建/关联、解绑/撤销 |
| 实现-实现 | [implementation/02-实现.md](./implementation/02-实现.md) | 核心流程、关键类函数、设计模式、技术债 |
| 实现-数据流转 | [implementation/03-数据流转.md](./implementation/03-数据流转.md) | 数据生命周期、五态状态机、异步流 |
| 实现-模型 | [implementation/04-模型.md](./implementation/04-模型.md) | TapdWorkspaceBinding / tombstone / IssueTapdRelation |
| 实现-接口 | [implementation/05-接口.md](./implementation/05-接口.md) | 端点清单、契约示例、错误码、鉴权 |

## 覆盖文件

| 文件 | 大小 | 职责 |
|------|------|------|
| `resources.py`（TAPD 部分） | — | TAPD 相关 Resource 类 |
| `views.py`（TAPD 部分） | — | TAPD 端点注册 + 权限校验 |
| `urls.py`（TAPD 回调路由） | — | OAuth/应用安装回调路由 |
| `utils/tapd.py` | 12KB | TAPD 工具函数 |

## TAPD 端点总览

| 端点 | Resource 类 | 权限 | 说明 |
|------|-------------|------|------|
| `issue/get_tapd_fields` | `GetTapdFieldsResource` | VIEW_EVENT + TAPDAuth | 获取 TAPD 单类型字段定义 |
| `issue/search_tapd_items` | `SearchTAPDItemsResource` | VIEW_EVENT + TAPDAuth | 搜索 TAPD 项 |
| `issue/create_tapd` | `CreateTapdResource` | MANAGE_EVENT + TAPDAuth | 创建 TAPD 单并关联 |
| `issue/link_tapd` | `LinkIssueToTapdResource` | MANAGE_EVENT + TAPDAuth | 关联已有 TAPD 单 |
| `issue/tapd_relations` | `ListIssueTapdRelationsResource` | VIEW_EVENT + TAPDAuth | 查询 TAPD 关联列表 |
| `tapd/workspace` | `ListTapdWorkspaceResource` | VIEW_EVENT | 已授权 TAPD 项目列表（应用态） |
| `tapd/user_workspace` | `ListUserTapdWorkspaceResource` | VIEW_EVENT | 用户可见 TAPD 项目（用户态，含 install_url） |
| `tapd/unbind_workspace` | `UnbindTapdWorkspaceResource` | MANAGE_EVENT | 手动解绑工作区（持久化 tombstone） |
| `tapd/rebind_workspace` | `RebindTapdWorkspaceResource` | MANAGE_EVENT | 重新关联已解绑工作区 |
| `tapd/revoke_auth` | `RevokeTapdUserAuthResource` | MANAGE_EVENT | 撤销用户授权 |

## 用户态授权流程

### TAPDAuthPermission

所有 `TAPD_ENDPOINTS` 中的接口前置校验 Redis `tapd_uat:{tenant}:{user}` token：
- 未授权 + 携带 `success_url`（仅 `tapd/user_workspace`）：返回 403 + `auth_url` 引导前端跳转
- 未授权 + 无 `success_url`：返回 403 提示先完成授权

### OAuth 回调

`tapd/oauth_callback/`、`tapd/app_install_callback/` 两个 `csrf_exempt` 路由完成用户态授权码兑换并写回 `tapd_uat` token。

## 工作区解绑/重绑

### 解绑（unbind_workspace）

- 持久化 tombstone：`TapdWorkspaceManualUnbind` 记录
- 阻断周期任务自动回绑

### 重绑（rebind_workspace）

- 清除 tombstone 记录
- 恢复周期任务自动同步

## 创建 TAPD 单流程

1. `CreateTapdResource` 接收请求参数
2. 调用 TAPD API 创建工单
3. 写 `IssueTapdRelation` 持久化关联
4. 记 `create_tapd` 活动日志

## 关联已有 TAPD 单流程

1. `LinkIssueToTapdResource` 接收请求参数
2. 批量查重（防止重复关联）
3. 写 `IssueTapdRelation` 持久化关联
4. 记 `tapd_link` 活动日志

## 关键设计决策

| 决策 | 说明 |
|------|------|
| 用户态 token 存储 | Redis `tapd_uat:{tenant}:{user}` |
| 解绑持久化 | `TapdWorkspaceManualUnbind` 模型，阻断自动回绑 |
| 授权引导 | 仅 `tapd/user_workspace` 支持 `success_url` 参数触发授权跳转 |
| 撤销授权 | 清除 Redis token，不删除关联数据 |
