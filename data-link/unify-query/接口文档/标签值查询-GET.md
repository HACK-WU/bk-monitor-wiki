[待审核]

# 标签值查询接口（GET /query/ts/label/:label_name/values）

<cite>
- [service/http/api.go](file://bkmonitor-datalink/pkg/unify-query/service/http/api.go#L500-L603)
- [service/http/infos.go](file://bkmonitor-datalink/pkg/unify-query/service/http/infos.go#L30-L51)
</cite>

## 目录
- [接口说明](#接口说明)
- [请求示例](#请求示例)
- [请求字段说明](#请求字段说明)
- [响应说明](#响应说明)

## 接口说明

| 项 | 值 |
|----|----|
| 方法 / 路径 | GET `/query/ts/label/:label_name/values` |
| Handler | `HandlerLabelValues` |
| 鉴权 | `MetaData` + `JwtAuth` |
| 用途 | 以 URL 路径参数指定标签名，查询该标签的取值列表（PromQL `label_values` 等价能力） |

`:label_name` 为路径参数；时间范围等通过 query string 传递（语义同 `Params` 的 `start_time`/`end_time`）。响应直接返回数据对象（HTTP 200）；失败 `ErrResponse`（HTTP 400）。

章节来源
- [service/http/api.go](file://bkmonitor-datalink/pkg/unify-query/service/http/api.go#L500-L603)

## 请求示例

```
GET /query/ts/label/bk_target_ip/values?start_time=1657848000&end_time=1657851600&table_id=system.cpu_summary
```
章节来源
- [service/http/api.go](file://bkmonitor-datalink/pkg/unify-query/service/http/api.go#L500-L603)
- [service/http/infos.go](file://bkmonitor-datalink/pkg/unify-query/service/http/infos.go#L30-L51)
## 请求字段说明

`:label_name` 为路径参数；其余参数经 query string 传递，语义同 `Params`（`service/http/infos.go#L30-L51`）：

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `label_name` | 路径 | string | 是 | 标签键名，如 `bk_target_ip` |
| `data_source` | query | string | 是 | 数据源。枚举：`bk_monitor`（别名 `bkmonitor`）、`custom`、`bkdata`、`bklog`、`bkapm` |
| `table_id` | query | string | 是 | 数据实体 ID，格式 `{db}.{measurement}` |
| `metric_name` | query | string | 否 | 指标名 |
| `conditions` | query | object | 否 | 过滤条件 `Conditions`：`field_list`/`condition_list`（枚举 `and`/`or`） |
| `start_time` / `end_time` | query | string | 是 | 起止时间（秒级时间戳） |
| `limit` / `slimit` | query | int | 否 | 限制数量 / 维度限制 |
| `timezone` | query | string | 否 | 时区，如 `"Asia/Shanghai"` |

`ConditionField.op` 枚举：`eq`(等于)、`ne`(不等于)、`req`(正则匹配)、`nreq`(正则不匹配)、`contains`(包含)、`ncontains`(不包含)、`existed`(存在)、`nexisted`(不存在)。

## 响应说明

成功返回标签值（数据对象直接返回 `TagValuesData`，`service/http/info.go#L27-L30`，与 `tag_values` 一致）：

```json
{
  "trace_id": "b4c5d6e7",
  "values": {"bk_target_ip": ["10.0.0.1", "10.0.0.2"]}
}
```

> `values` 的键为路径中的标签名（`label_name`）。失败响应 `ErrResponse`：`{"trace_id": "...", "error": "..."}`。

### 返回字段与请求字段的映射关系

返回为 `TagValuesData`，与 [标签值查询接口](标签值查询.md#返回字段与请求字段的映射关系) 一致；差异在于标签键来自 **URL 路径参数**：

| 返回字段 | 与请求字段的映射关系 |
|---------|-------------------|
| `values` 的键 | 来自路径参数 `label_name`（而非请求体 `keys`） |
| `values` 的值 | 该标签在 `table_id`/`data_source`/`metric_name` 下、满足 `conditions` 与 `start_time`/`end_time` 的全部取值 |
| `trace_id` | 请求追踪 ID |

章节来源
- [service/http/api.go](file://bkmonitor-datalink/pkg/unify-query/service/http/api.go#L500-L603)
- [service/http/info.go](file://bkmonitor-datalink/pkg/unify-query/service/http/info.go#L27-L30)
