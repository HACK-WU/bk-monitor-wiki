# ETL 转换

> `etl` 包是 transfer 的**声明式字段/记录转换框架**：以 `Container`（中间数据结构）为媒介，把上游 `Payload` 中的原始字段按 `MetaFieldConfig` 抽取、转换、裂变，产出标准化的 `ETLRecord`。它既定义了丰富的 Record/Field 组合原语，也提供了按字段类型分发的具体转换器。

<cite>
**本文引用的文件**
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go)
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go)
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go)
</cite>

## 目录

1. [简介](#简介)
2. [记录模型（Record）](#记录模型record)
3. [字段与转换（Field）](#字段与转换field)
4. [转换函数与类型分发](#转换函数与类型分发)
5. [中间容器与层级裂变](#中间容器与层级裂变)
6. [结论](#结论)

## 简介

ETL 的核心问题是"如何把任意结构的原始上报，转换为统一的 `ETLRecord`"。transfer 采用**声明式**方案：每个字段由 `Field`（含 `extract` 抽取 + `transform` 转换）描述，多个字段组合进 `Record`，`Record.Transform(from, to)` 在 `Container` 上完成"从原始容器抽取 → 写入目标容器"。这种组合式设计让同一套引擎能适配时序/事件/日志等多种数据。

**章节来源**
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go#L27-L72)
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L22-L47)

## 记录模型（Record）

`Record` 是转换单元的组合原语，所有具体类型内嵌 `BaseRecord`（含 `name` 与默认 `Finish`），并通过 `Transform(from, to Container) error` 实现各自的转换逻辑：

- **`SimpleRecord`**：管理一组 `Fields` 与子 `Records`，`Transform` 先转换所有子记录再 `LazyTransform` 字段（支持 `ErrFieldNotReady` 延迟二次执行）。
- **`ComplexRecord`**：顺序执行多个子 `Record`，`Finish` 聚合各子记录错误。
- **`IterationRecord`**：取某字段的 `[]interface{}`，对其每个元素迭代执行子 `Record`（用于数组展开/裂变）。
- **`OptionalRecord`**：字段转换失败仅告警不中断（可选字段）。
- **`PrepareRecord` / `ReprocessRecord`**：分别在 `from→from` / `to→to` 上做预处理/后处理。
- **`FunctionalRecord` / `NewCopyRecord`**：以函数或"全量拷贝"方式转换（如把 `from` 的所有 key 复制到 `to`）。

`LazyFieldsMixin.LazyTransform` 是延迟字段机制的核心：首轮遇到 `ErrFieldNotReady` 的字段留到末轮执行，解决字段间依赖顺序问题。

**章节来源**
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L76-L136)
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L138-L256)
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L258-L326)
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L20-L74)

## 字段与转换（Field）

`Field` 描述"一个目标字段如何由源数据得到"，核心是 `SimpleField`：

- **`BaseField`**：持有 `name` 与默认值构造器（`DefaultValue()` 在缺失时回退）。
- **`DefaultsField`**：`Transform` 时若目标容器无该字段则写入默认值（`ErrDisaster` 兜底）。
- **`ConstantField`**：`Transform` 直接把常量写入目标。
- **`SimpleField`**：最常用。`extract` 从源容器抽取原始值，`transform` 转换后 `GetValue` 返回；抽取/转换失败均回退默认值。`Transform` 还会处理 `DbmRecord` 特殊类型（把响应体/响应字段拆分写入），并依据 `options` 做时间戳单位换算。
- **`FutureField`**：首轮 `Transform` 返回 `ErrFieldNotReady`（`ready=false`），由 `LazyTransform` 在末轮重放，用于跨字段依赖。
- **`FunctionField` / `MergeField`**：以函数方式转换；`MergeField` 把一个容器字段展开平铺到目标容器。
- **`PrepareField` / `InitialField`**：分别在对 `from` / 仅首次写入目标时转换。

字段体系与 Record 体系正交组合，构成"Record 编排字段、字段描述取值"的声明式 ETL。

**章节来源**
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go#L27-L133)
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go#L135-L317)
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go#L357-L454)

## 转换函数与类型分发

`transformer.go` 提供一系列可复用的 `TransformFn` 与按类型工厂：

- **`TransformAsIs`**：原样返回。
- **`TransformMapByJSON` / `TransformMapByRegexp` / `TransformMapBySeparator`**：把字符串按 JSON / 正则命名分组 / 分隔符拆成 map；均带 `LogCleanFailedFlag` 标记清洗是否失败。
- **`TransformContainer` / `TransformObject` / `TransformNested`**：处理 object / nested 类型（map 与数组互转）。
- **`TransformChain`**：把多个转换函数串联。
- **`NewTransformByType(name MetaFieldType)`**：按元数据字段类型选择转换器（int/uint/float/string/bool/timestamp → 对应 `TransformNilXxx`；object/nested → 对应转换）。
- **`NewTransformByField(field, rt)`**：综合字段配置生成转换器，支持 dbm 慢查询解析（`ParseDbmSlowQuery` 带指数退避重试）、保留原始字符串、按时间格式/时区/单位解析时间戳等高级能力。

这些是 `SimpleField.transform` 的具体实现来源，使"元数据驱动 ETL"得以落地。

**章节来源**
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go#L37-L40)
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go#L125-L188)
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go#L209-L284)
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go#L365-L483)

## 中间容器与层级裂变

ETL 全程以 `Container` 作为中间数据结构（`from` 原始容器、`to` 目标容器），所有 `Field`/`Record` 的 `Transform(from, to)` 都基于 `Container` 的 `Get`/`Put`/`Keys`/`Del` 操作。容器屏蔽了底层 JSON/map 差异，使同一套字段逻辑可复用于不同数据来源。

结合 `IterationRecord`（数组裂变）、`MergeField`（层级平铺）、`TransformNested`/`TransformObject`（嵌套展开），transfer 能处理从平面日志到多层嵌套指标/事件的复杂结构，最终落到 `define.ETLRecord` 的 `Dimensions`/`Metrics`/`Exemplar` 上，供后端写入存储。

**章节来源**
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L107-L117)
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go#L428-L446)
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go#L230-L260)

## 结论

`etl` 包以"Record 组合 + Field 取值 + Container 媒介 + Transformer 类型分发"的声明式框架，把任意原始上报转换为标准 `ETLRecord`。其延迟字段（`FutureField`/`LazyTransform`）、可选字段、裂变/聚合、dbm 解析等能力，使其足以承载时序/事件/日志的统一 ETL，并完全由 consul 下发的 `MetaFieldConfig` 驱动。本篇是理解 pipeline 中 `ProcessNode` 如何完成数据标准化的关键。

**章节来源**
- [etl/record.go](file://bkmonitor-datalink/pkg/transfer/etl/record.go#L76-L136)
- [etl/field.go](file://bkmonitor-datalink/pkg/transfer/etl/field.go#L135-L317)
- [etl/transformer.go](file://bkmonitor-datalink/pkg/transfer/etl/transformer.go#L262-L284)
