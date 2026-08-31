---
groupPath: 决策记录/UnifyQuery查询
relation: 性能取舍-is_es_batch默认关闭按需开启
exportedAt: "2026-08-31T02:06:21.187Z"
---
【决策记录｜UnifyQuery ES 批处理 is_es_batch 默认关闭，由调用方按需 opt-in】
- 分类：性能取舍
- 动机：优化（APM Trace 跨结果表查询的批量 ES 读取性能）
- 决策：统一查询 query_raw 的可选参数 is_es_batch 缺省时不发送（不改变其他调用方行为）；仅 APM Trace 的跨结果表 Trace 查询（TraceQuery.query_by_trace_ids）显式传 is_es_batch 为真；前端资源参数不暴露该开关
- 背景约束：批处理是性能优化手段，未经验证前不应影响既有调用方的行为与返回
- 被否决方案：全局开启 ES 批处理，否决理由为会改变所有 query_raw 调用方的行为，风险面过大（commit body 明确缺省时不发送、不改变其他调用方行为、调用范围由 APM Trace 服务端控制）
- 已知代价：需要该优化的场景必须逐个显式开启，收益面受限
- 重新评估触发条件：批处理被验证稳定且需要推广到更多场景；或出现批处理相关的查询异常
- 关联代码：UnifyQuery._query_log_using_unify_query（is_es_batch 分支）@ unify_query/query.py；TraceQuery.query_by_trace_ids @ apm_web 侧
- 证据来源：commit b3307f2138（body：UQ query_raw 请求模型支持可选 is_es_batch 参数，缺省时不发送不改变其他调用方行为；仅在 TraceQuery.query_by_trace_ids 的跨 RT Trace 查询中显式传入 is_es_batch 为真；前端资源参数不暴露该开关，调用范围由 APM Trace 服务端控制）
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 13