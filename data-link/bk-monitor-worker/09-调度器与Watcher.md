<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->
# 调度器与 Watcher

<cite>
**本文引用的文件**
- [service/scheduler/async.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/async.go)
- [service/scheduler/periodic/periodic.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/periodic/periodic.go)
- [service/worker_service.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/worker_service.go)
- [watcher/watcher.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/watcher.go)
- [watcher/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/redis/redis.go)
- [watcher/consul/consul.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/consul/consul.go)
</cite>

## 目录
1. [简介](#简介)
2. [异步任务注册（async.go）](#异步任务注册asyncgo)
3. [周期任务注册（periodic.go）](#周期任务注册periodicgo)
4. [调度注册与 worker 加载](#调度注册与-worker-加载)
5. [顶层 Watcher：周期任务订阅](#顶层-watcher周期任务订阅)
6. [与 daemon 调度（常驻任务）的关系](#与-daemon-调度常驻任务的关系)
7. [结论](#结论)

## 简介

除常驻任务（见《06》由 `service/scheduler/daemon` 专门调度）外，BMW 的**异步任务**与**周期任务**也通过 `service/scheduler` 包统一注册：`async.go` 与 `periodic/periodic.go` 各自维护 `Kind→Handler` 映射，并在 worker 启动时自动加载进 `WorkerMux`。此外，顶层 `watcher` 包提供「配置/周期任务变更订阅」能力。本篇说明这些调度注册机制与 Watcher 抽象。

**章节来源**
- [service/scheduler/async.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/async.go#L10-L38)
- [service/scheduler/periodic/periodic.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/periodic/periodic.go#L30-L120)

## 异步任务注册（async.go）

`async.go` 定义轻量 `Task{Handler processor.HandlerFunc}`，并以 `asyncTaskDefine` 注册：

| Kind | Handler |
|------|---------|
| `async:test_example` | `example.HandleExampleTask` |
| `async:collect_es_task` | `task.CollectESTask`（metadata 包） |

`GetAsyncTaskMapping()` 返回该 map，供 worker 注册。

```go
asyncTaskDefine = map[string]Task{
	"async:test_example":   {Handler: example.HandleExampleTask},
	"async:collect_es_task": {Handler: task.CollectESTask},
}
func GetAsyncTaskMapping() map[string]Task { return asyncTaskDefine }
```

**章节来源**
- [service/scheduler/async.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/async.go#L22-L38)

## 周期任务注册（periodic.go）

`PeriodicTask` 在 `Handler` 之外多了 `Cron`/`Payload`/`Option`：

```go
type PeriodicTask struct {
	Cron    string
	Handler processor.HandlerFunc
	Payload []byte
	Option  []task.Option
}
```

`getPeriodicTasks()` 注册了十余个周期任务（cron 表达式驱动），例如：

| Kind | Cron | Handler | 关键 Option |
|------|------|---------|------------|
| `periodic:metadata:refresh_ts_metric` | `*/5 * * * *` | `metadataTask.RefreshTimeSeriesMetric` | Timeout 10m |
| `periodic:metadata:refresh_datasource` | `*/20 * * * *` | `metadataTask.RefreshDatasource` | Timeout 40m |
| `periodic:metadata:refresh_kafka_topic_info` | `*/10 * * * *` | `metadataTask.RefreshKafkaTopicInfo` | Timeout 20m |
| `periodic:cluster_metrics:report_influxdb` | `*/1 * * * *` | `cmInfluxdbTask.ReportInfluxdbClusterMetric` | Timeout 2m |
| `periodic:cluster_metrics:report_es` | `*/1 * * * *` | `cmESTask.ReportESClusterMetrics` | Queue=ESClusterMetricQueue, Timeout 5m |
| `periodic:cluster_metrics:report_rabbitmq` | `*/1 * * * *` | `cmRabbitMQTask.ReportRabbitMQClusterMetrics` | Queue=RabbitMQClusterMetricQueue |
| `periodic:metadata:clear_deprecated_redis_key` | `0 0 */14 * *` | `metadataTask.ClearDeprecatedRedisKey` | Timeout 24h |
| `periodic:metadata:clean_data_id_consul_path` | `0 2 * * *` | `metadataTask.CleanDataIdConsulPath` | Timeout 2h |
| `periodic:metadata:slo_push` | `*/5 * * * *` | `metadataTask.SloPush` | Timeout 10m |
| `periodic:relation:report_custom_resource_relation` | `*/1 * * * *` | `relation.ReportCustomRelation` | Timeout 2m |
| `periodic:cluster_metrics:push_and_publish_space_router_info` | `*/15 * * * *` | `metadataTask.PushAndPublishSpaceRouterInfo` | Queue=BigResourceTaskQueueName |

`GetPeriodicTaskMapping()` 经 `sync.Once` 返回（注释提示后续可从 Redis 同步任务）。

**章节来源**
- [service/scheduler/periodic/periodic.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/periodic/periodic.go#L30-L120)

## 调度注册与 worker 加载

`WorkerService.Run()` 在启动消费前，遍历两个映射把 handler 注册进 `WorkerMux`：

```go
for p, h := range scheduler.GetAsyncTaskMapping()    { w.mux.HandleFunc(p, h.Handler) }
for p, h := range periodic.GetPeriodicTaskMapping()  { w.mux.HandleFunc(p, h.Handler) }
err := w.worker.Run(w.mux)
```

即：所有异步/周期任务的 `Kind` 在 worker 进程启动那一刻即完成路由注册；随后 `Processor` 出队任务时按 `Kind` 精确匹配（见《03》《05》）。周期任务由 `Forwarder` 按 `Cron`→`ProcessAt` 经 broker 的 scheduled ZSet 到期后投入执行。

**章节来源**
- [service/worker_service.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/worker_service.go#L38-L50)

## 顶层 Watcher：周期任务订阅

顶层 `watcher` 包定义抽象的监听接口：

```go
type Watcher interface {
	Watch(ctx context.Context, path string) (<-chan any, error)
}
```

其实现用于「订阅外部变更事件」：

- `watcher/redis`：`NewWatcher` 返回单例（`instance = GetStorageRedisInstance()`）；`Watch(ctx, receiveChan)` 订阅 `StoragePeriodicTaskChannelKey` 频道，收到消息即推入 `receiveChan`（用于周期任务动态下发/刷新）。
- `watcher/consul`：`Watcher` 封装 `consul.Instance`，监听 Consul KV 路径变化。

> 注意：顶层 `watcher` 包（订阅周期任务/配置变更）与 `service/scheduler/daemon` 包内的 `Watcher` 接口（常驻任务调度用，含 `handleAddTask/handleDeleteWorker` 等）**是两套独立抽象**，前者偏「配置/周期任务事件订阅」，后者偏「常驻任务的 task↔worker 映射维护」。

**章节来源**
- [watcher/watcher.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/watcher.go#L16-L18)
- [watcher/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/redis/redis.go#L18-L59)
- [watcher/consul/consul.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/consul/consul.go#L18-L21)

## 与 daemon 调度（常驻任务）的关系

BMW 的「调度」概念分散在三处，需明确边界：

| 调度对象 | 注册/调度位置 | 执行触发 |
|---------|--------------|---------|
| 异步任务 | `scheduler/async.go` → `WorkerMux` | broker 入队后 `Processor` 消费 |
| 周期任务 | `scheduler/periodic` → `WorkerMux` | `Forwarder` 按 cron 到期投入 |
| 常驻任务 | `scheduler/daemon`（`Watcher`+`Numerator`+`RunMaintainer`） | 监听 Binding 后 `Operator.Start` |

前两者是「一次性的 Handler 注册 + 队列消费」；后者是「长生命周期的保活/重试/心跳维护」。三者共用 `broker`/`store`/`metrics` 底座，但调度语义不同。

**章节来源**
- [service/scheduler/async.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/async.go#L36-L38)
- [service/scheduler/periodic/periodic.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/periodic/periodic.go#L115-L119)
- [service/scheduler/daemon/daemon.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/daemon/daemon.go#L33-L45)

## 结论

异步与周期任务通过 `service/scheduler` 的 `async.go`/`periodic.go` 以 `Kind→Handler` 映射集中注册，worker 启动时一次性加载进 `WorkerMux`；周期任务额外携带 cron 表达式，由 `Forwarder` 按延迟投入执行。顶层 `watcher` 包（redis/consul 实现）提供「周期任务/配置变更订阅」能力，与 `daemon` 包内常驻任务调度用的 `Watcher` 是两套独立抽象。三者各司其职，共同构成 BMW 多类型任务的调度体系。

**章节来源**
- [service/scheduler/async.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/async.go#L22-L38)
- [service/scheduler/periodic/periodic.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/scheduler/periodic/periodic.go#L30-L120)
- [watcher/watcher.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/watcher/watcher.go#L16-L18)
- [service/worker_service.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/worker_service.go#L38-L50)
