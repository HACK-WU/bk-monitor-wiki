# Config（`bkmonitor`）

> **职责**：监控核心与公共层：策略/告警/报表数据模型 + 公共工具 + `api/` 外部系统集成（34 个第三方系统）

> **职责**：监控核心与公共层：策略/告警/报表数据模型 + 公共工具 + `api/` 外部系统集成（34 个第三方系统）

- **位置**：`bkmonitor/` · 归属文件 **372** 个 · 约 **78730** 行
- **定义**：`bkmonitor/db_routers.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`apm`、`apm_web`、`audit`、`bk_dataview`、`bkm_space`、`calendars`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`monitor_web`、`rum_web`
- **被依赖**（动它会影响）：`ai_whale`、`alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`audit`、`bk_dataview`、`bkm_ipchooser`、`calendars`、`core.drf_resource`、`fta_web`、`kernel_api`、`metadata`、`monitor`、`monitor_api`、`monitor_web`、`performance`、`profile`、`query_api`、`rum`、`rum_web`

## 数据表（109）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `action_config` | ActionConfig | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:261` |
| `action_instance` | ActionInstance | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:283` |
| `action_instance_log` | ActionInstanceLog | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:730` |
| `action_plugin` | ActionPlugin | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:61` |
| `ai_feature_settings` | AIFeatureSettings | 1 | models.Model（定义） | `bkmonitor/models/aiops.py:18` |
| `alarm_action` | Action | 1 | models.Model（定义） | `bkmonitor/models/base.py:345` |
| `alarm_action_notice_group_mapping` | ActionNoticeMapping | 1 | models.Model（定义） | `bkmonitor/models/base.py:426` |
| `alarm_alert` | Alert | 1 | models.Model（定义） | `bkmonitor/models/base.py:727` |
| `alarm_alert_collect` | AlertCollect | 1 | models.Model（定义） | `bkmonitor/models/base.py:756` |
| `alarm_algorithm_v2` | AlgorithmModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:152` |
| `alarm_anomaly_record` | AnomalyRecord | 1 | models.Model（定义） | `bkmonitor/models/base.py:441` |
| `alarm_base_alarm_config` | BaseAlarmQueryConfig | 1 | models.Model（定义） | `bkmonitor/models/base.py:205` |
| `alarm_cachenode` | CacheNode | 1 | models.Model（定义） | `bkmonitor/models/base.py:838` |
| `alarm_cacherouter` | CacheRouter | 1 | models.Model（定义） | `bkmonitor/models/base.py:941` |
| `alarm_custom_event_group_config` | CustomEventQueryConfig | 1 | models.Model（定义） | `bkmonitor/models/base.py:189` |
| `alarm_detect_algorithm` | DetectAlgorithm | 1 | models.Model（定义） | `bkmonitor/models/base.py:287` |
| `alarm_detect_v2` | DetectModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:114` |
| `alarm_event` | Event | 1 | models.Model（定义） | `bkmonitor/models/base.py:467` |
| `alarm_event_action` | EventAction | 1 | models.Model（定义） | `bkmonitor/models/base.py:606` |
| `alarm_event_stats` | EventStats | 1 | models.Model（定义） | `bkmonitor/models/base.py:716` |
| `alarm_item` | Item | 1 | models.Model（定义） | `bkmonitor/models/base.py:214` |
| `alarm_item_v2` | ItemModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:81` |
| `alarm_notice_group` | NoticeGroup | 1 | models.Model（定义） | `bkmonitor/models/base.py:387` |
| `alarm_notice_template` | NoticeTemplate | 1 | models.Model（定义） | `bkmonitor/models/base.py:371` |
| `alarm_query_config_v2` | QueryConfigModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:245` |
| `alarm_rt_dsl_config` | ResultTableDSLConfig | 1 | models.Model（定义） | `bkmonitor/models/base.py:169` |
| `alarm_rt_sql_config` | ResultTableSQLConfig | 1 | models.Model（定义） | `bkmonitor/models/base.py:149` |
| `alarm_shield` | Shield | 1 | models.Model（定义） | `bkmonitor/models/base.py:780` |
| `alarm_strategy` | Strategy | 1 | models.Model（定义） | `bkmonitor/models/base.py:259` |
| `alarm_strategy_biz_access` | DefaultStrategyBizAccessModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:911` |
| `alarm_strategy_history` | StrategyHistoryModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:428` |
| `alarm_strategy_label` | StrategyLabel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:284` |
| `alarm_strategy_v2` | StrategyModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:335` |
| `algorithm_choice_config` | AlgorithmChoiceConfig | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:949` |
| `api_auth_token` | ApiAuthToken | 1 | models.Model（定义） | `bkmonitor/models/token.py:104` |
| `apm_web_application` ⚠︎默认命名 | Application | 8 | import（apm_web） | `bkmonitor/iam/resource.py:225` |
| `app_snapshot_host_index` | SnapshotHostIndex | 1 | models.Model（定义） | `bkmonitor/models/base.py:57` |
| `as_code_import_history` | AsCodeImportTask | 1 | models.Model（定义） | `bkmonitor/models/as_code.py:28` |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | AlertAssignGroup | 1 | models.Model（定义） | `bkmonitor/models/fta/assign.py:20` |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | AlertAssignRule | 1 | models.Model（定义） | `bkmonitor/models/fta/assign.py:53` |
| `bkmonitor_alertconfig` ⚠︎默认命名 | AlertConfig | 1 | models.Model（定义） | `bkmonitor/models/fta/plugin.py:213` |
| `bkmonitor_bcsclusterlabels` ⚠︎默认命名 | BCSClusterLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_cluster.py:474` |
| `bkmonitor_bcscontainerlabels` ⚠︎默认命名 | BCSContainerLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_container.py:384` |
| `bkmonitor_bcsingresslabels` ⚠︎默认命名 | BCSIngressLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_ingress.py:190` |
| `bkmonitor_bcslabel` ⚠︎默认命名 | BCSLabel | 1 | models.Model（定义） | `bkmonitor/models/bcs_label.py:15` |
| `bkmonitor_bcsnodelabels` ⚠︎默认命名 | BCSNodeLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_node.py:463` |
| `bkmonitor_bcspodlabels` ⚠︎默认命名 | BCSPodLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_pod.py:542` |
| `bkmonitor_bcspodmonitorlabels` ⚠︎默认命名 | BCSPodMonitorLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_pod_monitor.py:54` |
| `bkmonitor_bcsservicelabels` ⚠︎默认命名 | BCSServiceLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_service.py:315` |
| `bkmonitor_bcsservicemonitorlabels` ⚠︎默认命名 | BCSServiceMonitorLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_service_monitor.py:54` |
| `bkmonitor_bcsworkloadlabels` ⚠︎默认命名 | BCSWorkloadLabels | 1 | models.Model（定义） | `bkmonitor/models/bcs_workload.py:406` |
| `bkmonitor_dutyplan` ⚠︎默认命名 | DutyPlan | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:814` |
| `bkmonitor_eventplugin` ⚠︎默认命名 | EventPlugin | 1 | models.Model（定义） | `bkmonitor/models/fta/plugin.py:110` |
| `bkmonitor_issue_merge_relation` | IssueMergeRelation | 1 | models.Model（定义） | `bkmonitor/models/issue.py:22` |
| `bkmonitor_issue_tapd_relation` | IssueTapdRelation | 1 | models.Model（定义） | `bkmonitor/models/issue.py:242` |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | MetricListCache | 1 | models.Model（定义） | `bkmonitor/models/metric_list_cache.py:53` |
| `bkmonitor_querytemplate` ⚠︎默认命名 | QueryTemplate | 1 | models.Model（定义） | `bkmonitor/models/query_template.py:19` |
| `bkmonitor_reportcontents` ⚠︎默认命名 | ReportContents | 1 | models.Model（定义） | `bkmonitor/models/base.py:1079` |
| `bkmonitor_reportitems` ⚠︎默认命名 | ReportItems | 1 | models.Model（定义） | `bkmonitor/models/base.py:1031` |
| `bkmonitor_reportstatus` ⚠︎默认命名 | ReportStatus | 1 | models.Model（定义） | `bkmonitor/models/base.py:1094` |
| `bkmonitor_statisticsmetric` ⚠︎默认命名 | StatisticsMetric | 1 | models.Model（定义） | `bkmonitor/models/statistics.py:15` |
| `bkmonitor_strategy_issue_config` | StrategyIssueConfig | 1 | models.Model（定义） | `bkmonitor/models/issue.py:85` |
| `calendar` | CalendarModel | 1 | import（calendars） | `bkmonitor/management/commands/default_calendar_sync.py:19` |
| `calendar_item` | CalendarItemModel | 1 | import（calendars） | `bkmonitor/management/commands/default_calendar_sync.py:19` |
| `converge_instance` | ConvergeInstance | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:767` |
| `converge_relation` | ConvergeRelation | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:843` |
| `dashboard` | Dashboard | 1 | import（bk_dataview） | `bkmonitor/iam/resource.py:19` |
| `data_source` | DataSource | 7 | import（bk_dataview） | `bkmonitor/data_source/data_source/__init__.py:3109` |
| `dict_base_alarm` | BaseAlarm | 1 | models.Model（定义） | `bkmonitor/models/base.py:109` |
| `duty_arrange` | DutyArrange | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:673` |
| `duty_arrange_snap` | DutyArrangeSnap | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:796` |
| `duty_plan_send_record` | DutyPlanSendRecord | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:657` |
| `duty_rule` | DutyRule | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:585` |
| `duty_rule_relation` | DutyRuleRelation | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:641` |
| `duty_rule_snap` | DutyRuleSnap | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:621` |
| `event_plugin` | EventPluginV2 | 1 | models.Model（定义） | `bkmonitor/models/fta/plugin.py:147` |
| `event_plugin_instance` | EventPluginInstance | 1 | models.Model（定义） | `bkmonitor/models/fta/plugin.py:166` |
| `external_permission` | ExternalPermission | 1 | models.Model（定义） | `bkmonitor/models/external_iam.py:29` |
| `external_permission_apply_record` | ExternalPermissionApplyRecord | 1 | models.Model（定义） | `bkmonitor/models/external_iam.py:78` |
| `global_setting` | GlobalConfig | 1 | models.Model（定义） | `bkmonitor/models/config.py:18` |
| `home_alarm_graph_config` | HomeAlarmGraphConfig | 1 | models.Model（定义） | `bkmonitor/models/home.py:5` |
| `metadata_datasourceresulttable` ⚠︎默认命名 | DataSourceResultTable | 1 | import（metadata） | `bkmonitor/data_source/data_source/__init__.py:3109` |
| `metadata_resulttable` ⚠︎默认命名 | ResultTable | 2 | import（metadata） | `bkmonitor/data_source/data_source/__init__.py:3109` |
| `metadata_space` ⚠︎默认命名 | Space | 1 | import（metadata） | `bkmonitor/iam/resource.py:146` |
| `metadata_spacedatasource` ⚠︎默认命名 | SpaceDataSource | 1 | import（metadata） | `bkmonitor/management/commands/change_custom_group_biz.py:15` |
| `metadata_spacetype` ⚠︎默认命名 | SpaceType | 1 | import（metadata） | `bkmonitor/iam/resource.py:146` |
| `metadata_timeseriesmetric` ⚠︎默认命名 | TimeSeriesMetric | 1 | import（metadata） | `bkmonitor/management/commands/check_plugin_status.py:19` |
| `metric_mapping_config` | MetricMappingConfigModel | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:778` |
| `monitor_migration` | MonitorMigration | 1 | models.Model（定义） | `bkmonitor/models/config.py:81` |
| `monitor_rolepermission` ⚠︎默认命名 | RolePermission | 1 | import（monitor） | `bkmonitor/iam/upgrade.py:22` |
| `monitor_web_collectconfigmeta` ⚠︎默认命名 | CollectConfigMeta | 1 | import（monitor_web） | `bkmonitor/share/handler.py:27` |
| `monitor_web_collectorpluginmeta` ⚠︎默认命名 | CollectorPluginMeta | 4 | import（monitor_web） | `bkmonitor/management/commands/check_plugin_status.py:28` |
| `monitor_web_customeventgroup` ⚠︎默认命名 | CustomEventGroup | 1 | import（monitor_web） | `bkmonitor/share/handler.py:27` |
| `monitor_web_customtstable` ⚠︎默认命名 | CustomTSTable | 3 | import（monitor_web） | `bkmonitor/management/commands/change_custom_group_biz.py:17` |
| `monitor_web_datatargetmapping` ⚠︎默认命名 | DataTargetMapping | 1 | import（monitor_web） | `bkmonitor/models/strategy.py:415` |
| `notice_subscribe` | NoticeSubscribe | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:975` |
| `org` | Org | 1 | import（bk_dataview） | `bkmonitor/iam/resource.py:19` |
| `permission` | Permission | 3 | import（bk_dataview） | `bkmonitor/iam/migrate.py:17` |
| `render_image_task` | RenderImageTask | 1 | models.Model（定义） | `bkmonitor/models/report.py:143` |
| `report` | Report | 1 | models.Model（定义） | `bkmonitor/models/report.py:81` |
| `report_apply_record` | ReportApplyRecord | 1 | models.Model（定义） | `bkmonitor/models/report.py:121` |
| `report_channel` | ReportChannel | 1 | models.Model（定义） | `bkmonitor/models/report.py:45` |
| `report_send_record` | ReportSendRecord | 1 | models.Model（定义） | `bkmonitor/models/report.py:62` |
| `strategy_action_relation` | StrategyActionConfigRelation | 1 | models.Model（定义） | `bkmonitor/models/fta/action.py:897` |
| `tapd_workspace_binding` | TapdWorkspaceBinding | 1 | models.Model（定义） | `bkmonitor/models/tapd.py:19` |
| `tapd_workspace_manual_unbind` | TapdWorkspaceManualUnbind | 1 | models.Model（定义） | `bkmonitor/models/tapd.py:45` |
| `token_access_record` | TokenAccessRecord | 1 | models.Model（定义） | `bkmonitor/models/token.py:197` |
| `user` | User | 1 | import（bk_dataview） | `bkmonitor/management/commands/set_superuser.py:10` |
| `user_group` | UserGroup | 1 | models.Model（定义） | `bkmonitor/models/strategy.py:467` |

## 非 HTTP 入口

- **信号接收**：2 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/UnifyQuery查询专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/issue专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/告警屏蔽专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/告警查询专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/场景视图专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/性能场景专家`（命中标识 `bkmonitor`）
- `/root/bk-monitor/.module-experts/数据源查询构造专家`（命中标识 `bkmonitor`）


**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/外部API集成专题`

**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/外部API集成专题`
## 专家资产（深挖读这些）

**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/外部API集成专题`


**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/外部API集成专题`
## 专家资产（深挖读这些）

**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/外部API集成专题`

## 归属文件（372）

- `bkmonitor/db_routers.py`
- `bkmonitor/profiling.py`
- `bkmonitor/__init__.py`
- `bkmonitor/admin.py`
- `bkmonitor/migrate.py`
- `bkmonitor/apps.py`
- `bkmonitor/action/utils.py`
- `bkmonitor/action/converter.py`
- `bkmonitor/action/__init__.py`
- `bkmonitor/action/duty_manage.py`
- `bkmonitor/action/alert_assign.py`
- `bkmonitor/action/serializers/report.py`
- `bkmonitor/action/serializers/strategy.py`
- `bkmonitor/action/serializers/__init__.py`
- `bkmonitor/action/serializers/assign.py`
- `bkmonitor/action/serializers/action.py`
- `bkmonitor/aiops/utils.py`
- `bkmonitor/aiops/__init__.py`
- `bkmonitor/aiops/alert/utils.py`
- `bkmonitor/aiops/alert/maintainer.py`
- `bkmonitor/aiops/alert/__init__.py`
- `bkmonitor/aiops/incident/models.py`
- `bkmonitor/aiops/incident/graph.py`
- `bkmonitor/aiops/incident/__init__.py`
- `bkmonitor/aiops/incident/operation.py`
- `bkmonitor/aiops/incident/notice.py`
- `bkmonitor/as_code/parse.py`
- `bkmonitor/as_code/utils.py`
- `bkmonitor/as_code/schema.py`
- `bkmonitor/as_code/__init__.py`
- `bkmonitor/as_code/constants.py`
- `bkmonitor/as_code/parse_yaml.py`
- `bkmonitor/as_code/ply/__init__.py`
- `bkmonitor/as_code/ply/error.py`
- `bkmonitor/as_code/ply/conditions/parsetab.py`
- `bkmonitor/as_code/ply/conditions/__init__.py`
- `bkmonitor/as_code/ply/expression/parsetab.py`
- `bkmonitor/as_code/ply/expression/__init__.py`
- `bkmonitor/as_code/ply/function/parsetab.py`
- `bkmonitor/as_code/ply/function/__init__.py`
- ……其余 20 个见 JSON 输出（完整清单）
