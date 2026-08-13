---
groupPath: 专题记忆/kernel_api网关
relation: 内部Resource复用
exportedAt: "2026-08-13T09:11:00.045Z"
---
kernel_api 内部 Resource 复用：resource/ 下的 Resource 不给前端直接调用，作为批发场景在其他 ViewSet/Resource 内部复用，常做薄封装适配内部调用参数。覆盖 MCP 告警/日志检索/运营指标等域。

## 与 views/ 的区别
- `views/` 下的 `ResourceViewSet` → 对外暴露给 API 网关（前端/其他系统调用）
- `resource/` 下的 `Resource` → 仅内部调用（被其他 Resource 的 `perform_request` 使用）

## 核心能力域与关键 Resource
- 符号: `ListAlertResource` / `ListAlertTopNResource` / `SearchAlarmStrategiesResource` / `CreateAlarmShieldResource` / `AlertRelatedResource`
- 位置: `bkmonitor/kernel_api/resource/alert.py`（MCP 告警管理 + 告警关联数据）
- 符号: `GetIndexSetListResource` / `SearchLogResource` / `FieldAnalyzeResource`
- 位置: `bkmonitor/kernel_api/resource/log_search.py`（日志检索）
- 符号: `CreateLogExtractTaskResource` / `GetLogExtractDownloadUrlResource`
- 位置: `bkmonitor/kernel_api/resource/log_extract.py`（日志提取）
- 符号: `ListOperationMetricsResource` / `GetOperationMetricResource` / `GetOperationOverviewResource`
- 位置: `bkmonitor/kernel_api/resource/operation/`（运营指标，Redis 缓存 `operation_mcp:metric:*`）
- 符号: `KernelRPCResource` / `BkmCliOpCallResource`
- 位置: `bkmonitor/kernel_api/resource/kernel_rpc.py` / `bkm_cli.py`（RPC 入口）
- 符号: `QueryEsResource` / `ExecuteRangeQueryResource`
- 位置: `bkmonitor/kernel_api/resource/query.py` / `metrics.py`

## 薄封装模式
- 常做一层参数适配/别名映射后复用下游 Resource（如 `resource.alert.xxx()` 或 `SomeResource().request()`）
- 使用场景：当某个查询/操作在多个对外的 ViewSet 中都需要用到时，抽成 `resource/` 下独立 Resource 供多 ViewSet 复用

## 踩坑点
- MCP 请求报时间跨度超限：`start_time`/`end_time` 跨度 > `settings.MCP_MAX_TIME_SPAN_SECONDS` → 用 `TimeSpanValidationPassThroughSerializer`（`serializers/mixins.py`）拆批查询
- 复用 resource 时线程安全：直接持有实例多次 `request()` 不安全 → 用全局入口 `resource.xxx.yyy()`（内部自动新建临时实例）或 `SomeResource().request()` 新建
- 运营指标取不到值：环境未部署对应能力（eBPF/doris）或 MANUAL 类型无 handler → 检查 `supported_envs`/`programmable`；overview 默认跳过 slow 指标