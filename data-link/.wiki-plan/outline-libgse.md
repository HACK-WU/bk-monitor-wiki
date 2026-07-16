# libgse Wiki 大纲（Outline）

> 模块根：`bkmonitor-datalink/pkg/libgse/`
> Wiki 根：`bk-monitor-wiki/data-link/libgse/`
> 排除项：`*_test.go`、`docs/`、`*.md`(非源码)、`go.mod`/`go.sum`/`Makefile`/`VERSION`、各 `test/` 子目录
> 源文件数估算：≈48（>30 → 启用分批）
> 拆分粒度：5 页（文件数 < 8，但源文件 > 30，仍按分批撰写）

## 目录树

```
bk-monitor-wiki/data-link/libgse/
├── 01-概览与架构.md
├── 02-beat框架入口与生命周期.md
├── 03-GSE-SDK通信层.md
├── 04-输出层与处理链.md
└── 05-基础组件.md
```

## 各页条目

### 01-概览与架构.md
- 引用：`README.md`、`beat/beat.go`、`gse/client.go`、`output/bkpipe/bkpipe.go`、`monitoring/bkmonitoring.go`
- 章节：简介 / 模块定位（蓝鲸监控底层通信组件）/ 包组织与职责地图 / 整体架构（mermaid graph）/ 数据上报主流程（sequenceDiagram）/ 与 data-link 其他模块关系 / 结论

### 02-beat框架入口与生命周期.md
- 引用：`beat/beat.go`、`beat/beater.go`、`beat/config.go`、`beat/init.go`、`beat/push.go`、`beat/version.go`、`beat/resource_limit_linux.go`
- 章节：简介 / 核心类型（Beat/Beater 接口）/ 启动与生命周期（Init→Run→Stop）/ 配置加载 / Push 上报封装 / 资源限制（Linux cgroup）/ 版本信息 / 故障排查

### 03-GSE-SDK通信层.md
- 引用：`gse/client.go`、`gse/gsesocket_unix.go`、`gse/gsetype.go`、`gse/mockagent.go`、`gse/simple_client.go`
- 章节：简介 / Client 接口与连接模型 / Unix Domain Socket 通信（gsesocket）/ 消息类型（gsetype）/ MockAgent / SimpleClient / 错误处理与重连 / 故障排查

### 04-输出层与处理链.md
- 引用：`output/bkpipe/bkpipe.go`、`output/bkpipe_multi/bkpipe_multi.go`、`output/bkpipe_multi/clients.go`、`output/bkpipe_multi/hash.go`、`output/bkpush/bkpush.go`、`output/gse/gse.go`、`output/gse/config.go`、`output/otlp/otlp.go`、`processor/actions/check.go`、`processor/actions/set_dataid.go`
- 章节：简介 / 输出后端总览（mermaid）/ bkpipe 单管道 / bkpipe_multi 多管道与一致性哈希 / bkpush / gse 输出 / otlp 输出 / processor actions 处理链 / 故障排查

### 05-基础组件.md
- 引用：`common/set.go`、`common/flowlimiter.go`、`common/utils.go`、`logp/logp.go`、`monitoring/bkmonitoring.go`、`monitoring/report/`、`reloader/reload.go`、`storage/storage.go`、`debug/debug.go`、`pidfile/pidfile.go`
- 章节：简介 / common 公共接口（集合/流控/工具）/ logp 日志 / monitoring 指标上报 / reloader 热重启 / storage 磁盘存储 / debug 调试 / pidfile / 结论

## 排期表（分批）

| 批次 | 页面 | 预计源文件数 |
|------|------|-------------|
| Batch 1 | 01, 02, 03 | ≈20（beat 8 + gse 8 + 概览引用 4） |
| Batch 2 | 04, 05 | ≈28（output 11 + processor 2 + 基础组件 15） |
