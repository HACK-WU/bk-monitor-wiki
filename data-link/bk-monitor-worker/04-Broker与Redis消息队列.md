<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->
# Broker 与 Redis 消息队列

<cite>
**本文引用的文件**
- [broker/broker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/broker.go)
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go)
- [common/common.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/common/common.go)
</cite>

## 目录
1. [简介](#简介)
2. [Broker 接口](#broker-接口)
3. [Redis 数据结构与 key 规则](#redis-数据结构与-key-规则)
4. [入队与出队](#入队与出队)
5. [延迟 / 重试 / 归档](#延迟--重试--归档)
6. [租约与恢复](#租约与恢复)
7. [Server State 与 Result](#server-state-与-result)
8. [结论](#结论)

## 简介

`broker` 抽象了任务在消息中间件中的存储与流转。BMW 当前唯一实现是 `broker/redis`——基于 Redis 的单个文件 `redis.go`（约 1177 行）。它用 List + Sorted Set + Hash 组合表达 asynq 风格的多状态队列。本篇说明 Broker 接口契约与 Redis 实现细节。

**章节来源**
- [broker/broker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/broker.go#L20-L60)

## Broker 接口

```go
type Broker interface {
	Open() / Close() error
	Enqueue(ctx, *TaskMessage) error
	EnqueueUnique(ctx, *TaskMessage, ttl) error
	Dequeue(qnames ...string) (*TaskMessage, time.Time, error)
	Done(ctx, *TaskMessage) error
	MarkAsComplete(ctx, *TaskMessage) error
	Requeue(ctx, *TaskMessage) error
	Schedule(ctx, *TaskMessage, processAt) error
	ScheduleUnique(...) error
	Retry(ctx, *TaskMessage, processAt, errMsg, isFailure) error
	Archive(ctx, *TaskMessage, errMsg) error
	ForwardIfReady(qnames ...string) error
	DeleteExpiredCompletedTasks(qname) error
	ListLeaseExpired(cutoff, qnames...) ([]*TaskMessage, error)
	ExtendLease(qname, ids...) (time.Time, error)
	WriteServerState(info, workers, ttl) error
	ClearServerState(host, pid, serverID) error
	WriteResult(qname, id, data) (int, error)
}
```

接口方法可分为：入队类（Enqueue/Schedule/EnqueueUnique/ScheduleUnique）、出队类（Dequeue/Done/Requeue）、状态迁移类（Retry/Archive/MarkAsComplete/ForwardIfReady）、租约类（ListLeaseExpired/ExtendLease）、运维类（WriteServerState/ClearServerState/WriteResult）。

**章节来源**
- [broker/broker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/broker.go#L20-L60)

## Redis 数据结构与 key 规则

key 前缀 `bmw:{<qname>}:`，由 `common` 包的函数生成：

| 用途 | key 函数 | Redis 结构 |
|------|----------|-----------|
| 等待队列 | `PendingKey` | List（LPUSH / RPOPLPUSH） |
| 执行中 | `ActiveKey` | List |
| 已调度（延迟） | `ScheduledKey` | Sorted Set（score=执行时间戳） |
| 重试 | `RetryKey` | Sorted Set |
| 已归档 | `ArchivedKey` | Sorted Set（上限 10000，保留 90 天） |
| 已完成 | `CompletedKey` | Sorted Set（仅 Retention>0 时） |
| 租约 | `LeaseKey` | Sorted Set（score=租约到期 unix 秒） |
| 任务本体 | `TaskKey` → `bmw:{q}:t:<id>` | Hash（`msg/state/pending_since/unique_key`） |

全局集合键：`bmw:queues`（SADD 队列名）、`bmw:servers`、`bmw:workers`、`bmw:schedulers`。

`RDB` 结构：`type RDB struct { client redis.UniversalClient; clock timex.Clock }`；单例 `GetRDB()` 懒加载，内部用 `redisUtils.NewRedisClient` 连接（standalone/sentinel），失败重试 3 次后 `logger.Fatalf`。租约默认时长 `LeaseDuration=30min`。

**章节来源**
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L37-L94)
- [common/common.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/common/common.go#L45-L77)

## 入队与出队

- **Enqueue**（L168）：写 task Hash + 推入 `PendingKey` List + 向 `bmw:queues` SADD 队列名；`EnqueueUnique` 用 `unique_key` + TTL 去重（重复返回 `ErrDuplicateTask`）。
- **Dequeue**（L298）：`dequeueCmd`（L281）按 `qnames` 顺序对每个队列 `RPOPLPUSH pending active`，写 `LeaseKey`，**跳过 paused 队列**；返回 `TaskMessage` 与租约到期时间。

```go
func (r *RDB) Enqueue(ctx, msg) error { /* HSet task + LPUSH pending + SADD bmw:queues */ }
func (r *RDB) Dequeue(qnames ...string) (*TaskMessage, time.Time, error) {
	// 遍历队列 RPOPLPUSH → active，写 lease
}
```

**章节来源**
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L168-L332)

## 延迟 / 重试 / 归档

- **Schedule / ScheduleUnique**（L581/L641）：写入 `ScheduledKey` ZSet（score=processAt）。
- **Retry**（L721）：active→`RetryKey` ZSet，记录失败计数与错误；`isFailure` 影响后续统计。
- **Archive**（L804）：active→`ArchivedKey` ZSet，按时间+大小（maxArchiveSize=10000）裁剪，保留约 90 天。
- **ForwardIfReady**（L840）→ `forwardAll`/`forward`（L868）：用 `forwardCmd` 将 `ScheduledKey`/`RetryKey` 中 `score<=now` 的任务批量（每次 100 条）移到 `PendingKey`，由 `Forwarder` 周期性触发。

**章节来源**
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L581-L903)

## 租约与恢复

任务出队后获得租约（`LeaseKey` ZSet，默认 30min）。`Processor.Exec` 监听 `lease.Done()`：若处理超时，判定失败并 `HandleFailedMessage`，同时 `ListLeaseExpired`（L970）可被独立 recoverer 扫描，把过期 lease 的任务取回重投。`ExtendLease`（L997）仅 `ZAddXX` 续期（防止长任务租约过期）。`Done`/`Requeue` 等完成后从 lease 移除。`common.Lease`（L461）封装 `IsValid/Reset`。

**章节来源**
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L960-L1011)
- [common/common.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/common/common.go#L461-L478)

## Server State 与 Result

- `WriteServerState`（L1030）：写 `bmw:servers:{host:pid:sid}` 与 `bmw:workers:{...}` Hash，并加入 `bmw:servers`/`bmw:workers` ZSet（带 TTL），供 Watcher/Numerator 感知 worker 存活与调度。
- `ClearServerState`（L1065）：进程退出时清理。
- `WriteResult`（L1168）：将任务结果写入 task Hash 的 `result` 字段，供查询。

这些状态是「worker 心跳」与「常驻任务调度」的数据底座——`WorkerHealthMaintainer` 周期性 `SET WorkerKey`，Watcher 通过 `Keys WorkerKeyPrefix*` 感知 worker 上下线。

**章节来源**
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L1030-L1077)
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L1168-L1176)

## 结论

`broker/redis` 以「List 承载 pending/active、ZSet 承载 scheduled/retry/archived/completed/lease、Hash 承载任务本体」的组合，在单 Redis 实例上实现了完整的多状态任务队列。`Processor` 通过 `Dequeue` 出队并持租约、`ForwardIfReady` 由 `Forwarder` 周期触发搬回 pending、`Retry/Archive` 完成状态迁移，`WriteServerState/WriteResult` 则为上层调度与可观测性提供数据。这是 BMW 异步/周期任务可靠性的存储基石。

**章节来源**
- [broker/broker.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/broker.go#L20-L60)
- [broker/redis/redis.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/broker/redis/redis.go#L37-L1176)
- [common/common.go](file://bkmonitor-datalink/pkg/bk-monitor-worker/common/common.go#L45-L77)
