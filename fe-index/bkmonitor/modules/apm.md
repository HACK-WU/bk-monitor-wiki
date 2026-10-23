# ApmApiConfig（`apm`）

> **职责**：APM 数据层/API：应用、服务、链路、容器、K8s 的模型与 `/apm_api/v1` 接口

> **职责**：APM 数据层/API：应用、服务、链路、容器、K8s 的模型与 `/apm_api/v1` 接口

- **位置**：`apm/` · 归属文件 **99** 个 · 约 **20613** 行
- **定义**：`apm/types.py:1`（django）
- **挂载前缀**：`/apm_api/v1` · 视图/接口入口 **4** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`alarm_backends`、`apm_ebpf`、`apm_web`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`metadata`
- **被依赖**（动它会影响）：`apm_web`、`bkmonitor`、`kernel_api`、`metadata`、`monitor_web`、`rum_web`

## 数据表（25）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `apm_apmapplication` ⚠︎默认命名 | ApmApplication | 1 | models.Model（定义） | `apm/models/application.py:37` |
| `apm_apminstancediscover` ⚠︎默认命名 | ApmInstanceDiscover | 1 | models.Model（定义） | `apm/models/config.py:280` |
| `apm_apmmetricdimension` ⚠︎默认命名 | ApmMetricDimension | 1 | models.Model（定义） | `apm/models/config.py:341` |
| `apm_apmtopodiscoverrule` ⚠︎默认命名 | ApmTopoDiscoverRule | 1 | models.Model（定义） | `apm/models/config.py:36` |
| `apm_bcsclusterdefaultapplicationrelation` ⚠︎默认命名 | BcsClusterDefaultApplicationRelation | 1 | models.Model（定义） | `apm/models/application.py:361` |
| `apm_bkdataflowconfig` ⚠︎默认命名 | BkdataFlowConfig | 1 | models.Model（定义） | `apm/models/datasource.py:1763` |
| `apm_datalink` ⚠︎默认命名 | DataLink | 1 | models.Model（定义） | `apm/models/datasource.py:1716` |
| `apm_ebpf_clusterrelation` ⚠︎默认命名 | ClusterRelation | 1 | import（apm_ebpf） | `apm/task/tasks.py:299` |
| `apm_ebpf_deepflowworkload` ⚠︎默认命名 | DeepflowWorkload | 1 | import（apm_ebpf） | `apm/core/handlers/query/proxy.py:37` |
| `apm_ebpfapplicationconfig` ⚠︎默认命名 | EbpfApplicationConfig | 1 | models.Model（定义） | `apm/models/application.py:353` |
| `apm_endpoint` ⚠︎默认命名 | Endpoint | 1 | models.Model（定义） | `apm/models/application.py:335` |
| `apm_fieldnormalizerconfig` ⚠︎默认命名 | FieldNormalizerConfig | 1 | models.Model（定义） | `apm/models/config.py:875` |
| `apm_profileservice` ⚠︎默认命名 | ProfileService | 1 | models.Model（定义） | `apm/models/profile.py:14` |
| `apm_remoteservicediscover` ⚠︎默认命名 | RemoteServiceDiscover | 1 | models.Model（定义） | `apm/models/config.py:602` |
| `apm_rootendpoint` ⚠︎默认命名 | RootEndpoint | 1 | models.Model（定义） | `apm/models/application.py:321` |
| `apm_subscriptionconfig` ⚠︎默认命名 | SubscriptionConfig | 1 | models.Model（定义） | `apm/models/subscription_config.py:21` |
| `apm_tracescopeindexset` ⚠︎默认命名 | TraceScopeIndexSet | 1 | models.Model（定义） | `apm/models/meta.py:17` |
| `apm_web_application` ⚠︎默认命名 | Application | 3 | import（apm_web） | `apm/resources.py:2225` |
| `data_source` | DataSource | 2 | import（bk_dataview） | `apm/resources.py:96` |
| `metadata_bcsclusterinfo` ⚠︎默认命名 | BCSClusterInfo | 3 | import（metadata） | `apm/core/platform_config.py:83` |
| `metadata_clusterinfo` ⚠︎默认命名 | ClusterInfo | 2 | import（metadata） | `apm/core/discover/precalculation/consul_handler.py:28` |
| `metadata_esstorage` ⚠︎默认命名 | ESStorage | 2 | import（metadata） | `apm/core/discover/precalculation/storage.py:46` |
| `metadata_resulttable` ⚠︎默认命名 | ResultTable | 1 | import（metadata） | `apm/models/datasource.py:908` |
| `monitor_applicationconfig` ⚠︎默认命名 | ApplicationConfig | 2 | import（monitor） | `apm/management/commands/migrate_apm_trace_datasource.py:16` |
| `permission` | Permission | 1 | import（bk_dataview） | `apm/core/handlers/query/proxy.py:39` |

## 非 HTTP 入口

- **定时任务**：13 处

## 专家资产（深挖读这些）

- `/root/bk-monitor/.module-experts/UnifyQuery查询专家`（命中标识 `apm`）
- `/root/bk-monitor/.module-experts/issue专家`（命中标识 `apm`）
- `/root/bk-monitor/.module-experts/kernel_api网关专家`（命中标识 `apm`）
- `/root/bk-monitor/.module-experts/场景视图专家`（命中标识 `apm`）
- `/root/bk-monitor/.module-experts/数据源查询构造专家`（命中标识 `apm`）

## 归属文件（99）

- `apm/types.py`
- `apm/views.py`
- `apm/__init__.py`
- `apm/admin.py`
- `apm/serializers.py`
- `apm/urls.py`
- `apm/constants.py`
- `apm/resources.py`
- `apm/apps.py`
- `apm/core/platform_config.py`
- `apm/core/cluster_config.py`
- `apm/core/__init__.py`
- `apm/core/application_config.py`
- `apm/core/deepflow/__init__.py`
- `apm/core/deepflow/constants.py`
- `apm/core/deepflow/base.py`
- `apm/core/discover/instance.py`
- `apm/core/discover/root_endpoint.py`
- `apm/core/discover/relation.py`
- `apm/core/discover/__init__.py`
- `apm/core/discover/endpoint.py`
- `apm/core/discover/cached_mixin.py`
- `apm/core/discover/instance_data.py`
- `apm/core/discover/remote_service_relation.py`
- `apm/core/discover/host.py`
- `apm/core/discover/base.py`
- `apm/core/discover/node.py`
- `apm/core/discover/log/service.py`
- `apm/core/discover/log/__init__.py`
- `apm/core/discover/log/base.py`
- `apm/core/discover/metric/service.py`
- `apm/core/discover/metric/__init__.py`
- `apm/core/discover/metric/base.py`
- `apm/core/discover/precalculation/daemon.py`
- `apm/core/discover/precalculation/task_spec.py`
- `apm/core/discover/precalculation/check.py`
- `apm/core/discover/precalculation/__init__.py`
- `apm/core/discover/precalculation/consul_handler.py`
- `apm/core/discover/precalculation/storage.py`
- `apm/core/discover/precalculation/processor.py`
- ……其余 20 个见 JSON 输出（完整清单）
