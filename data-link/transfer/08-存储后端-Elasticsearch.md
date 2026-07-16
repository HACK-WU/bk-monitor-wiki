# 存储后端 - Elasticsearch

> `elasticsearch` 包是 transfer 对接 ES 的存储后端：`BulkHandler` 把管道产出的 `ETLRecord` 转成 ES 文档、按索引渲染规则分桶、批量 `_bulk` 写入，并通过版本化的 `BulkWriter` 适配不同 ES 版本。

<cite>
**本文引用的文件**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go)
- [elasticsearch/define.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/define.go)
- [elasticsearch/render.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/render.go)
</cite>

## 目录

1. [简介](#简介)
2. [BulkHandler 结构](#bulkhander-结构)
3. [写入流程（Handle / Flush）](#写入流程handle--flush)
4. [索引渲染（IndexRenderFn）](#索引渲染indexrenderfn)
5. [版本化写入器（BulkWriter）](#版本化写入器bulkwriter)
6. [注册与配置](#注册与配置)
7. [结论](#结论)

## 简介

transfer 的 `Backend` 节点把 ETL 结果写入目标存储。`elasticsearch` 包实现 `define.Backend` 接口：核心类型 `BulkHandler` 内嵌 `pipeline.BaseBulkHandler`，负责把 `ETLRecord` 映射为 ES 文档、计算 `_id`、按时间/模板渲染目标索引，并委托 `BulkWriter` 完成批量写。不同 ES 大版本对应不同的 `BulkWriter` 实现，由 `NewBulkWriter` 工厂按版本号（`v6/v7/...`）选择。

**章节来源**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L34-L43)
- [elasticsearch/define.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/define.go#L48-L70)

## BulkHandler 结构

`BulkHandler` 的关键字段：

- `resultTable *config.MetaResultTableConfig`：结果表元数据，决定字段映射与时间格式化。
- `uniqueField []string`：用于计算文档 `_id` 的去重字段集合。
- `writer BulkWriter`：版本化批量写入器。
- `indexRender IndexRenderFn`：索引名渲染函数。
- `transformers map[string]etl.TransformFn`：字段级转换（如时间字段字符串化）。

`makeRecordID` 把 `uniqueField` 的值拼接后用 `xxhash` 计算为一个稳定字符串 `_id`，保证相同维度组合的数据幂等写入同一文档；`asRecord` 将 `ETLRecord` 的 `Metrics`/`Dimensions`/`Time` 合并为 `map`，应用 `transformers`，再生成带 `ID` 与 `Type` 的 `Record`。

**章节来源**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L34-L55)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L57-L87)

## 写入流程（Handle / Flush）

`mermaid` 展示了从 `Payload` 到批量 `_bulk` 写入的处理路径：

```mermaid
flowchart LR
    P[Payload] --> H[Handle: 转 ETLRecord]
    H --> A[asRecord: 合并字段 + transformers + 算 _id]
    A --> F[Flush: 按 indexRender 分桶]
    F --> FL[flush: writer.Write 单桶批量写]
    FL --> R[解析 ESWriteResult 统计成功数]
```

**图表来源**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L90-L104)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L173-L214)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L106-L171)

- **`Handle`**：从 `Payload` 取出 `ETLRecord`（已解码则复用，否则 `To` 反序列化），返回记录与解析出的时间戳，标记为可进入后端批量阶段。
- **`Flush`**：遍历一批 `ETLRecord`，逐条 `asRecord` 后用 `indexRender` 求索引名；当索引切换时把上一索引的 `Records` 整体 `flush`，避免跨索引混写。
- **`flush`**：调用 `writer.Write(ctx, index, records)`，解析 `Response`。区分三类结果：`err != nil`、`response == nil`（按 `ErrDisaster` 处理）、`IsSysError()`（5xx，按 `ErrOperationForbidden` 处理）；正常响应则解析 `ESWriteResult`，统计 `Errors` 为 false 的条目数作为成功写入量，对失败项做分钟级采样告警。

**章节来源**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L90-L104)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L106-L171)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L173-L214)

## 索引渲染（IndexRenderFn）

`IndexRenderFn` 即 `func(record *Record) (string, error)`，决定文档落到哪个索引。`render.go` 提供三种实现：

- **`FixedIndexRender(name)`**：固定索引名，直接返回 `name`。
- **`ConfigTemplateRender(cluster)`**：依据 `StorageConfig` 的 `index_template_separator`、`index_datetime_field`、`index_datetime_timezone`、`index_datetime_format` 拼接 `时间串 + 分隔符 + index`。这是日志类结果表常用的"按天分索引"策略。
- **`TimeBasedIndexAliasRender(cluster)`**：依据 `index_alias_template` 把时间戳渲染成别名（要求 `index_alias_format` 存在，否则报错）。

`NewBackend` 在构建 `BulkHandler` 时调用 `ConfigTemplateRender(cluster)` 得到 `fn` 注入。

**章节来源**
- [elasticsearch/render.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/render.go#L23-L28)
- [elasticsearch/render.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/render.go#L30-L50)
- [elasticsearch/render.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/render.go#L52-L75)

## 版本化写入器（BulkWriter）

`BulkWriter` 接口仅两个方法：`Write(ctx, index, records) (*Response, error)` 与 `Close()`。`NewBulkWriter(version, config)` 通过全局 `writers` map 按版本号找到对应 `BulkWriterCreator`，各 ES 版本在各自 `init` 中 `RegisterBulkWriter(version, creator)` 注册。

`Response` 提供 `IsError()`（>299）与 `IsSysError()`（>499）辅助判定；`ESWriteResult` 对应 ES `_bulk` 响应结构，`Errors` 为 true 时遍历 `Items` 收集 `ESWriteResultError`（type/reason/caused_by）用于告警。

`NewBulkHandler` 依据 `cluster.GetVersion()` 取主版本号拼为 `vN`，据此创建对应 `BulkWriter`；同时遍历结果表的用户指定字段，对 `MetaFieldTypeTimestamp` 且配置了 `MetaFieldOptESFormat` 的字段注入时间字符串化 `transformer`。

**章节来源**
- [elasticsearch/define.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/define.go#L30-L95)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L221-L268)

## 注册与配置

`init()` 中 `define.RegisterBackend("elasticsearch", ...)` 把后端注册到全局工厂。工厂函数会校验 `config.FromContext` / `ShipperConfigFromContext` / `ResultTableConfigFromContext` 均非空，再读取 `PipelineConfig.Option` 中的 `maxQps`，调用 `NewBackend(ctx, rt.FormatName(name), maxQps)` 经 `pipeline.NewBulkBackendDefaultAdapter` 包装为限流后端。

`NewBackend` 从 `Context` 取 `ResultTableConfig`、`ShipperConfig.AsElasticSearchCluster()` 与 `ConfKeyPayloadFlushInterval`，组装 `BulkHandler` 并注入 `ConfigTemplateRender` 渲染函数。

**章节来源**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L270-L304)
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L306-L324)

## 结论

`elasticsearch` 包把 transfer 的 ETL 产物以幂等 `_id` + 时间分索引的方式批量写入 ES：版本化 `BulkWriter` 屏蔽 ES 版本差异，多种 `IndexRenderFn` 支持固定/按天/别名索引，写入结果按 `ESWriteResult` 精确统计成功量并做失败采样告警。

**章节来源**
- [elasticsearch/backend.go](file://bkmonitor-datalink/pkg/transfer/elasticsearch/backend.go#L34-L324)
