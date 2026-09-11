---
groupPath: 专题记忆/APM
relation: Profiling技术架构总览
exportedAt: "2026-09-07T03:43:18.231Z"
---
APM Profiling 技术架构：开源生态 + 自研实现的混合方案。Profiling 是与 Trace/Metric/Log 并列的第四类遥测数据，回答“代码里哪个函数消耗 CPU/内存”，以周期性采样调用栈方式聚合成函数级资源统计，可视化核心产物为火焰图。
- 技术分层：① 上报协议=兼容 Grafana Pyroscope 的 ingest 协议（端点 /pyroscope/ingest），数据格式 pprof（Go 原生）/perf_script/jfr，另支持 OTLP HTTP；② 采集探针=应用侧 Pyroscope SDK / OpenTelemetry，eBPF 免插桩场景走 DeepFlow（应用名带 ebpf- 前缀，EBPF_PROFILING_APP_PREFIX）；③ 接入端=bk-collector（蓝鲸自研 Go 采集器，已集成 pyroscope ingestion）；④ 存储=Doris（经 BkData V3/V4 清洗链路入 Doris，不走 ES）；⑤ 解析与可视化=apm_web/profile 自研模块。
- 设计动机：面向用户兼容 Pyroscope 生态（用户可直接用 Grafana 成熟 SDK，无需自造探针）；底座复用 Doris + bk-collector；中间解析、存储链路与可视化全部自研。
- 位置: `bkmonitor/packages/apm_web/profile/`（约 148 个 Python 文件涉及 profiling）