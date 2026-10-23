# BkDataviewConfig（`bk-dataview`）

> **职责**：数据可视化集成：Grafana（BK-Dataview）租户、仪表盘、权限对接

> **职责**：数据可视化集成：Grafana（BK-Dataview）租户、仪表盘、权限对接

- **位置**：`bk_dataview/` · 归属文件 **13** 个 · 约 **1904** 行
- **定义**：`bk_dataview/models.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **4** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkm_space`、`bkmonitor`、`core.drf_resource`
- **被依赖**（动它会影响）：`apm_ebpf`、`bkmonitor`、`kernel_api`、`monitor_web`

## 数据表（15）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `builtin_role` | BuiltinRole | 1 | models.Model（定义） | `bk_dataview/models.py:286` |
| `dashboard` | Dashboard | 1 | models.Model（定义） | `bk_dataview/models.py:130` |
| `data_source` | DataSource | 1 | models.Model（定义） | `bk_dataview/models.py:97` |
| `folder` | Folder | 1 | models.Model（定义） | `bk_dataview/models.py:168` |
| `org` | Org | 1 | models.Model（定义） | `bk_dataview/models.py:62` |
| `org_user` | OrgUser | 1 | models.Model（定义） | `bk_dataview/models.py:82` |
| `permission` | Permission | 1 | models.Model（定义） | `bk_dataview/models.py:270` |
| `preferences` | Preferences | 1 | models.Model（定义） | `bk_dataview/models.py:246` |
| `role` | Role | 1 | models.Model（定义） | `bk_dataview/models.py:301` |
| `star` | Star | 1 | models.Model（定义） | `bk_dataview/models.py:321` |
| `team` | Team | 1 | models.Model（定义） | `bk_dataview/models.py:191` |
| `team_member` | TeamMember | 1 | models.Model（定义） | `bk_dataview/models.py:207` |
| `team_role` | TeamRole | 1 | models.Model（定义） | `bk_dataview/models.py:228` |
| `user` | User | 1 | models.Model（定义） | `bk_dataview/models.py:16` |
| `user_role` | UserRole | 1 | models.Model（定义） | `bk_dataview/models.py:44` |

## 归属文件（13）

- `bk_dataview/models.py`
- `bk_dataview/authentication.py`
- `bk_dataview/utils.py`
- `bk_dataview/views.py`
- `bk_dataview/settings.py`
- `bk_dataview/permissions.py`
- `bk_dataview/provisioning.py`
- `bk_dataview/__init__.py`
- `bk_dataview/client.py`
- `bk_dataview/router.py`
- `bk_dataview/urls.py`
- `bk_dataview/apps.py`
- `bk_dataview/api.py`
