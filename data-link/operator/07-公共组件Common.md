<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->
# operator 公共组件 Common

<cite>
- [common/k8sutils/client.go](file://bkmonitor-datalink/pkg/operator/common/k8sutils/client.go)
- [common/define/monitor.go](file://bkmonitor-datalink/pkg/operator/common/define/monitor.go)
- [common/tasks/tasks.go](file://bkmonitor-datalink/pkg/operator/common/tasks/tasks.go)
- [common/notifier/bus.go](file://bkmonitor-datalink/pkg/operator/common/notifier/bus.go)
- [common/notifier/alarm.go](file://bkmonitor-datalink/pkg/operator/common/notifier/alarm.go)
- [common/feature/feature.go](file://bkmonitor-datalink/pkg/operator/common/feature/feature.go)
- [common/action/action.go](file://bkmonitor-datalink/pkg/operator/common/action/action.go)
</cite>

## 目录
- [模块定位](#模块定位)
- [k8sutils：客户端构造](#k8sutils客户端构造)
- [define：领域类型](#define领域类型)
- [tasks：任务命名与类型](#tasks任务命名与类型)
- [notifier：事件总线与告警](#notifier事件总线与告警)
- [feature：注解与标签特性](#feature注解与标签特性)
- [action：资源操作动作](#action资源操作动作)
- [其他公共子包](#其他公共子包)

## 模块定位

`common/` 是 operator 与 reloader 共享的公共组件层，提供 k8s 客户端构造、领域类型、任务/Secret 命名、事件总线、注解特性解析、资源操作动作等基础能力。核心控制器（`operator/`、`reloader/`）均强依赖本层。

**章节来源**
- [common/k8sutils/client.go](file://bkmonitor-datalink/pkg/operator/common/k8sutils/client.go#L46-L70)

## k8sutils：客户端构造

`k8sutils` 封装各类 k8s 客户端构造：`NewK8SClient`（带 TLS 的 kubernetes 客户端）、`NewMetadataClient`（metadata 客户端）、`NewK8SClientInsecure`（insecure 客户端，reloader 使用）、`NewBKClient`/`NewPromClient`（operator 中的 bk/prom 客户端）。统一设置 protobuf 内容类型。

**章节来源**
- [common/k8sutils/client.go](file://bkmonitor-datalink/pkg/operator/common/k8sutils/client.go#L46-L70)

## define：领域类型

`define` 定义全局常量与领域类型：`AppName`/`MonitorNamespace`/`UnknownNode`、`ReSyncPeriod`（informer 默认 resync 周期 5min）；`MonitorMeta`（监控资源的元数据：Name/Kind/Namespace/Index，其 `ID()` 即 discover 名称）；`ClusterInfo`（集群元数据）。`MonitorMeta` 贯穿所有 discover 与控制器。

**章节来源**
- [common/define/monitor.go](file://bkmonitor-datalink/pkg/operator/common/define/monitor.go#L17-L39)

## tasks：任务命名与类型

`tasks` 定义任务类型与 Secret 命名规则：`TaskTypeDaemonSet`/`TaskTypeEvent`/`TaskTypeStatefulSet` 三种类型及前缀；`GetDaemonSetTaskSecretName`（按 node）、`GetStatefulSetTaskSecretName`（按索引）、`GetEventTaskSecretName`、`GetTaskLabelSelector`（taskType 标签选择）用于 Secret 的命名与查询。`ValidateTaskType` 校验类型合法性。

**章节来源**
- [common/tasks/tasks.go](file://bkmonitor-datalink/pkg/operator/common/tasks/tasks.go#L16-L50)

## notifier：事件总线与告警

`notifier` 提供解耦的事件通知原语：`RateBus` 是一个带限频的发布/订阅总线（`NewDefaultRateBus`/`NewRateBus`，`Publish` 重置定时器、`Subscribe` 返回通道），discover 与 operator 的调度即基于此去抖；`Alarmer` 是按周期的告警触发（`NewAlarmer`/`Alarm`），用于周期性全量 resync 的标志。

**章节来源**
- [common/notifier/bus.go](file://bkmonitor-datalink/pkg/operator/common/notifier/bus.go#L20-L53)
- [common/notifier/alarm.go](file://bkmonitor-datalink/pkg/operator/common/notifier/alarm.go#L14-L29)

## feature：注解与标签特性

`feature` 解析监控资源上的注解/标签特性：如 `scheduledDataID`（直接指定 DataID，优先级最高）、`extendLabels`（扩展标签）、`isSystem`/`isCommon`（资源分类）、`antiAffinity`/`relabelRule`/`monitorMatchSelector` 等。`LabelJoinMatcherSpec` 描述 labeljoin 规则。这些特性在 discover 构建与 DataID 选择时被消费。

**章节来源**
- [common/feature/feature.go](file://bkmonitor-datalink/pkg/operator/common/feature/feature.go#L19-L63)

## action：资源操作动作

`action` 定义资源操作的动作常量：`Add`/`Delete`/`Update`/`CreateOrUpdate`/`Skip`，被 operator 与 reloader 在 Secret 增删改处理时统一使用（如 `k8sutils.CreateOrUpdateSecret`、reloader 的 `handleSecrets`）。

**章节来源**
- [common/action/action.go](file://bkmonitor-datalink/pkg/operator/common/action/action.go#L12-L18)

## 其他公共子包

| 子包 | 定位（基于目录与命名） |
|------|------|
| `env` | 运行环境变量与元信息（MetaEnv）读取 |
| `eplabels` | 监控资源 Endpoint 标签处理 |
| `filewatcher` | 配置文件路径监听（run/reloader 热加载配置） |
| `httpx` | HTTP 请求/客户端辅助 |
| `labelspool` | 标签池管理（discover 标签分配） |
| `logx` | 日志封装（k8sutils 使用） |
| `promfmt` | Prometheus 配置/格式辅助 |
| `utils` | 通用工具（字符串/哈希/匹配等，被多处引用） |

**章节来源**
- [common/k8sutils/client.go](file://bkmonitor-datalink/pkg/operator/common/k8sutils/client.go#L46-L70)
