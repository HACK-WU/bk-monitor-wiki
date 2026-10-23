---
groupPath: 关联关系/IP选择器
relation: bkm_ipchooser拓扑树-api.cmdb服务实例索引
exportedAt: "2026-10-21T09:40:35.069Z"
---
[强关联] bkm_ipchooser 拓扑树 与 api.cmdb 服务实例索引及全量明细接口
强度：必改——改 ServiceInstanceModuleIndex 的 cache key、字段名、build 逻辑或刷新调度，bkm_ipchooser 拓扑树的 service_instance 分支必须跟着改；只改拓扑树的统计分支，api.cmdb 不用管
原因：拓扑树复用该索引做数量统计，索引结构（key 为 str 的 module_id、value 为 id 列表）与写入时机（cron 分片刷新）直接决定统计结果正确性

bkm_ipchooser 端：
- TopoTool.get_topo_tree_with_count（service_instance 分支，当前全量拉取、目标改读索引）@ bkm_ipchooser/tools/topo_tool.py:93-103
- fill_host_count_to_tree（递归聚合，父节点为子树 ID 并集，module 节点取 len）@ bkm_ipchooser/tools/topo_tool.py:51-63
- IpChooserTopoViewSet.trees @ bkm_ipchooser/views.py:107
- IpChooserServiceInstanceViewSet.details（按 service_instance_id_list 反查详情）@ bkm_ipchooser/views.py:213-221
- batch_request（limit 与并发度全局参数）@ bkm_ipchooser/tools/batch_request.py:38-94

api.cmdb 端：
- ServiceInstanceModuleIndex（CACHE_KEY、build、set、get）@ api/cmdb/default.py:183-220
- get_service_instance_by_biz（全量拉明细后写索引）@ api/cmdb/default.py:223-234
- GetServiceInstanceIdsByTopoNode（现成消费方，索引缺失抛 CustomError）@ api/cmdb/default.py:758-778
- GetServiceInstanceByID（带 id 过滤反查详情）@ api/cmdb/default.py:781-799
- ListServiceInstanceDetail（CMDB 接口，返回含 process_instances）@ api/cmdb/client.py:178-262

刷新调度端：
- cache_cmdb_resource、biz_is_ready、API_CRONTAB、RING_NODES @ alarm_backends/core/api_cache/library.py:50-64,112-137,169-184
- 覆盖范围取决于 StrategyModel 中是否存在该业务的策略

关键不变式：索引 key 为 str(module_id)，消费侧必须 int 与 str 双向转换；索引缺失时必须回退而非抛错（拓扑树不能因缓存未就绪报错）；数量语义是去重后的 id 集合长度，父节点为子树并集而非简单求和