instant 参数与两层聚合语义（avg_over_time vs mean），分析 instant 参数对采样步长的影响以及两层聚合（时间维度 avg_over_time + series 维度 mean）的串联执行机制。调研日期 2026-07-22，来源为 UnifyQuery 查询专家 + 源码核实。

## 1. instant 参数作用

- 符号: `UnifyQuery._query_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `instant=True`：`params["instant"]=True` 且 `step` 被覆盖为 `"1m"`
- `instant=None`：不传 instant，`step` 保持 `f"{interval}s"`（`get_unify_query_params` 计算）

核心结论：instant **只决定返回多少个评估时刻**（True=仅 end_time 单点；None=区间内按 step 采样多点），**不改变聚合函数**。instant 与区间模式下每个评估点的计算方式完全一致。

## 2. step vs time_aggregation.window（易误解点）

- `step=1m`（instant 覆盖）是**采样步长，不是聚合窗口**
- 真正聚合窗口是 `time_aggregation.window`（由 `interval` 决定，`data_source/__init__.py` `to_unify_query_config`）
- instant 单点查询中 step 被"虚化"——它只在 range query 才决定采样密度，强制成 1m 是后端兼容值

## 3. avg_over_time 由 method="AVG" 决定，与 instant 无关

- 符号: `DataSource.to_unify_query_config` + `AggMethods`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py` / `bkmonitor/bkmonitor/data_source/unify_query/functions.py`
- `AggMethods` **仅含 `*_without_time` 变体**（avg_without_time/sum_without_time/...），普通 `avg` **不在**其中
- 普通 `avg` 走 else 分支 → 生成 `time_aggregation={"function":"avg_over_time","window":"<interval>s"}`
- 真正"不跨时间聚合、只取瞬时点"的是 `avg_without_time`（走 if 分支，不写 time_aggregation）
- 结论：`avg_over_time` 两种模式都带，不是区间模式专属

## 4. 两层聚合（串联执行）

| 层 | 参数 | 聚合维度 | 语义 |
|----|------|---------|------|
| 1 | `time_aggregation.function="avg_over_time"` | 时间维度 | 单条 series 在 [T-window,T] 内原始采集点求平均 |
| 2 | `function[0].method="mean"` | series 维度 | 按 group_by 分组，组内多条 series 求平均，组间隔离 |

- `mean` = 算术平均（InfluxDB MEAN），跨 series 不跨时间点
- `group_by` 是**分组边界**，不同 group 互不混合；mean 是**组内**聚合不是跨组
- group_by 含唯一标识字段（如 pid）时组内通常仅 1 条 series，mean 退化为恒等

## 5. 调用示例

- 符号: `get_process_runtime_metrics`
- 位置: `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`
- 即时模式：interval=180、end_time=now、instant=True → end_time 前 180s 原始点做 avg_over_time，返回单点快照
- 区间模式：interval=max(end-start,60)、instant=None → step=区间长度，整区间一个聚合点

两层聚合在两种模式下完全相同，区别仅在返回点数。
