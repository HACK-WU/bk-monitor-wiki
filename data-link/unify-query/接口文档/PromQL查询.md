[待审核]

# PromQL 查询接口（POST /query/ts/promql）

<cite>
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
- [service/http/register_urls.go](file://bkmonitor-datalink/pkg/unify-query/service/http/register_urls.go#L25-L94)
- [service/http/prom_data.go](file://bkmonitor-datalink/pkg/unify-query/service/http/prom_data.go#L22-L32)
</cite>

## 目录
- [接口说明](#接口说明)
- [请求示例](#请求示例)
- [响应示例](#响应示例)
- [字段说明](#字段说明)

## 接口说明

| 项 | 值 |
|----|----|
| 方法 / 路径 | POST `/query/ts/promql` |
| Handler | `HandlerQueryPromQL` |
| 鉴权 | `MetaData` + `JwtAuth` |
| 用途 | 以 PromQL 文本发起查询，由引擎解析后翻译到各存储后端 |

响应约定同 `/query/ts`：成功直接返回 `PromData`（HTTP 200）；失败时 `ErrResponse`（HTTP 400）。

章节来源
- [service/http/register_urls.go](file://bkmonitor-datalink/pkg/unify-query/service/http/register_urls.go#L25-L94)

## 请求示例

```json
{
  "promql": "sum(system_cpu_summary_usage{bk_biz_id=\"2\"}) by (bk_target_ip)",
  "start": "1657848000",
  "end": "1657851600",
  "step": "1m",
  "bk_biz_ids": ["2"],
  "down_sample_range": "5m",
  "timezone": "Asia/Shanghai",
  "instant": false
}
```

章节来源
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)

## 响应示例

```json
{
  "series": [
    {
      "name": "_result0",
      "metric_name": "",
      "columns": ["_time", "_value", "bk_target_ip"],
      "types": ["time", "double", "string"],
      "group_keys": ["bk_target_ip"],
      "group_values": ["10.0.0.1"],
      "values": [[1657848000, 42.3, "10.0.0.1"]],
      "stat": {"avg": 42.3, "max": 42.3, "min": 42.3, "count": 1}
    }
  ],
  "status": {"series_limit_reached": false, "is_partial": false},
  "trace_id": "c3d4e5f6",
  "is_partial": false
}
```

章节来源
- [service/http/prom_data.go](file://bkmonitor-datalink/pkg/unify-query/service/http/prom_data.go#L22-L32)

## 字段说明

- 请求 `QueryPromQL`：`query/structured/query_promql.go#L27-L54`（`promql`/`start`/`end`/`step`/`bk_biz_ids`/`down_sample_range`/`timezone`/`instant` 等）
- 响应 `PromData`：`service/http/prom_data.go#L22-L32`
- 错误 `ErrResponse`：`service/http/response.go#L96-L99`
- PromQL 解析/翻译细节见 [PromQL支持与扩展.md](PromQL支持与扩展.md)
章节来源
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
- [service/http/register_urls.go](file://bkmonitor-datalink/pkg/unify-query/service/http/register_urls.go#L25-L94)
- [service/http/prom_data.go](file://bkmonitor-datalink/pkg/unify-query/service/http/prom_data.go#L22-L32)
