# MonitorWebConfig（`monitor-web`）

> **职责**：监控 Web 资源层：策略/屏蔽/采集/场景视图等配置类页面的后端

> **职责**：监控 Web 资源层：策略/屏蔽/采集/场景视图等配置类页面的后端

- **位置**：`packages/monitor_web/` · 归属文件 **528** 个 · 约 **126539** 行
- **定义**：`packages/monitor_web/tasks.py:1`（django）
- **挂载前缀**：`/commons`、`/k8s`、`/overview` 等 7 个 · 视图/接口入口 **147** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bk_dataview`、`bkm_ipchooser`、`bkm_space`、`bkmonitor`、`calendars`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`rum_web`
- **被依赖**（动它会影响）：`apm_web`、`bkmonitor`、`fta_web`、`kernel_api`、`metadata`、`monitor`、`performance`、`rum_web`

## 数据表（177）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `action_config` | ActionConfig | 5 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `action_plugin` | ActionPlugin | 2 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `ai_feature_settings` | AIFeatureSettings | 2 | import（bkmonitor） | `packages/monitor_web/data_migrate/data_import.py:7` |
| `alarm_action` | Action | 2 | import（bkmonitor） | `packages/monitor_web/notice_group/resources/front.py:18` |
| `alarm_action_notice_group_mapping` | ActionNoticeMapping | 2 | import（bkmonitor） | `packages/monitor_web/notice_group/resources/front.py:18` |
| `alarm_alert` | Alert | 2 | import（bkmonitor） | `packages/monitor_web/alert_events/event_filters.py:19` |
| `alarm_algorithm_v2` | AlgorithmModel | 12 | import（bkmonitor） | `packages/monitor_web/tasks.py:55` |
| `alarm_anomaly_record` | AnomalyRecord | 2 | import（bkmonitor） | `packages/monitor_web/alert_events/event_filters.py:19` |
| `alarm_cachenode` | CacheNode | 1 | import（bkmonitor） | `packages/monitor_web/redis_management/resources.py:25` |
| `alarm_cacherouter` | CacheRouter | 1 | import（bkmonitor） | `packages/monitor_web/redis_management/resources.py:25` |
| `alarm_detect_v2` | DetectModel | 3 | import（bkmonitor） | `packages/monitor_web/data_migrate/strategy_migration.py:23` |
| `alarm_event` | Event | 4 | import（bkmonitor） | `packages/monitor_web/alert_events/event_filters.py:19` |
| `alarm_event_action` | EventAction | 1 | import（bkmonitor） | `packages/monitor_web/alert_events/resources/frontend_resource.py:30` |
| `alarm_item_v2` | ItemModel | 10 | import（bkmonitor） | `packages/monitor_web/tasks.py:55` |
| `alarm_notice_group` | NoticeGroup | 2 | import（bkmonitor） | `packages/monitor_web/notice_group/resources/backend.py:12` |
| `alarm_query_config_v2` | QueryConfigModel | 20 | import（bkmonitor） | `packages/monitor_web/tasks.py:671` |
| `alarm_shield` | Shield | 9 | import（bkmonitor） | `packages/monitor_web/tasks.py:436` |
| `alarm_strategy` | Strategy | 4 | import（bkmonitor） | `packages/monitor_web/tasks.py:57` |
| `alarm_strategy_biz_access` | DefaultStrategyBizAccessModel | 4 | import（bkmonitor） | `packages/monitor_web/data_migrate/data_import.py:7` |
| `alarm_strategy_history` | StrategyHistoryModel | 2 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/strategy.py:7` |
| `alarm_strategy_label` | StrategyLabel | 7 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/strategy.py:7` |
| `alarm_strategy_v2` | StrategyModel | 38 | import（bkmonitor） | `packages/monitor_web/tasks.py:55` |
| `algorithm_choice_config` | AlgorithmChoiceConfig | 2 | import（bkmonitor） | `packages/monitor_web/tasks.py:55` |
| `api_auth_token` | ApiAuthToken | 3 | import（bkmonitor） | `packages/monitor_web/commons/token/service.py:12` |
| `apm_apmapplication` ⚠︎默认命名 | ApmApplication | 6 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_apminstancediscover` ⚠︎默认命名 | ApmInstanceDiscover | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_apmmetricdimension` ⚠︎默认命名 | ApmMetricDimension | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_apmtopodiscoverrule` ⚠︎默认命名 | ApmTopoDiscoverRule | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_bcsclusterdefaultapplicationrelation` ⚠︎默认命名 | BcsClusterDefaultApplicationRelation | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_bkdataflowconfig` ⚠︎默认命名 | BkdataFlowConfig | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_datalink` ⚠︎默认命名 | DataLink | 2 | import（apm） | `packages/monitor_web/data_migrate/fetcher/metadata/datalink.py:2` |
| `apm_ebpf_clusterrelation` ⚠︎默认命名 | ClusterRelation | 1 | import（apm_ebpf） | `packages/monitor_web/data_migrate/fetcher/apm_ebpf.py:2` |
| `apm_ebpf_deepflowdashboardrecord` ⚠︎默认命名 | DeepflowDashboardRecord | 1 | import（apm_ebpf） | `packages/monitor_web/data_migrate/fetcher/apm_ebpf.py:2` |
| `apm_ebpf_deepflowworkload` ⚠︎默认命名 | DeepflowWorkload | 3 | import（apm_ebpf） | `packages/monitor_web/data_migrate/fetcher/apm_ebpf.py:2` |
| `apm_ebpfapplicationconfig` ⚠︎默认命名 | EbpfApplicationConfig | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_profileservice` ⚠︎默认命名 | ProfileService | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_remoteservicediscover` ⚠︎默认命名 | RemoteServiceDiscover | 2 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_subscriptionconfig` ⚠︎默认命名 | SubscriptionConfig | 3 | import（apm） | `packages/monitor_web/data_migrate/partial.py:15` |
| `apm_web_apmmetaconfig` ⚠︎默认命名 | ApmMetaConfig | 4 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_application` ⚠︎默认命名 | Application | 15 | import（apm_web） | `packages/monitor_web/commons/biz/func_control.py:81` |
| `apm_web_applicationcustomservice` ⚠︎默认命名 | ApplicationCustomService | 2 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_applicationrelationinfo` ⚠︎默认命名 | ApplicationRelationInfo | 2 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_profileuploadrecord` ⚠︎默认命名 | ProfileUploadRecord | 2 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_strategyinstance` ⚠︎默认命名 | StrategyInstance | 2 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_strategytemplate` ⚠︎默认命名 | StrategyTemplate | 2 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_tracecomparison` ⚠︎默认命名 | TraceComparison | 2 | import（apm_web） | `packages/monitor_web/data_migrate/partial.py:40` |
| `apm_web_uservisitrecord` ⚠︎默认命名 | UserVisitRecord | 1 | import（apm_web） | `packages/monitor_web/overview/search.py:19` |
| `app_snapshot_host_index` | SnapshotHostIndex | 1 | import（bkmonitor） | `packages/monitor_web/strategies/metric_list_cache.py:34` |
| `as_code_import_history` | AsCodeImportTask | 1 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:61` |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | AlertAssignGroup | 3 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | AlertAssignRule | 3 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `bkmonitor_alertconfig` ⚠︎默认命名 | AlertConfig | 1 | import（bkmonitor） | `packages/monitor_web/strategies/metric_list_cache.py:34` |
| `bkmonitor_bcsclusterlabels` ⚠︎默认命名 | BCSClusterLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcscontainerlabels` ⚠︎默认命名 | BCSContainerLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcslabel` ⚠︎默认命名 | BCSLabel | 2 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcsnodelabels` ⚠︎默认命名 | BCSNodeLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcspodlabels` ⚠︎默认命名 | BCSPodLabels | 2 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcspodmonitorlabels` ⚠︎默认命名 | BCSPodMonitorLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcsservicelabels` ⚠︎默认命名 | BCSServiceLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcsservicemonitorlabels` ⚠︎默认命名 | BCSServiceMonitorLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_bcsworkloadlabels` ⚠︎默认命名 | BCSWorkloadLabels | 1 | import（bkmonitor） | `packages/monitor_web/scene_view/resources/kubernetes.py:32` |
| `bkmonitor_dutyplan` ⚠︎默认命名 | DutyPlan | 1 | import（bkmonitor） | `packages/monitor_web/user_group/views.py:19` |
| `bkmonitor_eventplugin` ⚠︎默认命名 | EventPlugin | 1 | import（bkmonitor） | `packages/monitor_web/statistics/v2/event_plugin.py:17` |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | MetricListCache | 24 | import（bkmonitor） | `packages/monitor_web/tasks.py:373` |
| `bkmonitor_querytemplate` ⚠︎默认命名 | QueryTemplate | 4 | import（bkmonitor） | `packages/monitor_web/data_migrate/migration_status_check.py:1519` |
| `bkmonitor_reportcontents` ⚠︎默认命名 | ReportContents | 3 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/report.py:1` |
| `bkmonitor_reportitems` ⚠︎默认命名 | ReportItems | 4 | import（bkmonitor） | `packages/monitor_web/tasks.py:956` |
| `bkmonitor_reportstatus` ⚠︎默认命名 | ReportStatus | 2 | import（bkmonitor） | `packages/monitor_web/report/resources.py:32` |
| `bkmonitor_statisticsmetric` ⚠︎默认命名 | StatisticsMetric | 3 | import（bkmonitor） | `packages/monitor_web/statistics/v2/factory.py:12` |
| `builtin_role` | BuiltinRole | 1 | import（bk_dataview） | `packages/monitor_web/data_migrate/data_rebuilder.py:15` |
| `calendar` | CalendarModel | 1 | import（calendars） | `packages/monitor_web/data_migrate/fetcher/calendar.py:1` |
| `calendar_item` | CalendarItemModel | 1 | import（calendars） | `packages/monitor_web/data_migrate/fetcher/calendar.py:1` |
| `custom_report_subscription_config_v2` | CustomReportSubscription | 1 | import（metadata） | `packages/monitor_web/data_migrate/bk_collector.py:22` |
| `dashboard` | Dashboard | 13 | import（bk_dataview） | `packages/monitor_web/tasks.py:1791` |
| `data_source` | DataSource | 11 | import（bk_dataview） | `packages/monitor_web/as_code/resources.py:35` |
| `dict_base_alarm` | BaseAlarm | 1 | import（bkmonitor） | `packages/monitor_web/strategies/metric_list_cache.py:34` |
| `duty_arrange` | DutyArrange | 4 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `duty_rule` | DutyRule | 5 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `duty_rule_relation` | DutyRuleRelation | 2 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `duty_rule_snap` | DutyRuleSnap | 2 | import（bkmonitor） | `packages/monitor_web/user_group/views.py:19` |
| `event_plugin` | EventPluginV2 | 1 | import（bkmonitor） | `packages/monitor_web/strategies/metric_list_cache.py:34` |
| `external_permission` | ExternalPermission | 3 | import（bkmonitor） | `packages/monitor_web/commons/biz/resources.py:23` |
| `external_permission_apply_record` | ExternalPermissionApplyRecord | 2 | import（bkmonitor） | `packages/monitor_web/tasks.py:56` |
| `folder` | Folder | 1 | import（bk_dataview） | `packages/monitor_web/data_migrate/data_rebuilder.py:15` |
| `fta_web_alertexperience` ⚠︎默认命名 | AlertExperience | 1 | import（fta_web） | `packages/monitor_web/data_migrate/fetcher/fta_web.py:1` |
| `fta_web_alertsuggestion` ⚠︎默认命名 | AlertSuggestion | 1 | import（fta_web） | `packages/monitor_web/data_migrate/fetcher/fta_web.py:1` |
| `fta_web_metricrecommendationfeedback` ⚠︎默认命名 | MetricRecommendationFeedback | 1 | import（fta_web） | `packages/monitor_web/data_migrate/fetcher/fta_web.py:1` |
| `fta_web_searchfavorite` ⚠︎默认命名 | SearchFavorite | 1 | import（fta_web） | `packages/monitor_web/statistics/v2/alert_action.py:26` |
| `fta_web_searchhistory` ⚠︎默认命名 | SearchHistory | 1 | import（fta_web） | `packages/monitor_web/incident/resources.py:55` |
| `global_setting` | GlobalConfig | 5 | import（bkmonitor） | `packages/monitor_web/tasks.py:194` |
| `home_alarm_graph_config` | HomeAlarmGraphConfig | 2 | import（bkmonitor） | `packages/monitor_web/overview/resources.py:35` |
| `metadata_bcsclusterinfo` ⚠︎默认命名 | BCSClusterInfo | 6 | import（metadata） | `packages/monitor_web/data_migrate/biz_matadata.py:19` |
| `metadata_bcsfederalclusterinfo` ⚠︎默认命名 | BcsFederalClusterInfo | 2 | import（metadata） | `packages/monitor_web/data_migrate/partial.py:67` |
| `metadata_bkappspacerecord` ⚠︎默认命名 | BkAppSpaceRecord | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metadata_bkbaseresulttable` ⚠︎默认命名 | BkBaseResultTable | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/datalink.py:2` |
| `metadata_clusterconfig` ⚠︎默认命名 | ClusterConfig | 1 | import（metadata） | `packages/monitor_web/data_migrate/data_rebuilder.py:39` |
| `metadata_clusterinfo` ⚠︎默认命名 | ClusterInfo | 4 | import（metadata） | `packages/monitor_web/data_migrate/data_export.py:23` |
| `metadata_datasourceresulttable` ⚠︎默认命名 | DataSourceResultTable | 5 | import（metadata） | `packages/monitor_web/data_migrate/biz_matadata.py:19` |
| `metadata_dorisstorage` ⚠︎默认命名 | DorisStorage | 2 | import（metadata） | `packages/monitor_web/data_migrate/data_export.py:23` |
| `metadata_esfieldqueryaliasoption` ⚠︎默认命名 | ESFieldQueryAliasOption | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/storage.py:4` |
| `metadata_essnapshot` ⚠︎默认命名 | EsSnapshot | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/storage.py:2` |
| `metadata_essnapshotindice` ⚠︎默认命名 | EsSnapshotIndice | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/storage.py:2` |
| `metadata_esstorage` ⚠︎默认命名 | ESStorage | 5 | import（metadata） | `packages/monitor_web/data_migrate/data_export.py:23` |
| `metadata_influxdbclusterinfo` ⚠︎默认命名 | InfluxDBClusterInfo | 1 | import（metadata） | `packages/monitor_web/statistics/v2/storage.py:14` |
| `metadata_kafkastorage` ⚠︎默认命名 | KafkaStorage | 2 | import（metadata） | `packages/monitor_web/data_migrate/data_export.py:23` |
| `metadata_kafkatopicinfo` ⚠︎默认命名 | KafkaTopicInfo | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/data_source.py:8` |
| `metadata_logsubscriptionconfig` ⚠︎默认命名 | LogSubscriptionConfig | 1 | import（metadata） | `packages/monitor_web/data_migrate/bk_collector.py:22` |
| `metadata_recordrule` ⚠︎默认命名 | RecordRule | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:24` |
| `metadata_recordrulev4` ⚠︎默认命名 | RecordRuleV4 | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:25` |
| `metadata_recordrulev4flow` ⚠︎默认命名 | RecordRuleV4Flow | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:25` |
| `metadata_resulttable` ⚠︎默认命名 | ResultTable | 9 | import（metadata） | `packages/monitor_web/collecting/resources/status.py:26` |
| `metadata_resulttablefield` ⚠︎默认命名 | ResultTableField | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/data_source.py:7` |
| `metadata_space` ⚠︎默认命名 | Space | 11 | import（metadata） | `packages/monitor_web/commons/context/resources.py:17` |
| `metadata_spacedatasource` ⚠︎默认命名 | SpaceDataSource | 2 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metadata_spacerelatedstorageinfo` ⚠︎默认命名 | SpaceRelatedStorageInfo | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metadata_spaceresource` ⚠︎默认命名 | SpaceResource | 2 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metadata_spacestickyinfo` ⚠︎默认命名 | SpaceStickyInfo | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metadata_spacetype` ⚠︎默认命名 | SpaceType | 1 | import（metadata） | `packages/monitor_web/iam/views.py:29` |
| `metadata_spacevminfo` ⚠︎默认命名 | SpaceVMInfo | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metadata_storageclusterrecord` ⚠︎默认命名 | StorageClusterRecord | 3 | import（metadata） | `packages/monitor_web/data_migrate/partial.py:57` |
| `metadata_timeseriesmetric` ⚠︎默认命名 | TimeSeriesMetric | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/data_source.py:5` |
| `metadata_timeseriesscope` ⚠︎默认命名 | TimeSeriesScope | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/data_source.py:3` |
| `metadata_vmresulttableconfig` | ResultTableConfig | 1 | import（metadata） | `packages/monitor_web/data_migrate/fetcher/metadata/datalink.py:4` |
| `metadata_vmshortlinkrecord` ⚠︎默认命名 | VMShortLinkRecord | 1 | import（metadata） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:12` |
| `metric_mapping_config` | MetricMappingConfigModel | 1 | import（bkmonitor） | `packages/monitor_web/promql_import/resources.py:17` |
| `monitor_applicationconfig` ⚠︎默认命名 | ApplicationConfig | 12 | import（monitor） | `packages/monitor_web/tasks.py:308` |
| `monitor_migration` | MonitorMigration | 1 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/internal_config.py:2` |
| `monitor_rolepermission` ⚠︎默认命名 | RolePermission | 1 | import（monitor） | `packages/monitor_web/models/config.py:11` |
| `monitor_uploadedfile` ⚠︎默认命名 | UploadedFile | 1 | import（monitor） | `packages/monitor_web/commons/file_manager.py:19` |
| `monitor_uptimecheckgroup` ⚠︎默认命名 | UptimeCheckGroup | 3 | import（monitor） | `packages/monitor_web/data_migrate/fetcher/uptimecheck.py:1` |
| `monitor_uptimechecknode` ⚠︎默认命名 | UptimeCheckNode | 4 | import（monitor） | `packages/monitor_web/data_migrate/fetcher/uptimecheck.py:1` |
| `monitor_uptimechecktask` ⚠︎默认命名 | UptimeCheckTask | 6 | import（monitor） | `packages/monitor_web/data_migrate/biz_matadata.py:21` |
| `monitor_uptimechecktaskcollectorlog` ⚠︎默认命名 | UptimeCheckTaskCollectorLog | 1 | import（monitor） | `packages/monitor_web/models/uptime_check.py:14` |
| `monitor_uptimechecktasksubscription` ⚠︎默认命名 | UptimeCheckTaskSubscription | 3 | import（monitor） | `packages/monitor_web/data_migrate/subscription_tasks.py:6` |
| `monitor_userconfig` ⚠︎默认命名 | UserConfig | 3 | import（monitor） | `packages/monitor_web/commons/context/resources.py:33` |
| `monitor_web_alertsolution` ⚠︎默认命名 | AlertSolution | 1 | models.Model（定义） | `packages/monitor_web/models/alert_events.py:17` |
| `monitor_web_bcsareamodel` ⚠︎默认命名 | BCSAreaModel | 1 | models.Model（定义） | `packages/monitor_web/models/kubernetes.py:40` |
| `monitor_web_bcsclustermodel` ⚠︎默认命名 | BCSClusterModel | 1 | models.Model（定义） | `packages/monitor_web/models/kubernetes.py:23` |
| `monitor_web_bcsprojectmodel` ⚠︎默认命名 | BCSProjectModel | 1 | models.Model（定义） | `packages/monitor_web/models/kubernetes.py:14` |
| `monitor_web_collectconfigmeta` ⚠︎默认命名 | CollectConfigMeta | 1 | models.Model（定义） | `packages/monitor_web/models/collecting.py:34` |
| `monitor_web_collectorpluginconfig` ⚠︎默认命名 | CollectorPluginConfig | 1 | models.Model（定义） | `packages/monitor_web/models/plugin.py:717` |
| `monitor_web_collectorplugininfo` ⚠︎默认命名 | CollectorPluginInfo | 1 | models.Model（定义） | `packages/monitor_web/models/plugin.py:771` |
| `monitor_web_collectorpluginmeta` ⚠︎默认命名 | CollectorPluginMeta | 1 | models.Model（定义） | `packages/monitor_web/models/plugin.py:42` |
| `monitor_web_customeventgroup` ⚠︎默认命名 | CustomEventGroup | 1 | models.Model（定义） | `packages/monitor_web/models/custom_report.py:31` |
| `monitor_web_customeventitem` ⚠︎默认命名 | CustomEventItem | 1 | models.Model（定义） | `packages/monitor_web/models/custom_report.py:64` |
| `monitor_web_customtsfield` ⚠︎默认命名 | CustomTSField | 1 | models.Model（定义） | `packages/monitor_web/models/custom_report.py:77` |
| `monitor_web_customtsgroupingrule` ⚠︎默认命名 | CustomTSGroupingRule | 1 | models.Model（定义） | `packages/monitor_web/models/custom_report.py:280` |
| `monitor_web_customtsitem` ⚠︎默认命名 | CustomTSItem | 1 | models.Model（定义） | `packages/monitor_web/models/custom_report.py:257` |
| `monitor_web_customtstable` ⚠︎默认命名 | CustomTSTable | 1 | models.Model（定义） | `packages/monitor_web/models/custom_report.py:105` |
| `monitor_web_datatargetmapping` ⚠︎默认命名 | DataTargetMapping | 1 | models.Model（定义） | `packages/monitor_web/models/data_target.py:20` |
| `monitor_web_deploymentconfigversion` ⚠︎默认命名 | DeploymentConfigVersion | 1 | models.Model（定义） | `packages/monitor_web/models/collecting.py:296` |
| `monitor_web_favoritegroup` ⚠︎默认命名 | FavoriteGroup | 1 | models.Model（定义） | `packages/monitor_web/models/data_explorer.py:36` |
| `monitor_web_importdetail` ⚠︎默认命名 | ImportDetail | 1 | models.Model（定义） | `packages/monitor_web/models/export_import.py:79` |
| `monitor_web_importhistory` ⚠︎默认命名 | ImportHistory | 1 | models.Model（定义） | `packages/monitor_web/models/export_import.py:27` |
| `monitor_web_importparse` ⚠︎默认命名 | ImportParse | 1 | models.Model（定义） | `packages/monitor_web/models/export_import.py:101` |
| `monitor_web_operatorsystem` ⚠︎默认命名 | OperatorSystem | 1 | models.Model（定义） | `packages/monitor_web/models/plugin.py:1070` |
| `monitor_web_pluginversionhistory` ⚠︎默认命名 | PluginVersionHistory | 1 | models.Model（定义） | `packages/monitor_web/models/plugin.py:840` |
| `monitor_web_queryhistory` ⚠︎默认命名 | QueryHistory | 1 | models.Model（定义） | `packages/monitor_web/models/data_explorer.py:18` |
| `monitor_web_scenemodel` ⚠︎默认命名 | SceneModel | 1 | models.Model（定义） | `packages/monitor_web/models/scene_view.py:19` |
| `monitor_web_sceneviewmodel` ⚠︎默认命名 | SceneViewModel | 1 | models.Model（定义） | `packages/monitor_web/models/scene_view.py:36` |
| `monitor_web_sceneviewordermodel` ⚠︎默认命名 | SceneViewOrderModel | 1 | models.Model（定义） | `packages/monitor_web/models/scene_view.py:99` |
| `monitor_web_uploadedfileinfo` ⚠︎默认命名 | UploadedFileInfo | 1 | models.Model（定义） | `packages/monitor_web/models/file.py:26` |
| `monitor_web_useraccessrecord` ⚠︎默认命名 | UserAccessRecord | 1 | models.Model（定义） | `packages/monitor_web/extend_account/models.py:38` |
| `notice_subscribe` | NoticeSubscribe | 2 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/strategy.py:7` |
| `org` | Org | 8 | import（bk_dataview） | `packages/monitor_web/data_migrate/bkci_space_prefix.py:8` |
| `permission` | Permission | 16 | import（bk_dataview） | `packages/monitor_web/alert_events/resources/frontend_resource.py:29` |
| `preferences` | Preferences | 1 | import（bk_dataview） | `packages/monitor_web/data_migrate/fetcher/dashboard.py:1` |
| `report` | Report | 3 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/report.py:2` |
| `report_apply_record` | ReportApplyRecord | 1 | import（bkmonitor） | `packages/monitor_web/new_report/resources.py:25` |
| `report_channel` | ReportChannel | 2 | import（bkmonitor） | `packages/monitor_web/data_migrate/fetcher/report.py:2` |
| `report_send_record` | ReportSendRecord | 1 | import（bkmonitor） | `packages/monitor_web/new_report/resources.py:25` |
| `role` | Role | 1 | import（bk_dataview） | `packages/monitor_web/data_migrate/data_rebuilder.py:15` |
| `star` | Star | 3 | import（bk_dataview） | `packages/monitor_web/data_migrate/fetcher/dashboard.py:1` |
| `strategy_action_relation` | StrategyActionConfigRelation | 5 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |
| `token_access_record` | TokenAccessRecord | 1 | import（bkmonitor） | `packages/monitor_web/share/resources.py:18` |
| `user` | User | 1 | import（bk_dataview） | `packages/monitor_web/overview/resources.py:26` |
| `user_group` | UserGroup | 10 | import（bkmonitor） | `packages/monitor_web/as_code/resources.py:50` |

## 非 HTTP 入口

- **定时任务**：32 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `monitor_web`）
- `/root/bk-monitor/.module-experts/告警屏蔽专家`（命中标识 `monitor_web`）
- `/root/bk-monitor/.module-experts/告警查询专家`（命中标识 `monitor_web`）
- `/root/bk-monitor/.module-experts/场景视图专家`（命中标识 `monitor_web`）
- `/root/bk-monitor/.module-experts/性能场景专家`（命中标识 `monitor_web`）

## 归属文件（528）

- `packages/monitor_web/tasks.py`
- `packages/monitor_web/views.py`
- `packages/monitor_web/permissions.py`
- `packages/monitor_web/__init__.py`
- `packages/monitor_web/admin.py`
- `packages/monitor_web/urls.py`
- `packages/monitor_web/constants.py`
- `packages/monitor_web/apps.py`
- `packages/monitor_web/aiops/views.py`
- `packages/monitor_web/aiops/__init__.py`
- `packages/monitor_web/aiops/urls.py`
- `packages/monitor_web/aiops/constants.py`
- `packages/monitor_web/aiops/resources.py`
- `packages/monitor_web/aiops/ai_setting/views.py`
- `packages/monitor_web/aiops/ai_setting/__init__.py`
- `packages/monitor_web/aiops/ai_setting/serializers.py`
- `packages/monitor_web/aiops/ai_setting/resources.py`
- `packages/monitor_web/aiops/host_monitor/constant.py`
- `packages/monitor_web/aiops/host_monitor/utils.py`
- `packages/monitor_web/aiops/host_monitor/views.py`
- `packages/monitor_web/aiops/host_monitor/__init__.py`
- `packages/monitor_web/aiops/host_monitor/serializers.py`
- `packages/monitor_web/aiops/host_monitor/resources.py`
- `packages/monitor_web/aiops/metric_recommend/constant.py`
- `packages/monitor_web/aiops/metric_recommend/utils.py`
- `packages/monitor_web/aiops/metric_recommend/__init__.py`
- `packages/monitor_web/alert_events/constant.py`
- `packages/monitor_web/alert_events/event_filters.py`
- `packages/monitor_web/alert_events/views.py`
- `packages/monitor_web/alert_events/__init__.py`
- `packages/monitor_web/alert_events/urls.py`
- `packages/monitor_web/alert_events/resources/frontend_resource.py`
- `packages/monitor_web/alert_events/resources/__init__.py`
- `packages/monitor_web/as_code/views.py`
- `packages/monitor_web/as_code/__init__.py`
- `packages/monitor_web/as_code/urls.py`
- `packages/monitor_web/as_code/resources.py`
- `packages/monitor_web/cc/__init__.py`
- `packages/monitor_web/cc/resources/__init__.py`
- `packages/monitor_web/cc/resources/cmdb.py`
- ……其余 20 个见 JSON 输出（完整清单）
