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
      "columns": ["_time", "_value"],
      "types": ["time", "double"],
      "group_keys": ["bk_target_ip"],
      "group_values": ["10.0.0.1"],
      "values": [[1657848000, 42.3]],
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

## 请求字段说明

请求体为 `QueryPromQL`（`query/structured/query_promql.go#L27-L54`）。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `promql` | string | 是 | PromQL 查询语句 |
| `start` | string | 是 | 开始时间 |
| `end` | string | 是 | 结束时间 |
| `step` | string | 否 | 步长，如 `"1m"` |
| `bk_biz_ids` | array[string] | 否 | 业务 ID 列表 |
| `max_source_resolution` | string | 否 | 最大源分辨率 |
| `not_align_influxdb` | bool | 否 | 是否与 influxdb 对齐 |
| `limit` | int | 否 | 点数限制数量 |
| `slimit` | int | 否 | 维度限制数量 |
| `match` | string | 否 | 匹配 |
| `is_verify_dimensions` | bool | 否 | 是否校验维度 |
| `reference` | bool | 否 | 查询开始时间是否对齐 |
| `not_time_align` | bool | 否 | 查询开始时间与聚合是否对齐 |
| `down_sample_range` | string | 否 | 降采样周期，如 `"5m"` |
| `timezone` | string | 否 | 时区，如 `"Asia/Shanghai"` |
| `look_back_delta` | string | 否 | 偏移量 |
| `instant` | bool | 否 | 是否瞬时数据 |
| `add_dimensions` | array[string] | 否 | 额外聚合维度 |

## 返回字段说明

成功响应为 `PromData`（`service/http/prom_data.go#L22-L32`），HTTP 200、无 `code/data` 包裹：

| 字段 | 类型 | 说明 |
|------|------|------|
| `series` | array[TablesItem] | 时序数据表列表 |
| `status` | object | 状态信息 |
| `trace_id` | string | 链路 ID |
| `is_partial` | bool | 是否为部分数据 |

`TablesItem` 字段及失败响应 `ErrResponse` 见 [结构体查询接口](结构体查询.md#返回字段说明)。PromQL 解析/翻译细节见 [PromQL支持与扩展.md](PromQL支持与扩展.md)。

### 返回字段与请求字段的映射关系

返回为 `PromData`，`TablesItem` 字段与 [结构体查询接口](结构体查询.md#返回字段与请求字段的映射关系) 一致，区别在于分组维度由 **PromQL 文本** 而非结构化 `dimensions` 字段驱动：

| 返回字段 | 与请求字段的映射关系 | 源码依据 |
|---------|-------------------|---------|
| `group_keys` / `group_values` | 来自 PromQL 查询结果 series 的 labels；分组维度由 promql 中的 `by (...)`/`without` 聚合子句与 label matcher `{...}` 决定。示例 `sum(...) by (bk_target_ip)` → `group_keys` 含 `bk_target_ip` | `query/promql/tables.go` L44-L60 由 `sample.Metric` 填充 |
| `columns` / `values` | 仅含 `_time`/`_value`，维度在 `group_values`（同结构体查询） | `prom_data.go` Fill L106-L140 |
| `metric_name` | 通常为空（PromQL 无显式指标名） | `prom_data.go` Fill L105 |
| `result_table_id` / `stat` / `is_partial` | 同结构体查询 | — |

> 本接口的响应示例已同步修正：维度不再写入 `columns`/`values`，而是落在 `group_keys`/`group_values`（如 `by (bk_target_ip)` → `group_keys: ["bk_target_ip"]`）。

章节来源
- [query/structured/query_promql.go](file://bkmonitor-datalink/pkg/unify-query/query/structured/query_promql.go#L27-L54)
- [service/http/register_urls.go](file://bkmonitor-datalink/pkg/unify-query/service/http/register_urls.go#L25-L94)
- [service/http/prom_data.go](file://bkmonitor-datalink/pkg/unify-query/service/http/prom_data.go#L22-L32)
