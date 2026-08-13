---
groupPath: 关联关系/性能场景
relation: Resource-resource.cc-多源拉取
exportedAt: "2026-08-13T12:07:32.331Z"
---
[强关联] HostPerformanceResource/SearchHostMetricResource 与 resource.cc.* 多源数据拉取
强度：必改——改 resource.cc.* 的方法签名或返回结构时，所有 fetch 静态方法必须跟着改；改 fetch 方法的参数，resource.cc.* 不用管
原因：4 路并行聚合依赖 resource.cc.get_agent_status/get_host_performance_data/get_process_info/get_host_alarm_count 拉取异构数据，任一方法签名或返回结构变更级联影响 host_dict 填充

源端（聚合 Resource + fetch 方法）:
- `HostPerformanceResource.perform_request` / `get_process_status` / `get_alarm_count` @ `bkmonitor/packages/monitor_web/performance/resources.py`
- `SearchHostMetricResource.perform_request` / `get_agent_status` / `get_performance_data` / `get_process_status` / `get_alarm_count` @ `bkmonitor/packages/monitor_web/performance/resources.py`
- ThreadPool 4 路并行: get_agent_status/get_performance_data/get_process_status/get_alarm_count

目标端（resource.cc.* 底层实现）:
- `resource.cc.get_agent_status` @ `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`（返回 {bk_host_id: status} 映射）
- `resource.cc.get_host_performance_data` @ `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`（返回 {bk_host_id: {cpu_usage, mem_usage, ...}}，查 TSDB）
- `resource.cc.get_process_info` @ `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`（返回 {bk_host_id: [process_dict]}）
- `resource.cc.get_host_alarm_count` @ `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`（返回 {bk_host_id: {level: count}}）
- `resource.cc.get_topo_strategy_count` @ `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`（拓扑节点策略数）