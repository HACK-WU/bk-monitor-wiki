# MonitorConfig（`monitor`）

> **职责**：监控数据模型层（packages/monitor）：采集、拨测、自定义时序等模型定义

> **职责**：监控数据模型层（packages/monitor）：采集、拨测、自定义时序等模型定义

- **位置**：`packages/monitor/` · 归属文件 **12** 个 · 约 **1508** 行
- **定义**：`packages/monitor/models.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkmonitor`、`monitor_web`
- **被依赖**（动它会影响）：`apm_web`、`bkmonitor`、`fta_web`、`kernel_api`、`monitor_api`、`monitor_web`、`rum_web`

## 数据表（34）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `monitor_application` ⚠︎默认命名 | Application | 1 | models.Model（定义） | `packages/monitor/models/old.py:244` |
| `monitor_applicationconfig` ⚠︎默认命名 | ApplicationConfig | 1 | models.Model（定义） | `packages/monitor/models/models.py:64` |
| `monitor_applicationgroupmembership` ⚠︎默认命名 | ApplicationGroupMembership | 1 | models.Model（定义） | `packages/monitor/models/old.py:260` |
| `monitor_componentcategory` ⚠︎默认命名 | ComponentCategory | 1 | models.Model（定义） | `packages/monitor/models/old.py:710` |
| `monitor_componentcategoryrelationship` ⚠︎默认命名 | ComponentCategoryRelationship | 1 | models.Model（定义） | `packages/monitor/models/old.py:719` |
| `monitor_componentimporttask` ⚠︎默认命名 | ComponentImportTask | 1 | models.Model（定义） | `packages/monitor/models/old.py:738` |
| `monitor_dashboardmenu` ⚠︎默认命名 | DashboardMenu | 1 | models.Model（定义） | `packages/monitor/models/old.py:143` |
| `monitor_dashboardmenulocation` ⚠︎默认命名 | DashboardMenuLocation | 1 | models.Model（定义） | `packages/monitor/models/old.py:163` |
| `monitor_dashboardview` ⚠︎默认命名 | DashboardView | 1 | models.Model（定义） | `packages/monitor/models/old.py:149` |
| `monitor_datacollector` ⚠︎默认命名 | DataCollector | 1 | models.Model（定义） | `packages/monitor/models/old.py:67` |
| `monitor_datagenerateconfig` ⚠︎默认命名 | DataGenerateConfig | 1 | models.Model（定义） | `packages/monitor/models/old.py:39` |
| `monitor_exporterdeposittask` ⚠︎默认命名 | ExporterDepositTask | 1 | models.Model（定义） | `packages/monitor/models/old.py:650` |
| `monitor_globalconfig` ⚠︎默认命名 | GlobalConfig | 1 | models.Model（定义） | `packages/monitor/models/models.py:78` |
| `monitor_hostproperty` ⚠︎默认命名 | HostProperty | 1 | models.Model（定义） | `packages/monitor/models/old.py:199` |
| `monitor_hostpropertyconf` ⚠︎默认命名 | HostPropertyConf | 1 | models.Model（定义） | `packages/monitor/models/old.py:214` |
| `monitor_indexcolorconf` ⚠︎默认命名 | IndexColorConf | 1 | models.Model（定义） | `packages/monitor/models/old.py:861` |
| `monitor_logcollectorhost` ⚠︎默认命名 | LogCollectorHost | 1 | models.Model（定义） | `packages/monitor/models/old.py:831` |
| `monitor_metricconf` ⚠︎默认命名 | MetricConf | 1 | models.Model（定义） | `packages/monitor/models/old.py:219` |
| `monitor_metricmonitor` ⚠︎默认命名 | MetricMonitor | 1 | models.Model（定义） | `packages/monitor/models/old.py:237` |
| `monitor_monitorhoststicky` ⚠︎默认命名 | MonitorHostSticky | 1 | models.Model（定义） | `packages/monitor/models/old.py:91` |
| `monitor_monitorlocation` ⚠︎默认命名 | MonitorLocation | 1 | models.Model（定义） | `packages/monitor/models/old.py:126` |
| `monitor_operaterecord` ⚠︎默认命名 | OperateRecord | 1 | models.Model（定义） | `packages/monitor/models/old.py:21` |
| `monitor_rolepermission` ⚠︎默认命名 | RolePermission | 1 | models.Model（定义） | `packages/monitor/models/models.py:34` |
| `monitor_scenariomenu` ⚠︎默认命名 | ScenarioMenu | 1 | models.Model（定义） | `packages/monitor/models/old.py:101` |
| `monitor_serviceauthorization` ⚠︎默认命名 | ServiceAuthorization | 1 | models.Model（定义） | `packages/monitor/models/old.py:171` |
| `monitor_shellcollectorconfig` ⚠︎默认命名 | ShellCollectorConfig | 1 | models.Model（定义） | `packages/monitor/models/old.py:412` |
| `monitor_shellcollectordeposittask` ⚠︎默认命名 | ShellCollectorDepositTask | 1 | models.Model（定义） | `packages/monitor/models/old.py:446` |
| `monitor_uploadedfile` ⚠︎默认命名 | UploadedFile | 1 | models.Model（定义） | `packages/monitor/models/models.py:247` |
| `monitor_uptimecheckgroup` ⚠︎默认命名 | UptimeCheckGroup | 1 | models.Model（定义） | `packages/monitor/models/models.py:221` |
| `monitor_uptimechecknode` ⚠︎默认命名 | UptimeCheckNode | 1 | models.Model（定义） | `packages/monitor/models/models.py:95` |
| `monitor_uptimechecktask` ⚠︎默认命名 | UptimeCheckTask | 1 | models.Model（定义） | `packages/monitor/models/models.py:143` |
| `monitor_uptimechecktaskcollectorlog` ⚠︎默认命名 | UptimeCheckTaskCollectorLog | 1 | models.Model（定义） | `packages/monitor/models/models.py:209` |
| `monitor_uptimechecktasksubscription` ⚠︎默认命名 | UptimeCheckTaskSubscription | 1 | models.Model（定义） | `packages/monitor/models/models.py:133` |
| `monitor_userconfig` ⚠︎默认命名 | UserConfig | 1 | models.Model（定义） | `packages/monitor/models/models.py:46` |

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `monitor`）

## 归属文件（12）

- `packages/monitor/models.py`
- `packages/monitor/utils.py`
- `packages/monitor/schedulers.py`
- `packages/monitor/tasks.py`
- `packages/monitor/__init__.py`
- `packages/monitor/admin.py`
- `packages/monitor/urls.py`
- `packages/monitor/constants.py`
- `packages/monitor/apps.py`
- `packages/monitor/models/models.py`
- `packages/monitor/models/__init__.py`
- `packages/monitor/models/old.py`
