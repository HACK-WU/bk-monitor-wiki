# ApmWebConfig（`apm-web`）

> **职责**：APM Web 资源层：应用/服务/容器/Profiling 页面后端（含 profile 子模块）

> **职责**：APM Web 资源层：应用/服务/容器/Profiling 页面后端（含 profile 子模块）

- **位置**：`packages/apm_web/` · 归属文件 **210** 个 · 约 **47230** 行
- **定义**：`packages/apm_web/icon.py:1`（django）
- **挂载前缀**：`/apm`、`/apm_log_forward`、`/container` 等 15 个 · 视图/接口入口 **29** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`apm`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`monitor_web`
- **被依赖**（动它会影响）：`ai_whale`、`apm`、`bkmonitor`、`fta_web`、`kernel_api`、`monitor_web`、`profile`

## 数据表（18）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `alarm_algorithm_v2` | AlgorithmModel | 1 | import（bkmonitor） | `packages/apm_web/strategy/constants.py:15` |
| `apm_web_apmmetaconfig` ⚠︎默认命名 | ApmMetaConfig | 1 | models.Model（定义） | `packages/apm_web/models/application.py:1080` |
| `apm_web_application` ⚠︎默认命名 | Application | 1 | models.Model（定义） | `packages/apm_web/models/application.py:66` |
| `apm_web_applicationcustomservice` ⚠︎默认命名 | ApplicationCustomService | 1 | models.Model（定义） | `packages/apm_web/models/application.py:1158` |
| `apm_web_applicationrelationinfo` ⚠︎默认命名 | ApplicationRelationInfo | 1 | models.Model（定义） | `packages/apm_web/models/application.py:1059` |
| `apm_web_profileuploadrecord` ⚠︎默认命名 | ProfileUploadRecord | 1 | models.Model（定义） | `packages/apm_web/models/profile.py:26` |
| `apm_web_strategyinstance` ⚠︎默认命名 | StrategyInstance | 1 | models.Model（定义） | `packages/apm_web/models/strategy.py:77` |
| `apm_web_strategytemplate` ⚠︎默认命名 | StrategyTemplate | 1 | models.Model（定义） | `packages/apm_web/models/strategy.py:26` |
| `apm_web_tracecomparison` ⚠︎默认命名 | TraceComparison | 1 | models.Model（定义） | `packages/apm_web/models/trace.py:47` |
| `apm_web_uservisitrecord` ⚠︎默认命名 | UserVisitRecord | 1 | models.Model（定义） | `packages/apm_web/models/visit_record.py:14` |
| `bkmonitor_querytemplate` ⚠︎默认命名 | QueryTemplate | 1 | import（bkmonitor） | `packages/apm_web/service/resources.py:54` |
| `bkmonitor_statisticsmetric` ⚠︎默认命名 | StatisticsMetric | 2 | import（bkmonitor） | `packages/apm_web/metric/resources.py:56` |
| `global_setting` | GlobalConfig | 1 | import（bkmonitor） | `packages/apm_web/tasks.py:34` |
| `metadata_resulttablefield` ⚠︎默认命名 | ResultTableField | 1 | import（metadata） | `packages/apm_web/meta/resources.py:144` |
| `monitor_applicationconfig` ⚠︎默认命名 | ApplicationConfig | 1 | import（monitor） | `packages/apm_web/meta/resources.py:146` |
| `monitor_web_sceneviewmodel` ⚠︎默认命名 | SceneViewModel | 3 | import（monitor_web） | `packages/apm_web/metric/handler/statistics.py:37` |
| `permission` | Permission | 1 | import（bk_dataview） | `packages/apm_web/models/application.py:50` |
| `user_group` | UserGroup | 5 | import（bkmonitor） | `packages/apm_web/tasks.py:108` |

## 非 HTTP 入口

- **定时任务**：12 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/UnifyQuery查询专家`（命中标识 `apm_web`）
- `/root/bk-monitor/.module-experts/场景视图专家`（命中标识 `apm_web`）

## 归属文件（210）

- `packages/apm_web/icon.py`
- `packages/apm_web/metric_handler.py`
- `packages/apm_web/utils.py`
- `packages/apm_web/tasks.py`
- `packages/apm_web/views.py`
- `packages/apm_web/calculation.py`
- `packages/apm_web/__init__.py`
- `packages/apm_web/admin.py`
- `packages/apm_web/serializers.py`
- `packages/apm_web/urls.py`
- `packages/apm_web/constants.py`
- `packages/apm_web/resources.py`
- `packages/apm_web/metrics.py`
- `packages/apm_web/apps.py`
- `packages/apm_web/decorators.py`
- `packages/apm_web/signals.py`
- `packages/apm_web/container/helpers.py`
- `packages/apm_web/container/views.py`
- `packages/apm_web/container/__init__.py`
- `packages/apm_web/container/urls.py`
- `packages/apm_web/container/resources.py`
- `packages/apm_web/custom_metric/views.py`
- `packages/apm_web/custom_metric/__init__.py`
- `packages/apm_web/custom_metric/serializers.py`
- `packages/apm_web/custom_metric/urls.py`
- `packages/apm_web/custom_metric/resources.py`
- `packages/apm_web/db/db_utils.py`
- `packages/apm_web/db/views.py`
- `packages/apm_web/db/__init__.py`
- `packages/apm_web/db/urls.py`
- `packages/apm_web/db/resources.py`
- `packages/apm_web/db/handler/__init__.py`
- `packages/apm_web/event/handler.py`
- `packages/apm_web/event/views.py`
- `packages/apm_web/event/__init__.py`
- `packages/apm_web/event/serializers.py`
- `packages/apm_web/event/urls.py`
- `packages/apm_web/event/resources.py`
- `packages/apm_web/handlers/endpoint_handler.py`
- `packages/apm_web/handlers/task_handler.py`
- ……其余 20 个见 JSON 输出（完整清单）
