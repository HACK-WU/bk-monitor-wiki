---
groupPath: 决策记录/UnifyQuery查询
relation: 接口契约-两层聚合与without_time变体
exportedAt: "2026-08-31T02:05:56.777Z"
---
【决策记录｜UnifyQuery 两层聚合：time_aggregation 时间轴加 function 跨 series，并提供 without_time 变体】
- 分类：接口契约
- 动机：一致性（同时支持 PromQL 风格与 InfluxDB 风格的聚合语义）
- 决策：to_unify_query_config 把 metrics 的 method 拆成两层：普通 method（avg、sum、count、max、min）生成 time_aggregation 为 method_over_time 且 window 为 interval 秒，加 function[0].method（avg 映射为 mean、count 映射为 sum）；AggMethods 中的 without_time 变体（sum、avg、count、min、max 五种）不生成 time_aggregation，只做跨 series 聚合（PromQL 风格）；CpAggMethods（cp50、cp90、cp95、cp99）time_aggregation.function 为 histogram_quantile 并带 vargs_list 与 position
- 背景约束：同一查询既要时间窗口平滑又要同组多条 series 归并，二者是独立维度；部分场景（进程实例数、稀疏采集点）需要跳过时间聚合
- 被否决方案：单一聚合层（只做时间聚合或只做跨 series 聚合），否决理由为无法同时表达两种语义，从 AggMethods 与 CpAggMethods 的并存结构看两层拆分是必须的
- 已知代价：method 为 AVG 实际是 avg_over_time 加 mean 两层，与调用方直觉不符；需要瞬时值必须显式用 avg_without_time
- 重新评估触发条件：需要新的聚合语义（如不跨 series 也不跨时间的原始点直出）且两层模型无法表达
- 关联代码：TimeSeriesDataSource.to_unify_query_config @ data_source/__init__.py；AggMethods 与 CpAggMethods @ unify_query/functions.py
- 证据来源：代码实现（if 与 else 两分支加 _over_time 生成）；functions.py 中 AggMethods 各条目 name 字段标注 PromQL；项目记忆 专题记忆/数据源查询机制 已有 count_without_time 与 COUNT 聚合语义差异条目
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 6