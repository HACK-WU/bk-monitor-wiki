---
groupPath: 决策记录/UnifyQuery查询
relation: 接口契约-instant语义step固定1m保留边界点
exportedAt: "2026-08-31T02:07:22.651Z"
---
【决策记录｜UnifyQuery instant 语义：step 固定 1m，且保留 end_time 边界点】
- 分类：接口契约
- 动机：一致性（instant 是查此刻的瞬时值，按非 instant 规则丢弃边界点会返回空）
- 决策：instant 为真时请求参数追加 instant 且 step 被覆盖为 1m（忽略原 interval 计算出的 step）；结果后处理 process_unify_query_data 中保留 _time_ 等于 end_time 的点（非 instant 会丢弃）；Builder 侧 UnifyQuerySet.instant(align_interval=N) 通过前移 end_time 补偿，使 instant 返回值与非 instant 丢弃边界点后的最后一个有效点对齐
- 背景约束：非 instant 模式下 end_time 边界点采集周期不完整图表中应排除；step 只是采样步长，真正的聚合窗口是 time_aggregation.window（由 interval 决定），因此 instant 覆盖 step 不改变聚合语义
- 被否决方案：instant 沿用原 step 或沿用非 instant 的边界点丢弃规则，否决理由为前者返回点数不可控，后者在当前时刻无完整采集点时返回空
- 已知代价：instant 查询的 step 参数失效固定为 1m；start_time 不受 instant 影响仍原样下传；instant 对原生查询分支无效
- 重新评估触发条件：需要 instant 查询返回自定义步长数据；或统一查询后端调整 instant 的边界点语义
- 关联代码：UnifyQuery._query_unify_query（step 等于 1m）、UnifyQuery.process_unify_query_data（边界点丢弃分支）@ unify_query/query.py；UnifyQuerySet.instant @ unify_query/builder.py
- 证据来源：代码注释（query.py：使用 instant 查询时 step 固定为 1m；如果是最后一条数据且时间戳等于结束时间不返回，且该分支带 not params.get(instant) 条件；builder.py UnifyQuerySet.instant：时序数据在 SaaS 侧的处理策略为丢弃最后一个时间戳为 end_time 的点，瞬时量 instant 在相同时间范围内是返回时间戳为 end_time 的点，为保证瞬时和时序行为一致 end_time 减 interval，instant 的 end_time 需要往前推一个 interval）
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 4