# transfer 模块 Wiki 索引

<cite>
**本文引用的文件**
- [01-概览与架构.md](file://bk-monitor-wiki/data-link/transfer/01-概览与架构.md)
- [02-核心抽象与数据模型.md](file://bk-monitor-wiki/data-link/transfer/02-核心抽象与数据模型.md)
- [03-配置体系.md](file://bk-monitor-wiki/data-link/transfer/03-配置体系.md)
- [04-事件总线与生命周期.md](file://bk-monitor-wiki/data-link/transfer/04-事件总线与生命周期.md)
- [05-管道编排.md](file://bk-monitor-wiki/data-link/transfer/05-管道编排.md)
- [06-ETL转换.md](file://bk-monitor-wiki/data-link/transfer/06-ETL转换.md)
- [07-Kafka前端与后端.md](file://bk-monitor-wiki/data-link/transfer/07-Kafka前端与后端.md)
- [08-存储后端-Elasticsearch.md](file://bk-monitor-wiki/data-link/transfer/08-存储后端-Elasticsearch.md)
- [09-存储后端-InfluxDB.md](file://bk-monitor-wiki/data-link/transfer/09-存储后端-InfluxDB.md)
- [10-存储抽象与KV缓存.md](file://bk-monitor-wiki/data-link/transfer/10-存储抽象与KV缓存.md)
- [11-Consul协调与调度.md](file://bk-monitor-wiki/data-link/transfer/11-Consul协调与调度.md)
- [12-分发与Shipper.md](file://bk-monitor-wiki/data-link/transfer/12-分发与Shipper.md)
- [13-缓冲池与资源管控.md](file://bk-monitor-wiki/data-link/transfer/13-缓冲池与资源管控.md)
- [14-监控指标与HTTP服务.md](file://bk-monitor-wiki/data-link/transfer/14-监控指标与HTTP服务.md)
- [15-辅助子包概述.md](file://bk-monitor-wiki/data-link/transfer/15-辅助子包概述.md)
</cite>

## 目录
1. [简介](#简介)
2. [模块定位](#模块定位)
3. [页面索引](#页面索引)
4. [推荐阅读路径](#推荐阅读路径)
5. [结论](#结论)

## 简介

本索引页用于串联 `bkmonitor-datalink/pkg/transfer` 模块的 15 篇 Wiki 文档，覆盖从模块启动、核心抽象、配置、事件总线，到管道编排、ETL 转换、Kafka 收发、存储后端、协调调度、分发 Shipper、缓冲池、监控与辅助子包的全链路知识。每篇子页均含源码引用（`file://` + 行号），可点击 [页面索引](#页面索引) 中的链接直达。

**章节来源**
- [01-概览与架构.md](file://bk-monitor-wiki/data-link/transfer/01-概览与架构.md#L1-L8)

## 模块定位

`transfer` 是 BlueKing Monitor 数据链路（data-link）的中枢采集 / ETL / 分发（Shipper）枢纽：从 Kafka 消费原始数据，经 Pipeline 编排与 ETL 声明式转换，最终经 Elasticsearch / InfluxDB 等存储后端写入，或经 Shipper 二次投递。其核心设计以 `define` 包抽象出 Payload / Frontend / Backend / Pipeline / DataProcessor / Scheduler / Store 等接口，配合 Consul 做配置发现与多实例协调。

**章节来源**
- [02-核心抽象与数据模型.md](file://bk-monitor-wiki/data-link/transfer/02-核心抽象与数据模型.md#L1-L8)
- [11-Consul协调与调度.md](file://bk-monitor-wiki/data-link/transfer/11-Consul协调与调度.md#L1-L8)

## 页面索引

下表按大纲序号列出 15 篇子页及其内容概要，点击页面名跳转。

| 序号 | 页面 | 内容概要 |
|------|------|----------|
| 01 | [概览与架构](./01-概览与架构.md) | 模块定位、启动链（main→cmd→Scheduler）、组件地图与数据流 |
| 02 | [核心抽象与数据模型](./02-核心抽象与数据模型.md) | `define` 包接口体系与 ETLRecord 数据模型、字段常量 |
| 03 | [配置体系](./03-配置体系.md) | viper 加载、Consul 配置版本、元数据模型与 Context 注入 |
| 04 | [事件总线与生命周期](./04-事件总线与生命周期.md) | eventbus 发布订阅、系统事件常量与进程生命周期 |
| 05 | [管道编排](./05-管道编排.md) | Node 节点、连接器（FanOut/Chain/Group 等）与 Pipeline 生命周期 |
| 06 | [ETL 转换](./06-ETL转换.md) | Record / Field / Transformer 声明式转换框架与 Container |
| 07 | [Kafka 前端与后端](./07-Kafka前端与后端.md) | 消费者组、限流、生产者与 TLS/SASL 注册 |
| 08 | [存储后端 - Elasticsearch](./08-存储后端-Elasticsearch.md) | BulkHandler、BulkWriter 与索引渲染策略 |
| 09 | [存储后端 - InfluxDB](./09-存储后端-InfluxDB.md) | BulkHandler、measurement 拆分与 tag 校验处理器 |
| 10 | [存储抽象与 KV 缓存](./10-存储抽象与KV缓存.md) | Store 抽象、RedisStore 与分布式锁、缓存读取器 |
| 11 | [Consul 协调与调度](./11-Consul协调与调度.md) | 配置发现、PipelineManager 与 Scheduler 调度 |
| 12 | [分发与 Shipper](./12-分发与Shipper.md) | Dispatcher 分发、负载均衡与 Shipper 投递 |
| 13 | [缓冲池与资源管控](./13-缓冲池与资源管控.md) | bufferpool 缓冲池与资源限制策略 |
| 14 | [监控指标与 HTTP 服务](./14-监控指标与HTTP服务.md) | Prometheus 指标暴露与 HTTP 服务 |
| 15 | [辅助子包概述](./15-辅助子包概述.md) | template / json / conv / logging / models 等辅助子包 |

**章节来源**
- [01-概览与架构.md](file://bk-monitor-wiki/data-link/transfer/01-概览与架构.md#L1-L8)
- [02-核心抽象与数据模型.md](file://bk-monitor-wiki/data-link/transfer/02-核心抽象与数据模型.md#L1-L8)
- [03-配置体系.md](file://bk-monitor-wiki/data-link/transfer/03-配置体系.md#L1-L8)
- [04-事件总线与生命周期.md](file://bk-monitor-wiki/data-link/transfer/04-事件总线与生命周期.md#L1-L8)
- [05-管道编排.md](file://bk-monitor-wiki/data-link/transfer/05-管道编排.md#L1-L8)
- [06-ETL转换.md](file://bk-monitor-wiki/data-link/transfer/06-ETL转换.md#L1-L8)
- [07-Kafka前端与后端.md](file://bk-monitor-wiki/data-link/transfer/07-Kafka前端与后端.md#L1-L8)
- [08-存储后端-Elasticsearch.md](file://bk-monitor-wiki/data-link/transfer/08-存储后端-Elasticsearch.md#L1-L8)
- [09-存储后端-InfluxDB.md](file://bk-monitor-wiki/data-link/transfer/09-存储后端-InfluxDB.md#L1-L8)
- [10-存储抽象与KV缓存.md](file://bk-monitor-wiki/data-link/transfer/10-存储抽象与KV缓存.md#L1-L8)
- [11-Consul协调与调度.md](file://bk-monitor-wiki/data-link/transfer/11-Consul协调与调度.md#L1-L8)
- [12-分发与Shipper.md](file://bk-monitor-wiki/data-link/transfer/12-分发与Shipper.md#L1-L8)
- [13-缓冲池与资源管控.md](file://bk-monitor-wiki/data-link/transfer/13-缓冲池与资源管控.md#L1-L8)
- [14-监控指标与HTTP服务.md](file://bk-monitor-wiki/data-link/transfer/14-监控指标与HTTP服务.md#L1-L8)
- [15-辅助子包概述.md](file://bk-monitor-wiki/data-link/transfer/15-辅助子包概述.md#L1-L8)

## 推荐阅读路径

本节为概念性内容，不直接分析具体文件，故无章节来源。

- **入门**：先读 `01 概览与架构` 建立全局视图，再读 `02 核心抽象与数据模型` 理解接口契约。
- **数据流主线**：`03 配置体系` → `04 事件总线与生命周期` → `05 管道编排` → `06 ETL 转换` → `07 Kafka 前端与后端` → `08/09 存储后端` → `10 存储抽象与 KV 缓存`。
- **协调与运维**：`11 Consul 协调与调度` → `12 分发与 Shipper` → `13 缓冲池与资源管控` → `14 监控指标与 HTTP 服务`。
- **扩展查阅**：`15 辅助子包概述` 作为工具类子包速查。

## 结论

`transfer` 模块 15 篇 Wiki 已覆盖其核心设计全貌，文档均通过 `codetowiki wiki-format --strict` 校验（0 错误 0 警告）。本索引页可作为入口，按阅读路径逐篇深入；各页源码引用均可溯源至 `bkmonitor-datalink/pkg/transfer` 对应子包。

本节为概念性内容，不直接分析具体文件，故无章节来源。
