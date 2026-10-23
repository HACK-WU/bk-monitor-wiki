# uptime · 接口 → 页面（monitor-pc · 27 个接口）

> 拨测（uptime_check）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| GET | `rest/v2/uptime_check/get_http_headers` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（1） | — | `src/monitor-api/modules/uptime_check.js:4` |
| POST | `rest/v2/uptime_check/import_uptime_check` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/uptime_check.js:11` |
| GET | `rest/v2/uptime_check/import_uptime_check/parse` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/uptime_check.js:10` |
| GET | `rest/v2/uptime_check/select_carrier_operator` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/uptime_check.js:13` |
| GET | `rest/v2/uptime_check/select_uptime_check_node` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/uptime_check.js:12` |
| GET | `rest/v2/uptime_check/uptime_check_group` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:51` |
| POST | `rest/v2/uptime_check/uptime_check_group` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:49` |
| DELETE | `rest/v2/uptime_check/uptime_check_group/:param` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:50` |
| PUT | `rest/v2/uptime_check/uptime_check_group/:param` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:55` |
| POST | `rest/v2/uptime_check/uptime_check_group/:param/add_task` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:48` |
| GET | `rest/v2/uptime_check/uptime_check_node` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0）、`/uptime-check`（1） | — | `src/monitor-api/modules/model.js:32` |
| POST | `rest/v2/uptime_check/uptime_check_node` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/model.js:28` |
| DELETE | `rest/v2/uptime_check/uptime_check_node/:param` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:29` |
| GET | `rest/v2/uptime_check/uptime_check_node/:param` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/model.js:34` |
| PUT | `rest/v2/uptime_check/uptime_check_node/:param` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/model.js:35` |
| GET | `rest/v2/uptime_check/uptime_check_node/fix_name_conflict` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/model.js:30` |
| GET | `rest/v2/uptime_check/uptime_check_node/is_exist` | `/uptime-check/node-add、/uptime-check/node-edit/:id`（0） | — | `src/monitor-api/modules/model.js:31` |
| GET | `rest/v2/uptime_check/uptime_check_task` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:42` |
| POST | `rest/v2/uptime_check/uptime_check_task` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:39` |
| DELETE | `rest/v2/uptime_check/uptime_check_task/:param` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:41` |
| GET | `rest/v2/uptime_check/uptime_check_task/:param` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:44` |
| PUT | `rest/v2/uptime_check/uptime_check_task/:param` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:47` |
| POST | `rest/v2/uptime_check/uptime_check_task/:param/change_status` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:36` |
| POST | `rest/v2/uptime_check/uptime_check_task/:param/clone` | `/uptime-check`（1） | — | `src/monitor-api/modules/model.js:37` |
| POST | `rest/v2/uptime_check/uptime_check_task/:param/deploy` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:40` |
| GET | `rest/v2/uptime_check/uptime_check_task/:param/running_status` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:45` |
| POST | `rest/v2/uptime_check/uptime_check_task/test` | `/uptime-check/task-add、/uptime-check/task-edit/:id`（0） | — | `src/monitor-api/modules/model.js:46` |
