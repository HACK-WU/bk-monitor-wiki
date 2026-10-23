# scene · 接口 → 页面（monitor-pc · 45 个接口）

> 场景视图与性能/K8s/APM/故障（scene_view、performance、k8s…）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| POST | `apm/metric/metric_event/error_list_by_trace_ids` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/apm_metric.js:3` |
| POST | `apm/service/application/log_service_relation_bk_log_index_set` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/apm_service.js:43` |
| POST | `apm/service_log/log/log_relation` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/apm_log.js:3` |
| POST | `apm/service_log/log/log_relation_list` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/apm_log.js:4` |
| POST | `apm/trace_api/trace_query/trace_list_by_id` | `/view-detail`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/apm_trace.js:37` |
| GET | `rest/v2/datalink_status/alert_status` | `/collect-config/detail/:id`（1） | — | `src/monitor-api/modules/datalink.js:3` |
| GET | `rest/v2/datalink_status/collecting_target_status` | `/collect-config/detail/:id`（0）、`/collect-config/operate-detail/:id`（0） | — | `src/monitor-api/modules/datalink.js:5` |
| GET | `rest/v2/datalink_status/storage_status` | `/collect-config/detail/:id`（0） | — | `src/monitor-api/modules/datalink.js:8` |
| GET | `rest/v2/datalink_status/transfer_count_series` | `/collect-config/detail/:id`（1） | — | `src/monitor-api/modules/datalink.js:6` |
| GET | `rest/v2/datalink_status/transfer_latest_msg` | `/collect-config/detail/:id`（1） | — | `src/monitor-api/modules/datalink.js:7` |
| POST | `rest/v2/datalink_status/update_alert_user_groups` | `/collect-config/detail/:id`（1） | — | `src/monitor-api/modules/datalink.js:4` |
| POST | `rest/v2/favorite` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:110` |
| DELETE | `rest/v2/favorite/:param` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:111` |
| PUT | `rest/v2/favorite/:param` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:117` |
| GET | `rest/v2/favorite/list_by_group` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:113` |
| GET | `rest/v2/favorite_group` | — | 4 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:103` |
| POST | `rest/v2/favorite_group` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:101` |
| DELETE | `rest/v2/favorite_group/:param` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:102` |
| PUT | `rest/v2/favorite_group/:param` | `/data-retrieval`（1）、`/event-explore`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/model.js:106` |
| GET | `rest/v2/incident/alert_incident_detail` | `/event-center/detail/:id`（1） | — | `src/monitor-api/modules/incident.js:25` |
| POST | `rest/v2/incident/export_incident` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/incident.js:7` |
| POST | `rest/v2/incident/incident_list` | `/event-center、/event-action`（0） | — | `src/monitor-api/modules/incident.js:6` |
| POST | `rest/v2/incident/incident_overview` | `/event-center、/event-action`（0） | — | `src/monitor-api/modules/incident.js:8` |
| POST | `rest/v2/incident/top_n` | `/event-center、/event-action`（0） | — | `src/monitor-api/modules/incident.js:9` |
| GET | `rest/v2/k8s/resources/list_bcs_cluster` | `/k8s-new`（1） | — | `src/monitor-api/modules/k8s.js:3` |
| POST | `rest/v2/k8s/resources/list_resources` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/k8s.js:5` |
| POST | `rest/v2/k8s/resources/resource_trend` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/k8s.js:8` |
| GET | `rest/v2/k8s/resources/scenario_metric_list` | `/k8s-new`（1） | — | `src/monitor-api/modules/k8s.js:4` |
| GET | `rest/v2/k8s/resources/workload_overview` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/k8s.js:7` |
| POST | `rest/v2/overview/function_shortcut/add_access_record` | `/grafana、/grafana/new 等 7 条`（0） | — | `src/monitor-api/modules/overview.js:4` |
| GET | `rest/v2/performance/host_list` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/performance.js:6` |
| POST | `rest/v2/performance/host_performance_detail` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/performance.js:3` |
| POST | `rest/v2/performance/host_topo_node_detail` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/performance.js:4` |
| POST | `rest/v2/performance/search_host_info` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/performance.js:7` |
| POST | `rest/v2/performance/search_host_metric` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/performance.js:8` |
| POST | `rest/v2/scene_view/bulk_update_scene_view_order_and_name` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/scene_view.js:8` |
| POST | `rest/v2/scene_view/delete_scene_view` | `/custom-escalation-view/:id`（1） | — | `src/monitor-api/modules/scene_view.js:7` |
| GET | `rest/v2/scene_view/get_host_info` | `/performance/detail/:id/:process?、/performance/detail-new/:id/:process?`（0） | — | `src/monitor-api/modules/scene_view.js:50` |
| POST | `rest/v2/scene_view/get_host_or_topo_node_detail` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/scene_view.js:13` |
| GET | `rest/v2/scene_view/get_observation_scene_list` | `/custom-scenes`（0） | — | `src/monitor-api/modules/scene_view.js:52` |
| POST | `rest/v2/scene_view/get_observation_scene_status_list` | `/custom-scenes`（0） | — | `src/monitor-api/modules/scene_view.js:53` |
| GET | `rest/v2/scene_view/get_plugin_by_result_table` | `/event-center/detail/:id`（0） | — | `src/monitor-api/modules/scene_view.js:55` |
| GET | `rest/v2/scene_view/get_scene_view` | `/collect-config/view/:id`（1）、`/custom-escalation-event-view/:id`（1）、`/custom-escalation-view/:id`（1）、`/custom-scenes/view/:id`（1）、`/event-center、/event-action`（1）、`/k8s`（1） …另 4 页 | 1 个（🔵 深度≥2） | `src/monitor-api/modules/scene_view.js:4` |
| GET | `rest/v2/scene_view/get_scene_view_list` | `/collect-config/view/:id`（1）、`/custom-escalation-event-view/:id`（1）、`/custom-escalation-view/:id`（1）、`/custom-scenes/view/:id`（1）、`/event-center、/event-action`（1）、`/k8s`（1） …另 4 页 | 1 个（🔵 深度≥2） | `src/monitor-api/modules/scene_view.js:5` |
| POST | `rest/v2/scene_view/update_scene_view` | `/custom-escalation-view/:id`（1） | — | `src/monitor-api/modules/scene_view.js:6` |
