# MetaDataAppConfig（`metadata`）

> **职责**：元数据管理：数据源/结果表/存储/空间/BCS 集群元信息，数据链路的事实来源

> **职责**：元数据管理：数据源/结果表/存储/空间/BCS 集群元信息，数据链路的事实来源

- **位置**：`metadata/` · 归属文件 **218** 个 · 约 **85110** 行
- **定义**：`metadata/health_check.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`apm`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`monitor_web`
- **被依赖**（动它会影响）：`alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bkmonitor`、`kernel_api`、`monitor_web`、`query_api`、`rum`

## 数据表（71）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `alarm_query_config_v2` | QueryConfigModel | 1 | import（bkmonitor） | `metadata/task/custom_report.py:24` |
| `apm_apmapplication` ⚠︎默认命名 | ApmApplication | 1 | import（apm） | `metadata/health_check.py:32` |
| `apm_datalink` ⚠︎默认命名 | DataLink | 9 | import（apm） | `metadata/health_check.py:45` |
| `custom_report_subscription_config_v2` | CustomReportSubscription | 1 | models.Model（定义） | `metadata/models/custom_report/subscription_config.py:58` |
| `data_source` | DataSource | 36 | import（bk_dataview） | `metadata/health_check.py:38` |
| `global_setting` | GlobalConfig | 1 | import（bkmonitor） | `metadata/management/commands/deploy_official_plugin.py:13` |
| `metadata_accessvmrecord` ⚠︎默认命名 | AccessVMRecord | 1 | models.Model（定义） | `metadata/models/vm/record.py:24` |
| `metadata_argusstorage` ⚠︎默认命名 | ArgusStorage | 1 | models.Model（定义） | `metadata/models/storage.py:6023` |
| `metadata_bcsclusterinfo` ⚠︎默认命名 | BCSClusterInfo | 1 | models.Model（定义） | `metadata/models/bcs/cluster.py:24` |
| `metadata_bcsfederalclusterinfo` ⚠︎默认命名 | BcsFederalClusterInfo | 1 | models.Model（定义） | `metadata/models/bcs/cluster.py:621` |
| `metadata_bkappspacerecord` ⚠︎默认命名 | BkAppSpaceRecord | 1 | models.Model（定义） | `metadata/models/space/space.py:180` |
| `metadata_bkbaseresulttable` ⚠︎默认命名 | BkBaseResultTable | 1 | models.Model（定义） | `metadata/models/bkdata/result_table.py:21` |
| `metadata_bkdatastorage` ⚠︎默认命名 | BkDataStorage | 1 | models.Model（定义） | `metadata/models/storage.py:5513` |
| `metadata_clusterconfig` ⚠︎默认命名 | ClusterConfig | 1 | models.Model（定义） | `metadata/models/data_link/data_link_configs.py:1348` |
| `metadata_clusterinfo` ⚠︎默认命名 | ClusterInfo | 1 | models.Model（定义） | `metadata/models/storage.py:99` |
| `metadata_cmdblevelrecord` ⚠︎默认命名 | CMDBLevelRecord | 1 | models.Model（定义） | `metadata/models/result_table.py:2945` |
| `metadata_customreportsubscriptionconfig` ⚠︎默认命名 | CustomReportSubscriptionConfig | 1 | models.Model（定义） | `metadata/models/custom_report/subscription_config.py:45` |
| `metadata_datalink` ⚠︎默认命名 | DataLink | 1 | models.Model（定义） | `metadata/models/data_link/data_link.py:435` |
| `metadata_datalinkresourceconfigbase` ⚠︎默认命名 | DataLinkResourceConfigBase | 1 | models.Model（定义） | `metadata/models/data_link/data_link_configs.py:45` |
| `metadata_datasource` ⚠︎默认命名 | DataSource | 1 | models.Model（定义） | `metadata/models/data_source.py:66` |
| `metadata_datasourceresulttable` ⚠︎默认命名 | DataSourceResultTable | 1 | models.Model（定义） | `metadata/models/data_source.py:1438` |
| `metadata_dorisstorage` ⚠︎默认命名 | DorisStorage | 1 | models.Model（定义） | `metadata/models/storage.py:6295` |
| `metadata_esfieldqueryaliasoption` ⚠︎默认命名 | ESFieldQueryAliasOption | 1 | models.Model（定义） | `metadata/models/result_table.py:3628` |
| `metadata_essnapshot` ⚠︎默认命名 | EsSnapshot | 1 | models.Model（定义） | `metadata/models/es_snapshot.py:48` |
| `metadata_essnapshotindice` ⚠︎默认命名 | EsSnapshotIndice | 1 | models.Model（定义） | `metadata/models/es_snapshot.py:662` |
| `metadata_essnapshotrepository` ⚠︎默认命名 | EsSnapshotRepository | 1 | models.Model（定义） | `metadata/models/es_snapshot.py:561` |
| `metadata_essnapshotrestore` ⚠︎默认命名 | EsSnapshotRestore | 1 | models.Model（定义） | `metadata/models/es_snapshot.py:724` |
| `metadata_esstorage` ⚠︎默认命名 | ESStorage | 1 | models.Model（定义） | `metadata/models/storage.py:2591` |
| `metadata_event` ⚠︎默认命名 | Event | 1 | models.Model（定义） | `metadata/models/custom_report/event.py:387` |
| `metadata_graphrelationbindingconfig` ⚠︎默认命名 | GraphRelationBindingConfig | 1 | models.Model（定义） | `metadata/models/data_link/data_link_configs.py:642` |
| `metadata_influxdbclusterinfo` ⚠︎默认命名 | InfluxDBClusterInfo | 1 | models.Model（定义） | `metadata/models/influxdb_cluster.py:347` |
| `metadata_influxdbhostinfo` ⚠︎默认命名 | InfluxDBHostInfo | 1 | models.Model（定义） | `metadata/models/influxdb_cluster.py:478` |
| `metadata_influxdbproxystorage` ⚠︎默认命名 | InfluxDBProxyStorage | 1 | models.Model（定义） | `metadata/models/influxdb_cluster.py:800` |
| `metadata_influxdbstorage` ⚠︎默认命名 | InfluxDBStorage | 1 | models.Model（定义） | `metadata/models/storage.py:1532` |
| `metadata_influxdbtaginfo` ⚠︎默认命名 | InfluxDBTagInfo | 1 | models.Model（定义） | `metadata/models/influxdb_cluster.py:74` |
| `metadata_kafkastorage` ⚠︎默认命名 | KafkaStorage | 1 | models.Model（定义） | `metadata/models/storage.py:2457` |
| `metadata_kafkatopicinfo` ⚠︎默认命名 | KafkaTopicInfo | 1 | models.Model（定义） | `metadata/models/storage.py:1397` |
| `metadata_label` ⚠︎默认命名 | Label | 1 | models.Model（定义） | `metadata/models/common.py:19` |
| `metadata_logsubscriptionconfig` ⚠︎默认命名 | LogSubscriptionConfig | 1 | models.Model（定义） | `metadata/models/custom_report/subscription_config.py:718` |
| `metadata_pingserversubscriptionconfig` ⚠︎默认命名 | PingServerSubscriptionConfig | 1 | models.Model（定义） | `metadata/models/ping_server.py:33` |
| `metadata_recordrule` ⚠︎默认命名 | RecordRule | 1 | models.Model（定义） | `metadata/models/record_rule/rules.py:39` |
| `metadata_recordrulev4` ⚠︎默认命名 | RecordRuleV4 | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:314` |
| `metadata_recordrulev4event` ⚠︎默认命名 | RecordRuleV4Event | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:1138` |
| `metadata_recordrulev4flow` ⚠︎默认命名 | RecordRuleV4Flow | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:936` |
| `metadata_recordrulev4resolved` ⚠︎默认命名 | RecordRuleV4Resolved | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:867` |
| `metadata_recordrulev4resolvedrecord` ⚠︎默认命名 | RecordRuleV4ResolvedRecord | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:905` |
| `metadata_recordrulev4spec` ⚠︎默认命名 | RecordRuleV4Spec | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:786` |
| `metadata_recordrulev4specrecord` ⚠︎默认命名 | RecordRuleV4SpecRecord | 1 | models.Model（定义） | `metadata/models/record_rule/v4/models.py:825` |
| `metadata_redisstorage` ⚠︎默认命名 | RedisStorage | 1 | models.Model（定义） | `metadata/models/storage.py:2340` |
| `metadata_replaceconfig` ⚠︎默认命名 | ReplaceConfig | 1 | models.Model（定义） | `metadata/models/bcs/replace.py:10` |
| `metadata_resulttable` ⚠︎默认命名 | ResultTable | 1 | models.Model（定义） | `metadata/models/result_table.py:59` |
| `metadata_resulttablefield` ⚠︎默认命名 | ResultTableField | 1 | models.Model（定义） | `metadata/models/result_table.py:2098` |
| `metadata_resulttableflow` ⚠︎默认命名 | ResultTableFlow | 1 | models.Model（定义） | `metadata/models/record_rule/rules.py:196` |
| `metadata_resulttablerecordformat` ⚠︎默认命名 | ResultTableRecordFormat | 1 | models.Model（定义） | `metadata/models/result_table.py:2858` |
| `metadata_space` ⚠︎默认命名 | Space | 1 | models.Model（定义） | `metadata/models/space/space.py:39` |
| `metadata_spacedatasource` ⚠︎默认命名 | SpaceDataSource | 1 | models.Model（定义） | `metadata/models/space/space.py:130` |
| `metadata_spacerelatedstorageinfo` ⚠︎默认命名 | SpaceRelatedStorageInfo | 1 | models.Model（定义） | `metadata/models/storage.py:6277` |
| `metadata_spaceresource` ⚠︎默认命名 | SpaceResource | 1 | models.Model（定义） | `metadata/models/space/space.py:145` |
| `metadata_spacestickyinfo` ⚠︎默认命名 | SpaceStickyInfo | 1 | models.Model（定义） | `metadata/models/space/space.py:171` |
| `metadata_spacetype` ⚠︎默认命名 | SpaceType | 1 | models.Model（定义） | `metadata/models/space/space.py:18` |
| `metadata_spacevminfo` ⚠︎默认命名 | SpaceVMInfo | 1 | models.Model（定义） | `metadata/models/vm/record.py:110` |
| `metadata_storageclusterrecord` ⚠︎默认命名 | StorageClusterRecord | 1 | models.Model（定义） | `metadata/models/storage.py:6103` |
| `metadata_surrealdbstorage` ⚠︎默认命名 | SurrealDBStorage | 1 | models.Model（定义） | `metadata/models/storage.py:6984` |
| `metadata_timeseriesmetric` ⚠︎默认命名 | TimeSeriesMetric | 1 | models.Model（定义） | `metadata/models/custom_report/time_series.py:1861` |
| `metadata_timeseriesscope` ⚠︎默认命名 | TimeSeriesScope | 1 | models.Model（定义） | `metadata/models/custom_report/time_series.py:1205` |
| `metadata_timeseriestag` ⚠︎默认命名 | TimeSeriesTag | 1 | models.Model（定义） | `metadata/models/custom_report/time_series.py:2798` |
| `metadata_vmqueryclusterconfig` ⚠︎默认命名 | VmQueryClusterConfig | 1 | models.Model（定义） | `metadata/models/data_link/vm_query_cluster.py:10` |
| `metadata_vmresulttableconfig` | ResultTableConfig | 1 | models.Model（定义） | `metadata/models/data_link/data_link_configs.py:308` |
| `metadata_vmshortlinkrecord` ⚠︎默认命名 | VMShortLinkRecord | 1 | models.Model（定义） | `metadata/models/vm/short_link.py:19` |
| `monitor_web_collectorpluginmeta` ⚠︎默认命名 | CollectorPluginMeta | 1 | import（monitor_web） | `metadata/service/data_source.py:116` |
| `monitor_web_customeventgroup` ⚠︎默认命名 | CustomEventGroup | 1 | import（monitor_web） | `metadata/health_check.py:683` |

## 非 HTTP 入口

- **定时任务**：33 处
- **信号接收**：3 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `metadata`）
- `/root/bk-monitor/.module-experts/数据源查询构造专家`（命中标识 `metadata`）


**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/元数据管理专题`

**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/元数据管理专题`
## 专家资产（深挖读这些）

**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/元数据管理专题`


**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/元数据管理专题`
## 专家资产（深挖读这些）

**人工指认**（机械匹配未命中）：`/root/bk-monitor/.module-experts/元数据管理专题`

## 归属文件（218）

- `metadata/health_check.py`
- `metadata/views.py`
- `metadata/__init__.py`
- `metadata/admin.py`
- `metadata/apps.py`
- `metadata/config.py`
- `metadata/signals.py`
- `metadata/migration_util.py`
- `metadata/agents/__init__.py`
- `metadata/agents/diagnostic/__init__.py`
- `metadata/agents/diagnostic/metadata_diagnostic_agent.py`
- `metadata/management/__init__.py`
- `metadata/management/commands/migrate_nano_log.py`
- `metadata/management/commands/delete_spec_gse_router.py`
- `metadata/management/commands/sync_bklog_es_router.py`
- `metadata/management/commands/check_bcs_cluster_status.py`
- `metadata/management/commands/check_realtime_strategy_kafka_storage.py`
- `metadata/management/commands/query_data_id_by_mq.py`
- `metadata/management/commands/update_bcs_replace_config.py`
- `metadata/management/commands/switch_vm_cluster.py`
- `metadata/management/commands/add_bkci_metrics_and_dimensions.py`
- `metadata/management/commands/check_ts_metrics.py`
- `metadata/management/commands/sync_cluster_config.py`
- `metadata/management/commands/query_disabled_data_id.py`
- `metadata/management/commands/add_bkci_system_dimensions.py`
- `metadata/management/commands/query_storage.py`
- `metadata/management/commands/clean_old_consul_config.py`
- `metadata/management/commands/clean_disabled_config_in_global_k8s_cluster.py`
- `metadata/management/commands/deploy_proxy_and_collector_plugin.py`
- `metadata/management/commands/access_bkdata_vm.py`
- `metadata/management/commands/add_extend_dimensions.py`
- `metadata/management/commands/refresh_ts_metric.py`
- `metadata/management/commands/update_bcs_cluster_cloud_id_config.py`
- `metadata/management/commands/query_space.py`
- `metadata/management/commands/query_es_index.py`
- `metadata/management/commands/init_influxdb_proxy_storage.py`
- `metadata/management/commands/move_last_day_write_alias.py`
- `metadata/management/commands/check_bkbase_cluster.py`
- `metadata/management/commands/access_bkdata_prom_compute_datasource.py`
- `metadata/management/commands/fix_esstorage_origin_table_options.py`
- ……其余 20 个见 JSON 输出（完整清单）
