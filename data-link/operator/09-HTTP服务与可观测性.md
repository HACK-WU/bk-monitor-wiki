<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->
# operator HTTP 服务与可观测性

<cite>
- [operator/server.go](file://bkmonitor-datalink/pkg/operator/operator/server.go)
- [operator/recorder.go](file://bkmonitor-datalink/pkg/operator/operator/recorder.go)
- [operator/metrics.go](file://bkmonitor-datalink/pkg/operator/operator/metrics.go)
- [operator/relabel.go](file://bkmonitor-datalink/pkg/operator/operator/relabel.go)
- [operator/scrape.go](file://bkmonitor-datalink/pkg/operator/operator/scrape.go)
</cite>

## 目录
- [模块定位](#模块定位)
- [HTTP 路由矩阵](#http-路由矩阵)
- [健康巡检 CheckRoute](#健康巡检-checkroute)
- [Recorder 活动配置记录](#recorder-活动配置记录)
- [指标与 relabel 构造](#指标与-relabel-构造)
- [抓取调试](#抓取调试)

## 模块定位

本页说明 operator 暴露的 HTTP 服务与可观测能力：提供健康检查（`/check/*`）、活动配置查询、Prometheus 指标端点、relabel 规则构造与抓取调试接口，是运维排查与自监控的主要入口。

**章节来源**
- [operator/server.go](file://bkmonitor-datalink/pkg/operator/operator/server.go#L281-L399)

## HTTP 路由矩阵

| 路由 | Handler | 说明 |
|------|---------|------|
| `/check` | `CheckRoute` | 集群健康度聚合巡检 |
| `/check/namespace` | `CheckNamespaceRoute` | 监测命名空间白/黑名单 |
| `/check/blacklist` | `CheckMonitorBlacklistRoute` | 监控资源黑名单规则 |
| `/check/dataid` | `CheckDataIdRoute` | 已加载 DataID 列表 |
| `/check/discover` | `CheckActiveDiscoverRoute` | 当前活跃 discover |
| `/check/childconfig` | `CheckActiveChildConfigRoute` | 当前活跃子配置 |
| `/check/shareddiscovery` | `CheckActiveSharedDiscoveryRoute` | 共享发现状态 |
| `/check/monitorresource` | `CheckMonitorResourceRoute` | 监控资源记录 |
| `/check/scrape` | `CheckScrapeRoute` | 抓取指标统计 |

**章节来源**
- [operator/server.go](file://bkmonitor-datalink/pkg/operator/operator/server.go#L61-L158)
- [operator/server.go](file://bkmonitor-datalink/pkg/operator/operator/server.go#L281-L399)

## 健康巡检 CheckRoute

`CheckRoute` 聚合多项健康检查：kubernetes 版本、operator/helmcharts 版本、DataID 数量（应 ≥3）、集群信息、dryrun 标识、命名空间、黑名单、集群资源数量、Endpoint 数量、采集数据行数（>300w 预警）、Secret 操作错误、关键字匹配的监控资源。输出可读的诊断报告，是排障第一入口。

**章节来源**
- [operator/server.go](file://bkmonitor-datalink/pkg/operator/operator/server.go#L281-L399)

## Recorder 活动配置记录

`Recorder` 记录当前活动配置与监控资源：`activeConfigFile`（`ConfigFileRecord`：Service/DataID/FileName/Node/Meta/Address/Target）与 `MonitorResourceRecord`。它支撑 `/check/childconfig`、`/check/monitorresource` 等接口，并供指标上报使用（`updateConfigFiles`/`getActiveConfigFiles`/`getMonitorResources`）。

**章节来源**
- [operator/recorder.go](file://bkmonitor-datalink/pkg/operator/operator/recorder.go#L21-L42)

## 指标与 relabel 构造

`metrics.go` 以 `promauto` 注册 Prometheus 指标：`cluster_version`、`uptime`、`build_info`、`node_config_count` 等，覆盖集群/节点/Secret/StatefulSet Worker/dispatch 耗时等维度。`relabel.go` 负责 relabel 规则构造：`initRelabelings` 内置把 prometheus job 名重标签为 `monitor_type` 的规则，`yamlToRelabels` 把 YAML 配置转换为 prometheus relabel 配置。

**章节来源**
- [operator/metrics.go](file://bkmonitor-datalink/pkg/operator/operator/metrics.go#L22-L49)
- [operator/relabel.go](file://bkmonitor-datalink/pkg/operator/operator/relabel.go#L31-L54)

## 抓取调试

`scrape.go` 定义抓取统计结构（`scrapeStats`/`scrapeStat`：monitor 数量、数据行数、错误数、TOP 明细），`/check/scrape`（`CheckScrapeRoute`）由此提供按 worker/namespace/monitor 的抓取数据统计与指标分析，用于核对采集数据量与错误。

**章节来源**
- [operator/scrape.go](file://bkmonitor-datalink/pkg/operator/operator/scrape.go#L24-L40)
- [operator/server.go](file://bkmonitor-datalink/pkg/operator/operator/server.go#L94-L99)
