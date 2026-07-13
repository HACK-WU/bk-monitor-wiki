[待审核]

# PromQL 查询校验接口（POST /check/query/ts/promql）

<cite>
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L94-L142)
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L33-L41)
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
</cite>

## 目录
- [接口说明](#接口说明)
- [请求示例](#请求示例)
- [响应示例](#响应示例)
- [字段说明](#字段说明)

## 接口说明

| 项 | 值 |
|----|----|
| 方法 / 路径 | POST `/check/query/ts/promql` |
| Handler | `HandlerCheckQueryPromQL` |
| 鉴权 | `MetaData` + `JwtAuth` |
| 用途 | 与 `/query/ts/promql` 同请求体，仅做解析与路由校验，不下发真实查询 |

响应 `CheckQueryTsDataResponse`（HTTP 200）；失败 `ErrResponse`（HTTP 400）。

章节来源
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L94-L142)

## 请求示例

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

## 响应示例

```json
{
  "data": [
    {"metricql": "sum(system_cpu_summary_usage{bk_biz_id=\"2\"})"}
  ],
  "route_info": [
    {"table_id": "system.cpu_summary", "db": "influxdb", "is_strict": false}
  ],
  "trace_id": "d4e5f6a7"
}
```

章节来源
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L33-L41)

## 字段说明

- 请求 `QueryPromQL`：`query/structured/query_promql.go#L27-L54`
- 响应 `CheckQueryTsDataResponse`：`service/http/check_handler.go#L33-L41`
- 错误 `ErrResponse`：`service/http/response.go#L96-L99`
章节来源
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L94-L142)
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L33-L41)
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
