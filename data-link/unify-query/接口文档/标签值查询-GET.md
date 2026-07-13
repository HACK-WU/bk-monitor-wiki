[待审核]

# 标签值查询接口（GET /query/ts/label/:label_name/values）

<cite>
- [service/http/api.go](file://bkmonitor-datalink/pkg/unify-query/service/http/api.go#L500-L603)
- [service/http/infos.go](file://bkmonitor-datalink/pkg/unify-query/service/http/infos.go#L30-L51)
</cite>

## 目录
- [接口说明](#接口说明)
- [请求示例](#请求示例)
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
## 响应说明

```json
{
  "list": ["10.0.0.1", "10.0.0.2"],
  "trace_id": "b4c5d6e7"
}
```

章节来源
- [service/http/infos.go](file://bkmonitor-datalink/pkg/unify-query/service/http/infos.go#L30-L51)
