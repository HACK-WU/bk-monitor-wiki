# platform · 接口 → 页面（monitor-pc · 32 个接口）

> 权限、外部集成、AI 设置、Grafana、平台开关（iam、external…）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| GET | `rest/v1/global_config` | — | 7 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:24` |
| GET | `rest/v1/user_config` | `/event-explore`（1）、`/k8s-new`（1）、`/strategy-config`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:12` |
| POST | `rest/v1/user_config` | `/event-explore`（1）、`/k8s-new`（1）、`/strategy-config`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:10` |
| PATCH | `rest/v1/user_config/:param` | `/event-explore`（1）、`/k8s-new`（1）、`/strategy-config`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:13` |
| GET | `rest/v2/ai_setting/fetch_ai_setting` | `/ai-settings`（0）、`/ai-settings-set`（0）、`/event-center/detail/:id`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/aiops.js:3` |
| POST | `rest/v2/ai_setting/save_ai_setting` | `/ai-settings-set`（0） | — | `src/monitor-api/modules/aiops.js:4` |
| POST | `rest/v2/external/create_or_update_authorizer` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:15` |
| POST | `rest/v2/external/create_or_update_external_permission` | `/external-auth`（1） | — | `src/monitor-api/modules/iam.js:13` |
| POST | `rest/v2/external/delete_external_permission` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:14` |
| GET | `rest/v2/external/get_apply_record_list` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:18` |
| GET | `rest/v2/external/get_authorizer_by_biz` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:16` |
| GET | `rest/v2/external/get_authorizer_list` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:17` |
| GET | `rest/v2/external/get_external_permission_list` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:10` |
| GET | `rest/v2/external/get_resource_by_action` | `/external-auth`（0） | — | `src/monitor-api/modules/iam.js:11 （另 1 处定义）` |
| GET | `rest/v2/function_switch` | `/function-switch`（0） | — | `src/monitor-api/modules/function_switch.js:3` |
| POST | `rest/v2/function_switch/switch` | `/function-switch`（1） | — | `src/monitor-api/modules/function_switch.js:4` |
| GET | `rest/v2/get_token/get_share_params` | `/share/:token`（0） | — | `src/monitor-api/modules/share.js:7` |
| GET | `rest/v2/grafana/dashboards` | `/email-subscriptions/add、/email-subscriptions/edit/:id`（0）、`/grafana、/grafana/new 等 7 条`（0） | — | `src/monitor-api/modules/grafana.js:21` |
| GET | `rest/v2/grafana/get_data_source_config` | `/event-explore`（0） | 3 个（🔵 深度≥2） | `src/monitor-api/modules/grafana.js:14` |
| GET | `rest/v2/grafana/get_directory_tree` | `/export-import/import-config`（0） | — | `src/monitor-api/modules/grafana.js:24` |
| POST | `rest/v2/grafana/time_series/dimension_query` | `/view-detail`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/grafana.js:40` |
| GET | `rest/v2/grafana/time_series/functions` | `/query-template/create`（0）、`/custom-escalation-detail/timeseries/:id/:activeTab?`（1）、`/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1）、`/query-template/edit/:id`（1） …另 1 页 | — | `src/monitor-api/modules/grafana.js:37` |
| POST | `rest/v2/grafana/time_series/unify_trace_query` | `/event-center/detail/:id`（0） | — | `src/monitor-api/modules/grafana.js:48` |
| POST | `rest/v2/iam/check_allowed` | `/event-center、/event-action`（0） | — | `src/monitor-api/modules/iam.js:6` |
| POST | `rest/v2/iam/check_allowed_by_action_ids` | `/custom-event、/custom-metric`（0）、`/event-center/detail/:id`（0）、`/event-center、/event-action`（1）、`/trace/incident/detail/:id?`（1） | 28 个（🔵 深度≥2） | `src/monitor-api/modules/iam.js:4` |
| POST | `rest/v2/iam/get_authority_detail` | `/custom-event、/custom-metric`（0）、`/exception/:type?/:queryUid?`（0）、`/`（1）、`/event-center/detail/:id`（1）、`/strategy-config`（1） | 29 个（🔵 深度≥2） | `src/monitor-api/modules/iam.js:5` |
| GET | `rest/v2/iam/get_authority_meta` | `/event-center/detail/:id`（1） | 31 个（🔵 深度≥2） | `src/monitor-api/modules/iam.js:3` |
| GET | `rest/v2/redis_management/overview` | `/redis-management`（0） | — | `src/monitor-api/modules/redis-management.js:29` |
| GET | `rest/v2/service_classify/service_category_list` | `/service-classify`（0） | — | `src/monitor-api/modules/service_classify.js:3` |
| POST | `rest/v2/share/create_share_token` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/share.js:3` |
| POST | `rest/v2/share/delete_share_token` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/share.js:5` |
| POST | `rest/v2/share/update_share_token` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/share.js:4` |
