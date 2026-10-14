---
groupPath: 关联关系/性能场景
relation: GetHostIdentities-业务主机预热缓存
exportedAt: "2026-09-22T08:22:27.541Z"
---
[强关联] api.cmdb.GetHostIdentities 与 CMDB 业务主机预热缓存（cmdb_api_list）
强度：必改——改任何一端的缓存键构造方式或字段集，统计接口会静默退化为全量回源（性能退化，不是功能报错）；改 GetHostIdentities 的输出字段，统计表达式与身份歧义判定必改

原因：GetHostIdentities 不查 CMDB，而是复用 get_host_dict_by_biz(bk_biz_id, Host.Fields) 的预热结果；缓存键由位置参数与字段集决定

缓存消费端：
- GetHostIdentities.perform_request（预热位置参数、has_duplicate_ip 的 Counter 统计）@ bkmonitor/api/cmdb/default.py:381
- get_host_dict_by_biz @ bkmonitor/api/cmdb/default.py:53

统计消费端：
- SearchHostMetricStatsResource.perform_request（取身份白名单）@ bkmonitor/packages/monitor_web/performance/resources.py:684
- query_host_metric_stats（身份歧义判定用 has_duplicate_ip）@ bkmonitor/packages/monitor_web/performance/host_metric_stats.py:67

排查信号：统计接口变慢但结果正确，先查预热缓存是否命中（调用参数与字段集是否与 cmdb_api_list 一致）