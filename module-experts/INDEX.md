# 模块专家包索引
> 由 expert-team 自动维护

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

## 告警屏蔽专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/shield/ + bkmonitor/alarm_backends/service/converge/shield/
- 生成日期：2026-07-28
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型, 05-接口
- 子专家：无
