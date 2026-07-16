<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->
# Worker 与路由

<cite>
**本文引用的文件**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go)
- [service/worker_service.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/worker_service.go)
- [cmd/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/cmd/worker.go)
</cite>

## 目录
1. [简介](#简介)
2. [Worker 结构与配置](#worker-结构与配置)
3. [NewWorker 组装](#newworker-组装)
4. [启动与停止](#启动与停止)
5. [WorkerMux 任务路由](#workermux-任务路由)
6. [WorkerService 与心跳维护器](#workerservice-与心跳维护器)
7. [结论](#结论)

## 简介

`worker` 包把 `broker`、`processor`、`forwarder` 组装成一个可运行的任务执行单元，并提供 `WorkerMux`——一个按任务 `Kind` 精确路由到 `Handler` 的注册表（类似 `http.ServeMux`）。`service.WorkerService` 在其上叠加「handler 自动注册」与「worker 心跳维护」。本篇说明这些组件。

**章节来源**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go#L34-L43)

## Worker 结构与配置

```go
type Worker struct {
	broker    broker.Broker
	wg        sync.WaitGroup
	forwarder *processor.Forwarder
	processor *processor.Processor
}

type WorkerConfig struct {
	Concurrency              int
	BaseContext              func() context.Context
	RetryDelayFunc           processor.RetryDelayFunc
	IsFailure                func(error) bool
	Queues                   map[string]int
	StrictPriority           bool
	ErrorHandler             processor.ErrorHandler
	ShutdownTimeout          time.Duration
	HealthCheckFunc          func(error)
	HealthCheckInterval      time.Duration
	DelayedTaskCheckInterval time.Duration
}
```

**章节来源**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go#L35-L58)

## NewWorker 组装

`NewWorker` 负责把所有默认值补全并构造子组件：

- `Concurrency` 默认 `runtime.NumCPU()`（<1 时）；
- `RetryDelayFunc` 默认 `DefaultRetryDelayFunc`（n⁴ 退避，见《03》）；
- `IsFailure` 默认 `err != nil`；
- `Queues` 经 `common.ValidateQueueName` 过滤、权重 >0 才保留，空则回退 `{default:1}`；
- `ShutdownTimeout` 默认 `common.DefaultShutdownTimeout`（8s）；
- `DelayedTaskCheckInterval` 默认 `common.DefaultDelayedTaskCheckInterval`（5s）；
- 统一使用 `rdb.GetRDB()` 作为 broker，构造 `Forwarder`（监听队列、interval=延迟检查间隔）与 `Processor`（含并发、队列、优先级、handler 等）。

```go
rdb := rdb.GetRDB()
forwarder := processor.NewForwarder(processor.ForwarderParams{
	Broker: rdb, Queues: qnames, Interval: delayedTaskCheckInterval,
})
processor := processor.NewProcessor(processor.ProcessorParams{
	Broker: rdb, RetryDelayFunc: delayFunc, BaseCtxFn: baseCtxFn,
	Concurrency: n, Queues: queues, StrictPriority: cfg.StrictPriority,
	ErrHandler: cfg.ErrorHandler, ShutdownTimeout: shutdownTimeout,
})
```

**章节来源**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go#L68-L145)

## 启动与停止

```go
func (w *Worker) Run(handler processor.Handler) error {
	if handler == nil { return fmt.Errorf("server cannot run with nil handler") }
	w.processor.Handler = handler
	w.forwarder.Start(&w.wg)
	w.processor.Start(&w.wg)
	return nil
}
func (w *Worker) Shutdown() {
	w.forwarder.Shutdown(); w.processor.Shutdown(); w.wg.Wait(); w.broker.Close()
}
func (w *Worker) Stop() { w.processor.Stop() }
```

`Run` 注入 handler 并启动 forwarder + processor 两个 goroutine；`Shutdown` 顺序关停并等待所有 goroutine 退出后关闭 broker；`Stop` 仅停 processor（用于收到信号时的第一步）。此外 `waitForSignals` 监听 `SIGTERM/SIGINT/SIGTSTP` 触发 `Stop`。

**章节来源**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go#L147-L193)

## WorkerMux 任务路由

`WorkerMux` 是按 `Kind` 精确匹配的 handler 注册表：

- `Handle(pattern, handler)` / `HandleFunc(pattern, fn)`：注册，重复注册 `panic`；
- `ProcessTask(ctx, task)`：对外执行入口，内部 `Handler(task)` 按 `task.Kind` 调 `match`；
- `match(kind)`：在 `map[string]muxEntry` 中精确查找，未命中返回 `NotFoundHandler()`（返回 `handler not found for task %q`）。

注意匹配是**精确字符串匹配**（`mux.m[kind]`），不支持前缀/正则，因此每个 `Kind` 必须显式注册。

```go
func (mux *WorkerMux) match(kind string) (h processor.Handler, pattern string) {
	v, ok := mux.m[kind]
	if ok { return v.h, v.pattern }
	return nil, ""
}
```

**章节来源**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go#L195-L280)

## WorkerService 与心跳维护器

`service.WorkerService` 在 `Worker` 之上封装「启动即注册全部 handler」与「worker 心跳」：

- `NewWorkerService(ctx, queues)`：用 `config.WorkerConcurrency` + 队列构造 `Worker`，并创建 `WorkerHealthMaintainer`（`id = GenerateProcessorId()`）。
- `Run()`：遍历 `scheduler.GetAsyncTaskMapping()` 与 `periodic.GetPeriodicTaskMapping()`，对每个 `pattern` 调 `mux.HandleFunc` 注册；随后 `worker.Run(mux)` 启动消费；最后 `go maintainer.Start()`。
- `WorkerHealthMaintainer`：定时（`WorkerHealthCheckInterval`，默认 3s）向 `WorkerKey(queue, id)` 写入 `WorkerInfo{Id, StartTime}`（TTL=`WorkerHealthCheckInfoDuration`），供 Watcher/Numerator 感知存活。

`cmd/worker.go` 的 `startWorker` 即调用 `NewWorkerService` + `Run`，并另起 `daemon.NewDaemonTaskRunMaintainer` 处理常驻任务。

**章节来源**
- [service/worker_service.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/worker_service.go#L29-L143)
- [cmd/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/cmd/worker.go#L53-L110)

## 结论

`Worker` 是 BMW 执行面的核心载体：以 Redis broker 为底座，组合 `Forwarder`（延迟搬运）与 `Processor`（并发消费），并通过 `WorkerMux` 按任务 `Kind` 精确路由到 `Handler`。`WorkerService` 进一步在启动时自动从 `scheduler` 注册异步/周期任务 handler，并以心跳（`WorkerKey`）向调度面宣告自身存活。整个执行面与《04》《06》的 broker、常驻任务调度协同，构成完整的任务运行闭环。

**章节来源**
- [worker/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/worker/worker.go#L34-L193)
- [service/worker_service.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/service/worker_service.go#L29-L143)
- [cmd/worker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/cmd/worker.go#L53-L110)
