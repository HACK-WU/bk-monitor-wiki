# RumWebConfig（`rum-web`）

> **职责**：RUM Web 层：前端监控（RUM）配置页面后端

> **职责**：RUM Web 层：前端监控（RUM）配置页面后端

- **位置**：`packages/rum_web/` · 归属文件 **51** 个 · 约 **5769** 行
- **定义**：`packages/rum_web/metric_handler.py:1`（django）
- **挂载前缀**：`/meta`、`/metric`、`/rum` · 视图/接口入口 **5** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`apm`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`monitor`、`monitor_web`
- **被依赖**（动它会影响）：`bkmonitor`、`monitor_web`

## 数据表（4）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `apm_web_application` ⚠︎默认命名 | Application | 8 | import（apm_web） | `packages/rum_web/tasks.py:25` |
| `monitor_applicationconfig` ⚠︎默认命名 | ApplicationConfig | 1 | import（monitor） | `packages/rum_web/meta/resources.py:30` |
| `rum_web_application` ⚠︎默认命名 | Application | 1 | models.Model（定义） | `packages/rum_web/models/application.py:31` |
| `rum_web_rumappconfig` ⚠︎默认命名 | RumAppConfig | 1 | models.Model（定义） | `packages/rum_web/models/application.py:229` |

## 非 HTTP 入口

- **定时任务**：3 处

## 归属文件（51）

- `packages/rum_web/metric_handler.py`
- `packages/rum_web/tasks.py`
- `packages/rum_web/views.py`
- `packages/rum_web/calculation.py`
- `packages/rum_web/__init__.py`
- `packages/rum_web/admin.py`
- `packages/rum_web/serializers.py`
- `packages/rum_web/urls.py`
- `packages/rum_web/constants.py`
- `packages/rum_web/resources.py`
- `packages/rum_web/metrics.py`
- `packages/rum_web/apps.py`
- `packages/rum_web/handlers/__init__.py`
- `packages/rum_web/handlers/backend_data_handler.py`
- `packages/rum_web/handlers/service_handler.py`
- `packages/rum_web/handlers/builder/utils.py`
- `packages/rum_web/handlers/builder/__init__.py`
- `packages/rum_web/handlers/builder/constants.py`
- `packages/rum_web/handlers/builder/base.py`
- `packages/rum_web/handlers/builder/span/vital.py`
- `packages/rum_web/handlers/builder/span/__init__.py`
- `packages/rum_web/handlers/builder/span/error.py`
- `packages/rum_web/handlers/builder/span/action.py`
- `packages/rum_web/handlers/builder/span/resource.py`
- `packages/rum_web/handlers/builder/span/longtask.py`
- `packages/rum_web/handlers/builder/span/view.py`
- `packages/rum_web/handlers/builder/span/base.py`
- `packages/rum_web/handlers/level/span.py`
- `packages/rum_web/handlers/level/__init__.py`
- `packages/rum_web/handlers/level/factory.py`
- `packages/rum_web/handlers/level/base.py`
- `packages/rum_web/handlers/query/span.py`
- `packages/rum_web/handlers/query/__init__.py`
- `packages/rum_web/meta/views.py`
- `packages/rum_web/meta/__init__.py`
- `packages/rum_web/meta/urls.py`
- `packages/rum_web/meta/resources.py`
- `packages/rum_web/metric/views.py`
- `packages/rum_web/metric/__init__.py`
- `packages/rum_web/metric/urls.py`
- ……其余 11 个见 JSON 输出（完整清单）
