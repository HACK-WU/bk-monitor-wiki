# CalendarsConfig（`calendars`）

> **职责**：日历/工作日：轮值排班等时间计算的基础数据

> **职责**：日历/工作日：轮值排班等时间计算的基础数据

- **位置**：`calendars/` · 归属文件 **14** 个 · 约 **1871** 行
- **定义**：`calendars/models.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **1** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkmonitor`、`core.drf_resource`
- **被依赖**（动它会影响）：`alarm_backends`、`bkmonitor`、`kernel_api`、`monitor_web`

## 数据表（2）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `calendar` | CalendarModel | 1 | models.Model（定义） | `calendars/models.py:58` |
| `calendar_item` | CalendarItemModel | 1 | models.Model（定义） | `calendars/models.py:90` |

## 归属文件（14）

- `calendars/models.py`
- `calendars/views.py`
- `calendars/__init__.py`
- `calendars/admin.py`
- `calendars/serializers.py`
- `calendars/urls.py`
- `calendars/constants.py`
- `calendars/apps.py`
- `calendars/resources/item.py`
- `calendars/resources/__init__.py`
- `calendars/resources/calendar.py`
- `calendars/tests/item.py`
- `calendars/tests/__init__.py`
- `calendars/tests/calendar.py`
