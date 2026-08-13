---
groupPath: 关联关系/kernel_api网关
relation: resource-views_v4复用
exportedAt: "2026-08-13T09:12:22.344Z"
---
[强关联] resource/ 内部 Resource 与 views/v4 ViewSet 复用
强度：必改——改 resource/ 下 Resource 的签名/行为/返回结构时，views/v4 中所有复用该 Resource 的 ViewSet 必须跟着改；改 ViewSet 装配逻辑，被复用的 Resource 不用动
原因：resource/ 是批发场景复用层，常做薄封装后被多个 ViewSet 在 perform_request 中调用，Resource 契约变更级联影响所有复用方

源端（内部 Resource）：
- `ListAlertResource` / `SearchAlarmStrategiesResource` / `AlertRelatedResource` @ `bkmonitor/kernel_api/resource/alert.py`
- `SearchLogResource` / `GetIndexSetListResource` @ `bkmonitor/kernel_api/resource/log_search.py`
- `CreateLogExtractTaskResource` @ `bkmonitor/kernel_api/resource/log_extract.py`
- `ListOperationMetricsResource` / `GetOperationMetricResource` @ `bkmonitor/kernel_api/resource/operation/`
- `KernelRPCResource` / `BkmCliOpCallResource` @ `bkmonitor/kernel_api/resource/kernel_rpc.py` / `bkm_cli.py`

目标端（v4 ViewSet 复用方）：
- `AlertViewSet` / `SearchAlertViewSet`（MCP）@ `bkmonitor/kernel_api/views/v4/alert.py`
- `LogSearchViewSet` / `LogExtractViewSet` @ `bkmonitor/kernel_api/views/v4/log_search.py` / `log_extract.py`
- `OperationViewSet` @ `bkmonitor/kernel_api/views/v4/operation.py`
- `KernelRPCViewSet` / `BkmCliViewSet` @ `bkmonitor/kernel_api/views/v4/kernel_rpc.py` / `bkm_cli.py`
- 薄封装模式：ViewSet 常做参数适配/别名映射后调 `resource.xxx.yyy()` 或 `SomeResource().request()`