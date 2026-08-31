---
groupPath: 决策记录/UnifyQuery查询
relation: 接口契约-时间对齐默认开启not_time_align关闭
exportedAt: "2026-08-31T02:05:27.218Z"
---
【决策记录｜UnifyQuery 时间对齐默认开启，通过 not_time_align 显式关闭】
- 分类：接口契约
- 动机：一致性（对齐到步长边界，避免同一步长内出现半个采集周期的点）
- 决策：get_unify_query_params 在 time_alignment 为真且 not_time_align 为假时，把 start_time 与 end_time 经 time_interval_align 按 step 对齐到步长边界；query_data 与 query_data_with_stat 提供显式入参 not_time_align 关闭对齐
- 背景约束：图表按固定步长渲染，未对齐的时间边界会产生不完整数据点
- 被否决方案：无（未找到相关记录）
- 已知代价：需要精确时间边界的查询（如告警比对、日志示例时间对齐）必须显式传 not_time_align 为真，否则边界会被移动
- 重新评估触发条件：出现时间范围被对齐导致边界数据缺失或时间不一致的反馈累计大于等于 2 次
- 关联代码：UnifyQuery.get_unify_query_params @ unify_query/query.py
- 证据来源：commit 565e246744 与 caabd6675b（unify-query 接口增加一个参数 not_time_align）、b3ea4eb131（优化 unify-query 时间对齐判定）；代码实现（time_interval_align 分支）
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 5