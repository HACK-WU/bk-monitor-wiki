UnifyQuery.query_data 参数拼装链路基线篇，追踪 data_source_class(bk_biz_id, interval, metrics, table, group_by) 的入参如何最终拼成 query_data 的 HTTP 请求参数。本文是 UnifyQuery 全查询链路调研的基线篇，其余 query_data_with_stat / query_reference / query_log / query_dimensions 均在此基础上扩展或分叉。

## 一、链路总览

```
data_source_class(bk_biz_id, interval, metrics, table, group_by)
   │  BkMonitorTimeSeriesDataSource(BK_MONITOR_COLLECTOR, TIME_SERIES)
   ▼
DataSource.to_unify_query_config()        ← 每个 metric 展开成一条 query_list 项
   │  query_list = chain(*[ds.to_unify_query_config() for ds in data_sources])
   ▼
UnifyQuery(bk_biz_id, data_sources=[ds], expression="a")
   │
   ▼
UnifyQuery.query_data(...)                ← 公开入口
   ▼
UnifyQuery._query_data_internal(with_series_stat=False)
   │
   ▼
UnifyQuery._query_unify_query()           ← 补 instant / step / down_sample_range / timezone
   │
   ▼
api.unify_query.query_data(**params)      ← POST /query/ts
```

## 二、各步详解

### 1. DataSource.to_unify_query_config

- 符号: `TimeSeriesDataSource.to_unify_query_config`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

`BK_MONITOR_COLLECTOR / TIME_SERIES` 走 `TimeSeriesDataSource.to_unify_query_config`。核心规则：

- **指标平铺**：`metrics` 列表（多指标）被展开成 `query_list` 数组里的多条独立条目；每条携带相同的 `table_id/group_by/time_field/conditions`，但各自有独立的 `field_name / reference_name / keep_columns`。
- **聚合映射**（`method` 非实时时）：
  - `AggMethods` 的 key 是 `*_without_time` 变体（`sum_without_time`/`avg_without_time`/`count_without_time`/`min_without_time`/`max_without_time`）。当 `method` 命中这些 key（如 `avg_without_time`）→ `function[0].method = AggMethods[method].method`（avg_without_time→mean），**不写 `time_aggregation`**（无 `_over_time` 时间窗口，属"PromQL 不带时间聚合"语义）。
  - **其余普通 method（`avg`/`sum`/`count`/`max`/`min` 等）→ 走 `else` 分支**：`time_aggregation = {"function": "<method>_over_time", "window": "<interval>s" 或 "1h"}`，`function[0].method` 经 `{"avg":"mean","count":"sum"}` 映射（其余 method 原样透传）。
  - 分位数 `CpAggMethods`（如 `cp95`）→ 额外带 `vargs_list / position` 到 `time_aggregation`，`function[0].method` 透传。
- `reference_name = (alias or field).lower()`；`table_id = data_label or table.lower()`；`driver = "influxdb"`；`time_field` 默认 `"time"`；`offset/offset_forward` 由 `time_shift` 决定。
- `keep_columns = ["_time", reference_name, *group_by]`。

> 完整示例（含 `system.proc` 进程查询的 4 指标展开）见 wiki 原文，本文不重复粘贴。

### 2. UnifyQuery.get_unify_query_params

- 符号: `UnifyQuery.get_unify_query_params`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `step`：`interval` 有值取 `interval`，否则默认 `"60"` → 形如 `"180s"`。
- `expression`：非空直接用（如 `"a"`）；为空则 `or` 拼接各 `reference_name`。
- `metric_merge = add_expression_functions(expression, functions)`；`functions` 为空 → 原样返回 expression。
- `order_by`：未传 → `["-_time"]`。
- `space_uid = bk_biz_id_to_space_uid(bk_biz_id)`、`bk_tenant_id = bk_biz_id_to_bk_tenant_id(bk_biz_id)`（构造时已由 `set_bk_tenant_id` 注入各 data_source）。
- `start_time/end_time`：`time_alignment=True` 且 `not_time_align=False` → 经 `time_interval_align(sec, step)` **时间对齐**到步长边界。

### 3. UnifyQuery._query_unify_query

- 符号: `UnifyQuery._query_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `instant=True` 触发：`params["instant"] = True`，且 **`step` 被覆盖为 `"1m"`**（固定 1 分钟，忽略原 interval）。
- 补 `down_sample_range = ""`、`timezone = get_current_timezone_name()`。
- 调用 `api.unify_query.query_data(**params)` → `QueryDataResource`。

### 4. API：QueryDataResource

- 符号: `QueryDataResource`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/api/default.py`

- `method = "POST"`，`path = "/query/ts"`。
- `RequestSerializer` 字段：`query_list`、`metric_merge`、`start_time`、`end_time`、`step`、`space_uid`、`down_sample_range`、`timezone`、`instant`、`not_time_align`。
- 返回结构含 `series`（每条带 `group_keys/group_values/columns/types/values/stat`）、`is_partial`、`result_table_id` 等。

### 5. 后处理

- 符号: `UnifyQuery.process_unify_query_data` / `UnifyQuery.process_unify_query_series_stat`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `process_unify_query_data`：从 `series` 的 `group_keys/group_values` 提取维度（剥离 `_tableN` 后缀），`columns` 中 `_time`→`_time_`、`_result/_value`→`_result_`，时间列秒级转毫秒；返回 `list[dict]`。
- `BK_MONITOR_COLLECTOR / TIME_SERIES` **不在** `process_data_by_datasource` 的特例列表（`CUSTOM/EVENT`、`BK_MONITOR_COLLECTOR/LOG`）内，故不额外调用 `ds.process_unify_query_data`，直接返回上述结果。
- `series_stat` 通过 `process_unify_query_series_stat` 计算（见 `query_data_with_stat` 篇），本方法不返回它。

## 三、最终 params 全貌（instant 查询）

```python
{
    "query_list": [ /* 见 to_unify_query_config 展开，每条含 table_id/field_name/reference_name/dimensions/function/time_aggregation/keep_columns 等 */ ],
    "metric_merge": "a",
    "order_by": ["-_time"],
    "step": "1m",                       # instant 查询固定 1m，覆盖原 interval
    "space_uid": "<bk_biz_id_to_space_uid(bk_biz_id)>",
    "bk_tenant_id": "<bk_biz_id_to_bk_tenant_id(bk_biz_id)>",
    "not_time_align": False,
    "start_time": "<time_interval_align(...)>"
    "end_time":   "<time_interval_align(...)>"
    "down_sample_range": "",
    "timezone": "<get_current_timezone_name()>",
    "instant": True
}
```

## 四、关键映射小结

| 入参 | 最终落点 |
|------|----------|
| metrics 多指标 | 平铺为 query_list 多条，各自 reference_name=a0~aN |
| method="AVG" | function[0].method="mean" + time_aggregation={"function":"avg_over_time","window":"<interval>s"} |
| table | table_id（data_label 未传则 table.lower()） |
| group_by | 同时写入 dimensions / function[0].dimensions / keep_columns |
| interval | 决定 time_aggregation.window；普通查询 step="<interval>s"，instant 覆盖为 "1m" |
| expression | metric_merge（UnifyQuery 级表达式，引用 data_source） |
| bk_biz_id | 经 UnifyQuery 转为 space_uid/bk_tenant_id，不直接进 query 项 |

> 注：`bk_biz_id` 传给 `data_source_class` 后主要用于 UnifyQuery 层租户/空间解析（`set_bk_tenant_id`），不出现在 query_list 单条里；最终 params 用 `space_uid/bk_tenant_id` 表达业务归属。
