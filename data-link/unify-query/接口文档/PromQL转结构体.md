[待审核]

# PromQL 转结构体接口（POST /query/ts/promql_to_struct）

<cite>
- [service/http/handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/handler.go#L37-L78)
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
- [query/structured/query_ts.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_ts.go#L42-L112)
</cite>

## 目录
- [接口说明](#接口说明)
- [请求示例](#请求示例)
- [响应示例](#响应示例)

## 接口说明

| 项 | 值 |
|----|----|
| 方法 / 路径 | POST `/query/ts/promql_to_struct` |
| Handler | `HandlerPromQLToStruct` |
| 鉴权 | `MetaData` + `JwtAuth` |
| 用途 | 调试类：将 PromQL 文本反向解析为 `QueryTs` 结构体，便于前后端结构互转 |

响应为 `{"data": QueryTs}`（HTTP 200）；失败 `ErrResponse`（HTTP 400）。

章节来源
- [service/http/handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/handler.go#L37-L78)

## 请求示例

```json
{
  "promql": "sum(system_cpu_summary_usage{bk_biz_id=\"2\"}) by (bk_target_ip)",
  "start": "1657848000",
  "end": "1657851600",
  "step": "1m"
}
```

章节来源
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)

## 响应示例

```json
{
  "data": {
    "space_uid": "",
    "query_list": [
      {
        "reference_name": "a",
        "table_id": "system.cpu_summary",
        "field_name": "usage",
        "function": [{"method": "MEAN", "dimensions": ["bk_target_ip"]}],
        "time_aggregation": {"method": "SUM", "window": "1m"}
      }
    ],
    "metric_merge": "a",
    "start_time": "1657848000",
    "end_time": "1657851600",
    "step": "1m"
  }
}
```

章节来源
- [query/structured/query_ts.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_ts.go#L42-L112)
