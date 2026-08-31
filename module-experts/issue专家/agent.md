# Issue 专家

> 模块路径：`bkmonitor/packages/fta_web/issue/`
> 最后更新：2026-08-03

## 测试状态

- **测试目录**：`alarm_backends/tests/service/fta_action/`（聚合/合并/LLM 标题）、`packages/fta_web/tests/issue/`（Web API）、`packages/fta_web/tests/alert/test_issue_merge_expand.py`、`tests/api/fta/test_issue_activities_contract.py`（AST 契约）、`kernel_api/tests/test_issue_v4.py`、`kernel_api/rpc/tests/test_bkm_cli_inspect_issue.py`
- **测试可执行性**：✅ 大部分可跑（纯单测 + Mock 隔离 + AST 契约），见 [implementation/06-测试.md](implementation/06-测试.md)
- **已知失败**：[test/known-failures.md](test/known-failures.md)（切面级：kernel_api RPC 需 api 角色、趋势契约 1 条需前端完整检出）
- **角色注意**：合并/拆分测试需 **api 角色**（`conf.api.development.community`），worker/web 角色下会"假失败"

## 模块定位

Issue 是 BK-Monitor 告警处理链路中的**问题聚合与跟踪域**。核心目标：将海量告警按"同一具体问题"聚合为 Issue，帮助运维人员聚焦问题根因而非逐条处理告警事件。

## 契约层就绪

- **父专家**：`C0 + C1 + C2 + C4 + C5` 就绪（C5 于 2026-08-31 补建，**14 条全部有证据、0 条推测**）
- **证据优势**：本模块有配套设计文档（Wiki `bk-monitor-wiki/wiki/告警系统设计/Issue功能/`），其中《Issue 聚合引擎》含「关键设计决策」表，是本模块决策记录的主要来源
- **先看哪条**：改聚合/指纹逻辑 → 决策 1/2/3；改权限或业务过滤 → 决策 10/11；改合并语义 → 决策 13；改状态或时间过滤 → 决策 12

## 功能覆盖

- **告警聚合**：基于策略配置 + 维度指纹（fingerprint），将同策略下维度组合相同的告警聚合到同一 Issue
- **状态管理**：完整状态机（待审核 → 未解决 → 已解决 → 归档），支持指派、解决、归档、重开、恢复等操作
- **活动日志**：每次状态变更、指派、评论、优先级调整均记录活动日志，形成完整审计链
- **影响范围**：自动按关联告警汇总受影响的主机、集群、Pod、APM 服务实例等
- **周期任务**：后台定期同步告警统计、漏关联补偿、影响范围重算
- **Web API**：提供列表查询、TopN 统计、导出、批量操作等完整 RESTful 接口
- **TAPD 关联管理**：Issue 与 TAPD 工作项打通——创建/关联/解绑/重新关联
- **LLM 标题生成**：新建 Issue 后异步调用 LLM 生成可读标题

## 子专家索引

| 子专家 | 覆盖范围 | 路径 |
|--------|----------|------|
| Issue API 子专家 | RESTful 接口层、权限控制、序列化 | [sub-experts/issue-api/](sub-experts/issue-api/) |
| Issue 查询子专家 | ES 查询构建、搜索结果处理 | [sub-experts/issue-query/](sub-experts/issue-query/) |
| Issue 状态聚合子专家 | 状态机、聚合引擎、周期任务 | [sub-experts/issue-state-aggregation/](sub-experts/issue-state-aggregation/) |
| TAPD 集成子专家 | TAPD 关联管理、OAuth 授权 | [sub-experts/tapd-integration/](sub-experts/tapd-integration/) |

## 关键文件

| 文件 | 大小 | 职责 |
|------|------|------|
| `resources.py` | 142KB | Web API Resource 层，所有端点实现 |
| `handlers/issue.py` | 56KB | 查询处理器 + 查询转换器 |
| `views.py` | 13KB | ViewSet 注册 + 权限配置 |
| `serializers.py` | 1.6KB | 请求序列化器 |
| `urls.py` | 1.2KB | URL 路由配置 |
| `utils/tapd.py` | 12KB | TAPD 工具函数 |

## 跨模块依赖

| 模块 | 路径 | 关系 |
|------|------|------|
| Issue 聚合处理器 | `alarm_backends/service/fta_action/issue_processor.py` | 告警 → Issue 的聚合入口 |
| Issue 周期任务 | `alarm_backends/service/fta_action/tasks/issue_tasks.py` | 后台统计同步、漏关联补偿 |
| Issue 数据模型 | `bkmonitor/documents/issue.py` | ES 文档模型 + 状态机 |
| Issue 常量 | `constants/issue.py` | 状态、优先级、活动类型枚举 |
| Issue 合并 | `bkmonitor/issue_merge.py` | Issue 合并/展开逻辑 |
| bkm-cli RPC | `kernel_api/rpc/functions/bkm_cli/issue.py` | CLI 诊断接口 |
| API Gateway | `api/issue/default.py` | 蓝鲸 API 网关接口 |
| LLM 标题 | `alarm_backends/service/fta_action/llm_title.py` | LLM 标题生成 |

## 数据模型速查

### IssueDocument（ES 索引：`bkfta_issue`）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Keyword | Issue ID，`{timestamp}{uuid8}` |
| `strategy_id` | Keyword | 关联策略 ID |
| `bk_biz_id` | Keyword | 业务 ID |
| `name` | Text(raw: Keyword) | Issue 名称 |
| `status` | Keyword | pending_review/unresolved/resolved/archived |
| `assignee` | Keyword(multi) | 负责人列表 |
| `priority` | Keyword | P0/P1/P2 |
| `alert_count` | Long | 关联告警数量 |
| `first_alert_time` | Date | 首次告警时间 |
| `last_alert_time` | Date | 最近告警时间 |
| `fingerprint` | Keyword | 聚合指纹（count_md5） |
| `dimension_values` | Flattened | 维度取值快照 |
| `impact_scope` | Flattened | 影响范围快照 |
| `is_regression` | Boolean | 是否回归 |

### IssueActivityDocument（ES 索引：`bkfta_fta_issue_act`）

| 字段 | 说明 |
|------|------|
| `issue_id` | 所属 Issue ID |
| `activity_type` | create/comment/status_change/assignee_change/priority_change/name_change/create_tapd/tapd_link |
| `operator` | 操作人 |
| `from_value` / `to_value` | 变更前后值 |
| `content` | 评论内容 |

## 状态机

```
pending_review → unresolved (assign)
pending_review → resolved (resolve)
pending_review → archived (archive)
unresolved → resolved (resolve)
unresolved → archived (archive)
resolved → unresolved (reopen)
archived → pending_review/unresolved (restore)
```

## 权限体系

| 接口类型 | IAM Action |
|----------|------------|
| 只读接口 | `VIEW_EVENT` |
| 写操作 | `MANAGE_EVENT` |

无需 `bk_biz_id` 的接口：`search`、`top_n`、`recent_assignees`（TAPD 工作区相关接口仍需 `bk_biz_id` 作为请求参数）

## 相关 Wiki 文档

- [Issue 系统设计总览](../../bk-monitor-wiki/wiki/告警系统设计/Issue功能/Issue%20系统设计总览.md)
- [Issue API 接口](../../bk-monitor-wiki/wiki/告警系统设计/Issue功能/Issue%20API%20接口.md)
- [Issue 状态管理](../../bk-monitor-wiki/wiki/告警系统设计/Issue功能/Issue%20状态管理.md)
- [Issue 周期任务](../../bk-monitor-wiki/wiki/告警系统设计/Issue功能/Issue%20周期任务.md)
- [Issue 聚合引擎](../../bk-monitor-wiki/wiki/告警系统设计/Issue功能/Issue%20聚合引擎.md)
