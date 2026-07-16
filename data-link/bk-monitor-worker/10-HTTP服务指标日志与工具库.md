<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->
# HTTP 服务、指标、日志与工具库

<cite>
**本文引用的文件**
- [http/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/metrics.go)
- [http/http.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/http.go)
- [metrics/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/metrics/metrics.go)
- [log/logger.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/log/logger.go)
- [utils/](file://bkmonitor-datalink/pkg/bk-monitor-worker/utils)
- [internal/](file://bkmonitor-datalink/pkg/bk-monitor-worker/internal)
</cite>

## 目录
1. [简介](#简介)
2. [HTTP 服务](#http-服务)
3. [指标（Prometheus）](#指标prometheus)
4. [日志](#日志)
5. [工具库 utils 概览](#工具库-utils-概览)
6. [业务实现包 internal 概览](#业务实现包-internal-概览)
7. [结论](#结论)

## 简介

本篇收尾 BMW 的运维与支撑代码：HTTP 服务（pprof/metrics/task API）、Prometheus 指标、日志初始化，以及 `utils` 通用工具库与 `internal` 业务实现包。这些是框架与各业务任务之间的「胶水层」。

**章节来源**
- [http/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/metrics.go#L27-L48)
- [metrics/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/metrics/metrics.go#L24-L201)

## HTTP 服务

BMW 提供两套 gin 引擎：

- **`NewProfHttpService()`**（worker/controller 进程用）：路由 `/bmw/metrics`（Prometheus，合并默认+自定义 Registry）、`/bmw/relation/metrics`、`/bmw/relation/debug`、`pprof`（gin-contrib/pprof）、`POST /bmw/log/level`（动态调日志级别）。
- **`NewHTTPService()`**（task 进程用）：在 `NewProfHttpService` 基础上 `addMetricMiddleware`（记录 API 耗时/总量），并在 `RouterPrefix`+`TaskRouterPrefix` 下注册常驻任务 API：`GET/POST/DELETE /bmw/task/`、`DELETE /bmw/task/<DeleteAllTaskPath>`、`POST /bmw/task/<DaemonTaskReloadPath>`（见《06》）。

```go
func NewProfHttpService() *gin.Engine {
	svr := gin.Default()
	svr.GET("/bmw/metrics", prometheusHandler())
	pprof.Register(svr)
	svr.POST("/bmw/log/level", SetLogLevel)
	return svr
}
```

**章节来源**
- [http/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/metrics.go#L27-L87)
- [http/http.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/http.go#L17-L33)

## 指标（Prometheus）

`metrics` 包以 namespace `bmw` 注册以下指标（`Registry` 自定义注册表，`init` 统一注册）：

| 指标 | 类型 | 维度 | 更新函数 |
|------|------|------|---------|
| `bmw_api_request_total` | Counter | method/path/status | `RequestApiTotal` |
| `bmw_api_request_cost` | Gauge | method/path | `RequestApiCostTime` |
| `bmw_task_total` | Counter | name/module/status | `RegisterTaskTotal`(registered)/`EnqueueTaskTotal`(enqueue)/`RunTaskTotal`(received)/`RunTaskSuccessTotal`(success)/`RunTaskFailureTotal`(failure) |
| `bmw_task_duration_seconds` | Histogram | name | `RunTaskDurationSeconds` |
| `daemon_running_task_count` | Gauge | task_dimension | `RecordDaemonTask`（每 30s 置 1） |
| `daemon_task_retry_count` | Gauge | task_dimension | `RecordDaemonTaskRetryCount` |

`module` 维度用 `common.TaskModuleName/ScheduleModuleName/WorkerModuleName` 区分任务来自哪一执行面；常驻任务两指标是观察常驻任务健康度的核心（见《06》）。

**章节来源**
- [metrics/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/metrics/metrics.go#L24-L201)

## 日志

`log.InitLogger()` 在 `config.InitConfig()` 之后调用，把 `config` 的日志配置（`LoggerEnabledStdout/Level/Path/MaxSize/MaxAge/MaxBackups`）灌入底层 `pkg/utils/logger` 的 `SetOptions`，完成日志初始化。所有模块通过 `pkg/utils/logger` 输出结构化日志。

**章节来源**
- [log/logger.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/log/logger.go#L17-L27)

## 工具库 utils 概览

`utils` 包下 15 个子包，提供跨模块通用能力（基于包名与用法归纳）：

| 子包 | 职责（归纳） |
|------|------------|
| `cipher` | AES 等加解密工具 |
| `common` | 通用辅助函数 |
| `deepcopy` | 结构体深拷贝 |
| `diffutil` | 差异比对 |
| `errors` | 错误类型与判定（如 `ErrNoProcessableTask`/`ErrDuplicateTask`） |
| `hashconsul` | Consul 相关哈希 |
| `hashring` | 一致性哈希（任务分片/路由） |
| `jsonx` | JSON 序列化（`Marshal`/`Unmarshal`，全模块通用） |
| `kafka` | Kafka 客户端封装 |
| `mapx` | Map 操作工具 |
| `mocker` | Mock 辅助（测试） |
| `optionx` | 选项/参数工具 |
| `remote` | 远程调用封装 |
| `runtimex` | 运行时工具（`HandleCrash` 崩溃恢复，cmd 已用） |
| `slicex` | Slice 操作工具 |
| `stringx` | 字符串工具（`IsEmpty` 等） |
| `timex` | 时间工具（`Clock`/`NewTimeClock`/`UnixTime2Time`，processor 用） |

**章节来源**
- [utils/](file://bkmonitor-datalink/pkg/bk-monitor-worker/utils)

## 业务实现包 internal 概览

`internal` 是各业务任务的具体实现（不在框架文档逐文件展开），按子包划分：

| 子包 | 规模 | 职责（归纳） |
|------|------|------------|
| `metadata` | 129 文件 | 元数据计算（refresh_ts_metric、refresh_datasource、kafka topic、slo、consul path 清理等周期任务） |
| `apm` | 48 文件 | APM 预计算常驻任务（`daemon:apm:pre_calculate`） |
| `alarm` | 20 文件 | 告警相关（CMDB 资源 watch / 缓存刷新常驻任务） |
| `clustermetrics` | 11 文件 | 集群指标上报（es/influxdb/rabbitmq 周期任务） |
| `relation` | 9 文件 | 资源关系/拓扑（SchemaProvider、`report_custom_resource_relation`） |
| `api` | 13 文件 | API 相关实现 |
| `example` | — | 示例任务（`async:test_example`） |
| `tenant` | — | 多租户支持 |

这些业务 Handler/Operator 通过《09》的 `asyncTaskDefine`/`getPeriodicTasks`/`taskDefine` 注册进调度体系，是 BMW「框架 + 业务」分层架构的业务侧落地。

**章节来源**
- [internal/](file://bkmonitor-datalink/pkg/bk-monitor-worker/internal)
- [service/scheduler/async.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/async.go#L26-L33)
- [service/scheduler/periodic/periodic.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/periodic/periodic.go#L39-L110)

## 结论

BMW 的支撑层由 HTTP 服务、Prometheus 指标、日志与 `utils` 工具库构成：`NewProfHttpService`/`NewHTTPService` 提供 pprof、metrics、日志级别动态调整与常驻任务 API；`metrics` 包以 `bmw` 命名空间覆盖 API/任务/常驻任务三类指标；`log.InitLogger` 统一日志；`utils` 17 个子包提供加解密、JSON、哈希、时间、运行时恢复等通用能力；`internal` 则承载 metadata/apm/alarm/clustermetrics/relation 等具体业务任务，通过调度体系注册，实现「框架与业务分离」。

**章节来源**
- [http/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/metrics.go#L27-L87)
- [http/http.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/http/http.go#L17-L33)
- [metrics/metrics.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/metrics/metrics.go#L24-L201)
- [log/logger.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/log/logger.go#L17-L27)
