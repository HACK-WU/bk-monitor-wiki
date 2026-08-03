# 模块专家包索引
> 由 expert-team 自动维护

## 项目全局（共享资产）
- 资产：PROJECT.md（项目信息/技术栈/架构形态/核心功能/核心服务清单/配套服务关系/架构图/数据流向图/运行环境）
- 说明：所有专家共享的项目全局上下文，创建/使用专家前建议先读
- 维护：expert-team 首次创建/发现全局信息时更新；expert-lookup 使用中发现变化时受限更新

## UnifyQuery查询专家（职责摘要见 agent.md）
- 模块根：bkmonitor/bkmonitor/data_source/unify_query/
- 生成日期：2026-07-27  git commit：host-view-api-split
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 05-接口
- 子专家：无

## 数据源查询构造专家（职责摘要见 agent.md）
- 功能域：load_data_source 工厂、14 组合映射、路径决策、查询描述构造
- 生成日期：2026-07-27  git commit：host-view-api-split
- 契约层：C0-使用总览, C1-能力契约
- 实现层：implementation/01-架构, 02-实现
- 子专家：无

## 场景视图专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/scene_view/
- 重建日期：2026-07-27  git commit：ca831622
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型
- 子专家：无
- 专用技能：skills/add-builtin-scene-view/

## 性能场景专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/performance/
- 重建日期：2026-07-27  git commit：916585db
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型
- 子专家：无
- 专用技能：skills/add-host-performance-field/

## 告警查询专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/fta_web/alert/
- 重建日期：2026-07-27  git commit：310f13e
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程（暂无 C3）
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 05-接口, 06-测试
- 子专家：无
- 专用技能：skills/query-alert/

## Issue 专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/fta_web/issue/
- 生成日期：2026-07-31
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程, C4-数据流向与消费
- 实现层：implementation/01-架构, 02-实现
- 匹配关键词：Issue, 告警聚合, 状态机, TAPD, LLM标题, IssueAggregationProcessor, IssueDocument, sync_issue_alert_stats, 合并, 拆分
- 子专家：
  - **Issue API 子专家**（sub-experts/issue-api/）：RESTful接口/权限/序列化/批量操作
  - **Issue 查询子专家**（sub-experts/issue-query/）：ES查询构建/时间分片/排序
  - **Issue 状态聚合子专家**（sub-experts/issue-state-aggregation/）：状态机/聚合引擎/周期任务/LLM标题
  - **TAPD 集成子专家**（sub-experts/tapd-integration/）：关联管理/OAuth授权/解绑重绑

## 告警屏蔽专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/shield/ + bkmonitor/alarm_backends/service/converge/shield/
- 生成日期：2026-07-28（测试文档补充：2026-08-03）
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型, 05-接口, 06-测试
- 测试：test/known-failures.md
- 匹配关键词：告警屏蔽, 屏蔽, scope, strategy, alert, dimension, ShieldObj, AddShieldResource, ShieldCacheManager, 快捷屏蔽, QuickShield, dimension_conditions, 屏蔽通知, HostShielder, ShieldDetectManager
- 子专家：无
