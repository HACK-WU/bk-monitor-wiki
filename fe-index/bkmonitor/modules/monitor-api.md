# MonitorAPIConfig（`monitor-api`）

> **职责**：监控对外 API v1（packages/monitor_api）：`/rest/v1` 接口层

> **职责**：监控对外 API v1（packages/monitor_api）：`/rest/v1` 接口层

- **位置**：`packages/monitor_api/` · 归属文件 **12** 个 · 约 **1246** 行
- **定义**：`packages/monitor_api/views.py:1`（django）
- **挂载前缀**：`/rest/v1` · 视图/接口入口 **3** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkmonitor`、`core.drf_resource`、`monitor`
- **被依赖**（动它会影响）：`kernel_api`

## 数据表（12）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `dict_base_alarm` | BaseAlarm | 1 | import（bkmonitor） | `packages/monitor_api/views.py:25` |
| `global_setting` | GlobalConfig | 1 | import（bkmonitor） | `packages/monitor_api/apps.py:27` |
| `ja_alarm_converge_config` | ConvergeConfig | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:541` |
| `ja_alarm_converge_def` | AlarmCollectDef | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:559` |
| `ja_alarm_notice_config` | NoticeConfig | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:583` |
| `ja_alarm_notice_group` | NoticeGroup | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:600` |
| `ja_alarm_solution_config` | SolutionConfig | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:522` |
| `ja_alarm_source` | AlarmSource | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:345` |
| `ja_detect_algorithm_config` | DetectAlgorithmConfig | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:412` |
| `ja_monitor` | MonitorSource | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:194` |
| `ja_monitor_item` | MonitorItem | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:296` |
| `ja_monitor_item_group` | MonitorItemGroup | 1 | models.Model（定义） | `packages/monitor_api/models/base.py:284` |

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `monitor_api`）

## 归属文件（12）

- `packages/monitor_api/views.py`
- `packages/monitor_api/middlewares.py`
- `packages/monitor_api/exceptions.py`
- `packages/monitor_api/__init__.py`
- `packages/monitor_api/admin.py`
- `packages/monitor_api/serializers.py`
- `packages/monitor_api/urls.py`
- `packages/monitor_api/filtersets.py`
- `packages/monitor_api/pagination.py`
- `packages/monitor_api/apps.py`
- `packages/monitor_api/models/__init__.py`
- `packages/monitor_api/models/base.py`
