# 路由层 Route

<cite>
**本文引用的文件**
- [route/route.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/route.go)
- [route/manager.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/manager.go)
- [route/execution.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/execution.go)
- [route/anaylize.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/anaylize.go)
- [route/utils.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/utils.go)
- [route/struct.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/struct.go)
- [route/define.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/define.go)
- [route/influxql/](file://bkmonitor-datalink/pkg/influxdb-proxy/route/influxql/)
</cite>

## 目录
1. [路由管理器与生命周期](#路由管理器与生命周期)
2. [请求入口与路由匹配](#请求入口与路由匹配)
3. [查询执行器](#查询执行器)
4. [写入执行器](#写入执行器)
5. [Line Protocol 解析](#line-protocol-解析)
6. [请求与数据模型](#请求与数据模型)

## 路由管理器与生命周期

`Manager` 是路由层的核心，内部维护 `routeMap → cluster.Cluster` 的映射。其生命周期由 `Init` / `Reload` / `Refresh` 驱动，配置来自 consul 的路由表。对外提供 `GetClusterByRoute`（按 `db.measurement` 路径匹配 cluster，含默认路由回退）与 `GetClusterByName`，是上层 `http` handler 获取目标集群的入口。

**章节来源**
- [route/manager.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/manager.go#L31-L107)
- [route/manager.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/manager.go#L125-L135)
- [route/manager.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/manager.go#L197-L263)

## 请求入口与路由匹配

`route.go` 暴露四个包级入口变量：`Query` / `Write` / `RawQuery` / `CreateDB`，由 `http` handler 直接调用。`FormatRoute` / `GetRouteCluster` 负责路由键拼装与 cluster 获取。匹配逻辑在 `Manager.GetClusterByRoute` 中完成，支持精确匹配与默认路由回退，保证未显式配置的 db 也能落到兜底集群。

**章节来源**
- [route/route.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/route.go#L24-L39)
- [route/utils.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/utils.go#L20-L42)

## 查询执行器

查询请求根据 InfluxQL 语句类型被分发到不同执行器：`getQueryExecution` 按语句类型（select / show measurements / show tag keys 等）选择 `selectExecution` / `showXxxExecution`；`basicQueryAction` 调用 `cluster.Query` / `cluster.QueryInfo` 执行实际查询，`handleResult` 统一处理返回结果。这种「按 SQL 类型分派」的设计让新增语句类型只需扩展对应执行器，不侵入主流程。

**章节来源**
- [route/execution.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/execution.go#L27-L66)
- [route/execution.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/execution.go#L283-L332)
- [route/execution.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/execution.go#L373-L400)
- [route/define.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/define.go#L19-L28)

## 写入执行器

写入链路：`writeExecution` 先解析 line protocol point，再按 route 维度分组，最终调用 `cluster.Write` 落到目标后端。分组粒度与 `common.GenerateBackendRoute` 的 tag 路由算法保持一致，确保同一 tag 集合的 point 写入同一 backend。`route/influxql/` 负责 SQL 语句类型识别，支撑写入/查询的分派判断。

**章节来源**
- [route/execution.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/execution.go#L69-L168)
- [common/tags.go](file://bkmonitor-datalink/pkg/influxdb-proxy/common/tags.go#L27-L27)

## Line Protocol 解析

`AnaylizeTagData` 逐行扫描 line protocol，识别 measurement / tag / field / timestamp，产出 `common.Points`。它是写入前的数据预处理环节，把原始文本转成结构化 point，供后续按 route 分组与分发。`route/influxdata.go` 提供 influxdb point 解析工具（源自 vendored 逻辑）。

**章节来源**
- [route/anaylize.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/anaylize.go#L22-L105)
- [common/struct.go](file://bkmonitor-datalink/pkg/influxdb-proxy/common/struct.go#L16-L29)

## 请求与数据模型

`struct.go` 定义请求/结果模型：`QueryParams` / `WriteParams` / `ExecuteResult`，承载 handler 与 route、route 与 cluster 之间的参数传递。`define.go` 定义执行器函数类型（如 `RawQueryExecution`），使执行器可被统一注册与调用，支撑「按类型分派」的可扩展架构。

**章节来源**
- [route/struct.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/struct.go#L41-L109)
- [route/define.go](file://bkmonitor-datalink/pkg/influxdb-proxy/route/define.go#L19-L28)
