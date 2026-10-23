# collect · 接口 → 页面（monitor-pc · 40 个接口）

> 采集配置与插件（collecting_config、collector_plugin…）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| POST | `rest/v2/collecting_config/batch_retry` | — | 3 个（🔵 深度≥2） | `src/monitor-api/modules/collecting.js:12` |
| POST | `rest/v2/collecting_config/batch_retry_detailed` | `/collect-config/detail/:id`（1）、`/collect-config/operate-detail/:id`（1） | — | `src/monitor-api/modules/collecting.js:27` |
| POST | `rest/v2/collecting_config/batch_revoke` | `/collect-config/detail/:id`（1）、`/collect-config/operate-detail/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/collecting.js:11` |
| POST | `rest/v2/collecting_config/check_plugin_version` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/node/:id`（1） | — | `src/monitor-api/modules/collecting.js:35` |
| GET | `rest/v2/collecting_config/config_detail` | `/collect-config/node/:id`（0）、`/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/collecting.js:4` |
| POST | `rest/v2/collecting_config/config_list` | `/collect-config`（0）、`/collect-config/detail/:id`（0） | — | `src/monitor-api/modules/collecting.js:3` |
| POST | `rest/v2/collecting_config/delete` | `/collect-config`（0） | — | `src/monitor-api/modules/collecting.js:6` |
| GET | `rest/v2/collecting_config/fetch_collect_config_stat` | `/collect-config`（0） | — | `src/monitor-api/modules/collecting.js:34` |
| GET | `rest/v2/collecting_config/frontend_config_detail` | `/collect-config/detail/:id`（0）、`/collect-config`（1） | — | `src/monitor-api/modules/collecting.js:17` |
| GET | `rest/v2/collecting_config/frontend_target_info` | `/collect-config/detail/:id`（0）、`/collect-config`（1） | — | `src/monitor-api/modules/collecting.js:18` |
| GET | `rest/v2/collecting_config/get_collect_log_detail` | `/collect-config/detail/:id`（1）、`/collect-config/operate-detail/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/collecting.js:25` |
| GET | `rest/v2/collecting_config/get_collect_variables` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/collecting.js:26` |
| POST | `rest/v2/collecting_config/is_task_ready` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/detail/:id`（1）、`/collect-config/node/:id`（1）、`/collect-config/operate-detail/:id`（1）、`/collect-config/update`（1） | — | `src/monitor-api/modules/collecting.js:32` |
| POST | `rest/v2/collecting_config/list_related_strategy` | `/collect-config`（1） | — | `src/monitor-api/modules/collecting.js:31` |
| POST | `rest/v2/collecting_config/rename` | `/collect-config`（1）、`/collect-config/detail/:id`（1） | — | `src/monitor-api/modules/collecting.js:22` |
| POST | `rest/v2/collecting_config/retry` | `/collect-config/detail/:id`（1）、`/collect-config/operate-detail/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/collecting.js:8` |
| POST | `rest/v2/collecting_config/revoke` | `/collect-config/detail/:id`（1）、`/collect-config/operate-detail/:id`（1） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/collecting.js:10` |
| POST | `rest/v2/collecting_config/rollback` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/node/:id`（1）、`/collect-config/update`（1） | — | `src/monitor-api/modules/collecting.js:15` |
| POST | `rest/v2/collecting_config/save` | `/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/node/:id`（1） | — | `src/monitor-api/modules/collecting.js:13` |
| GET | `rest/v2/collecting_config/status` | `/collect-config`（1）、`/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/collect-config/node/:id`（1）、`/collect-config/update`（1） | — | `src/monitor-api/modules/collecting.js:20` |
| POST | `rest/v2/collecting_config/toggle` | `/collect-config`（1） | — | `src/monitor-api/modules/collecting.js:5` |
| GET | `rest/v2/collector_plugin` | `/migrate-dashboard`（0）、`/plugin-manager`（0）、`/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:64` |
| GET | `rest/v2/collector_plugin/:param` | `/plugin/detail/:pluginId`（0）、`/plugin/setmetric/:pluginId`（0）、`/collect-config/add、/collect-config/clone/:id/:pluginId 等 3 条`（1）、`/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:70` |
| POST | `rest/v2/collector_plugin/:param/edit` | `/plugin-manager`（0） | — | `src/monitor-api/modules/model.js:60` |
| GET | `rest/v2/collector_plugin/:param/export_plugin` | `/plugin-manager`（0） | — | `src/monitor-api/modules/model.js:61` |
| GET | `rest/v2/collector_plugin/:param/fetch_debug_log` | `/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:62` |
| POST | `rest/v2/collector_plugin/:param/release` | `/plugin/add、/plugin/edit/:pluginId 等 3 条`（1）、`/plugin/setmetric/:pluginId`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:68` |
| POST | `rest/v2/collector_plugin/:param/start_debug` | `/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:71` |
| POST | `rest/v2/collector_plugin/:param/stop_debug` | `/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:72` |
| GET | `rest/v2/collector_plugin/check_id` | `/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:56` |
| POST | `rest/v2/collector_plugin/delete` | `/plugin-manager`（0） | — | `src/monitor-api/modules/model.js:58` |
| POST | `rest/v2/collector_plugin/import_plugin` | `/plugin-manager`（0） | — | `src/monitor-api/modules/model.js:63` |
| GET | `rest/v2/collector_plugin/operator_system` | `/plugin-manager`（1）、`/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/model.js:65` |
| GET | `rest/v2/collector_plugin/tag_options` | `/plugin-manager`（0） | — | `src/monitor-api/modules/model.js:73` |
| GET | `rest/v2/get_reserved_word` | `/plugin-manager`（1）、`/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/plugin.js:7` |
| POST | `rest/v2/metric_plugin/save` | `/plugin/setmetric/:pluginId`（1） | 2 个（🔵 深度≥2） | `src/monitor-api/modules/plugin.js:4` |
| GET | `rest/v2/plugin_upgrade_info` | `/collect-config`（1） | — | `src/monitor-api/modules/plugin.js:8` |
| POST | `rest/v2/process_collector_debug` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/plugin.js:10` |
| POST | `rest/v2/register_plugin` | `/plugin/add、/plugin/edit/:pluginId 等 3 条`（1） | — | `src/monitor-api/modules/plugin.js:5` |
| POST | `rest/v2/save_and_release_plugin` | `/plugin-manager`（0） | — | `src/monitor-api/modules/plugin.js:6` |
