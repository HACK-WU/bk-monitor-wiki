UnifyQuery.query_log 参数拼装链路，追踪 query_log 的入参如何拼成 HTTP 请求参数，并重点标注它与基线 query_data 的差异。query_log 主要服务于 LOG 类数据源，逐条剥离聚合（function/field_name/time_aggregation 清空），走 POST /query/ts/raw 端点。

## 一、链路总览

```
UnifyQuery.query_log(start_time, end_time, limit, offset, order_by, ...)
   ▼
UnifyQuery._query_log_using_unify_query(limit, offset, order_by, time_alignment)
   │  params = get_unify_query_params(..., order_by)
   │  逐条 query.update({"function": [], "field_name": "", "time_aggregation": {}})   ← 剥离聚合
   │  params["limit"] = limit or 1;  params["_from"] = offset or 0
   │  params["timezone"] = get_current_timezone_name()
   ▼
api.unify_query.query_raw(**params)      ← POST /query/ts/raw（_from→from 重命名）
```

## 二、与 query_data 的差异（核心）

| 维度 | query_data | query_log |
|------|-----------|-----------|
| 内部入口 | `_query_unify_query` | `_query_log_using_unify_query` |
| HTTP 接口 | POST /query/ts | **POST /query/ts/raw** |
| query_list 聚合 | 保留 `function/time_aggregation/field_name` | **逐条剥离**：`function=[]`、`field_name=""`、`time_aggregation={}`（原始日志查询无需聚合） |
| 分页 | 顶层 `slimit/limit` | 顶层 `limit` / `_from`（API 层重命名为 `from`） |
| order_by | 默认 `["-_time"]` | 由调用方透传 |
| instant | 支持（step→"1m"） | **不支持**（本链路不读取 instant，不覆盖 step） |
| down_sample_range / not_time_align | 设置 / 透传 | **down_sample_range 不设置；`not_time_align=False` 由 get_unify_query_params 默认写入但 QueryRawResource 未声明→忽略** |
| 返回 | `list[dict]` | **`(list[dict], total)` 二元组**（unify 路径下 `total` 恒为 `0`） |
| 后处理 | `process_unify_query_data` | `process_unify_query_log`（LOG 数据源经 `process_log_by_datasource` 触发） |

## 三、各步详解

### 1. _query_log_using_unify_query

- 符号: `UnifyQuery._query_log_using_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `params = self.get_unify_query_params(start_time, end_time, time_alignment, order_by)`。
- **逐条剥离聚合**（原始日志查询语义）：
  ```python
  for query in params["query_list"]:
      query.update({"function": [], "field_name": "", "time_aggregation": {}})
  ```
- 顶层分页：`params["limit"] = limit or 1`、`params["_from"] = offset or 0`。
- `params["timezone"] = timezone.get_current_timezone_name()`。
- **不处理 `instant`**，故 step 保持 `get_unify_query_params` 原值（不会被强制 "1m"）。
- 调用 `api.unify_query.query_raw(**params)` → `QueryRawResource`。

### 2. API：QueryRawResource

- 符号: `QueryRawResource`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/api/default.py`

- `method = "POST"`，`path = "/query/ts/raw"`。
- `RequestSerializer` 字段：`query_list`、`metric_merge`、`start_time`、`end_time`、`step`、`limit`、`_from`、`space_uid`、`timezone`、`instant`、`order_by`。
- `perform_request` 中 `params["from"] = params.pop("_from", 0)`：因 `from` 是 Python 关键字，内部用 `_from` 承载，真正请求时转回 `from`。
- 与 `QueryDataResource` 相比：**无 `down_sample_range` / `not_time_align`**，多 `limit` / `_from` / `order_by`。

### 3. 后处理

- 符号: `UnifyQuery.process_unify_query_log` / `UnifyQuery.process_log_by_datasource`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `process_unify_query_log`：将日志记录的元数据（`__data_label/__doc_id/__index/__result_table/__parse_failure`）移入 `_meta`，原 `_time` 移入 `_meta["_time_"]`。
- `process_log_by_datasource`：当 `(data_source_label, data_type_label)` ∈ `{BK_APM/LOG, CUSTOM/EVENT, BK_MONITOR_COLLECTOR/LOG, BK_LOG_SEARCH/LOG}` 时，调用 `ds.process_unify_query_log` 做数据源级后处理（如 LOG 数据源的 `_source` 展平）。
- 返回 `(records, total)`：**注意**——在 unify-query 路径下（`use_unify_query()=True`），`query_log` 将 `total` 硬编码为 `0` 并忽略 raw 响应中的总数；只有在走数据源原生路径（`_query_log_using_datasource`）时，`total` 才是真实的日志总数。因此聚焦的 unify-query 路径下 `total` 恒为 `0`。

### 4. 数据源差异：to_unify_query_config（LOG 类 vs TIME_SERIES）

- **TIME_SERIES**（`TimeSeriesDataSource`）：`table_id/field_name/reference_name/dimensions/function/time_aggregation/keep_columns` 完整——但经 `query_log` 后 `function/field_name/time_aggregation` 被清空。
- **LOG 类**（`BaseBkMonitorLogDataSource`）：`to_unify_query_config` 形态本就不同——`field_name=""`、`reference_name=""`、`function=[]`、`time_aggregation={}`、`keep_columns=[]`、`order_by=[]`，且带 `data_source`（bklog/bkapm）、`query_string`、`conditions`（日志操作符映射）。即 LOG 数据源天生就是"无聚合原始查询"形态，与 `query_log` 的剥离逻辑天然契合。

## 四、最终 params 全貌（LOG 数据源，原始查询）

```python
{
    "query_list": [
        {
            "driver": "influxdb",
            "data_source": "bklog",          # LOG 数据源特有
            "table_id": "<index_set 或 result_table>",
            "reference_name": "",
            "field_name": "",                # 被 query_log 清空
            "time_field": "dtEventTimeStamp",
            "dimensions": [...],
            "query_string": "*",
            "conditions": {...},
            "function": [],                  # 被 query_log 清空
            "time_aggregation": {},          # 被 query_log 清空
            "keep_columns": [],
            "order_by": []
        }
    ],
    "metric_merge": "a",
    "order_by": ["-_time"],                  # 由调用方透传
    "step": "<interval>s",                   # 不受 instant 影响（本链路不处理 instant）
    "limit": 100,
    "_from": 0,                              # API 层重命名为 from
    "space_uid": "<...>",
    "bk_tenant_id": "<...>",
    "timezone": "<get_current_timezone_name()>",
    "start_time": "<...>",
    "end_time":   "<...>"
    # 注意：无 instant / down_sample_range；not_time_align=False 由 get_unify_query_params 默认写入但 API 未声明→忽略
}
```

## 五、关键映射小结

| 入参 | 最终落点 |
|------|----------|
| limit / offset | 顶层 `limit` / `_from`（API 层转 `from`） |
| order_by | 透传到顶层 `order_by` |
| function / field_name / time_aggregation | **逐条被 `query_log` 清空**（原始日志语义） |
| instant | **本链路忽略**（不覆盖 step） |
| down_sample_range / not_time_align | **不设置** |
| 返回 | `(records, total)` 二元组 |
| LOG 数据源 | `to_unify_query_config` 自带 `query_string/conditions/data_source`，与 `query_log` 剥离逻辑契合 |
