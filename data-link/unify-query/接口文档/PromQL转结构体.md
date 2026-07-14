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
- [请求字段说明](#请求字段说明)
- [返回字段说明](#返回字段说明)

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

## 请求字段说明

请求体为 `QueryPromQL`（`query_promql.go#L27-L54`），完整字段表亦见[PromQL查询-请求字段说明](PromQL查询.md#请求字段说明)：

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| promql | string | 是 | 待反解的 PromQL 文本 |
| start | string | 是 | 开始时间（Unix 秒字符串） |
| end | string | 是 | 结束时间（Unix 秒字符串） |
| step | string | 否 | 步长，如 `"1m"` |
| bk_biz_ids | array(string) | 否 | 业务 ID 列表，用于鉴权与路由 |
| max_source_resolution | string | 否 | 源数据最大分辨率 |
| not_align_influxdb | bool | 否 | 是否不与 influxdb 对齐 |
| limit | int | 否 | 限制点数 |
| slimit | int | 否 | 限制序列数 |
| match | string | 否 | 序列匹配表达式 |
| is_verify_dimensions | bool | 否 | 是否校验维度 |
| reference | bool | 否 | 查询开始时间是否需要对齐 |
| not_time_align | bool | 否 | 查询开始时间与聚合是否需要对齐 |
| down_sample_range | string | 否 | 降采样区间，须大于 `step` 才生效 |
| timezone | string | 否 | 时区，如 `Asia/Shanghai` |
| look_back_delta | string | 否 | 偏移量，如 `"1h"` |
| instant | bool | 否 | 是否瞬时数据 |
| add_dimensions | array(string) | 否 | 额外追加的聚合维度 |

## 返回字段说明

响应为 `{"data": QueryTs}`（HTTP 200），`data` 即完整的 `QueryTs` 结构体。其字段说明见[结构体查询-请求字段说明](结构体查询.md#请求字段说明)（`space_uid` / `query_list` / `metric_merge` / `start_time` / `end_time` / `step` 等），响应示例中的 `function[].method`、`time_aggregation.method` 等可枚举取值亦在该处列出。

### 返回字段与请求字段的映射关系

返回为 `{"data": QueryTs}`，是请求 `QueryPromQL` 的**反向解析**，`data` 即反解出的结构化查询：

| 返回字段（`data` 内） | 与请求字段的映射关系 |
|---------|-------------------|
| `query_list[].table_id` / `field_name` | 由请求 `promql` 的 metric 名（如 `system_cpu_summary_usage`）反解为 `table_id`+`field_name` |
| `query_list[].function` / `dimensions` | 由 promql 的聚合函数与 `by (...)`/`without` 子句反解（`function[].method`/`dimensions`） |
| `query_list[].conditions` | 由 promql 的 label matcher `{...}` 反解为过滤条件 |
| `start_time` / `end_time` / `step` | 来自请求 `start` / `end` / `step` |
| `metric_merge` | 由 promql 多指标运算反解（若仅有单指标则为子查询别名） |

> 与 [结构体转 PromQL 接口](结构体转PromQL.md) 互为可逆。

章节来源
- [query/structured/query_ts.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_ts.go#L42-L112)
