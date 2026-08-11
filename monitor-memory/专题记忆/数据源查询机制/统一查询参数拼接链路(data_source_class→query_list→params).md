统一查询参数拼接链路：data_source_class → query_list → params，追踪 data_source_class(bk_biz_id, interval, metrics, table, group_by) 的入参如何最终拼成统一查询的 HTTP 请求参数。metrics 列表被平铺成 query_list 数组里的多条独立条目，每条携带相同的 table/group_by/time_aggregation，但各自有独立的 field_name/reference_name/keep_columns。

## 一、拼接链路总览

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
UnifyQuery.get_unify_query_params()       ← 顶层参数 + query_list 组装成 params
   │
   ▼
UnifyQuery._query_unify_query()           ← 补 instant/step/down_sample/timezone
   │
   ▼
api.unify_query.query_data(**params)      ← 最终 HTTP 调用
```

关键点：**统一查询参数拼接**时，metrics 列表（多指标）被**平铺（flatten）**成 query_list 数组里的多条独立条目；每条都携带相同的 table/group_by/time_aggregation，但各自有独立的 field_name/reference_name/keep_columns。

## 二、各步详解

### 1. DataSource.to_unify_query_config

- 符号: `DataSource.to_unify_query_config`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

入参（以 cc/resources/cmdb.py 进程查询为例）：
```python
METRIC_FIELDS = ["cpu_usage_pct", "mem_res", "mem_usage_pct", "uptime"]
DIM_FIELDS    = ["pid", "username"]
metrics = [
  {"field": "cpu_usage_pct", "method": "AVG", "alias": "A0"},
  {"field": "mem_res",       "method": "AVG", "alias": "A1"},
  {"field": "mem_usage_pct", "method": "AVG", "alias": "A2"},
  {"field": "uptime",        "method": "AVG", "alias": "A3"},
]
group_by = ["bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"]
```

**指标聚合映射**（method=AVG，"avg" 不在 AggMethods 带 `_without_time` 后缀的集合，走 else 分支）：
- `time_aggregation = {"function": "avg_over_time", "window": "180s"}`（由 interval=180 决定）
- `function = [{"method": "mean", "dimensions": <group_by>}]`（method_mapping 把 avg→mean）
- `reference_name = alias.lower()` → `a0/a1/a2/a3`
- `table_id = data_label or table` → data_label 未传(默认"")，故 `"system.proc"`
- `time_field` 未传 → 默认 `"time"`
- `conditions`：filter_dict/where 均为空 → `{"field_list": [], "condition_list": []}`

每条 query_list 项（以 cpu_usage_pct 为例）：
```python
{
    "table_id": "system.proc",
    "time_aggregation": {"function": "avg_over_time", "window": "180s"},
    "field_name": "cpu_usage_pct",
    "reference_name": "a0",
    "dimensions": ["bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"],
    "driver": "influxdb",
    "time_field": "time",
    "conditions": {"field_list": [], "condition_list": []},
    "function": [{"method": "mean", "dimensions": ["bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"]}],
    "offset": "", "offset_forward": False,
    "keep_columns": ["_time", "a0", "bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"]
}
```
mem_res/a1、mem_usage_pct/a2、uptime/a3 同理，仅 field_name/reference_name/keep_columns 第二项不同。

### 2. UnifyQuery.get_unify_query_params

- 符号: `UnifyQuery.get_unify_query_params`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `step`：interval=180 → `"180s"`
- `expression`：self.expression="a" 非空 → 直接用 "a"
- `metric_merge = add_expression_functions("a", [])` → functions 为空 → 返回 "a"
- `order_by`：未传 → `["-_time"]`
- `space_uid = bk_biz_id_to_space_uid(bk_biz_id)`、`bk_tenant_id = bk_biz_id_to_bk_tenant_id(bk_biz_id)`
- `start_time/end_time`：time_alignment=True 且 not_time_align=False → 经 `time_interval_align(sec, 180)` **时间对齐**到 180s 边界

### 3. UnifyQuery._query_unify_query

- 符号: `UnifyQuery._query_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

**瞬时查询**（instant=True）触发：`params["instant"]=True`，且 **step 被覆盖为 `"1m"`**；再补 `down_sample_range=""`、`timezone=<当前时区>`。

## 三、最终参数全貌（instant 查询）

```python
{
    "query_list": [
        {"table_id": "system.proc", "time_aggregation": {"function": "avg_over_time", "window": "180s"},
         "field_name": "cpu_usage_pct", "reference_name": "a0",
         "dimensions": ["bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"],
         "driver": "influxdb", "time_field": "time", "conditions": {"field_list": [], "condition_list": []},
         "function": [{"method": "mean", "dimensions": ["bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"]}],
         "offset": "", "offset_forward": False,
         "keep_columns": ["_time", "a0", "bk_host_id", "bk_target_ip", "bk_target_cloud_id", "display_name", "pid", "username"]},
        # mem_res/a1、mem_usage_pct/a2、uptime/a3 同结构，仅 field_name/reference_name/keep_columns 第二项不同
    ],
    "metric_merge": "a",
    "order_by": ["-_time"],
    "step": "1m",                       # instant 查询固定 1m，覆盖原 180s
    "space_uid": "<bk_biz_id_to_space_uid(bk_biz_id)>",
    "bk_tenant_id": "<bk_biz_id_to_bk_tenant_id(bk_biz_id)>",
    "not_time_align": False,
    "start_time": "<time_interval_align((now-180000)//1000, 180)>",
    "end_time":   "<time_interval_align(now//1000, 180)>",
    "down_sample_range": "",
    "timezone": "<get_current_timezone_name()>",
    "instant": True
}
```

## 四、关键映射小结

| 入参 | 最终落点 |
|------|----------|
| metrics 多指标 | 平铺为 query_list 的多条，各自 reference_name=a0~a3 |
| method="AVG" | function[0].method="mean" + time_aggregation={"function":"avg_over_time","window":"180s"} |
| table="system.proc" | table_id="system.proc"（data_label 未传） |
| group_by | 同时写入 dimensions 与 function[0].dimensions 与 keep_columns |
| interval=180 | 决定 time_aggregation.window="180s"；普通查询 step="180s"，instant 覆盖为 "1m" |
| expression="a" | metric_merge="a"（UnifyQuery 级表达式，引用 data_source） |
| bk_biz_id | 经 UnifyQuery 转为 space_uid/bk_tenant_id，不直接进 query 项 |

注：bk_biz_id 传给 data_source_class 后主要用于 UnifyQuery 层的租户空间解析（set_bk_tenant_id），并不出现在 query_list 单条里；最终 params 用 space_uid/bk_tenant_id 表达业务归属。
