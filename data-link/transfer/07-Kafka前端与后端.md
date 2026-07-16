# Kafka 前端与后端

> `kafka` 包实现 transfer 与 Kafka（MQ）的对接：前端 `Frontend` 作为消费组从 topic 拉取消息、做流控与 offset 管理，并把解码后的 `Payload` 送入管道；后端 `Backend` 作为异步生产者，把 `ETLRecord` 重新序列化后写入目标 Kafka topic（用于数据复制/转发场景）。

<cite>
**本文引用的文件**
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go)
</cite>

## 目录

1. [简介](#简介)
2. [前端消费（Frontend）](#前端消费frontend)
3. [后端生产（Backend）](#后端生产backend)
4. [鉴权与 TLS](#鉴权与-tls)
5. [注册与配置](#注册与配置)
6. [结论](#结论)

## 简介

transfer 通过 Kafka 既作为**数据入口**（前端消费各采集端上报）也作为**数据出口**（后端把处理后的数据转发到其它 Kafka topic）。`kafka` 包分别实现 `define.Frontend` 与 `define.Backend` 接口，并由 `init()` 注册到全局工厂（`"kafka"` 名称），供 `Builder` 按配置实例化。

**章节来源**
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L158-L178)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L56-L112)

## 前端消费（Frontend）

`Frontend` 内嵌 `define.BaseFrontend` 与 `ProcessorMonitor`，持有 sarama `ConsumerGroup`、`outputChan`、`killChan`，以及流控器 `fl`（`FlowLimiter`）与流量记录器 `fr`：

- **`NewFrontend` → `NewKafkaConsumerGroupFrontend`**：从 `Context` 取 MQ 配置（`AsKafkaCluster()`），初始化消费速率（`ConsumeRate`，缺省取 `define.DataIdFlowBytes()`）、提交间隔、流控与流量记录器。
- **`Pull(outputChan, killChan)`**：阻塞式消费主循环。先 `init()` 建立消费组与 topic，再循环调用 `group.Consume(ctx, [topic], f)`；遇到 rebalancing 时按服务器时间对齐重试。另起 goroutine 监听 `group.Errors()`，异常时通过 `killChan` 上报（用 `killOnce` 保证只发一次）。
- **`ConsumeClaim`**：单分区消费核心。每条消息先 `define.LimitRate`（全局流控）、`f.fl.Consume`（dataID 流控）、`f.fr.Add`（流量计数），再 `payload.From(msg.Value)` 解码；成功后送入 `outputChan`，并由 `DelayOffsetManager` 标记 offset（成功与否都只消费一次，保证 at-least-once 语义）。
- **`Close`**：停止流量记录、取消 ctx、关闭消费组并等待 goroutine 退出。

**章节来源**
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L175-L199)
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L213-L265)
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L267-L362)

## 后端生产（Backend）

`Backend` 内嵌 `define.BaseBackend` 与 `ProcessorMonitor`，持有 sarama 异步 `Producer`、`payloadChan` 与监控计数器：

- **`NewKafkaBackend`**：从 `ShipperConfig`（`AsKafkaCluster()`）取 topic/partition/cluster，创建带监控的 `Backend`；并按 `PipelineConfig.Option` 解析 `dropEmptyMetrics`。
- **`Push(d, killChan)`**：首次调用 `pushOnce.Do` 时 `init()` 建立 producer，并启动错误监听 goroutine 与 `define.Concurrency()` 个消费 goroutine 从 `payloadChan` 取数据调 `SendMsg`。之后每条 payload 入 `payloadChan`。
- **`SendMsg`**：把 `Payload` 转为 `ETLRecord`，若 metrics 全为 nil 或（开启 `dropEmptyMetrics` 后）为空则跳过；计算"接收时刻−数据时间"延迟并观测；最终 `payload.To(&message)` 序列化，构造 `sarama.ProducerMessage` 经 `write` 写入 producer（`ctx` 取消时放弃）。
- **`Close`**：取消 ctx、关闭 `payloadChan`、关闭 producer 并等待。

后端将 ETL 产物重新投递到 Kafka，是 transfer "数据复制 / 多活转发" 能力的出口。

**章节来源**
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L56-L112)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L176-L229)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L231-L320)

## 鉴权与 TLS

前端 `init()` 与后端 `init()` 都支持 Kafka 安全连接：

- **TLS**：`buildTlsConfig(ctx)` 从 MQ 配置读取 CA / 证书 / 密钥（`base64://` 前缀自动解码），支持 `ssl_insecure_skip_verify`；解析成功则启用 `Net.TLS`。
- **SASL/SCRAM**：当 `AuthInfo` 含用户名/密码且配置了 `sasl_mechanisms`，启用 SASL 并按 `SCRAM-SHA-512` / `SCRAM-SHA-256` 设置 `SCRAMClientGeneratorFunc`（基于 `XDGSCRAMClient` 实现）。

鉴权信息统一由 `config.NewAuthInfo` 从 `MetaClusterInfo` 解析，使连接配置完全由元数据驱动。

**章节来源**
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L90-L156)
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L429-L450)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L136-L166)

## 注册与配置

两个实现都在 `init()` 中向 `define` 全局工厂注册，使上层可凭名称创建：

- `define.RegisterFrontend("kafka", ...)`：校验 `PipelineConfig` 非空后返回 `NewFrontend(ctx, name)`。
- `define.RegisterBackend("kafka", ...)`：校验全局配置、`ShipperConfig`、`PipelineConfig` 均非空后返回 `NewKafkaBackend(ctx, name)`。

消费组名由 `ConfKafkaConsumerGroupPrefix` + topic 组成；初始 offset、版本、partitioner、acks、重试等均在 `NewKafkaConsumerConfig` / `NewKafkaProducerConfig` 中依据配置构造。

**章节来源**
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L471-L479)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L31-L54)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L322-L337)

## 结论

`kafka` 包以 `Frontend`（消费组 + 流控 + 延迟 offset 提交）与 `Backend`（异步生产者 + 空值过滤 + 延迟观测）实现 transfer 与 Kafka 的双向对接，并通过 TLS/SASL 支持安全连接、以 `init()` 注册到全局工厂。前端是 data-link 的主数据入口，后端支撑数据复制/转发，二者都完全由 consul 下发的 MQ / Shipper 元数据驱动。

**章节来源**
- [kafka/frontend.go](file://bkmonitor-datalink/pkg/transfer/kafka/frontend.go#L158-L199)
- [kafka/backend.go](file://bkmonitor-datalink/pkg/transfer/kafka/backend.go#L56-L112)
