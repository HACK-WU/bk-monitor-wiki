---
groupPath: 专题记忆/性能场景
relation: HOST缓存与实时查询机制
exportedAt: "2026-08-13T12:06:50.216Z"
---
HostPerformanceResource 继承 CacheResource，cache_type=CacheType.HOST，缓存整份主机列表降低 CMDB/TSDB 压力。SearchHostMetricResource 无缓存每次实时查。两者适用场景不同。

- 符号: `CacheResource`、`CacheType.HOST`、`HostPerformanceResource`、`SearchHostMetricResource`
- 位置: `bkmonitor/packages/monitor_web/performance/resources.py`

HostPerformanceResource 缓存机制:
- 继承 CacheResource，cache_type = CacheType.HOST
- 缓存 key: CacheType.HOST + bk_biz_id
- 缓存未命中时全量拉取（get_host_by_topo_node + get_topo_tree + 4路并行）
- 缓存命中时直接返回缓存数据（可能不实时）
- 缓存由 CacheResource 框架自动管理，模块内无主动刷新/失效逻辑

SearchHostMetricResource 实时查询:
- 无缓存，每次请求都 4 路并发查 TSDB
- 按 bk_host_ids 精确查询（api.cmdb.get_host_by_id）
- 支持 start_time/end_time 时间范围（不传默认最近三分钟）
- bk_biz_id 经 validate_bk_biz_id 空间/租户校验
- get_alarm_count 有 try/except 降级

选择指南:
- 需要全量主机列表 → HostPerformanceResource（走缓存，快但可能不实时）
- 需要指定主机实时指标 → SearchHostMetricResource（无缓存，实时但慢）
- 需要指定时间范围 → SearchHostMetricResource（HostPerformanceResource 不支持时间范围）

缓存一致性:
- 一致性依赖 HOST 缓存刷新周期与实时接口的 TSDB 查询时间范围
- 缓存失效后的首次请求会全量拉取（热点）
- 新增实时字段需评估缓存一致性影响