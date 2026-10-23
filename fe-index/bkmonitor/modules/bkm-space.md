# BkmSpaceConfig（`bkm-space`）

> **职责**：业务空间基座：多租户空间模型与空间隔离能力（被 15 个模块依赖）

> **职责**：业务空间基座：多租户空间模型与空间隔离能力（被 15 个模块依赖）

- **位置**：`bkm_space/` · 归属文件 **10** 个 · 约 **464** 行
- **定义**：`bkm_space/utils.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：无（顶层模块或被依赖方未在扫描范围）
- **被依赖**（动它会影响）：`alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bk_dataview`、`bkm_ipchooser`、`bkmonitor`、`core.drf_resource`、`fta_web`、`kernel_api`、`metadata`、`monitor_web`、`performance`、`rum`、`rum_web`

## 数据表（0）

（未引用数据表——纯计算/转发型模块）

## 归属文件（10）

- `bkm_space/utils.py`
- `bkm_space/scope.py`
- `bkm_space/define.py`
- `bkm_space/__init__.py`
- `bkm_space/serializers.py`
- `bkm_space/validate.py`
- `bkm_space/apps.py`
- `bkm_space/middleware.py`
- `bkm_space/api.py`
- `bkm_space/errors.py`
