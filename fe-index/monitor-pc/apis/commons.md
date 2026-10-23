# commons · 接口 → 页面（monitor-pc · 42 个接口）

> 通用接口（业务/拓扑/ip 选择器/空间），被多页面共用
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| GET | `rest/v2/commons/check_cluster_health` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/commons.js:11` |
| GET | `rest/v2/commons/country_list` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0）、`/uptime-check/task-add、/uptime-check/task-edit/:id`（1） | — | `src/monitor-api/modules/commons.js:18` |
| GET | `rest/v2/commons/fetch_business_info` | `/`（0）、`/no-business/:queryUid?`（0）、`/platform-setting`（1） | — | `src/monitor-api/modules/commons.js:4` |
| POST | `rest/v2/commons/frontend_report_event/frontend_report_event` | `/event-center/detail/:id`（1） | — | `src/monitor-api/modules/commons.js:36` |
| POST | `rest/v2/commons/get_business_target_detail` | `/ai-settings`（0） | — | `src/monitor-api/modules/commons.js:31` |
| GET | `rest/v2/commons/get_docs_link` | `/apm/home、/apm/application/add 等 3 条`（1）、`/collect-config`（1）、`/collect-config/node/:id`（1）、`/collect-config/update`（1）、`/collect-config/view/:id`（1）、`/custom-scenes`（1） …另 9 页 | — | `src/monitor-api/modules/commons.js:16` |
| POST | `rest/v2/commons/get_host_instance_by_ip` | `/export-import/config-target`（1） | — | `src/monitor-api/modules/commons.js:23` |
| POST | `rest/v2/commons/get_host_instance_by_node` | `/export-import/config-target`（1） | — | `src/monitor-api/modules/commons.js:24` |
| GET | `rest/v2/commons/get_label` | `/custom-escalation-set/event、/custom-escalation-set/timeseries`（0）、`/custom-scenes`（0）、`/plugin-manager`（0）、`/collect-config`（1）、`/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/commons.js:34` |
| GET | `rest/v2/commons/get_mainline_object_topo` | `/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/commons.js:28` |
| POST | `rest/v2/commons/get_nodes_by_template` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/node/:id`（1）、`/export-import/config-target`（1） | — | `src/monitor-api/modules/commons.js:30` |
| POST | `rest/v2/commons/get_service_instance_by_node` | `/export-import/config-target`（1） | — | `src/monitor-api/modules/commons.js:25` |
| GET | `rest/v2/commons/get_storage_cluster_detail` | `/platform-setting`（1） | — | `src/monitor-api/modules/commons.js:13` |
| POST | `rest/v2/commons/get_template` | `/export-import/config-target`（1） | — | `src/monitor-api/modules/commons.js:29` |
| POST | `rest/v2/commons/get_topo_list` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/commons.js:32` |
| POST | `rest/v2/commons/get_topo_tree` | `/export-import/config-target`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/commons.js:22` |
| POST | `rest/v2/commons/host_agent_status` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/node/:id`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/commons.js:27` |
| POST | `rest/v2/commons/ip_chooser_config/batch_get` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:77` |
| GET | `rest/v2/commons/ip_chooser_config/global_config` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:78` |
| POST | `rest/v2/commons/ip_chooser_config/update_config` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:79` |
| POST | `rest/v2/commons/ip_chooser_dynamic_group/agent_statistics` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:80` |
| POST | `rest/v2/commons/ip_chooser_dynamic_group/execute` | `/export-import/config-target`（1） | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:82 （另 1 处定义）` |
| POST | `rest/v2/commons/ip_chooser_dynamic_group/groups` | `/export-import/config-target`（1） | 7 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:81 （另 1 处定义）` |
| POST | `rest/v2/commons/ip_chooser_host/check` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:83` |
| POST | `rest/v2/commons/ip_chooser_host/details` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:84` |
| POST | `rest/v2/commons/ip_chooser_service_instance/details` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:85` |
| POST | `rest/v2/commons/ip_chooser_template/agent_statistics` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:86` |
| POST | `rest/v2/commons/ip_chooser_template/hosts` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:87` |
| POST | `rest/v2/commons/ip_chooser_template/nodes` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:88` |
| POST | `rest/v2/commons/ip_chooser_template/service_instance_count` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:89` |
| POST | `rest/v2/commons/ip_chooser_template/templates` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:90` |
| POST | `rest/v2/commons/ip_chooser_topo/agent_statistics` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:91` |
| POST | `rest/v2/commons/ip_chooser_topo/query_host_id_infos` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:92` |
| POST | `rest/v2/commons/ip_chooser_topo/query_hosts` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:93` |
| POST | `rest/v2/commons/ip_chooser_topo/query_path` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:94` |
| POST | `rest/v2/commons/ip_chooser_topo/query_service_instances` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:95` |
| POST | `rest/v2/commons/ip_chooser_topo/trees` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:97` |
| GET | `rest/v2/commons/isp_list` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/commons.js:19` |
| GET | `rest/v2/commons/list_clusters` | `/platform-setting`（1） | — | `src/monitor-api/modules/commons.js:12` |
| GET | `rest/v2/commons/query_async_task_result` | `/export-import/export-configuration`（0）、`/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | 4 个（🔵 深度≥2） | `src/monitor-api/modules/commons.js:38` |
| GET | `rest/v2/commons/space_introduce` | `/apm/home、/apm/application/add 等 3 条`（1）、`/collect-config`（1）、`/collect-config/node/:id`（1）、`/collect-config/update`（1）、`/collect-config/view/:id`（1）、`/custom-scenes`（1） …另 10 页 | — | `src/monitor-api/modules/commons.js:10` |
| GET | `rest/v2/commons/user/list_users` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:99` |
