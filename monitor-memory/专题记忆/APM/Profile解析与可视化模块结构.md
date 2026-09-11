---
groupPath: 专题记忆/APM
relation: Profile解析与可视化模块结构
exportedAt: "2026-09-07T03:43:18.232Z"
---
apm_web/profile 自研模块结构：负责 pprof/perf_script/jfr 三种格式解析与火焰图等可视化渲染。
- 位置: `bkmonitor/packages/apm_web/profile/`
- 关键组件:
  - 解析器: `pprof/converter.py`（pprof 格式）、`perf/converter.py`（perf_script 格式）；file_type choices 含 perf_script/pprof/jfr（见 models/profile.py ProfileUploadRecord）
  - 查询: `doris/querier.py`（Doris 查询）、`doris/converter.py`
  - 可视化: `diagrams/` 目录，含 flamegraph（火焰图）、callgraph（调用图）、tendency（趋势图）、diff（双图对比）、table、dotgraph、tree_converter、grafana_flame（Grafana 火焰图适配）、ebpf_converter
  - 数据模型: `models/profile.py` ProfileUploadRecord（上传记录：bk_biz_id/app_name/file_type/md5/数据时间窗口等）
- 关键常量（constants.py）: 默认数据类型 cpu/nanoseconds、默认导出格式 pprof、大应用查询上限 5000 条 sample、普通服务 10000 条、grafana label 上限 1000、内置全局存储应用名 builtin_profile_app