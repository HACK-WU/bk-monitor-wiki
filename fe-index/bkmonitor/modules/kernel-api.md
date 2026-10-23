# KernelAPIConfig（`kernel-api`）

> **职责**：内核 API 网关（v4）：统一 Resource/RPC 注册、鉴权与权限，216 个对外入口

> **职责**：内核 API 网关（v4）：统一 Resource/RPC 注册、鉴权与权限，216 个对外入口

- **位置**：`kernel_api/` · 归属文件 **198** 个 · 约 **52861** 行
- **定义**：`kernel_api/dbroutors.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **216** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bk_dataview`、`bkm_space`、`bkmonitor`、`calendars`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`monitor_api`、`monitor_web`、`query_api`
- **被依赖**（动它会影响）：`core.drf_resource`、`fta_web`、`query_api`

## 数据表（67）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `action_config` | ActionConfig | 4 | import（bkmonitor） | `kernel_api/resource/alert.py:21` |
| `action_instance` | ActionInstance | 1 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/assignment.py:116` |
| `action_plugin` | ActionPlugin | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:80` |
| `alarm_action` | Action | 2 | import（bkmonitor） | `kernel_api/unified_mcp/permissions.py:15` |
| `alarm_algorithm_v2` | AlgorithmModel | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `alarm_cachenode` | CacheNode | 2 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/cache_cost_snapshot.py:17` |
| `alarm_cacherouter` | CacheRouter | 5 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/strategy.py:291` |
| `alarm_detect_v2` | DetectModel | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `alarm_item_v2` | ItemModel | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `alarm_query_config_v2` | QueryConfigModel | 2 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `alarm_shield` | Shield | 1 | import（bkmonitor） | `kernel_api/resource/alert.py:21` |
| `alarm_strategy` | Strategy | 5 | import（bkmonitor） | `kernel_api/resource/alert.py:22` |
| `alarm_strategy_history` | StrategyHistoryModel | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `alarm_strategy_label` | StrategyLabel | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `alarm_strategy_v2` | StrategyModel | 9 | import（bkmonitor） | `kernel_api/resource/alert.py:21` |
| `api_auth_token` | ApiAuthToken | 5 | import（bkmonitor） | `kernel_api/middlewares/authentication.py:27` |
| `apm_apmapplication` ⚠︎默认命名 | ApmApplication | 1 | import（apm） | `kernel_api/rpc/functions/biz_scene.py:429` |
| `apm_datalink` ⚠︎默认命名 | DataLink | 4 | import（apm） | `kernel_api/rpc/functions/bkm_cli/db.py:99` |
| `apm_ebpf_deepflowworkload` ⚠︎默认命名 | DeepflowWorkload | 2 | import（apm_ebpf） | `kernel_api/resource/operation/handlers.py:179` |
| `apm_subscriptionconfig` ⚠︎默认命名 | SubscriptionConfig | 1 | import（apm） | `kernel_api/rpc/functions/admin/config_delivery.py:17` |
| `apm_web_application` ⚠︎默认命名 | Application | 5 | import（apm_web） | `kernel_api/resource/operation/handlers.py:137` |
| `as_code_import_history` | AsCodeImportTask | 1 | import（bkmonitor） | `kernel_api/rpc/functions/admin/ascode_import_task.py:13` |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | AlertAssignGroup | 2 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/assignment.py:197` |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | AlertAssignRule | 2 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/assignment.py:197` |
| `bkmonitor_issue_merge_relation` | IssueMergeRelation | 5 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/issue.py:174` |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | MetricListCache | 1 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/bcs_metadata.py:16` |
| `bkmonitor_reportitems` ⚠︎默认命名 | ReportItems | 1 | import（bkmonitor） | `kernel_api/views/v4/mail_report.py:27` |
| `bkmonitor_strategy_issue_config` | StrategyIssueConfig | 1 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:81` |
| `custom_report_subscription_config_v2` | CustomReportSubscription | 1 | import（metadata） | `kernel_api/rpc/functions/admin/config_delivery.py:40` |
| `dashboard` | Dashboard | 1 | import（bk_dataview） | `kernel_api/unified_mcp/permissions.py:193` |
| `data_source` | DataSource | 2 | import（bk_dataview） | `kernel_api/resource/metrics.py:23` |
| `duty_arrange` | DutyArrange | 3 | import（bkmonitor） | `kernel_api/resource/alert.py:1029` |
| `duty_rule` | DutyRule | 2 | import（bkmonitor） | `kernel_api/resource/alert.py:21` |
| `global_setting` | GlobalConfig | 4 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/double_check_strategy.py:8` |
| `metadata_bcsclusterinfo` ⚠︎默认命名 | BCSClusterInfo | 2 | import（metadata） | `kernel_api/resource/bcs.py:18` |
| `metadata_bcsfederalclusterinfo` ⚠︎默认命名 | BcsFederalClusterInfo | 1 | import（metadata） | `kernel_api/rpc/functions/bkm_cli/bcs_metadata.py:22` |
| `metadata_clusterconfig` ⚠︎默认命名 | ClusterConfig | 3 | import（metadata） | `kernel_api/rpc/functions/admin/cluster_info.py:875` |
| `metadata_clusterinfo` ⚠︎默认命名 | ClusterInfo | 2 | import（metadata） | `kernel_api/rpc/functions/bkm_cli/es.py:237` |
| `metadata_logsubscriptionconfig` ⚠︎默认命名 | LogSubscriptionConfig | 1 | import（metadata） | `kernel_api/rpc/functions/admin/config_delivery.py:40` |
| `metadata_pingserversubscriptionconfig` ⚠︎默认命名 | PingServerSubscriptionConfig | 1 | import（metadata） | `kernel_api/rpc/functions/admin/config_delivery.py:41` |
| `metadata_recordrulev4` ⚠︎默认命名 | RecordRuleV4 | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_recordrulev4event` ⚠︎默认命名 | RecordRuleV4Event | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_recordrulev4flow` ⚠︎默认命名 | RecordRuleV4Flow | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_recordrulev4resolved` ⚠︎默认命名 | RecordRuleV4Resolved | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_recordrulev4resolvedrecord` ⚠︎默认命名 | RecordRuleV4ResolvedRecord | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_recordrulev4spec` ⚠︎默认命名 | RecordRuleV4Spec | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_recordrulev4specrecord` ⚠︎默认命名 | RecordRuleV4SpecRecord | 1 | import（metadata） | `kernel_api/rpc/functions/admin/record_rule_v4.py:31` |
| `metadata_space` ⚠︎默认命名 | Space | 1 | import（metadata） | `kernel_api/rpc/functions/bkm_cli/bcs_metadata.py:24` |
| `metadata_spaceresource` ⚠︎默认命名 | SpaceResource | 1 | import（metadata） | `kernel_api/rpc/functions/bkm_cli/bcs_metadata.py:24` |
| `metadata_vmqueryclusterconfig` ⚠︎默认命名 | VmQueryClusterConfig | 2 | import（metadata） | `kernel_api/rpc/functions/admin/vm_query.py:14` |
| `monitor_uptimechecknode` ⚠︎默认命名 | UptimeCheckNode | 1 | import（monitor） | `kernel_api/rpc/functions/admin/uptime_check.py:16` |
| `monitor_uptimechecktask` ⚠︎默认命名 | UptimeCheckTask | 1 | import（monitor） | `kernel_api/rpc/functions/biz_scene.py:713` |
| `monitor_uptimechecktasksubscription` ⚠︎默认命名 | UptimeCheckTaskSubscription | 1 | import（monitor） | `kernel_api/rpc/functions/admin/uptime_check.py:16` |
| `monitor_web_collectconfigmeta` ⚠︎默认命名 | CollectConfigMeta | 3 | import（monitor_web） | `kernel_api/rpc/functions/biz_scene.py:483` |
| `monitor_web_collectorpluginmeta` ⚠︎默认命名 | CollectorPluginMeta | 3 | import（monitor_web） | `kernel_api/rpc/functions/biz_scene.py:483` |
| `monitor_web_customeventgroup` ⚠︎默认命名 | CustomEventGroup | 2 | import（monitor_web） | `kernel_api/rpc/functions/biz_scene.py:483` |
| `monitor_web_customtstable` ⚠︎默认命名 | CustomTSTable | 2 | import（monitor_web） | `kernel_api/resource/operation/handlers.py:117` |
| `monitor_web_deploymentconfigversion` ⚠︎默认命名 | DeploymentConfigVersion | 1 | import（monitor_web） | `kernel_api/rpc/functions/admin/collect_config.py:38` |
| `monitor_web_pluginversionhistory` ⚠︎默认命名 | PluginVersionHistory | 3 | import（monitor_web） | `kernel_api/rpc/functions/biz_scene.py:508` |
| `org` | Org | 2 | import（bk_dataview） | `kernel_api/rpc/functions/bkm_cli/platform_catalog/grafana.py:12` |
| `permission` | Permission | 3 | import（bk_dataview） | `kernel_api/unified_mcp/permissions.py:300` |
| `render_image_task` | RenderImageTask | 2 | import（bkmonitor） | `kernel_api/rpc/functions/admin/render_image_task.py:17` |
| `report` | Report | 2 | import（bkmonitor） | `kernel_api/rpc/functions/bkm_cli/db.py:1168` |
| `report_channel` | ReportChannel | 1 | import（bkmonitor） | `kernel_api/views/v4/new_report.py:13` |
| `strategy_action_relation` | StrategyActionConfigRelation | 3 | import（bkmonitor） | `kernel_api/rpc/tests/run_strategy_adapter_tests.py:67` |
| `user` | User | 2 | import（bk_dataview） | `kernel_api/middlewares/authentication.py:19` |
| `user_group` | UserGroup | 7 | import（bkmonitor） | `kernel_api/resource/alert.py:21` |

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/issue专家`（命中标识 `kernel_api`）
- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `kernel_api`）
- `/root/bk-monitor/.module-experts/告警屏蔽专家`（命中标识 `kernel_api`）
- `/root/bk-monitor/.module-experts/告警查询专家`（命中标识 `kernel_api`）

## 归属文件（198）

- `kernel_api/dbroutors.py`
- `kernel_api/exceptions.py`
- `kernel_api/__init__.py`
- `kernel_api/adapters.py`
- `kernel_api/urls.py`
- `kernel_api/apps.py`
- `kernel_api/extend_resource/__init__.py`
- `kernel_api/extend_utils/__init__.py`
- `kernel_api/extend_views/__init__.py`
- `kernel_api/management/__init__.py`
- `kernel_api/management/commands/__init__.py`
- `kernel_api/management/commands/check_apis.py`
- `kernel_api/middlewares/authentication.py`
- `kernel_api/middlewares/__init__.py`
- `kernel_api/middlewares/exception_handler.py`
- `kernel_api/models/__init__.py`
- `kernel_api/resource/unified_mcp.py`
- `kernel_api/resource/log_collection_clean_config.py`
- `kernel_api/resource/strategy.py`
- `kernel_api/resource/apm.py`
- `kernel_api/resource/uptimecheck.py`
- `kernel_api/resource/k8s_resource.py`
- `kernel_api/resource/utils.py`
- `kernel_api/resource/log_collection_special_create.py`
- `kernel_api/resource/log_collection_common.py`
- `kernel_api/resource/relation.py`
- `kernel_api/resource/bcs.py`
- `kernel_api/resource/log_extract.py`
- `kernel_api/resource/alert.py`
- `kernel_api/resource/log_collection_special_update.py`
- `kernel_api/resource/shield.py`
- `kernel_api/resource/collecting.py`
- `kernel_api/resource/__init__.py`
- `kernel_api/resource/log_collection_create.py`
- `kernel_api/resource/query.py`
- `kernel_api/resource/log_collection.py`
- `kernel_api/resource/action.py`
- `kernel_api/resource/log_collection_update.py`
- `kernel_api/resource/qos.py`
- `kernel_api/resource/event.py`
- ……其余 20 个见 JSON 输出（完整清单）
