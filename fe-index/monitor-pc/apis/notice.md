# notice · 接口 → 页面（monitor-pc · 28 个接口）

> 通知方式、告警组、轮值、订阅报表（notice_group、user_groups、report…）
>
> 「直接调用页面」= 页面自身或直接依赖内的调用点；🔵 候选只给条数（不等于该页面在用）。

| 方法 | 接口 | 直接调用页面（🟢0 / 🟡1，括号内为深度） | 间接候选 | 定义位置 |
|---|---|---|---|---|
| GET | `calendars/list_calendar` | `/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/calendar.js:6` |
| GET | `rest/v2/bkchat_group/get_bkchat_group` | `/alarm-group/add、/alarm-group/edit/:id 等 3 条`（1）、`/strategy-config`（1） | 4 个（🔵 深度≥2） | `src/monitor-api/modules/user_groups.js:3` |
| POST | `rest/v2/duty_plan/preview_user_group_plan` | `/strategy-config`（1） | 5 个（🔵 深度≥2） | `src/monitor-api/modules/user_groups.js:5` |
| GET | `rest/v2/duty_rules` | `/alarm-group`（1）、`/strategy-config`（1） | 4 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:133` |
| POST | `rest/v2/new_report/cancel_or_resubscribe_report` | `/trace/report/my-report`（1） | — | `src/monitor-api/modules/new_report.js:9` |
| GET | `rest/v2/new_report/get_apply_records` | `/trace/report/my-applied-report`（1） | — | `src/monitor-api/modules/new_report.js:11` |
| GET | `rest/v2/new_report/get_report` | `/trace/report/my-applied-report`（1） | — | `src/monitor-api/modules/new_report.js:4` |
| POST | `rest/v2/new_report/get_report_list` | `/trace/report/my-report`（1） | — | `src/monitor-api/modules/new_report.js:3` |
| GET | `rest/v2/new_report/get_send_records` | `/trace/report/my-report`（1） | — | `src/monitor-api/modules/new_report.js:10` |
| POST | `rest/v2/new_report/send_report` | `/trace/report/my-report`（1） | — | `src/monitor-api/modules/new_report.js:8` |
| GET | `rest/v2/notice_group/get_notice_way` | `/email-subscriptions/add、/email-subscriptions/edit/:id`（0）、`/event-center/detail/:id`（1）、`/event-center、/event-action`（1）、`/set-meal-add、/clone-meal/:id 等 3 条`（1）、`/set-meal、/set-meal/:id`（1）、`/strategy-config`（1） | 6 个（🔵 深度≥2） | `src/monitor-api/modules/notice_group.js:4` |
| GET | `rest/v2/notice_group/get_receiver` | `/alarm-group/add、/alarm-group/edit/:id 等 3 条`（1） | 1 个（🔵 深度≥2） | `src/monitor-api/modules/notice_group.js:3` |
| GET | `rest/v2/notice_group/notice_group_list` | `/strategy-config`（0） | — | `src/monitor-api/modules/notice_group.js:7` |
| GET | `rest/v2/report/build_in_metric` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/report.js:9` |
| GET | `rest/v2/report/get_panels_by_dashboard` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/report.js:6` |
| GET | `rest/v2/report/group_list` | `/email-subscriptions`（0）、`/email-subscriptions/add、/email-subscriptions/edit/:id`（0） | — | `src/monitor-api/modules/report.js:12` |
| GET | `rest/v2/report/report_clone` | `/email-subscriptions`（0） | — | `src/monitor-api/modules/report.js:13` |
| GET | `rest/v2/report/report_content` | `/email-subscriptions/add、/email-subscriptions/edit/:id`（0） | — | `src/monitor-api/modules/report.js:10` |
| POST | `rest/v2/report/report_create_or_update` | `/email-subscriptions`（0）、`/email-subscriptions/add、/email-subscriptions/edit/:id`（0） | — | `src/monitor-api/modules/report.js:7` |
| POST | `rest/v2/report/report_delete` | `/email-subscriptions`（0） | — | `src/monitor-api/modules/report.js:11` |
| GET | `rest/v2/report/report_list` | `/email-subscriptions`（0） | — | `src/monitor-api/modules/report.js:3` |
| POST | `rest/v2/report/report_test` | `/email-subscriptions/add、/email-subscriptions/edit/:id`（0） | — | `src/monitor-api/modules/report.js:8` |
| GET | `rest/v2/report/status_list` | `/email-subscriptions/history`（0） | — | `src/monitor-api/modules/report.js:4` |
| GET | `rest/v2/user_groups` | `/collect-config/detail/:id`（0）、`/alarm-dispatch`（1）、`/alarm-dispatch-config/:id`（1）、`/alarm-group`（1）、`/strategy-config`（1）、`/strategy-config/edit/:id、/strategy-config/detail/:id 等 4 条`（1） | — | `src/monitor-api/modules/model.js:127` |
| DELETE | `rest/v2/user_groups/:param` | `/alarm-group`（1） | — | `src/monitor-api/modules/model.js:126` |
| GET | `rest/v2/user_groups/:param` | `/alarm-group/add、/alarm-group/edit/:id 等 3 条`（1）、`/strategy-config`（1） | 4 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:129` |
| PUT | `rest/v2/user_groups/:param` | `/alarm-group/add、/alarm-group/edit/:id 等 3 条`（1） | — | `src/monitor-api/modules/model.js:130` |
| POST | `rest/v2/user_groups/bulk_update` | — | 1 个（🔵 深度≥2） | `src/monitor-api/modules/model.js:124` |
