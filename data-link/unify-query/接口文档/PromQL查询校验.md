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
    {"table_id": "system.cpu_summary", "db": "influxdb"}
  ],
  "trace_id": "d4e5f6a7"
}
```

章节来源
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L33-L41)

## 请求字段说明

请求体为 `QueryPromQL`（与 [PromQL查询接口](PromQL查询.md#请求字段说明) 一致）。校验接口仅做解析与路由校验，不下发真实查询。

## 返回字段说明

成功响应为 `CheckQueryTsDataResponse`（`service/http/check_handler.go#L33-L41`），HTTP 200、直接返回数据对象：

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | array[any] | 各子查询对应 `tsdb.Instance.GetRequestBody` 的序列化预览体；仅路由预览（无存储预览体）时可为空仍返回 200 |
| `route_info` | array[RouteInfo] | 与子查询一一对应的路由摘要，用于排障 |
| `trace_id` | string | 链路 ID |

### RouteInfo（route_info 元素）

`metadata/struct.go#L374-L384`。

| 字段 | 类型 | 说明 |
|------|------|------|
| `reference_name` | string | 子查询别名 |
| `metric_name` | string | 指标名 |
| `table_id` | string | 结果表 ID，格式 `{db}.{measurement}` |
| `db` | string | 数据库名 |
| `data_label` | string | 数据标签 |
| `data_source` | string | 数据源 |
| `storage_type` | string | 存储类型 |
| `storage_id` | string | 存储 ID |
| `measurement` | string | 数据表名 |

错误响应为 `ErrResponse`：`{"trace_id": "...", "error": "..."}`。

### 返回字段与请求字段的映射关系

返回为 `CheckQueryTsDataResponse`，是请求的**校验/预览**结果：

| 返回字段 | 与请求字段的映射关系 |
|---------|-------------------|
| `data` | 由请求 `promql` 翻译生成的预览体 |
| `route_info` | 与请求（promql 解析出的各子查询）一一对应的路由摘要；`reference_name`/`table_id`/`db`/`data_source`/`storage_type` 由 promql 解析 + 路由得到 |
| `trace_id` | 请求追踪 ID |

章节来源
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L94-L142)
- [service/http/check_handler.go](file://bkmonitor-datalink/pkg/unify-query/service/http/check_handler.go#L33-L41)
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
- [metadata/struct.go](file://bkmonitor-datalink/pkg/unify-query/metadata/struct.go#L374-L384)
