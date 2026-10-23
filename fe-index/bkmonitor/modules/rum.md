# RumApiConfig（`rum`）

> **职责**：RUM 数据层：`/rum_api/v1` 接口与 RUM 数据模型

> **职责**：RUM 数据层：`/rum_api/v1` 接口与 RUM 数据模型

- **位置**：`rum/` · 归属文件 **17** 个 · 约 **1682** 行
- **定义**：`rum/views.py:1`（django）
- **挂载前缀**：`/rum_api/v1` · 视图/接口入口 **1** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`metadata`
- **被依赖**（动它会影响）：无

## 数据表（3）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `rum_rumappconfig` ⚠︎默认命名 | RumAppConfig | 1 | models.Model（定义） | `rum/models/config.py:16` |
| `rum_rumapplication` ⚠︎默认命名 | RumApplication | 1 | models.Model（定义） | `rum/models/application.py:24` |
| `rum_web_rumappconfig` ⚠︎默认命名 | RumAppConfig | 3 | import（rum_web） | `rum/resources.py:22` |

## 非 HTTP 入口

- **定时任务**：3 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/UnifyQuery查询专家`（命中标识 `rum`）
- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `rum`）
- `/root/bk-monitor/.module-experts/数据源查询构造专家`（命中标识 `rum`）

## 归属文件（17）

- `rum/views.py`
- `rum/__init__.py`
- `rum/admin.py`
- `rum/urls.py`
- `rum/constants.py`
- `rum/resources.py`
- `rum/apps.py`
- `rum/core/__init__.py`
- `rum/core/application_config.py`
- `rum/core/handlers/__init__.py`
- `rum/core/handlers/application_helper.py`
- `rum/models/application.py`
- `rum/models/__init__.py`
- `rum/models/datasource.py`
- `rum/models/config.py`
- `rum/task/tasks.py`
- `rum/task/__init__.py`
