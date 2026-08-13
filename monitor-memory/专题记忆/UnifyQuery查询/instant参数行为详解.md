---
groupPath: 专题记忆/UnifyQuery查询
relation: instant参数行为详解
exportedAt: "2026-08-13T10:00:49.767Z"
---
instant 参数是 UnifyQuery 最重要的开关之一，有 instant=True 和没有 instant 时查询行为完全不同，不仅影响返回数据点数量，还影响数据内容本身。

- 符号: `UnifyQuery._query_unify_query`、`process_unify_query_data`、`UnifyQuerySet.instant`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`、`bkmonitor/bkmonitor/data_source/unify_query/builder.py`

行为差异对照:
- 返回点数: 非 instant 按步长采样多个评估点；instant 仅返回 end_time 一个评估点
- step 参数: 非 instant 来自 interval（如 "180s"）；instant 强制覆盖为 "1m"
- end_time 边界点: 非 instant 丢弃（process_unify_query_data 中 _time_==end_time 时 skip）；instant 保留（不 skip）
- 聚合函数: 不变（avg_over_time + mean 照常执行）
- 下推到原生查询: instant 被忽略（不走 _query_data_using_datasource 时 instant 不传递）
- start_time: 正常传入（不会被重算），但 instant 模式只看 end_time 单点

end_time 边界点丢弃是最关键差异:
- 非 instant: SaaS 侧策略丢弃 end_time 最后一条数据（边界点采集周期不完整）
- instant: 保留 end_time 边界点（instant 查“此刻”瞬时值，丢弃会导致结果为空）
- 实际影响: 同一时间范围 [T-start, T]，非 instant 返回 [T-start, T) 内数据点（不含T），instant 返回 T 时刻数据点

Builder 层 align_interval 补偿:
- UnifyQuerySet.instant(align_interval=N) 在设 instant=True 同时把 end_time 前移 N 毫秒
- 目的: 让 instant 返回 end_time - interval 时刻的点，与非 instant 丢弃边界点后保留的最后有效点对齐

约束与限制:
- 仅对统一查询后端路径有效，_query_data_using_datasource 分支不受 instant 影响
- (BK_MONITOR_COLLECTOR, TIME_SERIES) 恒走统一查询后端，故 instant 始终生效
- instant 模式下 step="1m" 是采样步长，不是聚合窗口；聚合窗口仍由 interval → time_aggregation.window 决定