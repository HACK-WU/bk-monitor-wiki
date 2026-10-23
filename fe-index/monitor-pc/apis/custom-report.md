# custom-report · 接口 → 页面（monitor-pc · 11 个接口）

> 自定义事件/指标上报（custom_metric_report、custom_event_report）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| POST | `rest/v2/custom_event_report/create_custom_event_group` | `/custom-escalation-set/event、/custom-escalation-set/timeseries`（0） | — | `src/monitor-api/modules/custom_report.js:8` |
| GET | `rest/v2/custom_event_report/query_custom_event_group` | `/event-center、/event-action`（1）、`/performance`（1）、`/uptime-check`（1） | 6 个（🔵 深度≥2） | `src/monitor-api/modules/custom_report.js:4` |
| GET | `rest/v2/custom_event_report/validate_custom_event_group_label` | `/custom-escalation-detail/event/:id`（0）、`/custom-escalation-set/event、/custom-escalation-set/timeseries`（0） | — | `src/monitor-api/modules/custom_report.js:7` |
| POST | `rest/v2/custom_metric_report/add_custom_metric` | — | 4 个（🔵 深度≥2） | `src/monitor-api/modules/custom_report.js:20` |
| POST | `rest/v2/custom_metric_report/create_custom_time_series` | `/custom-escalation-set/event、/custom-escalation-set/timeseries`（0） | — | `src/monitor-api/modules/custom_report.js:17` |
| POST | `rest/v2/custom_metric_report/create_or_update_grouping_rule` | `/custom-escalation-detail/event/:id`（0） | — | `src/monitor-api/modules/custom_report.js:25` |
| GET | `rest/v2/custom_metric_report/custom_time_series` | `/migrate-dashboard`（0） | — | `src/monitor-api/modules/custom_report.js:12` |
| GET | `rest/v2/custom_metric_report/custom_ts_grouping_rule_list` | `/custom-escalation-detail/event/:id`（0） | — | `src/monitor-api/modules/custom_report.js:26` |
| POST | `rest/v2/custom_metric_report/modify_custom_time_series_desc` | `/custom-escalation-detail/event/:id`（0） | — | `src/monitor-api/modules/custom_report.js:32` |
| POST | `rest/v2/custom_metric_report/modify_custom_ts_grouping_rule_list` | `/custom-escalation-detail/event/:id`（0） | — | `src/monitor-api/modules/custom_report.js:30` |
| GET | `rest/v2/custom_metric_report/validate_custom_ts_group_label` | `/custom-escalation-detail/event/:id`（0）、`/custom-escalation-set/event、/custom-escalation-set/timeseries`（0） | — | `src/monitor-api/modules/custom_report.js:15` |
