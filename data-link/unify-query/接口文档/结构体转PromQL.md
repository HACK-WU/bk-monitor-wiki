[待审核]

# 结构体转 PromQL 接口（POST /query/ts/struct_to_promql）

<cite>
- [service/http/handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/handler.go#L91-L130)
- [query/structured/query_ts.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_ts.go#L42-L112)
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
</cite>

## 目录
- [接口说明](#接口说明)
- [请求示例](#请求示例)
- [响应示例](#响应示例)
- [请求字段说明](#请求字段说明)
- [返回字段说明](#返回字段说明)

## 接口说明

| 项 | 值 |
|----|----|
| 方法 / 路径 | POST `/query/ts/struct_to_promql` |
| Handler | `HandlerStructToPromQL` |
| 鉴权 | `MetaData` + `JwtAuth` |
| 用途 | 调试类：将 `QueryTs` 结构体翻译为等价的 PromQL 文本，便于对比与排障 |

响应直接返回 `QueryPromQL` 对象（HTTP 200，无 `code/data` 包裹）；失败 `ErrResponse`（HTTP 400）。

章节来源
- [service/http/handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/handler.go#L91-L130)

## 请求示例

```json
{
  "space_uid": "bkcc__2",
  "query_list": [
    {
      "reference_name": "a",
      "table_id": "system.cpu_summary",
      "field_name": "usage",
      "function": [{"method": "MEAN"}],
      "time_aggregation": {"method": "SUM", "window": "1m"}
    }
  ],
  "metric_merge": "a",
  "start_time": "1657848000",
  "end_time": "1657851600",
  "step": "1m"
}
```

章节来源
- [query/structured/query_ts.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_ts.go#L42-L112)

## 响应示例

```json
{
  "promql": "sum(system_cpu_summary_usage{bk_biz_id=\"2\"})",
  "start": "1657848000",
  "end": "1657851600",
  "step": "1m"
}
```

章节来源
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)

## 请求字段说明

请求体为 `QueryTs`（`query_ts.go#L42-L112`）。完整字段表见[结构体查询-请求字段说明](结构体查询.md#请求字段说明)，此处列出常用字段：

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| space_uid | string | 是 | 空间 ID，如 `bkcc__2` |
| query_list | array(Query) | 是 | 查询实例列表，详见[结构体查询-请求字段说明](结构体查询.md#请求字段说明)之子查询 `Query` 表（`data_source` 等可枚举字段亦在其中） |
| metric_merge | string | 否 | 多查询合并表达式，支持 PromQL 语法，如 `"a"` |
| start_time | string | 是 | 开始时间（Unix 秒字符串） |
| end_time | string | 是 | 结束时间（Unix 秒字符串） |
| step | string | 是 | 步长，如 `"1m"` |
| down_sample_range | string | 否 | 降采样区间，须大于 `step` 才生效，如 `"5m"` |
| instant | bool | 否 | 是否查询瞬时数据 |
| time_aggregation | object | 否 | 时间聚合（位于 `query_list[]` 内）：`method` 可枚举见[结构体查询-请求字段说明](结构体查询.md#请求字段说明)，`window` 为聚合窗口 |

## 返回字段说明

响应直接返回 `QueryPromQL` 对象（`query_promql.go#L27-L54`），HTTP 200，无 `code`/`data` 包裹：

| 字段 | 类型 | 说明 |
|------|------|------|
| promql | string | 由 `QueryTs` 翻译得到的 PromQL 文本 |
| start | string | 开始时间（Unix 秒字符串） |
| end | string | 结束时间（Unix 秒字符串） |
| step | string | 步长 |

> 失败返回 `ErrResponse`（HTTP 400），结构见[结构体查询-返回字段说明](结构体查询.md#返回字段说明)。

### 返回字段与请求字段的映射关系

返回为 `QueryPromQL`，是请求 `QueryTs` 的**正向翻译**，字段一一对应：

| 返回字段 | 与请求字段的映射关系 |
|---------|-------------------|
| `promql` | 由请求 `query_list`（含 `table_id`/`field_name`/`function`/`conditions`/`dimensions` 等）翻译为等价的 PromQL 文本；`metric_merge` 映射为 PromQL 中的多指标运算 |
| `start` / `end` | 来自请求 `start_time` / `end_time` |
| `step` | 来自请求 `step` |

> 即请求是"结构化描述"，返回是"等价的 PromQL 表达"，二者互为可逆转换（反向见 [PromQL 转结构体接口](PromQL转结构体.md)）。

章节来源
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
