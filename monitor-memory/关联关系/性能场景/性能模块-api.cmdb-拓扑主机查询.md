---
groupPath: 关联关系/性能场景
relation: 性能模块-api.cmdb-拓扑主机查询
exportedAt: "2026-08-13T12:07:32.331Z"
---
[强关联] 性能场景模块 与 api.cmdb.* 拓扑/主机查询接口
强度：必改——改 api.cmdb.* 的方法签名或返回结构时，性能模块的所有 Resource 必须跟着改；改 Resource 的查询逻辑，api.cmdb 不用管
原因：性能模块 6 个 Resource 都依赖 api.cmdb.* 拉取主机列表、拓扑树、主机详情、业务信息等，接口变更级联影响所有聚合路径

源端（性能模块 Resource）:
- `HostPerformanceResource.perform_request` @ `bkmonitor/packages/monitor_web/performance/resources.py`（调 api.cmdb.get_host_by_topo_node + get_topo_tree）
- `HostPerformanceDetailResource.perform_request` @ `bkmonitor/packages/monitor_web/performance/resources.py`（调 api.cmdb.get_host_by_id + get_business + get_module）
- `HostTopoNodeDetailResource.perform_request` @ `bkmonitor/packages/monitor_web/performance/resources.py`（调 api.cmdb.get_topo_tree + get_host_by_topo_node）
- `TopoNodeProcessStatusResource.perform_request` @ `bkmonitor/packages/monitor_web/performance/resources.py`（调 api.cmdb.get_service_instance_by_topo_node）
- `SearchHostInfoResource.perform_request` @ `bkmonitor/packages/monitor_web/performance/resources.py`（调 api.cmdb.get_host_by_topo_node + get_topo_tree）
- `SearchHostMetricResource.perform_request` @ `bkmonitor/packages/monitor_web/performance/resources.py`（调 api.cmdb.get_host_by_id）

目标端（api.cmdb.* 接口）:
- `api.cmdb.get_host_by_topo_node` / `get_topo_tree` / `get_host_by_id` / `get_business` / `get_service_instance_by_topo_node` / `get_module` @ `bkmonitor/api/cmdb/`
- get_topo_tree 返回拓扑树含 convert_to_topo_link/get_all_nodes_with_relation 方法