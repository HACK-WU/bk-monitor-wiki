# Config（`alarm-backends`）

> **职责**：告警后台（核心引擎）：检测/触发/动作执行/ACL/周期任务，41 个任务入口，不对外暴露 HTTP

> **职责**：告警后台（核心引擎）：检测/触发/动作执行/ACL/周期任务，41 个任务入口，不对外暴露 HTTP

- **位置**：`alarm_backends/` · 归属文件 **390** 个 · 约 **68489** 行
- **定义**：`alarm_backends/__init__.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkm_space`、`bkmonitor`、`calendars`、`core.drf_resource`、`metadata`、`query_api`
- **被依赖**（动它会影响）：`apm`、`apm_ebpf`、`bkmonitor`、`fta_web`、`kernel_api`、`metadata`、`monitor_web`、`rum`

## 数据表（51）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `action_config` | ActionConfig | 1 | import（bkmonitor） | `alarm_backends/core/cache/action_config.py:17` |
| `action_instance` | ActionInstance | 19 | import（bkmonitor） | `alarm_backends/core/alert/alert.py:33` |
| `action_instance_log` | ActionInstanceLog | 1 | import（bkmonitor） | `alarm_backends/service/fta_action/__init__.py:36` |
| `action_plugin` | ActionPlugin | 3 | import（bkmonitor） | `alarm_backends/core/cache/action_config.py:17` |
| `ai_feature_settings` | AIFeatureSettings | 1 | import（bkmonitor） | `alarm_backends/core/context/alarm.py:30` |
| `alarm_alert` | Alert | 8 | import（bkmonitor） | `alarm_backends/core/cache/mail_report.py:18` |
| `alarm_algorithm_v2` | AlgorithmModel | 7 | import（bkmonitor） | `alarm_backends/core/cache/strategy.py:38` |
| `alarm_anomaly_record` | AnomalyRecord | 2 | import（bkmonitor） | `alarm_backends/core/context/content.py:23` |
| `alarm_cachenode` | CacheNode | 5 | import（bkmonitor） | `alarm_backends/core/cache/strategy_cost_snapshot.py:26` |
| `alarm_cacherouter` | CacheRouter | 4 | import（bkmonitor） | `alarm_backends/core/cache/strategy_cost_snapshot.py:26` |
| `alarm_event` | Event | 3 | import（bkmonitor） | `alarm_backends/core/alert/alert.py:22` |
| `alarm_item` | Item | 2 | import（bkmonitor） | `alarm_backends/core/control/strategy.py:23` |
| `alarm_notice_group` | NoticeGroup | 1 | import（bkmonitor） | `alarm_backends/core/cache/mail_report.py:18` |
| `alarm_shield` | Shield | 4 | import（bkmonitor） | `alarm_backends/core/cache/mail_report.py:18` |
| `alarm_strategy` | Strategy | 12 | import（bkmonitor） | `alarm_backends/core/cache/mail_report.py:18` |
| `alarm_strategy_history` | StrategyHistoryModel | 1 | import（bkmonitor） | `alarm_backends/core/cache/strategy.py:38` |
| `alarm_strategy_v2` | StrategyModel | 4 | import（bkmonitor） | `alarm_backends/core/api_cache/library.py:34` |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | AlertAssignGroup | 1 | import（bkmonitor） | `alarm_backends/core/cache/assign.py:16` |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | AlertAssignRule | 1 | import（bkmonitor） | `alarm_backends/core/cache/assign.py:16` |
| `bkmonitor_dutyplan` ⚠︎默认命名 | DutyPlan | 1 | import（bkmonitor） | `alarm_backends/service/fta_action/utils.py:33` |
| `bkmonitor_issue_merge_relation` | IssueMergeRelation | 1 | import（bkmonitor） | `alarm_backends/service/fta_action/tasks/issue_tasks.py:25` |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | MetricListCache | 1 | import（bkmonitor） | `alarm_backends/core/cache/strategy.py:38` |
| `bkmonitor_reportcontents` ⚠︎默认命名 | ReportContents | 2 | import（bkmonitor） | `alarm_backends/service/report/handler.py:30` |
| `bkmonitor_reportitems` ⚠︎默认命名 | ReportItems | 2 | import（bkmonitor） | `alarm_backends/service/report/handler.py:30` |
| `bkmonitor_reportstatus` ⚠︎默认命名 | ReportStatus | 1 | import（bkmonitor） | `alarm_backends/service/report/tasks.py:30` |
| `bkmonitor_statisticsmetric` ⚠︎默认命名 | StatisticsMetric | 1 | import（bkmonitor） | `alarm_backends/service/report/tasks.py:30` |
| `bkmonitor_strategy_issue_config` | StrategyIssueConfig | 4 | import（bkmonitor） | `alarm_backends/service/issue/test.py:38` |
| `calendar` | CalendarModel | 1 | import（calendars） | `alarm_backends/core/cache/calendar.py:5` |
| `converge_instance` | ConvergeInstance | 7 | import（bkmonitor） | `alarm_backends/core/context/__init__.py:23` |
| `converge_relation` | ConvergeRelation | 5 | import（bkmonitor） | `alarm_backends/core/context/__init__.py:23` |
| `data_source` | DataSource | 3 | import（bk_dataview） | `alarm_backends/management/story/kernel_story.py:53` |
| `duty_arrange` | DutyArrange | 1 | import（bkmonitor） | `alarm_backends/service/fta_action/utils.py:33` |
| `duty_rule` | DutyRule | 1 | import（bkmonitor） | `alarm_backends/service/fta_action/tasks/action_tasks.py:43` |
| `duty_rule_relation` | DutyRuleRelation | 1 | import（bkmonitor） | `alarm_backends/service/fta_action/tasks/action_tasks.py:43` |
| `event_plugin_instance` | EventPluginInstance | 1 | import（bkmonitor） | `alarm_backends/service/alert/handler.py:30` |
| `global_setting` | GlobalConfig | 1 | import（bkmonitor） | `alarm_backends/core/context/__init__.py:23` |
| `metadata_clusterinfo` ⚠︎默认命名 | ClusterInfo | 1 | import（metadata） | `alarm_backends/management/story/elastic_story.py:29` |
| `metadata_esstorage` ⚠︎默认命名 | ESStorage | 1 | import（metadata） | `alarm_backends/management/story/elastic_story.py:29` |
| `metadata_influxdbclusterinfo` ⚠︎默认命名 | InfluxDBClusterInfo | 1 | import（metadata） | `alarm_backends/management/story/influxdb_story.py:20` |
| `metadata_influxdbhostinfo` ⚠︎默认命名 | InfluxDBHostInfo | 1 | import（metadata） | `alarm_backends/management/story/influxdb_story.py:20` |
| `metadata_kafkatopicinfo` ⚠︎默认命名 | KafkaTopicInfo | 1 | import（metadata） | `alarm_backends/management/story/transfer_story.py:29` |
| `metadata_pingserversubscriptionconfig` ⚠︎默认命名 | PingServerSubscriptionConfig | 1 | import（metadata） | `alarm_backends/management/story/function_story.py:26` |
| `metadata_resulttable` ⚠︎默认命名 | ResultTable | 1 | import（metadata） | `alarm_backends/management/story/elastic_story.py:28` |
| `metadata_space` ⚠︎默认命名 | Space | 1 | import（metadata） | `alarm_backends/service/report/handler.py:36` |
| `notice_subscribe` | NoticeSubscribe | 1 | import（bkmonitor） | `alarm_backends/core/cache/subscribe.py:15` |
| `permission` | Permission | 2 | import（bk_dataview） | `alarm_backends/service/report/handler.py:29` |
| `render_image_task` | RenderImageTask | 1 | import（bkmonitor） | `alarm_backends/service/report/tasks.py:30` |
| `report` | Report | 3 | import（bkmonitor） | `alarm_backends/service/new_report/tasks.py:19` |
| `report_channel` | ReportChannel | 2 | import（bkmonitor） | `alarm_backends/service/new_report/tasks.py:19` |
| `report_send_record` | ReportSendRecord | 1 | import（bkmonitor） | `alarm_backends/service/new_report/handler/base.py:16` |
| `user_group` | UserGroup | 2 | import（bkmonitor） | `alarm_backends/service/fta_action/utils.py:33` |

## 非 HTTP 入口

- **定时任务**：41 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/issue专家`（命中标识 `alarm_backends`）
- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `alarm_backends`）
- `/root/bk-monitor/.module-experts/告警屏蔽专家`（命中标识 `alarm_backends`）

## 归属文件（390）

- `alarm_backends/__init__.py`
- `alarm_backends/urls.py`
- `alarm_backends/constants.py`
- `alarm_backends/apps.py`
- `alarm_backends/cluster/define.py`
- `alarm_backends/cluster/__init__.py`
- `alarm_backends/core/cluster.py`
- `alarm_backends/core/__init__.py`
- `alarm_backends/core/detect_result_retention.py`
- `alarm_backends/core/i18n.py`
- `alarm_backends/core/alarmd/contract.py`
- `alarm_backends/core/alarmd/v2_access.py`
- `alarm_backends/core/alarmd/telemetry.py`
- `alarm_backends/core/alarmd/reference.py`
- `alarm_backends/core/alarmd/publisher.py`
- `alarm_backends/core/alarmd/encoder.py`
- `alarm_backends/core/alarmd/async_publish.py`
- `alarm_backends/core/alarmd/__init__.py`
- `alarm_backends/core/alarmd/config.py`
- `alarm_backends/core/alarmd/v2_writer.py`
- `alarm_backends/core/alarmd/reference_publisher.py`
- `alarm_backends/core/alert/adapter.py`
- `alarm_backends/core/alert/alert.py`
- `alarm_backends/core/alert/__init__.py`
- `alarm_backends/core/alert/event.py`
- `alarm_backends/core/api_cache/metadata.py`
- `alarm_backends/core/api_cache/__init__.py`
- `alarm_backends/core/api_cache/library.py`
- `alarm_backends/core/api_cache/log_search.py`
- `alarm_backends/core/cache/delay_queue.py`
- `alarm_backends/core/cache/action_config.py`
- `alarm_backends/core/cache/strategy.py`
- `alarm_backends/core/cache/mail_report.py`
- `alarm_backends/core/cache/strategy_cost_snapshot.py`
- `alarm_backends/core/cache/result_table.py`
- `alarm_backends/core/cache/shield.py`
- `alarm_backends/core/cache/__init__.py`
- `alarm_backends/core/cache/issue.py`
- `alarm_backends/core/cache/bcs_cluster.py`
- `alarm_backends/core/cache/assign.py`
- ……其余 20 个见 JSON 输出（完整清单）
