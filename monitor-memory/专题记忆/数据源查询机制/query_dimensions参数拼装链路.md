---
groupPath: 专题记忆/数据源查询机制
relation: query_dimensions参数拼装链路
keywords: [query_dimensions, get_dimension_data, InfluxdbDimensionFetcher, to_unify_query_config]
exportedAt: "2026-07-14T03:32:38.835Z"
---
# UnifyQuery.query_dimensions 参数拼装链路

> 调研目标：追踪 `query_dimensions` 的入参如何解析为查询，并重点标注它与基线 `query_data` 的**本质分叉**。
> 定位：本文是「UnifyQuery 全查询链路调研」之一。共享的 `to_unify_query_config` 见 `unify_query_query_data.md`。
> 数据源聚焦：`BK_MONITOR_COLLECTOR / TIME_SERIES`（其 `query_dimensions` 绑定 `InfluxdbDimensionFetcher.query_dimensions`）。

## 一、链路总览

```
UnifyQuery.query_dimensions(dimension_field, limit, start_time, end_time, ...)
   │
   ├─ 单数据源（len(data_sources)==1）
   │     ▼
   │     data_source.query_dimensions(...)        ← BK_MONITOR_COLLECTOR/TIME_SERIES 实际绑定 InfluxdbDimensionFetcher.query_dimensions
   │        │  conditions_param = to_unify_query_config()[0]   ← 复用 query_list 首条配置
   │        ▼  api.unify_query.get_dimension_data(**query_data)  ← POST /query/ts/info/tag_values
   │
   └─ 多数据源（len(data_sources)>1）
         ▼
         self.query_data(start_time, end_time)    ← 回退到 query_data 全量拉取
         → 从返回 records 中按 dimension_field 提取去重维度值
```

> ⚠️ 与 `query_data` 的最大区别：单数据源的 `query_dimensions` **不拼 `query_list/metric_merge/step` 那套时序参数**，而是复用 `to_unify_query_config()[0]` 提取 `table_id/field_name/conditions`，改走 unify-query 的「维度值」接口 `/query/ts/info/tag_values`。因此它**仍然触碰 unify-query**（只是不同端点、不同参数结构），并非"完全不经过 unify-query"。

## 二、与 query_data 的本质差异（核心）

| 维度 | query_data | query_dimensions（单数据源，聚焦数据源） |
|------|-----------|------------------|
| 是否拼时序 unify params | 是（query_list/metric_merge/step/...） | **否**：不拼 query_list/metric_merge/step |
| 实际调用的 unify 端点 | POST /query/ts | POST /query/ts/info/tag_values（`get_dimension_data`） |
| 是否复用 to_unify_query_config | 是（展开全部 metric） | 是（仅取 `[0]` 提取 table_id/field_name/conditions） |
| 内部入口 | `_query_data_internal` → `_query_unify_query` | 直接委托 `data_source.query_dimensions` |
| 目标 | 取指标时序点 | 取某维度字段的**去重值集合** |
| 入参 `dimension_field` | 无 | 指定要枚举的维度字段（list 或 str） |
| 返回 | `list[dict]` | `list`（维度值列表） |

**结论**：`query_dimensions` 与 `query_data` 目的不同。单数据源场景下它**不进入 `get_unify_query_params` 的时序拼装**，而是复用 `to_unify_query_config()[0]` 后改走 unify-query 的「维度值」接口（`get_dimension_data`）。仅当存在多个数据源时，才退化为"用 `query_data` 拉全量再在内存中去重提取维度"。

## 三、各步详解

### 1. UnifyQuery.query_dimensions（query.py:934）

```python
def query_dimensions(self, dimension_field, limit, start_time, end_time, *args, **kwargs):
    if len(self.data_sources) == 1:
        return self.data_sources[0].query_dimensions(
            dimension_field=dimension_field, limit=limit, start_time=start_time, end_time=end_time, *args, **kwargs
        )
    else:
        if isinstance(dimension_field, list):
            dimension_field = dimension_field[0]
        points = self.query_data(start_time, end_time)   # 复用 query_data 链路
        dimensions = set()
        for point in points:
            dimension = point.get(dimension_field)
            if dimension is None:
                continue
            dimensions.add(dimension)
        return list(dimensions)
```

### 2. 单数据源分支：InfluxdbDimensionFetcher.query_dimensions（data_source/__init__.py:762）

聚焦数据源 `BkMonitorTimeSeriesDataSource` 通过 `query_dimensions = InfluxdbDimensionFetcher.query_dimensions`（data_source/__init__.py:1273）绑定此方法：

- `conditions_param = self.to_unify_query_config()[0]`：取首条 query 配置，提取 `table_id` / `field_name` / `conditions`。
- 组装 `query_data`：
  - `info_type = "tag_values"`（维度值枚举语义）
  - `limit`（调用方透传）
  - `table_id = conditions_param["table_id"]`
  - 若 `conditions_param["field_name"]` 非空 → `metric_name = field_name`
  - 若 `start_time` 非空 → `start_time / end_time = ... // 1000`（转为秒级）
  - 若 `conditions_param` 含 `conditions` → 透传 `conditions`
  - `keys = [dimension_field]`（维度字段列表，str 会被包成 list）
  - 若 `kwargs` 含 `space_uid` → 透传 `space_uid`
- 调用 `api.unify_query.get_dimension_data(**query_data)` → `GetDimensionDataResource`（`POST /query/ts/info/tag_values`，见 api/unify_query/default.py:387）。
- 返回维度值列表（由该 Resource 直接返回，无需 Python 侧去重）。

> 即：单数据源的 `query_dimensions` 仍然**触碰 unify-query**（走维度端点），并复用 `to_unify_query_config` 的产物。这与"完全不经过 unify-query"的表述不同，需注意。

> 补充（非聚焦数据源）：`BkDataTimeSeriesDataSource`（data_source/__init__.py:1475）的 `query_dimensions` 给 `dimension_field` 包反引号后调用 `super().query_dimensions` → `TimeSeriesDataSource.query_dimensions`（data_source/__init__.py:1223），后者才走 `_get_queryset` 原生查询（`metrics[:1]`、`group_by=[dimension_field]`）。该路径适用于计算平台类数据源，不在本文聚焦范围内。

### 3. 多数据源分支

退化方案：直接 `self.query_data(...)`（即走完整的 unify-query 时序参数拼装，见基线篇），再在 Python 侧对 `dimension_field` 去重。代价是拉全量数据，仅用于多数据源无法单点枚举维度的兜底场景。

## 四、参数/返回对照

| 场景 | 实际查询路径 | 是否涉及 unify-query | 返回 |
|------|--------------|----------------------|------|
| 单数据源（聚焦） | `InfluxdbDimensionFetcher.query_dimensions` → `get_dimension_data` | 是（/query/ts/info/tag_values，复用 `to_unify_query_config[0]`） | `list`（维度值） |
| 单数据源（BkData 类） | `TimeSeriesDataSource.query_dimensions` → `_get_queryset` | 否（原生查询） | `list`（维度值） |
| 多数据源 | `query_data` → unify-query | 是（复用 query_data 的 params） | `list`（维度值，内存去重） |

## 五、关键映射小结

| 入参 | 落点（聚焦数据源） |
|------|------|
| dimension_field | `keys=[dimension_field]` 透传给 `get_dimension_data` |
| limit | 顶层 `limit` 透传给 `get_dimension_data` |
| table_id / field_name / conditions | 来自 `to_unify_query_config()[0]`，不重新拼装 |
| 与 query_data 关系 | 仅多数据源兜底时复用；单数据源走独立的 unify 维度端点，不拼时序 params |