UnifyQuery.query_reference 参数拼装链路，追踪 query_reference 的入参如何拼成 HTTP 请求参数，并重点标注它与基线 query_data 的差异。query_reference 逐条注入 limit/from 分页，透传 order_by，走 POST /query/ts/reference 端点，不计算 series_stat。

## 一、链路总览

```
UnifyQuery.query_reference(start_time, end_time, limit, offset, order_by, ...)
   ▼
UnifyQuery._query_reference_using_unify_query(limit, offset, time_alignment, instant, order_by)
   │  params = get_unify_query_params(..., order_by)   ← 与 query_data 同函数，但透传 order_by
   │  逐条 query.update({"limit": limit or 1, "from": offset or 0})
   │  instant → params["instant"]=instant, params["step"]="1m"
   │  params["timezone"] = get_current_timezone_name()
   ▼
api.unify_query.query_reference(**params)   ← POST /query/ts/reference
```

## 二、与 query_data 的差异（核心）

| 维度 | query_data | query_reference |
|------|-----------|-----------------|
| 内部入口 | `_query_unify_query` | `_query_reference_using_unify_query` |
| HTTP 接口 | POST /query/ts | **POST /query/ts/reference** |
| query_list 来源 | `to_unify_query_config`（同） | **同**（无聚合剥离） |
| 每条 query 附加 | 无 | **`limit` / `from`**（分页：`limit or 1` / `offset or 0`） |
| order_by | 走默认 `["-_time"]` | **由调用方透传**（`get_unify_query_params(order_by=...)`） |
| down_sample_range | 补 `""` | **不设置** |
| not_time_align | 透传（默认 False） | **params 含 `not_time_align=False`（来自 get_unify_query_params 默认），但 QueryReferenceResource 未声明该字段→API 忽略** |
| instant | 支持（step→"1m"） | **支持**（step→"1m"） |
| timezone | 补 | 补 |
| series_stat | 计算但不返回 | **不计算**（未调用 `process_unify_query_series_stat`） |
| 返回 | `list[dict]` | `list[dict]` |

## 三、各步详解

### 1. _query_reference_using_unify_query

- 符号: `UnifyQuery._query_reference_using_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`

- `params = self.get_unify_query_params(start_time, end_time, time_alignment, order_by)`：`order_by` 由调用方传入（可为 `["-_time"]` 或带维度的排序）。
- **逐条 query 注入分页**：
  ```python
  for query in params["query_list"]:
      query.update({"limit": limit or 1, "from": offset or 0})
  ```
  > 注意：分页是**每条子查询**级别的 `limit/from`，与 `query_data` 顶层 `slimit/limit` 语义不同。
- `instant` 处理与 `query_data` 一致：`params["instant"]=instant`、`params["step"]="1m"`。
- `params["timezone"] = timezone.get_current_timezone_name()`。
- 调用 `api.unify_query.query_reference(**params)` → `QueryReferenceResource`。

### 2. API：QueryReferenceResource

- 符号: `QueryReferenceResource`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/api/default.py`

- `method = "POST"`，`path = "/query/ts/reference"`。
- `RequestSerializer` 字段：`query_list`、`metric_merge`、`start_time`、`end_time`、`step`、`space_uid`、`timezone`、`instant`、`order_by`、`look_back_delta`（**默认 `"1m"`**）。
- 与 `QueryDataResource` 相比：**无 `down_sample_range` / `not_time_align`**，多 `order_by` / `look_back_delta`。

### 3. 后处理

- 同样走 `process_unify_query_data`（维度提取 + `_result_` 归一化），再经 `process_data_by_datasource`（TIME_SERIES 不触发 ds 级后处理）。
- **不调用** `process_unify_query_series_stat`，故无 `series_stat`。

## 四、最终 params 全貌（带分页 + order_by）

```python
{
    "query_list": [
        {
            # to_unify_query_config 展开项（同 query_data）
            "limit": 100,          # 逐条注入：limit or 1
            "from": 0              # 逐条注入：offset or 0
        }
    ],
    "metric_merge": "a",
    "order_by": ["-_time"],        # 由调用方透传
    "step": "1m",                  # instant 时固定 1m
    "space_uid": "<...>",
    "bk_tenant_id": "<...>",
    "timezone": "<get_current_timezone_name()>",
    "instant": True,               # 可选
    "start_time": "<...>",
    "end_time":   "<...>",
    # 注意：无 down_sample_range；not_time_align=False 由 get_unify_query_params 默认写入，但 QueryReferenceResource 未声明→被忽略
}
```

## 五、关键映射小结

| 入参 | 最终落点 |
|------|----------|
| limit / offset | 注入到 **每条 query_list 项** 的 `limit` / `from`（非顶层） |
| order_by | 透传到 `get_unify_query_params(order_by=...)` → 顶层 `order_by`（调用方通常传单字段字符串；为 None 时默认 `["-_time"]`） |
| look_back_delta | API 层默认 `"1m"`（调用方通常不传） |
| instant | 同 query_data（step→"1m"） |
| down_sample_range / not_time_align | **本链路不设置** |
| 其余 | 与 `query_data` 完全一致（见基线篇第四节） |
