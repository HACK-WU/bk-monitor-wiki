# 表 → 模块（反向索引）

> 用途：改/删某张表前，先看哪些模块引用了它（穷举反查，机械提取）。
> 接口级影响面（精确到某个 handler）见各模块的 `.module-experts/` 资产或现场 grep。

| 表 | 模块数 | 模块（引用次数 · 来源） |
|----|--------|--------------------------|
| `permission` | 8 | `monitor-web`（16 · import（bk_dataview））、`fta-web`（4 · import（bk_dataview））、`bkmonitor`（3 · import（bk_dataview））、`kernel-api`（3 · import（bk_dataview））、`alarm-backends`（2 · import（bk_dataview））、`apm`（1 · import（bk_dataview））、`bk-dataview`（1 · models.Model（定义））、`apm-web`（1 · import（bk_dataview）） |
| `global_setting` | 8 | `monitor-web`（5 · import（bkmonitor））、`kernel-api`（4 · import（bkmonitor））、`fta-web`（3 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`metadata`（1 · import（bkmonitor））、`apm-web`（1 · import（bkmonitor））、`monitor-api`（1 · import（bkmonitor）） |
| `data_source` | 7 | `metadata`（36 · import（bk_dataview））、`monitor-web`（11 · import（bk_dataview））、`bkmonitor`（7 · import（bk_dataview））、`alarm-backends`（3 · import（bk_dataview））、`apm`（2 · import（bk_dataview））、`kernel-api`（2 · import（bk_dataview））、`bk-dataview`（1 · models.Model（定义）） |
| `apm_web_application` ⚠︎默认命名 | 7 | `monitor-web`（15 · import（apm_web））、`bkmonitor`（8 · import（apm_web））、`rum-web`（8 · import（apm_web））、`kernel-api`（5 · import（apm_web））、`apm`（3 · import（apm_web））、`profile`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `alarm_algorithm_v2` | 6 | `monitor-web`（12 · import（bkmonitor））、`alarm-backends`（7 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor））、`apm-web`（1 · import（bkmonitor））、`fta-web`（1 · import（bkmonitor）） |
| `metadata_resulttable` ⚠︎默认命名 | 6 | `monitor-web`（9 · import（metadata））、`bkmonitor`（2 · import（metadata））、`query-api`（2 · import（metadata））、`alarm-backends`（1 · import（metadata））、`apm`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_space` ⚠︎默认命名 | 6 | `monitor-web`（11 · import（metadata））、`alarm-backends`（1 · import（metadata））、`apm-ebpf`（1 · import（metadata））、`bkmonitor`（1 · import（metadata））、`kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_clusterinfo` ⚠︎默认命名 | 6 | `monitor-web`（4 · import（metadata））、`apm`（2 · import（metadata））、`kernel-api`（2 · import（metadata））、`alarm-backends`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`query-api`（1 · import（metadata）） |
| `alarm_strategy_v2` | 5 | `monitor-web`（38 · import（bkmonitor））、`kernel-api`（9 · import（bkmonitor））、`alarm-backends`（4 · import（bkmonitor））、`fta-web`（3 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | 5 | `monitor-web`（24 · import（bkmonitor））、`fta-web`（3 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `alarm_query_config_v2` | 5 | `monitor-web`（20 · import（bkmonitor））、`kernel-api`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`metadata`（1 · import（bkmonitor））、`fta-web`（1 · import（bkmonitor）） |
| `user_group` | 5 | `monitor-web`（10 · import（bkmonitor））、`kernel-api`（7 · import（bkmonitor））、`apm-web`（5 · import（bkmonitor））、`alarm-backends`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_strategy` | 5 | `alarm-backends`（12 · import（bkmonitor））、`kernel-api`（5 · import（bkmonitor））、`monitor-web`（4 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor）） |
| `action_config` | 5 | `fta-web`（7 · import（bkmonitor））、`monitor-web`（5 · import（bkmonitor））、`kernel-api`（4 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `dashboard` | 5 | `monitor-web`（13 · import（bk_dataview））、`apm-ebpf`（1 · import（bk_dataview））、`bk-dataview`（1 · models.Model（定义））、`bkmonitor`（1 · import（bk_dataview））、`kernel-api`（1 · import（bk_dataview）） |
| `monitor_applicationconfig` ⚠︎默认命名 | 5 | `monitor-web`（12 · import（monitor））、`apm`（2 · import（monitor））、`apm-web`（1 · import（monitor））、`monitor`（1 · models.Model（定义））、`rum-web`（1 · import（monitor）） |
| `alarm_shield` | 5 | `monitor-web`（9 · import（bkmonitor））、`alarm-backends`（4 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor））、`fta-web`（1 · import（bkmonitor）） |
| `action_plugin` | 5 | `fta-web`（8 · import（bkmonitor））、`alarm-backends`（3 · import（bkmonitor））、`monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | 5 | `fta-web`（4 · import（bkmonitor））、`monitor-web`（3 · import（bkmonitor））、`kernel-api`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | 5 | `fta-web`（3 · import（bkmonitor））、`monitor-web`（3 · import（bkmonitor））、`kernel-api`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `monitor_web_customeventgroup` ⚠︎默认命名 | 5 | `kernel-api`（2 · import（monitor_web））、`bkmonitor`（1 · import（monitor_web））、`metadata`（1 · import（monitor_web））、`fta-web`（1 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `action_instance` | 4 | `alarm-backends`（19 · import（bkmonitor））、`fta-web`（5 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `apm_datalink` ⚠︎默认命名 | 4 | `metadata`（9 · import（apm））、`kernel-api`（4 · import（apm））、`monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `alarm_item_v2` | 4 | `monitor-web`（10 · import（bkmonitor））、`fta-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `metadata_bcsclusterinfo` ⚠︎默认命名 | 4 | `monitor-web`（6 · import（metadata））、`apm`（3 · import（metadata））、`kernel-api`（2 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `org` | 4 | `monitor-web`（8 · import（bk_dataview））、`kernel-api`（2 · import（bk_dataview））、`bk-dataview`（1 · models.Model（定义））、`bkmonitor`（1 · import（bk_dataview）） |
| `alarm_cacherouter` | 4 | `kernel-api`（5 · import（bkmonitor））、`alarm-backends`（4 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `strategy_action_relation` | 4 | `monitor-web`（5 · import（bkmonitor））、`kernel-api`（3 · import（bkmonitor））、`fta-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_cachenode` | 4 | `alarm-backends`（5 · import（bkmonitor））、`kernel-api`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `apm_apmapplication` ⚠︎默认命名 | 4 | `monitor-web`（6 · import（apm））、`apm`（1 · models.Model（定义））、`kernel-api`（1 · import（apm））、`metadata`（1 · import（apm）） |
| `duty_arrange` | 4 | `monitor-web`（4 · import（bkmonitor））、`kernel-api`（3 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `duty_rule` | 4 | `monitor-web`（5 · import（bkmonitor））、`kernel-api`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `metadata_esstorage` ⚠︎默认命名 | 4 | `monitor-web`（5 · import（metadata））、`apm`（2 · import（metadata））、`alarm-backends`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `monitor_web_collectorpluginmeta` ⚠︎默认命名 | 4 | `bkmonitor`（4 · import（monitor_web））、`kernel-api`（3 · import（monitor_web））、`metadata`（1 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `report` | 4 | `alarm-backends`（3 · import（bkmonitor））、`monitor-web`（3 · import（bkmonitor））、`kernel-api`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `bkmonitor_issue_merge_relation` | 4 | `kernel-api`（5 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor）） |
| `bkmonitor_reportitems` ⚠︎默认命名 | 4 | `monitor-web`（4 · import（bkmonitor））、`alarm-backends`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `apm_ebpf_deepflowworkload` ⚠︎默认命名 | 4 | `monitor-web`（3 · import（apm_ebpf））、`kernel-api`（2 · import（apm_ebpf））、`apm`（1 · import（apm_ebpf））、`apm-ebpf`（1 · models.Model（定义）） |
| `bkmonitor_querytemplate` ⚠︎默认命名 | 4 | `monitor-web`（4 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`apm-web`（1 · import（bkmonitor））、`profile`（1 · import（bkmonitor）） |
| `bkmonitor_statisticsmetric` ⚠︎默认命名 | 4 | `monitor-web`（3 · import（bkmonitor））、`apm-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_action` | 4 | `kernel-api`（2 · import（bkmonitor））、`monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor）） |
| `report_channel` | 4 | `alarm-backends`（2 · import（bkmonitor））、`monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `alarm_notice_group` | 4 | `monitor-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor）） |
| `alarm_strategy_history` | 4 | `monitor-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `metadata_spaceresource` ⚠︎默认命名 | 4 | `monitor-web`（2 · import（metadata））、`apm-ebpf`（1 · import（metadata））、`kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `user` | 4 | `kernel-api`（2 · import（bk_dataview））、`bk-dataview`（1 · models.Model（定义））、`bkmonitor`（1 · import（bk_dataview））、`monitor-web`（1 · import（bk_dataview）） |
| `calendar` | 4 | `alarm-backends`（1 · import（calendars））、`bkmonitor`（1 · import（calendars））、`calendars`（1 · models.Model（定义））、`monitor-web`（1 · import（calendars）） |
| `alarm_alert` | 3 | `alarm-backends`（8 · import（bkmonitor））、`monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_strategy_label` | 3 | `monitor-web`（7 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `api_auth_token` | 3 | `kernel-api`（5 · import（bkmonitor））、`monitor-web`（3 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_event` | 3 | `monitor-web`（4 · import（bkmonitor））、`alarm-backends`（3 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `converge_relation` | 3 | `alarm-backends`（5 · import（bkmonitor））、`fta-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `monitor_uptimechecktask` ⚠︎默认命名 | 3 | `monitor-web`（6 · import（monitor））、`kernel-api`（1 · import（monitor））、`monitor`（1 · models.Model（定义）） |
| `event_plugin` | 3 | `fta-web`（5 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `metadata_datasourceresulttable` ⚠︎默认命名 | 3 | `monitor-web`（5 · import（metadata））、`bkmonitor`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `apm_web_profileuploadrecord` ⚠︎默认命名 | 3 | `profile`（3 · import（apm_web））、`monitor-web`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `bkmonitor_reportcontents` ⚠︎默认命名 | 3 | `monitor-web`（3 · import（bkmonitor））、`alarm-backends`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `bkmonitor_strategy_issue_config` | 3 | `alarm-backends`（4 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `monitor_uptimechecknode` ⚠︎默认命名 | 3 | `monitor-web`（4 · import（monitor））、`kernel-api`（1 · import（monitor））、`monitor`（1 · models.Model（定义）） |
| `monitor_web_customtstable` ⚠︎默认命名 | 3 | `bkmonitor`（3 · import（monitor_web））、`kernel-api`（2 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `alarm_anomaly_record` | 3 | `alarm-backends`（2 · import（bkmonitor））、`monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_detect_v2` | 3 | `monitor-web`（3 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor）） |
| `apm_subscriptionconfig` ⚠︎默认命名 | 3 | `monitor-web`（3 · import（apm））、`apm`（1 · models.Model（定义））、`kernel-api`（1 · import（apm）） |
| `metadata_clusterconfig` ⚠︎默认命名 | 3 | `kernel-api`（3 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `monitor_uptimechecktasksubscription` ⚠︎默认命名 | 3 | `monitor-web`（3 · import（monitor））、`kernel-api`（1 · import（monitor））、`monitor`（1 · models.Model（定义）） |
| `monitor_userconfig` ⚠︎默认命名 | 3 | `monitor-web`（3 · import（monitor））、`fta-web`（1 · import（monitor））、`monitor`（1 · models.Model（定义）） |
| `monitor_web_collectconfigmeta` ⚠︎默认命名 | 3 | `kernel-api`（3 · import（monitor_web））、`bkmonitor`（1 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `ai_feature_settings` | 3 | `monitor-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_action_notice_group_mapping` | 3 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor）） |
| `bkmonitor_reportstatus` ⚠︎默认命名 | 3 | `monitor-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `duty_rule_relation` | 3 | `monitor-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `event_plugin_instance` | 3 | `fta-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `metadata_bcsfederalclusterinfo` ⚠︎默认命名 | 3 | `monitor-web`（2 · import（metadata））、`kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_spacedatasource` ⚠︎默认命名 | 3 | `monitor-web`（2 · import（metadata））、`bkmonitor`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `notice_subscribe` | 3 | `monitor-web`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `render_image_task` | 3 | `kernel-api`（2 · import（bkmonitor））、`alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `apm_ebpf_clusterrelation` ⚠︎默认命名 | 3 | `apm`（1 · import（apm_ebpf））、`apm-ebpf`（1 · models.Model（定义））、`monitor-web`（1 · import（apm_ebpf）） |
| `as_code_import_history` | 3 | `bkmonitor`（1 · models.Model（定义））、`kernel-api`（1 · import（bkmonitor））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_dutyplan` ⚠︎默认命名 | 3 | `alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_eventplugin` ⚠︎默认命名 | 3 | `bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor））、`monitor-web`（1 · import（bkmonitor）） |
| `calendar_item` | 3 | `bkmonitor`（1 · import（calendars））、`calendars`（1 · models.Model（定义））、`monitor-web`（1 · import（calendars）） |
| `custom_report_subscription_config_v2` | 3 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `dict_base_alarm` | 3 | `bkmonitor`（1 · models.Model（定义））、`monitor-api`（1 · import（bkmonitor））、`monitor-web`（1 · import（bkmonitor）） |
| `metadata_influxdbclusterinfo` ⚠︎默认命名 | 3 | `alarm-backends`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_kafkatopicinfo` ⚠︎默认命名 | 3 | `alarm-backends`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_logsubscriptionconfig` ⚠︎默认命名 | 3 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_pingserversubscriptionconfig` ⚠︎默认命名 | 3 | `alarm-backends`（1 · import（metadata））、`kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_recordrulev4` ⚠︎默认命名 | 3 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_recordrulev4flow` ⚠︎默认命名 | 3 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_resulttablefield` ⚠︎默认命名 | 3 | `metadata`（1 · models.Model（定义））、`apm-web`（1 · import（metadata））、`monitor-web`（1 · import（metadata）） |
| `metadata_spacetype` ⚠︎默认命名 | 3 | `bkmonitor`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_timeseriesmetric` ⚠︎默认命名 | 3 | `bkmonitor`（1 · import（metadata））、`metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `monitor_rolepermission` ⚠︎默认命名 | 3 | `bkmonitor`（1 · import（monitor））、`monitor`（1 · models.Model（定义））、`monitor-web`（1 · import（monitor）） |
| `report_send_record` | 3 | `alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `converge_instance` | 2 | `alarm-backends`（7 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_strategy_biz_access` | 2 | `monitor-web`（4 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `apm_web_apmmetaconfig` ⚠︎默认命名 | 2 | `monitor-web`（4 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `bkmonitor_issue_tapd_relation` | 2 | `fta-web`（3 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `external_permission` | 2 | `monitor-web`（3 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `metadata_label` ⚠︎默认命名 | 2 | `profile`（3 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_storageclusterrecord` ⚠︎默认命名 | 2 | `monitor-web`（3 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `monitor_uptimecheckgroup` ⚠︎默认命名 | 2 | `monitor-web`（3 · import（monitor））、`monitor`（1 · models.Model（定义）） |
| `monitor_web_pluginversionhistory` ⚠︎默认命名 | 2 | `kernel-api`（3 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `monitor_web_sceneviewmodel` ⚠︎默认命名 | 2 | `apm-web`（3 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `rum_web_rumappconfig` ⚠︎默认命名 | 2 | `rum`（3 · import（rum_web））、`rum-web`（1 · models.Model（定义）） |
| `star` | 2 | `monitor-web`（3 · import（bk_dataview））、`bk-dataview`（1 · models.Model（定义）） |
| `alarm_item` | 2 | `alarm-backends`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `algorithm_choice_config` | 2 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `apm_apminstancediscover` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_apmmetricdimension` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_apmtopodiscoverrule` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_bcsclusterdefaultapplicationrelation` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_bkdataflowconfig` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_ebpfapplicationconfig` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_profileservice` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_remoteservicediscover` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm））、`apm`（1 · models.Model（定义）） |
| `apm_web_applicationcustomservice` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `apm_web_applicationrelationinfo` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `apm_web_strategyinstance` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `apm_web_strategytemplate` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `apm_web_tracecomparison` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（apm_web））、`apm-web`（1 · models.Model（定义）） |
| `bkmonitor_bcslabel` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `bkmonitor_bcspodlabels` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `duty_rule_snap` | 2 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `external_permission_apply_record` | 2 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `home_alarm_graph_config` | 2 | `monitor-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `metadata_dorisstorage` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_kafkastorage` ⚠︎默认命名 | 2 | `monitor-web`（2 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_vmqueryclusterconfig` ⚠︎默认命名 | 2 | `kernel-api`（2 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `tapd_workspace_binding` | 2 | `fta-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `tapd_workspace_manual_unbind` | 2 | `fta-web`（2 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `action_instance_log` | 2 | `alarm-backends`（1 · import（bkmonitor））、`bkmonitor`（1 · models.Model（定义）） |
| `alarm_event_action` | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `alarm_notice_template` | 2 | `bkmonitor`（1 · models.Model（定义））、`fta-web`（1 · import（bkmonitor）） |
| `apm_ebpf_deepflowdashboardrecord` ⚠︎默认命名 | 2 | `apm-ebpf`（1 · models.Model（定义））、`monitor-web`（1 · import（apm_ebpf）） |
| `apm_web_uservisitrecord` ⚠︎默认命名 | 2 | `apm-web`（1 · models.Model（定义））、`monitor-web`（1 · import（apm_web）） |
| `app_snapshot_host_index` | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_alertconfig` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcsclusterlabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcscontainerlabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcsnodelabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcspodmonitorlabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcsservicelabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcsservicemonitorlabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `bkmonitor_bcsworkloadlabels` ⚠︎默认命名 | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `builtin_role` | 2 | `bk-dataview`（1 · models.Model（定义））、`monitor-web`（1 · import（bk_dataview）） |
| `folder` | 2 | `bk-dataview`（1 · models.Model（定义））、`monitor-web`（1 · import（bk_dataview）） |
| `fta_web_alertexperience` ⚠︎默认命名 | 2 | `fta-web`（1 · models.Model（定义））、`monitor-web`（1 · import（fta_web）） |
| `fta_web_alertsuggestion` ⚠︎默认命名 | 2 | `fta-web`（1 · models.Model（定义））、`monitor-web`（1 · import（fta_web）） |
| `fta_web_metricrecommendationfeedback` ⚠︎默认命名 | 2 | `fta-web`（1 · models.Model（定义））、`monitor-web`（1 · import（fta_web）） |
| `fta_web_searchfavorite` ⚠︎默认命名 | 2 | `fta-web`（1 · models.Model（定义））、`monitor-web`（1 · import（fta_web）） |
| `fta_web_searchhistory` ⚠︎默认命名 | 2 | `fta-web`（1 · models.Model（定义））、`monitor-web`（1 · import（fta_web）） |
| `metadata_bkappspacerecord` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_bkbaseresulttable` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_esfieldqueryaliasoption` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_essnapshot` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_essnapshotindice` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_influxdbhostinfo` ⚠︎默认命名 | 2 | `alarm-backends`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_recordrule` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_recordrulev4event` ⚠︎默认命名 | 2 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_recordrulev4resolved` ⚠︎默认命名 | 2 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_recordrulev4resolvedrecord` ⚠︎默认命名 | 2 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_recordrulev4spec` ⚠︎默认命名 | 2 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_recordrulev4specrecord` ⚠︎默认命名 | 2 | `kernel-api`（1 · import（metadata））、`metadata`（1 · models.Model（定义）） |
| `metadata_spacerelatedstorageinfo` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_spacestickyinfo` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_spacevminfo` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_timeseriesscope` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_vmresulttableconfig` | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metadata_vmshortlinkrecord` ⚠︎默认命名 | 2 | `metadata`（1 · models.Model（定义））、`monitor-web`（1 · import（metadata）） |
| `metric_mapping_config` | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `monitor_migration` | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `monitor_uploadedfile` ⚠︎默认命名 | 2 | `monitor`（1 · models.Model（定义））、`monitor-web`（1 · import（monitor）） |
| `monitor_uptimechecktaskcollectorlog` ⚠︎默认命名 | 2 | `monitor`（1 · models.Model（定义））、`monitor-web`（1 · import（monitor）） |
| `monitor_web_datatargetmapping` ⚠︎默认命名 | 2 | `bkmonitor`（1 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `monitor_web_deploymentconfigversion` ⚠︎默认命名 | 2 | `kernel-api`（1 · import（monitor_web））、`monitor-web`（1 · models.Model（定义）） |
| `preferences` | 2 | `bk-dataview`（1 · models.Model（定义））、`monitor-web`（1 · import（bk_dataview）） |
| `report_apply_record` | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `role` | 2 | `bk-dataview`（1 · models.Model（定义））、`monitor-web`（1 · import（bk_dataview）） |
| `token_access_record` | 2 | `bkmonitor`（1 · models.Model（定义））、`monitor-web`（1 · import（bkmonitor）） |
| `alarm_alert_collect` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `alarm_base_alarm_config` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `alarm_custom_event_group_config` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `alarm_detect_algorithm` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `alarm_event_stats` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `alarm_rt_dsl_config` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `alarm_rt_sql_config` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `apm_endpoint` ⚠︎默认命名 | 1 | `apm`（1 · models.Model（定义）） |
| `apm_fieldnormalizerconfig` ⚠︎默认命名 | 1 | `apm`（1 · models.Model（定义）） |
| `apm_rootendpoint` ⚠︎默认命名 | 1 | `apm`（1 · models.Model（定义）） |
| `apm_tracescopeindexset` ⚠︎默认命名 | 1 | `apm`（1 · models.Model（定义）） |
| `bk_weixin_user` | 1 | `core`（1 · models.Model（定义）） |
| `bkm_ipchooser_ipchooserconfig` ⚠︎默认命名 | 1 | `bkm-ipchooser`（1 · models.Model（定义）） |
| `bkmonitor_bcsingresslabels` ⚠︎默认命名 | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `duty_arrange_snap` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `duty_plan_send_record` | 1 | `bkmonitor`（1 · models.Model（定义）） |
| `fta_solutions_app_alarmapplication` | 1 | `fta-web`（1 · models.Model（定义）） |
| `fta_solutions_app_alarmdef` | 1 | `fta-web`（1 · models.Model（定义）） |
| `fta_solutions_app_alarmtype` | 1 | `fta-web`（1 · models.Model（定义）） |
| `fta_solutions_app_solution` | 1 | `fta-web`（1 · models.Model（定义）） |
| `fta_web_alertfeedback` ⚠︎默认命名 | 1 | `fta-web`（1 · models.Model（定义）） |
| `ja_alarm_converge_config` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_alarm_converge_def` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_alarm_notice_config` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_alarm_notice_group` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_alarm_solution_config` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_alarm_source` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_detect_algorithm_config` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_monitor` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_monitor_item` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `ja_monitor_item_group` | 1 | `monitor-api`（1 · models.Model（定义）） |
| `metadata_accessvmrecord` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_argusstorage` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_bkdatastorage` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_cmdblevelrecord` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_customreportsubscriptionconfig` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_datalink` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_datalinkresourceconfigbase` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_datasource` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_essnapshotrepository` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_essnapshotrestore` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_event` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_graphrelationbindingconfig` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_influxdbproxystorage` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_influxdbstorage` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_influxdbtaginfo` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_redisstorage` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_replaceconfig` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_resulttableflow` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_resulttablerecordformat` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_surrealdbstorage` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `metadata_timeseriestag` ⚠︎默认命名 | 1 | `metadata`（1 · models.Model（定义）） |
| `monitor_application` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_applicationgroupmembership` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_componentcategory` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_componentcategoryrelationship` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_componentimporttask` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_dashboardmenu` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_dashboardmenulocation` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_dashboardview` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_datacollector` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_datagenerateconfig` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_exporterdeposittask` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_globalconfig` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_hostproperty` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_hostpropertyconf` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_indexcolorconf` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_logcollectorhost` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_metricconf` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_metricmonitor` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_monitorhoststicky` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_monitorlocation` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_operaterecord` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_scenariomenu` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_serviceauthorization` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_shellcollectorconfig` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_shellcollectordeposittask` ⚠︎默认命名 | 1 | `monitor`（1 · models.Model（定义）） |
| `monitor_web_alertsolution` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_bcsareamodel` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_bcsclustermodel` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_bcsprojectmodel` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_collectorpluginconfig` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_collectorplugininfo` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_customeventitem` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_customtsfield` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_customtsgroupingrule` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_customtsitem` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_favoritegroup` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_importdetail` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_importhistory` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_importparse` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_operatorsystem` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_queryhistory` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_scenemodel` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_sceneviewordermodel` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_uploadedfileinfo` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `monitor_web_useraccessrecord` ⚠︎默认命名 | 1 | `monitor-web`（1 · models.Model（定义）） |
| `org_user` | 1 | `bk-dataview`（1 · models.Model（定义）） |
| `resource_data` | 1 | `drf-resource`（1 · models.Model（定义）） |
| `rum_rumappconfig` ⚠︎默认命名 | 1 | `rum`（1 · models.Model（定义）） |
| `rum_rumapplication` ⚠︎默认命名 | 1 | `rum`（1 · models.Model（定义）） |
| `rum_web_application` ⚠︎默认命名 | 1 | `rum-web`（1 · models.Model（定义）） |
| `team` | 1 | `bk-dataview`（1 · models.Model（定义）） |
| `team_member` | 1 | `bk-dataview`（1 · models.Model（定义）） |
| `team_role` | 1 | `bk-dataview`（1 · models.Model（定义）） |
| `user_role` | 1 | `bk-dataview`（1 · models.Model（定义）） |
