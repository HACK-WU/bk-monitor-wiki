---
groupPath: 专题记忆/UnifyQuery查询
relation: interval 双身份与 without_time 数值等价性
exportedAt: "2026-09-04T04:05:53.678Z"
---
查询参数 interval 的两个独立作用：① 普通方法（AVG/SUM/MIN/MAX/COUNT）作为 time_aggregation.window（桶内 over_time 聚合窗口，SUM 会随窗口放大数值）；② 所有方法（含 *_without_time）作为输出采样步长 step（unify_query/query.py get_unify_query_params：step=min(各 data_source.interval)，默认 60s）——without_time 下调大 interval 只改变采样密度不改变单点口径，但图表点数/形状会变，勿误判为「interval 对 without_time 无任何影响」。
- 数值等价性: MIN/MAX 可结合（min(桶内min)==桶内全局min），普通 MIN 与 min_without_time 数值基本一致；SUM/AVG/COUNT 不可结合，普通 SUM=桶内累加+跨维度求和（窗口内 k 个采样点会放大 k 倍），sum_without_time=每时刻跨 series 瞬时求和（PromQL sum）。
- 分发代码: data_source/data_source/__init__.py to_unify_query_config——method 命中 AggMethods（仅 5 个 *_without_time 变体，unify_query/functions.py）不生成 time_aggregation，否则生成 {method}_over_time + window=interval