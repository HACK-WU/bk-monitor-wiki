---
groupPath: 关联关系/性能场景
relation: SearchHostInfoResource-GetHostPage
exportedAt: "2026-09-22T08:22:27.541Z"
---
[强关联] SearchHostInfoResource（页模式） 与 api.cmdb.GetHostPage
强度：必改——改 GetHostPage 的分页语义、过滤条件或返回结构，SearchHostInfoResource 页模式与分享校验必须连带改；改 SearchHostInfoResource 的页参数校验，分享侧 params_check 的调用方式也要跟着改

原因：页模式的过滤、排序、分页与总数全部由 GetHostPage 决定，性能模块不再自行分页

性能模块端：
- SearchHostInfoResource.perform_request（page/page_size 分流、页返回结构）@ bkmonitor/packages/monitor_web/performance/resources.py:369
- SearchHostInfoResource.RequestSerializer.validate（page 与 page_size 必须成对、biz 根跨业务拒绝）@ resources.py:328

api.cmdb 端：
- GetHostPage（CMDB 端过滤 + 分页、地址过滤 [^,]、module_property_filter、total 取 count）@ bkmonitor/api/cmdb/default.py:327
- _trans_topo_node_to_module_ids（拓扑节点转模块集合）@ bkmonitor/api/cmdb/default.py:237

关键不变式：分页顺序沿用 CMDB 默认 bk_host_id 顺序（与原 batch_request 一致）；改名或调整该顺序会让页级与全量结果顺序不一致