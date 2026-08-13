---
groupPath: 专题记忆/UnifyQuery查询
relation: UnifyQuery专家路标
exportedAt: "2026-08-13T09:59:31.073Z"
---
【专题记忆｜UnifyQuery查询】
- 资产路径：.module-experts/UnifyQuery查询专家/（用 expert-lookup 加载详细资产）
- 一句话职责：BK-Monitor 统一查询门面，编排时序/日志/维度数据的查询，分流统一查询后端或数据源原生查询
- 核心能力（≤5）：query_data / query_log / query_dimensions / query_reference / query_data_with_stat
- 高频坑（≤3）：instant=True时step强制1m且保留end_time边界点（非instant丢弃该点）；AVG变avg_over_time+mean两层聚合（用avg_without_time取瞬时值）；query_log的total在统一查询路径恒为0
- 关键代码位置（≤5）：UnifyQuery类→bkmonitor/bkmonitor/data_source/unify_query/query.py；to_unify_query_config→bkmonitor/bkmonitor/data_source/data_source/__init__.py；QueryDataResource→bkmonitor/api/unify_query/default.py；UnifyQuerySet→bkmonitor/bkmonitor/data_source/unify_query/builder.py；DataQueryHandler→bkmonitor/bkmonitor/data_source/handler/__init__.py
- 数据落地：无持久化（查询门面，返回list[dict]给调用方处理）
- 检索触发词：UnifyQuery 统一查询 查询门面 query_data query_log query_dimensions instant 聚合函数 avg_over_time 两层聚合 数据源查询
- 详细资产：见 .module-experts/UnifyQuery查询专家/，契约层 C0~C2（怎么用）+ implementation/01~05（怎么实现）