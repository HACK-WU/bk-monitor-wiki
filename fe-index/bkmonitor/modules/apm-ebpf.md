# ApmEbpfConfig（`apm-ebpf`）

> **职责**：eBPF 观测：深度流量/网络指标采集与微服务拓扑数据

> **职责**：eBPF 观测：深度流量/网络指标采集与微服务拓扑数据

- **位置**：`apm_ebpf/` · 归属文件 **14** 个 · 约 **1450** 行
- **定义**：`apm_ebpf/__init__.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`bk_dataview`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`metadata`
- **被依赖**（动它会影响）：`apm`、`kernel_api`、`monitor_web`

## 数据表（6）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `apm_ebpf_clusterrelation` ⚠︎默认命名 | ClusterRelation | 1 | models.Model（定义） | `apm_ebpf/models/workload.py:41` |
| `apm_ebpf_deepflowdashboardrecord` ⚠︎默认命名 | DeepflowDashboardRecord | 1 | models.Model（定义） | `apm_ebpf/models/workload.py:62` |
| `apm_ebpf_deepflowworkload` ⚠︎默认命名 | DeepflowWorkload | 1 | models.Model（定义） | `apm_ebpf/models/workload.py:19` |
| `dashboard` | Dashboard | 1 | import（bk_dataview） | `apm_ebpf/handlers/provisioning.py:19` |
| `metadata_space` ⚠︎默认命名 | Space | 1 | import（metadata） | `apm_ebpf/handlers/relation.py:18` |
| `metadata_spaceresource` ⚠︎默认命名 | SpaceResource | 1 | import（metadata） | `apm_ebpf/handlers/relation.py:18` |

## 非 HTTP 入口

- **定时任务**：1 处

## 归属文件（14）

- `apm_ebpf/__init__.py`
- `apm_ebpf/admin.py`
- `apm_ebpf/resource.py`
- `apm_ebpf/constants.py`
- `apm_ebpf/apps.py`
- `apm_ebpf/handlers/relation.py`
- `apm_ebpf/handlers/provisioning.py`
- `apm_ebpf/handlers/__init__.py`
- `apm_ebpf/handlers/workload.py`
- `apm_ebpf/handlers/deepflow.py`
- `apm_ebpf/models/__init__.py`
- `apm_ebpf/models/workload.py`
- `apm_ebpf/task/tasks.py`
- `apm_ebpf/task/__init__.py`
