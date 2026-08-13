---
groupPath: 专题记忆/性能场景
relation: ThreadPool 4路并行聚合模式
exportedAt: "2026-08-13T12:06:50.216Z"
---
HostPerformanceResource 和 SearchHostMetricResource 都采用 ThreadPool 4 路并行聚合模式，拉取 Agent 状态、TSDB 性能指标、进程信息、告警计数四类异构数据源。核心聚合容器是 host_dict（dict[int, dict]），各 fetch 静态方法原地填充。

- 符号: `HostPerformanceResource.perform_request`、`SearchHostMetricResource.perform_request`、`get_agent_status`、`get_performance_data`、`get_process_status`、`get_alarm_count`、`ThreadPool`
- 位置: `bkmonitor/packages/monitor_web/performance/resources.py`

4 路并行聚合流程:
1. api.cmdb.get_host_by_topo_node 拉全量主机（或 get_host_by_id 精确拉）
2. api.cmdb.get_topo_tree 构造拓扑链
3. 构造 host_dict 默认值（status=UNKNOWN/cpu_usage=None/component=[]/alarm_count=[]）
4. ThreadPool 4 路并行:
   - get_agent_status → data[bk_host_id].status（调 resource.cc.get_agent_status）
   - get_performance_data → data[bk_host_id].update(metrics)（调 resource.cc.get_host_performance_data）
   - get_process_status → data[bk_host_id].component（调 resource.cc.get_process_info）
   - get_alarm_count → data[bk_host_id].alarm_count（调 resource.cc.get_host_alarm_count）
5. pool.join() 汇合 → 返回 {hosts, update_time}

两个 Resource 的关键差异:
- HostPerformanceResource: 走 HOST 缓存（CacheResource 子类）；get_alarm_count 无 try/except（异常中断聚合）；component 含 ports/protocol
- SearchHostMetricResource: 无缓存实时查；支持 start_time/end_time；get_alarm_count 有 try/except 降级（异常时 alarm_count 为空列表仅记日志）；component 不含 ports/protocol；bk_biz_id 经 validate_bk_biz_id 校验

host_dict 默认值兑底设计:
- status=AGENT_STATUS.UNKNOWN
- cpu_usage/mem_usage/io_util/disk_in_use/cpu_load/psc_mem_usage=None
- component=[]/alarm_count=[]
- 保证部分数据缺失时仍返回完整结构

扩展返回字段标准路径:
1. host_dict 默认值添加新字段（默认 None）
2. 新增静态 fetch 方法拉取新字段
3. ThreadPool 注册新方法
4. 如需实时查询也支持，在 SearchHostMetricResource 同步添加