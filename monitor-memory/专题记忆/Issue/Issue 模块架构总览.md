---
groupPath: 专题记忆/Issue
relation: Issue 模块架构总览
exportedAt: "2026-08-13T08:53:00.386Z"
---
Issue 是 BK-Monitor 告警处理链路中的问题聚合与跟踪域，将海量告警按同一具体问题聚合为 Issue，帮助运维聚焦根因。横跨 Web API、ES 查询、状态机、聚合引擎、周期任务五大区域。

## 关键文件
- 符号: `IssueViewSet` / 各 Resource 类
- 位置: `bkmonitor/packages/fta_web/issue/resources.py`（142KB，所有端点实现）、`views.py`（13KB，路由+权限）、`urls.py`（路由）、`serializers.py`（序列化）
- 符号: `IssueQueryHandler` / `IssueQueryTransformer`
- 位置: `bkmonitor/packages/fta_web/issue/handlers/issue.py`（56KB，查询处理器+转换器）
- 符号: `IssueDocument`
- 位置: `bkmonitor/documents/issue.py`（ES 文档模型+状态机）
- 符号: `IssueAggregationProcessor`
- 位置: `alarm_backends/service/fta_action/issue_processor.py`（告警→Issue 聚合入口）
- 符号: `sync_issue_alert_stats`
- 位置: `alarm_backends/service/fta_action/tasks/issue_tasks.py`（周期任务）
- 符号: `IssueMergeResolver`
- 位置: `bkmonitor/issue_merge.py`（合并/展开逻辑）
- 符号: `dispatch_llm_title`
- 位置: `alarm_backends/service/fta_action/llm_title.py`（LLM 标题）
- 符号: Issue 枚举常量
- 位置: `constants/issue.py`（状态/优先级/活动类型）

## 跨模块依赖
- API Gateway: `api/issue/default.py`（蓝鲸网关接口，超时 300s）
- bkm-cli RPC: `kernel_api/rpc/functions/bkm_cli/issue.py`（CLI 诊断，4 种只读 operation）
- kernel_api v4: `kernel_api/views/v4/issue.py`（MergeResource/SplitResource）

## 数据存储
- ES 索引 `bkfta_issue`（Issue 文档，按创建时间分片）
- ES 索引 `bkfta_fta_issue_act`（活动日志）
- Redis `issue_active_content:{fingerprint}`（活跃 Issue 缓存）
- MySQL `bkmonitor_issue_merge_relation`（合并关系）
- MySQL `bkmonitor_issue_tapd_relation`（TAPD 关联）
- MySQL `bkmonitor_tapd_workspace_manual_unbind`（解绑 tombstone）

## 专家资产位置
- 落盘: `.module-experts/issue专家/`（父专家 + 4 子专家：API/查询/状态聚合/TAPD集成，含 agent.md + implementation/ 双层资产）