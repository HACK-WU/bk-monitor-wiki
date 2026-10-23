# retrieval · 接口 → 页面（monitor-pc · 13 个接口）

> 查询模板与数据探索（query_template、data_explorer、query-api…）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| POST | `query-api/rest/v2/grafana/get_variable_value` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/grafana.js:15` |
| POST | `query-api/rest/v2/grafana/log/query` | — | 2 个（🔵 深度≥2） | `src/monitor-api/modules/grafana.js:20` |
| POST | `query-api/rest/v2/grafana/time_series/unify_query` | `/view-detail`（0） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/grafana.js:38` |
| POST | `rest/v2/as_code/export_config_file` | `/strategy-config`（0） | — | `src/monitor-api/modules/as_code.js:6` |
| POST | `rest/v2/data_explorer/event/generate_query_string` | `/event-explore`（1） | — | `src/monitor-api/modules/data_explorer.js:16` |
| POST | `rest/v2/data_explorer/get_graph_query_config` | `/data-retrieval`（1）、`/event-retrieval`（1）、`/log-retrieval`（1） | — | `src/monitor-api/modules/data_explorer.js:3` |
| POST | `rest/v2/data_explorer/get_group_by_count` | — | 3 个（🔵 深度≥2） | `src/monitor-api/modules/data_explorer.js:6` |
| POST | `rest/v2/export_import/export_package` | `/export-import/export-configuration`（0） | — | `src/monitor-api/modules/export_import.js:4` |
| POST | `rest/v2/query_template` | `/query-template/create`（0） | — | `src/monitor-api/modules/model.js:138` |
| DELETE | `rest/v2/query_template/:param` | `/query-template`（1） | — | `src/monitor-api/modules/model.js:139` |
| GET | `rest/v2/query_template/:param` | `/query-template/edit/:id`（1） | — | `src/monitor-api/modules/model.js:143` |
| PUT | `rest/v2/query_template/:param` | `/query-template/edit/:id`（0） | — | `src/monitor-api/modules/model.js:145` |
| POST | `rest/v2/query_template/:param/relation` | `/query-template/edit/:id`（1） | — | `src/monitor-api/modules/model.js:141` |
