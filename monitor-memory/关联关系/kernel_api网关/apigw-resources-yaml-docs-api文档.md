---
groupPath: 关联关系/kernel_api网关
relation: apigw-resources-yaml-docs-api文档
exportedAt: "2026-08-13T11:06:29.563Z"
---
[强关联] apigw resources yaml 资源定义 与 apigw docs API 文档
强度：必改——新增 yaml 资源（新增 operationId）必须在 apigw/docs 目录同步新增同名 API 文档；改 yaml 的请求/响应参数/描述时，对应 md 必须跟着改，漏任一处则文档与网关定义不一致
原因：yaml 的 operationId 与 docs/zh/{operationId}.md 一一对应，docs 是蓝鲸 API 网关对外发布的 API 文档唯一来源，新增 yaml 不同步文档会导致接口无法被调用方正确消费

源端（yaml 资源定义）:
- `data_query.yaml`（operationId: graph_promql_query/time_series_unify_query/grafana_log_query/v2_event_logs/get_variable_value/time_series_functions）@ `bkmonitor/support-files/apigw/resources/external/app/data_query.yaml`
- external/app、external/user、internal/app、internal/user 下全部 *.yaml @ `bkmonitor/support-files/apigw/resources/`
- yaml 关键字段: operationId（资源唯一标识）、backend.path（指向 kernel_api 的 /api/v4/... 端点）、authConfig

目标端（API 文档）:
- docs/zh/{operationId}.md @ `bkmonitor/support-files/apigw/docs/zh/`（如 time_series_functions.md、graph_promql_query.md）
- 每个 md 含功能描述/请求参数/响应参数/示例，字段与 yaml 对应 Resource 一致

新增规则:
- 新增 yaml 资源 → 必须在 docs/zh/ 新增 {operationId}.md
- 修改 yaml 参数 → 必须同步更新对应 md
- backend.path 变更 → 同时核对 kernel_api 对应 v4 视图端点