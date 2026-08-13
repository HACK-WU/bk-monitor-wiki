---
groupPath: 关联关系/场景视图
relation: GetHostProcessListResource-UnifyQuery-CMDB
exportedAt: "2026-08-13T11:54:56.254Z"
---
[强关联] GetHostProcessListResource 主机进程列表 与 UnifyQuery/CMDB 进程数据
强度：必改——改 system.proc 表字段名或 CMDB 进程接口结构时，GetHostProcessListResource 的 runtime_metric_map 和维度查询必须跟着改；改进程列表的返回字段，前端联动改
原因：GetHostProcessListResource 聚合 CMDB 进程信息 + 4 路并发 UnifyQuery 查询 system.proc 表，字段映射硬编码在 runtime_metric_map，TSDB 字段名变更直接级联影响 UI 返回

源端（进程列表聚合）:
- `GetHostProcessListResource.perform_request` @ `bkmonitor/packages/monitor_web/scene_view/resources/host.py`
- `get_process_runtime_metrics` @ `bkmonitor/packages/monitor_web/scene_view/resources/host.py`（4 路并发 ThreadPool 查询）
- `runtime_metric_map` 硬编码 UI→TSDB 字段名映射（cpuUsage→cpu_usage_pct、memRss→mem_res、memUsage→mem_usage_pct、fdNum→fd_num 等）

目标端（取数依赖）:
- `UnifyQuery` / `load_data_source(BK_MONITOR_COLLECTOR, TIME_SERIES)` @ `bkmonitor/bkmonitor/data_source/`（查 system.proc 表运行时指标）
- CMDB 进程接口（查进程基础信息：name/status/protocol/bindIp/port/user/startCommand）
- system.proc_port 表（端口健康状态 port_health，单独接口 GetHostProcessPortStatusResource）
- 单位高频坑: memRss 是字节；memUsage 是 percentunit 0-1；与主机列表 mem_usage（percent 0-100）含义不同