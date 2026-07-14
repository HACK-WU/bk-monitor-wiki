---
groupPath: 专题记忆/数据源查询机制
relation: query_data_with_stat参数拼装链路
keywords: [query_data_with_stat, process_unify_query_series_stat]
exportedAt: "2026-07-14T03:31:22.838Z"
---
# UnifyQuery.query_data_with_stat 参数拼装链路

> 调研目标：追踪 `query_data_with_stat` 的入参如何拼成 HTTP 请求参数，并重点标注它与基线 `query_data` 的差异。
> 定位：本文是「UnifyQuery 全查询链路调研」之一。前置见 `unify_query_query_data.md`（共享的 `to_unify_query_config` / `get_unify_query_params` 不再复述）。

## 一、链路总览

```
UnifyQuery.query_data_with_stat(...)
   ▼
UnifyQuery._query_data_internal(with_series_stat=True)   ← 唯一与 query_data 的分叉点
   │
   ▼
UnifyQuery._query_unify_query()           ← 与 query_data 完全相同
   │
   ▼
api.unify_query.query_data(**params)      ← POST /query/ts（同一接口）
```

## 二、与 query_data 的差异（核心）

| 维度 | query_data | query_data_with_stat |
|------|-----------|----------------------|
| 内部入口 | `_query_data_internal(with_series_stat=False)` | `_query_data_internal(with_series_stat=True)` |
| HTTP 接口 | POST /query/ts | **POST /query/ts（完全相同）** |
| params 拼装 | 完全一致 | **完全一致（无额外参数）** |
| 返回结构 | `list[dict]` | `{"series": list[dict], "series_stat": dict}` |
| series_stat | 计算但不返回（unify 路径下被 `_query_data_internal` 丢弃） | `process_unify_query_series_stat(params, data)` 计算后随返回值带出 |

**结论**：`query_data_with_stat` 与 `query_data` 走**完全相同的参数拼装链路**，唯一区别是 `with_series_stat=True` 开关，使内部在拿到 unify-query 返回后额外聚合 `series_stat` 并以 `dict` 形式返回。其 `params` 全貌与 `query_data`（见基线篇第三节）一字不差。

## 三、series_stat 的拼装（query.py:277 / 534）

- unify-query 返回的每个 `series` 自带 `stat`（如 `{"avg":12.8,"max":13.1,"min":12.5,"count":2}`），无 stat 时为空 dict。
- `process_unify_query_series_stat` 遍历 `data["series"]`，以 **`(dimensions, metric_field)` 二元组** 为 key 归并：
  - `dimensions = get_unify_query_series_dimensions(row)`：`group_keys/group_values` 提取维度后排序为 tuple（可哈希、可作 dict key）。
  - `metric_field = get_unify_query_series_metric_field(row, params)`：首列若为 `_result/_value` 或命中 `reference_names` → `"_result_"`；否则返回该列名。
- 最终：`series_stat[(dimensions, metric_field)] = stat`。

## 四、返回结构示例

```python
{
    "series": [
        {"bk_target_ip": "10.0.0.1", "_time_": 1657848000000, "_result_": 12.5},
        {"bk_target_ip": "10.0.0.1", "_time_": 1657848060000, "_result_": 13.1}
    ],
    "series_stat": {
        (("bk_target_ip", "10.0.0.1"), "_result_"): {
            "avg": 12.8, "max": 13.1, "min": 12.5, "count": 2
        }
    }
}
```

## 五、关键映射小结

| 入参 | 最终落点 |
|------|----------|
| with_series_stat=True | 触发 `process_unify_query_series_stat`，返回值由 `list` 变为 `{"series","series_stat"}` |
| 其余所有入参 | 与 `query_data` 完全一致（见基线篇第四节） |