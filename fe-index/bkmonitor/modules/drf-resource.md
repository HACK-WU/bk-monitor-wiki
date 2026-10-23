# DRFResourceConfig（`drf-resource`）

> **职责**：DRF Resource 框架：声明式 APIResource/ResourceViewSet，全站接口的公共基座（`core.drf_resource`）

> **职责**：DRF Resource 框架：声明式 APIResource/ResourceViewSet，全站接口的公共基座（`core.drf_resource`）

- **位置**：`core/drf_resource/` · 归属文件 **22** 个 · 约 **4213** 行
- **定义**：`core/drf_resource/models.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **1** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkm_space`、`bkmonitor`、`kernel_api`、`query_api`
- **被依赖**（动它会影响）：`ai_whale`、`alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bk_dataview`、`bkmonitor`、`calendars`、`fta_web`、`kernel_api`、`metadata`、`monitor_api`、`monitor_web`、`performance`、`profile`、`query_api`、`rum`、`rum_web`

## 数据表（1）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `resource_data` | ResourceData | 1 | models.Model（定义） | `core/drf_resource/models.py:87` |

## 非 HTTP 入口

- **定时任务**：1 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `core.drf_resource`）
- `/root/bk-monitor/.module-experts/告警查询专家`（命中标识 `core.drf_resource`）

## 归属文件（22）

- `core/drf_resource/tools.py`
- `core/drf_resource/models.py`
- `core/drf_resource/tasks.py`
- `core/drf_resource/viewsets.py`
- `core/drf_resource/routers.py`
- `core/drf_resource/exceptions.py`
- `core/drf_resource/__init__.py`
- `core/drf_resource/admin.py`
- `core/drf_resource/apps.py`
- `core/drf_resource/stubgen.py`
- `core/drf_resource/base.py`
- `core/drf_resource/contrib/__init__.py`
- `core/drf_resource/contrib/nested_api.py`
- `core/drf_resource/contrib/cache.py`
- `core/drf_resource/contrib/exception.py`
- `core/drf_resource/contrib/api.py`
- `core/drf_resource/management/exceptions.py`
- `core/drf_resource/management/__init__.py`
- `core/drf_resource/management/finder.py`
- `core/drf_resource/management/js_api_generator.py`
- `core/drf_resource/management/root.py`
- `core/drf_resource/management/stub_file_generator.py`
