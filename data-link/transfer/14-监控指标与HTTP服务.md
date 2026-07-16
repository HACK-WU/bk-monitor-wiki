# 监控指标与 HTTP 服务

> transfer 内置 Prometheus 指标与 HTTP 管理面：`monitor` 包提供 `CounterMixin`/`TimeObserver` 等通用指标封装；`http` 包提供带鉴权的 `Server` 与 `/metrics` 暴露，由 Scheduler 按需挂载。

<cite>
**本文引用的文件**
- [monitor/monitor.go](file://bkmonitor-datalink/pkg/transfer/monitor/monitor.go)
- [http/server.go](file://bkmonitor-datalink/pkg/transfer/http/server.go)
- [http/metrics.go](file://bkmonitor-datalink/pkg/transfer/http/metrics.go)
- [http/middleware.go](file://bkmonitor-datalink/pkg/transfer/http/middleware.go)
</cite>

## 目录

1. [简介](#简介)
2. [指标封装（monitor）](#指标封装monitor)
3. [HTTP Server](#http-server)
4. [/metrics 与鉴权中间件](#metrics-与鉴权中间件)
5. [结论](#结论)

## 简介

transfer 的所有关键路径（Redis 命令、管道启停、分发耗时、Kafka 消费等）都接入 Prometheus。`monitor` 包定义通用的指标 mixin 与耗时观测器，并给出 `DefBuckets`/`LargeDefBuckets` 两组直方图桶；`http` 包则在 Scheduler `buildPlugin` 中按 `ConfSchedulerPluginHTTPServer` 开关挂载管理 HTTP 服务，暴露 `/metrics` 并提供 Token 鉴权。

**章节来源**
- [monitor/monitor.go](file://bkmonitor-datalink/pkg/transfer/monitor/monitor.go#L18-L61)
- [scheduler/scheduler.go](file://bkmonitor-datalink/pkg/transfer/scheduler/scheduler.go#L57-L68)

## 指标封装（monitor）

`monitor` 提供两类可复用封装：

- **`CounterMixin{CounterSuccesses, CounterFails}`**：把"成功/失败"双计数器绑定到某操作（如 Redis 各命令），`NewCounterMixin` 构造，调用方在成功/失败分支 `Inc()`。
- **`TimeObserver`/`TimeObserverRecord`**：`Start()` 返回带起始时间的 record，`Finish()` 记录耗时并 `Observer.Observe(seconds)`，用于命令执行耗时直方图。

`DefBuckets`（`.005s ~ 60s`）用于秒级耗时，`LargeDefBuckets`（`1s ~ 3600s`）用于分钟/小时级任务（如缓存同步）。这些在 `redis_v2.go`、`pipeline` 等包被广泛复用。

**章节来源**
- [monitor/monitor.go](file://bkmonitor-datalink/pkg/transfer/monitor/monitor.go#L18-L61)

## HTTP Server

`Server` 内嵌 `define.BaseTask` 与标准 `*http.Server`，由 `NewServer(ctx, conf)` 构造：地址取 `ConfHost:ConfPort`，`Handler` 为 `AuthHandler`（包 `http.DefaultServeMux` + `ConfAuthToken` + `ConfAuthExemptPath` 豁免前缀）。

- **`Start`**：经 `BaseTask.Activate` 在 goroutine 中 `ListenAndServe`；`ErrServerClosed` 视为正常关闭。
- **`Stop`**：若 `ConfAutoShutdown` 为真则 `Shutdown(ctx)`，再停止 `BaseTask`。

Scheduler 在 `buildPlugin` 中当 `ConfSchedulerPluginHTTPServer` 为真时 `TaskManager.Add(http.NewServer(ctx, conf))` 挂入后台任务。

**章节来源**
- [http/server.go](file://bkmonitor-datalink/pkg/transfer/http/server.go#L22-L85)

## /metrics 与鉴权中间件

`metrics.go` 在 `init()` 中将 `promhttp.Handler()` 注册到 `http.DefaultServeMux` 的 `/metrics` 路径，使 Prometheus 可直接拉取。

`middleware.go` 的 `AuthHandler` 实现 `ServeHTTP`：`isPublicRequest` 判断豁免路径，`isAuthenticate` 校验 `ConfAuthToken`，未通过则 `reject`（返回 401），否则放行到内部 handler。这样 `/metrics` 等管理端点可在不暴露的前提下被受信的采集器访问（或配置为公开路径）。

**章节来源**
- [http/metrics.go](file://bkmonitor-datalink/pkg/transfer/http/metrics.go#L18-L20)
- [http/middleware.go](file://bkmonitor-datalink/pkg/transfer/http/middleware.go#L27-L76)

## 结论

transfer 通过 `monitor` 包统一了"成功/失败计数 + 耗时直方图"的指标语义，并以 `http` 包提供带 Token 鉴权的管理面，在 `/metrics` 暴露 Prometheus 数据——二者由 Scheduler 按配置挂载，构成 transfer 的可观测性底座。

**章节来源**
- [monitor/monitor.go](file://bkmonitor-datalink/pkg/transfer/monitor/monitor.go#L18-L61)
- [http/server.go](file://bkmonitor-datalink/pkg/transfer/http/server.go#L22-L85)
- [http/middleware.go](file://bkmonitor-datalink/pkg/transfer/http/middleware.go#L27-L76)
