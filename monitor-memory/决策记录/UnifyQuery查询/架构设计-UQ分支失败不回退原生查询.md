---
groupPath: 决策记录/UnifyQuery查询
relation: 架构设计-UQ分支失败不回退原生查询
exportedAt: "2026-08-31T02:05:56.777Z"
---
【决策记录｜推测 UnifyQuery 分支失败不回退原生查询】
- 分类：架构设计（本条为推测，置信度低于其他条目，查询侧请降级使用）
- 动机：可维护性（两条链路返回结构与口径不同，自动回退会掩盖问题）
- 决策：_query_data_internal 中统一查询分支异常时被 except 捕获，仅上报 Prometheus 指标（DATASOURCE_QUERY_COUNT 带 status 与 exception）后直接抛出，不会改走 _query_data_using_datasource
- 背景约束：统一查询与原生查询的结果结构、聚合口径、字段命名存在差异，静默切换会导致同一查询在不同时刻返回不同口径的数据
- 被否决方案：无（未找到相关记录）
- 已知代价：统一查询服务故障时查询整体失败，调用方需自行兜底（降级、重试或提示）
- 重新评估触发条件：出现统一查询后端大面积不可用且需要保底查询（可观测判据：UQ 分支 5xx 或异常占比大于百分之一）
- 关联代码：UnifyQuery._query_data_internal @ unify_query/query.py
- 证据来源：无直接证据，基于 try 与 except 捕获异常后仅上报指标并在末尾 raise exc、except 块内未调用原生查询分支的实现结构推断
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 7