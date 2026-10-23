# alarm · 接口 → 页面（monitor-pc · 100 个接口）

> 告警策略/事件/屏蔽/分派（fta、strategies、promql_import、shield、event_center）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| GET | `fta/action/config` | `/set-meal、/set-meal/:id`（0）、`/alarm-dispatch`（1）、`/alarm-dispatch-config/:id`（1）、`/event-center/detail/:id`（1）、`/event-center、/event-action`（1）、`/strategy-config`（1） …另 1 页 | — | `src/monitor-api/modules/model.js:148` |
| POST | `fta/action/config` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:146` |
| DELETE | `fta/action/config/:param` | `/set-meal、/set-meal/:id`（0） | — | `src/monitor-api/modules/model.js:147` |
| GET | `fta/action/config/:param` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:150` |
| PATCH | `fta/action/config/:param` | `/set-meal、/set-meal/:id`（0） | — | `src/monitor-api/modules/model.js:149` |
| PUT | `fta/action/config/:param` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:151` |
| POST | `fta/action/instances/assign_alert` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | — | `src/monitor-api/modules/action.js:18` |
| POST | `fta/action/instances/batch_create` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | — | `src/monitor-api/modules/action.js:13` |
| POST | `fta/action/instances/create_chat_group` | `/event-center、/event-action`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:14` |
| POST | `fta/action/instances/create_demo_action` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:16` |
| POST | `fta/action/instances/get_action_config_by_alerts` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | — | `src/monitor-api/modules/action.js:15` |
| POST | `fta/action/instances/get_action_params` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:12` |
| GET | `fta/action/instances/get_demo_action_detail` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:17` |
| POST | `fta/action/instances/preview_demo_action_context` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:19` |
| GET | `fta/action/plugins/get_converge_function` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1）、`/strategy-config`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:7` |
| GET | `fta/action/plugins/get_dimensions` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:6` |
| GET | `fta/action/plugins/get_plugin_templates` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1）、`/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:4` |
| GET | `fta/action/plugins/get_plugins` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:3` |
| GET | `fta/action/plugins/get_template_detail` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:5` |
| GET | `fta/action/plugins/get_variables` | `/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1）、`/strategy-config`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/action.js:8` |
| POST | `fta/alert/action/date_histogram` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:25` |
| GET | `fta/alert/action/detail` | `/event-center/action-detail/:id`（0） | — | `src/monitor-api/modules/alert.js:22` |
| GET | `fta/alert/action/detail/sub_actions` | `/event-center/detail/:id`（1） | — | `src/monitor-api/modules/alert.js:23` |
| POST | `fta/alert/action/export` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:24` |
| POST | `fta/alert/action/search` | `/event-center/detail/:id`（0）、`/event-center、/event-action`（0） | — | `src/monitor-api/modules/alert.js:21` |
| POST | `fta/alert/action/top_n` | `/event-center、/event-action`（0） | — | `src/monitor-api/modules/alert.js:29` |
| POST | `fta/alert/alert/ack` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:18` |
| POST | `fta/alert/alert/create_feedback` | `/event-center/detail/:id`（1） | — | `src/monitor-api/modules/alert.js:32` |
| POST | `fta/alert/alert/date_histogram` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:7` |
| POST | `fta/alert/alert/delete_experience` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:12` |
| GET | `fta/alert/alert/detail` | `/event-center/detail/:id`（0） | — | `src/monitor-api/modules/alert.js:9` |
| GET | `fta/alert/alert/dimension_drill_down` | `/event-center/detail/:id`（1） | — | `src/monitor-api/modules/alert.js:34` |
| POST | `fta/alert/alert/event_count` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:15` |
| POST | `fta/alert/alert/export` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:6` |
| GET | `fta/alert/alert/get_experience` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:10` |
| POST | `fta/alert/alert/graph_query` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:19` |
| GET | `fta/alert/alert/list_feedback` | `/event-center/detail/:id`（0） | — | `src/monitor-api/modules/alert.js:33` |
| POST | `fta/alert/alert/log` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:13` |
| GET | `fta/alert/alert/metric_recommendation` | `/event-center/detail/:id`（1） | — | `src/monitor-api/modules/alert.js:35` |
| POST | `fta/alert/alert/related_info` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:16` |
| POST | `fta/alert/alert/save_experience` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:11` |
| POST | `fta/alert/alert/search` | `/event-center/action-detail/:id`（0）、`/event-center、/event-action`（0） | — | `src/monitor-api/modules/alert.js:5` |
| POST | `fta/alert/alert/tags` | `/event-center、/event-action`（0） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:8` |
| POST | `fta/alert/alert/top_n` | `/event-center、/event-action`（0） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:28` |
| GET | `fta/alert/allowed_biz` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:3` |
| POST | `fta/alert/event/search` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:14` |
| POST | `fta/alert/event/top_n` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/alert.js:30` |
| GET | `fta/alert/search_favorite` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/model.js:160` |
| POST | `fta/alert/search_favorite` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/model.js:158` |
| DELETE | `fta/alert/search_favorite/:param` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/model.js:159` |
| PATCH | `fta/alert/search_favorite/:param` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/model.js:161` |
| GET | `fta/alert/search_history` | `/event-center、/event-action`（1） | — | `src/monitor-api/modules/alert.js:4` |
| GET | `fta/alert/strategy_snapshot` | `/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/alert.js:27` |
| GET | `fta/assign/cmdb/search_object_attribute` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/assign.js:6` |
| GET | `fta/assign/rule_groups` | `/alarm-dispatch`（1）、`/alarm-dispatch-config/:id`（1） | — | `src/monitor-api/modules/model.js:166` |
| POST | `fta/assign/rule_groups` | `/alarm-dispatch`（1） | — | `src/monitor-api/modules/model.js:164` |
| DELETE | `fta/assign/rule_groups/:param` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:165` |
| PATCH | `fta/assign/rule_groups/:param` | `/alarm-dispatch`（1） | — | `src/monitor-api/modules/model.js:167` |
| POST | `fta/assign/rule_operate/batch_update` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/assign.js:3` |
| GET | `fta/assign/rule_operate/get_assign_condition_keys` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/assign.js:5` |
| POST | `fta/assign/rule_operate/match_debug` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/assign.js:4` |
| GET | `fta/assign/rules` | `/alarm-dispatch`（1）、`/alarm-dispatch-config/:id`（1） | — | `src/monitor-api/modules/model.js:172` |
| GET | `fta/home/biz_with_alert_statistics` | `/event-center、/event-action`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/home.js:6` |
| GET | `fta/home/statistics` | `/`（0） | — | `src/monitor-api/modules/home.js:3` |
| GET | `fta/plugin/event` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/event_plugin.js:3` |
| GET | `rest/v1/event_center/alarm_detail_chart_data` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/event_center.js:30` |
| POST | `rest/v2/event_center/list_index_by_host` | `/event-center/detail/:id`（0） | — | `src/monitor-api/modules/alert_events.js:15` |
| POST | `rest/v2/promql_import/create_mapping_config` | `/migrate-dashboard`（0） | — | `src/monitor-api/modules/promql_import.js:3` |
| POST | `rest/v2/promql_import/delete_mapping_config` | `/migrate-dashboard`（0） | — | `src/monitor-api/modules/promql_import.js:5` |
| POST | `rest/v2/promql_import/get_mapping_config` | `/migrate-dashboard`（0） | — | `src/monitor-api/modules/promql_import.js:4` |
| POST | `rest/v2/promql_import/import_alert_rule` | `/migrate-dashboard`（0） | — | `src/monitor-api/modules/promql_import.js:7` |
| POST | `rest/v2/promql_import/import_grafana_dashboard` | `/migrate-dashboard`（0） | — | `src/monitor-api/modules/promql_import.js:6` |
| POST | `rest/v2/shield/add_shield` | `/strategy-config`（1） | — | `src/monitor-api/modules/shield.js:9` |
| POST | `rest/v2/shield/bulk_add_alert_shield` | `/event-center/detail/:id`（1）、`/event-center、/event-action`（1） | — | `src/monitor-api/modules/shield.js:10` |
| POST | `rest/v2/shield/disable_shield` | `/strategy-config`（0） | — | `src/monitor-api/modules/shield.js:12` |
| POST | `rest/v2/strategies/bulk_edit_strategy` | `/strategy-config`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:13` |
| POST | `rest/v2/strategies/delete_strategy_config` | `/collect-config`（1） | — | `src/monitor-api/modules/strategies.js:12` |
| POST | `rest/v2/strategies/fetch_item_status` | `/view-detail`（0） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:10` |
| GET | `rest/v2/strategies/get_intelligent_detect_access_status` | — | 4 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:29` |
| GET | `rest/v2/strategies/get_intelligent_model` | — | 4 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:27` |
| GET | `rest/v2/strategies/get_scenario_list` | `/strategy-config`（0）、`/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:3` |
| POST | `rest/v2/strategies/get_target_detail` | `/strategy-config`（0）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:11` |
| GET | `rest/v2/strategies/get_unit_info` | — | 5 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:6` |
| GET | `rest/v2/strategies/get_unit_list` | `/plugin/detail/:pluginId`（1）、`/plugin/setmetric/:pluginId`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:5` |
| GET | `rest/v2/strategies/list_intelligent_models` | `/ai-settings`（1）、`/ai-settings-set`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:26` |
| GET | `rest/v2/strategies/multivariate_anomaly_scenes` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:31` |
| GET | `rest/v2/strategies/notice_variable_list` | `/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/strategies.js:4` |
| GET | `rest/v2/strategies/plain_strategy_list` | `/alarm-dispatch-config/:id`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:14` |
| POST | `rest/v2/strategies/promql_to_query_config` | `/event-center、/event-action`（0）、`/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/strategies.js:25` |
| POST | `rest/v2/strategies/query_config_to_promql` | `/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/strategies.js:24` |
| GET | `rest/v2/strategies/strategy_label_list` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:8` |
| POST | `rest/v2/strategies/update_metric_list_by_biz` | — | 4 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:30` |
| POST | `rest/v2/strategies/v2/delete_strategy` | `/strategy-config`（0） | — | `src/monitor-api/modules/strategies.js:20` |
| POST | `rest/v2/strategies/v2/get_metric_list` | `/metrics-manager`（0）、`/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1）、`/view-detail`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:16` |
| GET | `rest/v2/strategies/v2/get_strategy` | `/strategy-config`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:19` |
| POST | `rest/v2/strategies/v2/get_strategy_alert_summary` | `/strategy-config`（0） | — | `src/monitor-api/modules/strategies.js:18` |
| POST | `rest/v2/strategies/v2/get_strategy_list` | `/strategy-config`（0）、`/set-meal、/set-meal/:id`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:17` |
| POST | `rest/v2/strategies/v2/save_strategy` | `/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/strategies.js:22` |
| POST | `rest/v2/strategies/v2/update_partial_strategy` | `/strategy-config`（0） | — | `src/monitor-api/modules/strategies.js:23` |
| POST | `rest/v2/strategies/v2/verify_strategy_name` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/strategies.js:21` |
