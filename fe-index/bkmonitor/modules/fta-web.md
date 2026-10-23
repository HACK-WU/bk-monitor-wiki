# FtaWebConfig（`fta-web`）

> **职责**：告警处理/故障自愈 Web 层：事件中心、动作、分派、Issue

> **职责**：告警处理/故障自愈 Web 层：事件中心、动作、分派、Issue

- **位置**：`packages/fta_web/` · 归属文件 **71** 个 · 约 **25059** 行
- **定义**：`packages/fta_web/tasks.py:1`（django）
- **挂载前缀**：`/action`、`/alert`、`/alert/v2` 等 8 个 · 视图/接口入口 **27** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`apm_web`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`kernel_api`、`monitor`、`monitor_web`
- **被依赖**（动它会影响）：`apm_web`、`bkmonitor`、`kernel_api`、`monitor_web`

## 数据表（39）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `action_config` | ActionConfig | 7 | import（bkmonitor） | `packages/fta_web/tasks.py:19` |
| `action_instance` | ActionInstance | 5 | import（bkmonitor） | `packages/fta_web/action/tasks.py:17` |
| `action_plugin` | ActionPlugin | 8 | import（bkmonitor） | `packages/fta_web/tasks.py:19` |
| `alarm_action` | Action | 1 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `alarm_action_notice_group_mapping` | ActionNoticeMapping | 1 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `alarm_algorithm_v2` | AlgorithmModel | 1 | import（bkmonitor） | `packages/fta_web/alert/resources.py:54` |
| `alarm_item_v2` | ItemModel | 2 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `alarm_notice_group` | NoticeGroup | 1 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `alarm_notice_template` | NoticeTemplate | 1 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `alarm_query_config_v2` | QueryConfigModel | 1 | import（bkmonitor） | `packages/fta_web/issue/resources.py:38` |
| `alarm_shield` | Shield | 1 | import（bkmonitor） | `packages/fta_web/alert/handlers/alert.py:29` |
| `alarm_strategy` | Strategy | 1 | import（bkmonitor） | `packages/fta_web/action/resources/backend_resources.py:363` |
| `alarm_strategy_v2` | StrategyModel | 3 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | AlertAssignGroup | 4 | import（bkmonitor） | `packages/fta_web/tasks.py:19` |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | AlertAssignRule | 3 | import（bkmonitor） | `packages/fta_web/tasks.py:19` |
| `bkmonitor_eventplugin` ⚠︎默认命名 | EventPlugin | 1 | import（bkmonitor） | `packages/fta_web/event_plugin/resources.py:35` |
| `bkmonitor_issue_merge_relation` | IssueMergeRelation | 1 | import（bkmonitor） | `packages/fta_web/issue/resources.py:39` |
| `bkmonitor_issue_tapd_relation` | IssueTapdRelation | 3 | import（bkmonitor） | `packages/fta_web/tasks.py:20` |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | MetricListCache | 3 | import（bkmonitor） | `packages/fta_web/alert/resources.py:54` |
| `converge_relation` | ConvergeRelation | 2 | import（bkmonitor） | `packages/fta_web/alert/handlers/alert.py:29` |
| `event_plugin` | EventPluginV2 | 5 | import（bkmonitor） | `packages/fta_web/handlers.py:18` |
| `event_plugin_instance` | EventPluginInstance | 2 | import（bkmonitor） | `packages/fta_web/handlers.py:18` |
| `fta_solutions_app_alarmapplication` | AlarmApplication | 1 | models.Model（定义） | `packages/fta_web/models/old_fta.py:7` |
| `fta_solutions_app_alarmdef` | AlarmDef | 1 | models.Model（定义） | `packages/fta_web/models/old_fta.py:83` |
| `fta_solutions_app_alarmtype` | AlarmType | 1 | models.Model（定义） | `packages/fta_web/models/old_fta.py:32` |
| `fta_solutions_app_solution` | Solution | 1 | models.Model（定义） | `packages/fta_web/models/old_fta.py:60` |
| `fta_web_alertexperience` ⚠︎默认命名 | AlertExperience | 1 | models.Model（定义） | `packages/fta_web/models/alert.py:102` |
| `fta_web_alertfeedback` ⚠︎默认命名 | AlertFeedback | 1 | models.Model（定义） | `packages/fta_web/models/alert.py:164` |
| `fta_web_alertsuggestion` ⚠︎默认命名 | AlertSuggestion | 1 | models.Model（定义） | `packages/fta_web/models/alert.py:118` |
| `fta_web_metricrecommendationfeedback` ⚠︎默认命名 | MetricRecommendationFeedback | 1 | models.Model（定义） | `packages/fta_web/models/alert.py:178` |
| `fta_web_searchfavorite` ⚠︎默认命名 | SearchFavorite | 1 | models.Model（定义） | `packages/fta_web/models/alert.py:86` |
| `fta_web_searchhistory` ⚠︎默认命名 | SearchHistory | 1 | models.Model（定义） | `packages/fta_web/models/alert.py:41` |
| `global_setting` | GlobalConfig | 3 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `monitor_userconfig` ⚠︎默认命名 | UserConfig | 1 | import（monitor） | `packages/fta_web/home/resources.py:20` |
| `monitor_web_customeventgroup` ⚠︎默认命名 | CustomEventGroup | 1 | import（monitor_web） | `packages/fta_web/alert/resources.py:132` |
| `permission` | Permission | 4 | import（bk_dataview） | `packages/fta_web/action/resources/backend_resources.py:35` |
| `strategy_action_relation` | StrategyActionConfigRelation | 2 | import（bkmonitor） | `packages/fta_web/handlers.py:86` |
| `tapd_workspace_binding` | TapdWorkspaceBinding | 2 | import（bkmonitor） | `packages/fta_web/issue/resources.py:38` |
| `tapd_workspace_manual_unbind` | TapdWorkspaceManualUnbind | 2 | import（bkmonitor） | `packages/fta_web/issue/resources.py:38` |

## 非 HTTP 入口

- **定时任务**：5 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/issue专家`（命中标识 `fta_web`）
- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `fta_web`）
- `/root/bk-monitor/.module-experts/告警屏蔽专家`（命中标识 `fta_web`）
- `/root/bk-monitor/.module-experts/告警查询专家`（命中标识 `fta_web`）

## 归属文件（71）

- `packages/fta_web/tasks.py`
- `packages/fta_web/views.py`
- `packages/fta_web/handlers.py`
- `packages/fta_web/__init__.py`
- `packages/fta_web/urls.py`
- `packages/fta_web/constants.py`
- `packages/fta_web/apps.py`
- `packages/fta_web/action/constant.py`
- `packages/fta_web/action/utils.py`
- `packages/fta_web/action/tasks.py`
- `packages/fta_web/action/views.py`
- `packages/fta_web/action/__init__.py`
- `packages/fta_web/action/urls.py`
- `packages/fta_web/action/resources/backend_resources.py`
- `packages/fta_web/action/resources/__init__.py`
- `packages/fta_web/action/resources/frontend_resources.py`
- `packages/fta_web/alert/utils.py`
- `packages/fta_web/alert/views.py`
- `packages/fta_web/alert/__init__.py`
- `packages/fta_web/alert/serializers.py`
- `packages/fta_web/alert/urls.py`
- `packages/fta_web/alert/resources.py`
- `packages/fta_web/alert/handlers/fulltext.py`
- `packages/fta_web/alert/handlers/alert_log.py`
- `packages/fta_web/alert/handlers/incident.py`
- `packages/fta_web/alert/handlers/alert.py`
- `packages/fta_web/alert/handlers/__init__.py`
- `packages/fta_web/alert/handlers/action.py`
- `packages/fta_web/alert/handlers/event.py`
- `packages/fta_web/alert/handlers/base.py`
- `packages/fta_web/alert/handlers/translator.py`
- `packages/fta_web/alert_v2/views.py`
- `packages/fta_web/alert_v2/__init__.py`
- `packages/fta_web/alert_v2/urls.py`
- `packages/fta_web/alert_v2/resources.py`
- `packages/fta_web/alert_v2/target.py`
- `packages/fta_web/assign/utils.py`
- `packages/fta_web/assign/views.py`
- `packages/fta_web/assign/__init__.py`
- `packages/fta_web/assign/urls.py`
- ……其余 20 个见 JSON 输出（完整清单）
