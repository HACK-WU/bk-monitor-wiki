---
groupPath: 专题记忆/性能场景
relation: host_dict运行时内存结构
exportedAt: "2026-08-13T12:07:32.331Z"
---
性能场景模块无持久化数据模型，models.py 已迁空（注释「迁移至 monitor_api 中的 model」）。所有数据为运行时聚合的内存结构 host_dict（dict[int, dict]），由 perform_request 构造，各 fetch 静态方法原地填充。

- 符号: `host_dict`、`component`、`alarm_count`
- 位置: `bkmonitor/packages/monitor_web/performance/resources.py`

host_dict 单项结构（运行时）:
- CMDB 字段: display_name/bk_host_id/bk_biz_id/bk_cloud_id/bk_cloud_name/bk_host_innerip/bk_host_outerip/bk_host_name/bk_os_name/bk_os_type/bk_state/region/ignore_monitoring/is_shielding
- 模块拓扑: module（list[dict]，由 SearchHostInfoResource.get_module_info 构造）
- TSDB 性能指标: cpu_usage/cpu_load/psc_mem_usage/mem_usage/io_util/disk_in_use（默认 None）
- Agent 状态: status（默认 AGENT_STATUS.UNKNOWN，由 resource.cc.get_agent_status 填充）
- 进程: component（list[dict]，默认 []，由 resource.cc.get_process_info 填充）
- 告警: alarm_count（list[dict]，默认 []，由 resource.cc.get_host_alarm_count 填充）

component 单项结构:
- display_name: 进程名
- ports/protocol: 端口列表/协议（仅 HostPerformanceResource 版含，SearchHostMetricResource 版不含）
- status: 进程状态
- id/bindIp/port/startCommand/user: 进程详情

alarm_count 单项结构:
- level: 告警级别
- count: 告警数量

字段差异高频坑:
- HostPerformanceResource 的 component 含 ports/protocol，SearchHostMetricResource 不含
- mem_usage 在性能场景是 system.mem.pct_used（percent 0-100）
- 与场景视图进程列表的 memUsage（system.proc.mem_usage_pct，percentunit 0-1）含义不同
- 跨接口消费时注意字段差异和单位混淆