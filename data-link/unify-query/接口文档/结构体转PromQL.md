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
