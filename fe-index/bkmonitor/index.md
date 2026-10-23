# bkmonitor 后端模块索引

> 根目录：`/root/bk-monitor/bkmonitor` · 框架：**django** · 全局前缀：（未探测到）
> 生成：2026-10-13 · commit：`ff89f63ff4` · 范围：`**` · 扫描器：scan_backend.py v2.1.0
> 新鲜度校验：`python3 scan_backend.py --root /root/bk-monitor/bkmonitor --check --index <本目录>`

**这个索引回答什么**：改某个模块要连带看谁（依赖/被依赖）、改某张表要通知哪些模块、某模块的数据面与非 HTTP 入口、模块的代码在哪。**接口级契约**见 `.module-experts/` 专家资产与 ki 接口信息（`tags=api`）——本索引不重复建设。

## 1. 模块地图（24）

| 模块 | 职责 | 目录 | 挂载前缀 | 接口 | 表 | 依赖 | 被依赖 | 非 HTTP 入口 | 专家资产 |
|------|------|------|----------|------|----|------|--------|--------------|----------|
| [KernelAPIConfig](modules/kernel-api.md) `kernel-api` | 内核 API 网关（v4）：统一 Resource/RPC 注册、鉴权与权限，216 个对外入口 | `kernel_api` | - | 216 | 67 | alarm_backends、apm、apm_ebpf 等 15 | core.drf_resource、fta_web、query_api | - | issue专家、kernel_api网关专家、告警屏蔽专家、告警查询专家 |
| [MonitorWebConfig](modules/monitor-web.md) `monitor-web` | 监控 Web 资源层：策略/屏蔽/采集/场景视图等配置类页面的后端 | `packages/monitor_web` | `/commons`、`/k8s`、`/overview` 等 7 个 | 147 | 177 | alarm_backends、apm、apm_ebpf 等 14 | apm_web、bkmonitor、fta_web 等 8 | 任务 32 | kernel_api网关专家、告警屏蔽专家、告警查询专家、场景视图专家、性能场景专家 |
| [ApmWebConfig](modules/apm-web.md) `apm-web` | APM Web 资源层：应用/服务/容器/Profiling 页面后端（含 profile 子模块） | `packages/apm_web` | `/apm`、`/apm_log_forward`、`/container` 等 15 个 | 29 | 18 | apm、bkm_space、bkmonitor 等 8 | ai_whale、apm、bkmonitor 等 7 | 任务 12 | UnifyQuery查询专家、场景视图专家 |
| [FtaWebConfig](modules/fta-web.md) `fta-web` | 告警处理/故障自愈 Web 层：事件中心、动作、分派、Issue | `packages/fta_web` | `/action`、`/alert`、`/alert/v2` 等 8 个 | 27 | 39 | alarm_backends、apm_web、bkm_space 等 8 | apm_web、bkmonitor、kernel_api 等 4 | 任务 5 | issue专家、kernel_api网关专家、告警屏蔽专家、告警查询专家 |
| [profile](modules/profile.md) `profile` | Profiling 子模块（apm_web 内）：Profile 采集、解析与查询 | `packages/apm_web/profile` | `/profile_api` | 13 | 4 | apm_web、bkmonitor、core.drf_resource | - | - | - |
| [IpChooserConfig](modules/bkm-ipchooser.md) `bkm-ipchooser` | IP 选择器 SDK：主机/动态分组/IP(v6) 选择统一 API | `bkm_ipchooser` | - | 7 | 1 | bkm_space、bkmonitor | monitor_web | 任务 1 | - |
| [performance](modules/performance.md) `performance` | 性能场景子模块（monitor_web 内）：主机性能/进程列表等资源 | `packages/monitor_web/performance` | `/performance` | 7 | 0 | bkm_space、bkmonitor、core.drf_resource 等 4 | - | - | 场景视图专家、性能场景专家 |
| [AiAgentsConfig](modules/ai-whale.md) `ai-whale` | AI 助手：智能体/对话能力接入与本地指令处理器 | `ai_whale` | `/ai_whale` | 6 | 0 | apm_web、bkmonitor、core.drf_resource | - | - | - |
| [RumWebConfig](modules/rum-web.md) `rum-web` | RUM Web 层：前端监控（RUM）配置页面后端 | `packages/rum_web` | `/meta`、`/metric`、`/rum` | 5 | 4 | apm、bkm_space、bkmonitor 等 6 | bkmonitor、monitor_web | 任务 3 | - |
| [ApmApiConfig](modules/apm.md) `apm` | APM 数据层/API：应用、服务、链路、容器、K8s 的模型与 `/apm_api/v1` 接口 | `apm` | `/apm_api/v1` | 4 | 25 | alarm_backends、apm_ebpf、apm_web 等 7 | apm_web、bkmonitor、kernel_api 等 6 | 任务 13 | UnifyQuery查询专家、issue专家、kernel_api网关专家、场景视图专家、数据源查询构造专家 |
| [BkDataviewConfig](modules/bk-dataview.md) `bk-dataview` | 数据可视化集成：Grafana（BK-Dataview）租户、仪表盘、权限对接 | `bk_dataview` | - | 4 | 15 | bkm_space、bkmonitor、core.drf_resource | apm_ebpf、bkmonitor、kernel_api 等 4 | - | - |
| [MonitorAPIConfig](modules/monitor-api.md) `monitor-api` | 监控对外 API v1（packages/monitor_api）：`/rest/v1` 接口层 | `packages/monitor_api` | `/rest/v1` | 3 | 12 | bkmonitor、core.drf_resource、monitor | kernel_api | - | kernel_api网关专家 |
| [CalendarsConfig](modules/calendars.md) `calendars` | 日历/工作日：轮值排班等时间计算的基础数据 | `calendars` | - | 1 | 2 | bkmonitor、core.drf_resource | alarm_backends、bkmonitor、kernel_api 等 4 | - | - |
| [DRFResourceConfig](modules/drf-resource.md) `drf-resource` | DRF Resource 框架：声明式 APIResource/ResourceViewSet，全站接口的公共基座（`core.drf_resource`） | `core/drf_resource` | - | 1 | 1 | bkm_space、bkmonitor、kernel_api 等 4 | ai_whale、alarm_backends、apm 等 18 | 任务 1 | kernel_api网关专家、告警查询专家 |
| [RumApiConfig](modules/rum.md) `rum` | RUM 数据层：`/rum_api/v1` 接口与 RUM 数据模型 | `rum` | `/rum_api/v1` | 1 | 3 | alarm_backends、bkm_space、bkmonitor 等 5 | - | 任务 3 | UnifyQuery查询专家、kernel_api网关专家、数据源查询构造专家 |
| [Config](modules/alarm-backends.md) `alarm-backends` | 告警后台（核心引擎）：检测/触发/动作执行/ACL/周期任务，41 个任务入口，不对外暴露 HTTP | `alarm_backends` | - | 0 | 51 | bkm_space、bkmonitor、calendars 等 6 | apm、apm_ebpf、bkmonitor 等 8 | 任务 41 | issue专家、kernel_api网关专家、告警屏蔽专家 |
| [ApmEbpfConfig](modules/apm-ebpf.md) `apm-ebpf` | eBPF 观测：深度流量/网络指标采集与微服务拓扑数据 | `apm_ebpf` | - | 0 | 6 | alarm_backends、bk_dataview、bkm_space 等 6 | apm、kernel_api、monitor_web | 任务 1 | - |
| [AuditConfig](modules/audit.md) `audit` | 审计：操作审计记录与上报 | `packages/audit` | - | 0 | 0 | bkmonitor | bkmonitor | - | - |
| [BkmSpaceConfig](modules/bkm-space.md) `bkm-space` | 业务空间基座：多租户空间模型与空间隔离能力（被 15 个模块依赖） | `bkm_space` | - | 0 | 0 | - | alarm_backends、apm、apm_ebpf 等 15 | - | - |
| [Config](modules/bkmonitor.md) `bkmonitor` | 监控核心与公共层：策略/告警/报表数据模型 + 公共工具 + `api/` 外部系统集成（34 个第三方系统） | `bkmonitor` | - | 0 | 109 | alarm_backends、apm、apm_web 等 13 | ai_whale、alarm_backends、apm 等 21 | 信号 2 | UnifyQuery查询专家、issue专家、kernel_api网关专家、告警屏蔽专家、告警查询专家、场景视图专家、性能场景专家、数据源查询构造专家、外部API集成专题 |
| [WeixiCoreConfig](modules/core.md) `core` | 微信/企业微信集成（packages/weixin/core）：登录、账号与用户模型 | `packages/weixin/core` | `/login` | 0 | 1 | - | - | - | kernel_api网关专家、告警屏蔽专家、告警查询专家 |
| [MetaDataAppConfig](modules/metadata.md) `metadata` | 元数据管理：数据源/结果表/存储/空间/BCS 集群元信息，数据链路的事实来源 | `metadata` | - | 0 | 71 | alarm_backends、apm、bkm_space 等 6 | alarm_backends、apm、apm_ebpf 等 9 | 任务 33 · 信号 3 | kernel_api网关专家、数据源查询构造专家、元数据管理专题 |
| [MonitorConfig](modules/monitor.md) `monitor` | 监控数据模型层（packages/monitor）：采集、拨测、自定义时序等模型定义 | `packages/monitor` | - | 0 | 34 | bkmonitor、monitor_web | apm_web、bkmonitor、fta_web 等 7 | - | kernel_api网关专家 |
| [QueryApiConfig](modules/query-api.md) `query-api` | 数据查询代理：bkmonitor data query proxy（统一查询转发） | `query_api` | - | 0 | 2 | bkmonitor、core.drf_resource、kernel_api 等 4 | alarm_backends、core.drf_resource、kernel_api | - | - |

## 2. 模块依赖图（125 条边）

（边数 125 > 120，图过密，按模块列出）

- `ai-whale` → `apm_web`、`bkmonitor`、`core.drf_resource`
- `alarm-backends` → `bkm_space`、`bkmonitor`、`calendars`、`core.drf_resource`、`metadata`、`query_api`
- `apm` → `alarm_backends`、`apm_ebpf`、`apm_web`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`metadata`
- `apm-ebpf` → `alarm_backends`、`bk_dataview`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`metadata`
- `bk-dataview` → `bkm_space`、`bkmonitor`、`core.drf_resource`
- `bkm-ipchooser` → `bkm_space`、`bkmonitor`
- `bkmonitor` → `alarm_backends`、`apm`、`apm_web`、`audit`、`bk_dataview`、`bkm_space`、`calendars`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`monitor_web`、`rum_web`
- `calendars` → `bkmonitor`、`core.drf_resource`
- `drf-resource` → `bkm_space`、`bkmonitor`、`kernel_api`、`query_api`
- `kernel-api` → `alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bk_dataview`、`bkm_space`、`bkmonitor`、`calendars`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`monitor_api`、`monitor_web`、`query_api`
- `metadata` → `alarm_backends`、`apm`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`monitor_web`
- `apm-web` → `apm`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`monitor_web`
- `profile` → `apm_web`、`bkmonitor`、`core.drf_resource`
- `audit` → `bkmonitor`
- `fta-web` → `alarm_backends`、`apm_web`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`kernel_api`、`monitor`、`monitor_web`
- `monitor` → `bkmonitor`、`monitor_web`
- `monitor-api` → `bkmonitor`、`core.drf_resource`、`monitor`
- `monitor-web` → `alarm_backends`、`apm`、`apm_ebpf`、`apm_web`、`bk_dataview`、`bkm_ipchooser`、`bkm_space`、`bkmonitor`、`calendars`、`core.drf_resource`、`fta_web`、`metadata`、`monitor`、`rum_web`
- `performance` → `bkm_space`、`bkmonitor`、`core.drf_resource`、`monitor_web`
- `rum-web` → `apm`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`monitor`、`monitor_web`
- `query-api` → `bkmonitor`、`core.drf_resource`、`kernel_api`、`metadata`
- `rum` → `alarm_backends`、`bkm_space`、`bkmonitor`、`core.drf_resource`、`metadata`

## 3. 表 → 模块（反向，286 张表）

| 表 | 模块数 | 模块（引用次数） |
|----|--------|------------------|
| `permission` | 8 | `monitor-web`（16）、`fta-web`（4）、`bkmonitor`（3）、`kernel-api`（3）、`alarm-backends`（2） 等 8 个模块 |
| `global_setting` | 8 | `monitor-web`（5）、`kernel-api`（4）、`fta-web`（3）、`alarm-backends`（1）、`bkmonitor`（1） 等 8 个模块 |
| `data_source` | 7 | `metadata`（36）、`monitor-web`（11）、`bkmonitor`（7）、`alarm-backends`（3）、`apm`（2） 等 7 个模块 |
| `apm_web_application` ⚠︎默认命名 | 7 | `monitor-web`（15）、`bkmonitor`（8）、`rum-web`（8）、`kernel-api`（5）、`apm`（3） 等 7 个模块 |
| `alarm_algorithm_v2` | 6 | `monitor-web`（12）、`alarm-backends`（7）、`bkmonitor`（1）、`kernel-api`（1）、`apm-web`（1） 等 6 个模块 |
| `metadata_resulttable` ⚠︎默认命名 | 6 | `monitor-web`（9）、`bkmonitor`（2）、`query-api`（2）、`alarm-backends`（1）、`apm`（1） 等 6 个模块 |
| `metadata_space` ⚠︎默认命名 | 6 | `monitor-web`（11）、`alarm-backends`（1）、`apm-ebpf`（1）、`bkmonitor`（1）、`kernel-api`（1） 等 6 个模块 |
| `metadata_clusterinfo` ⚠︎默认命名 | 6 | `monitor-web`（4）、`apm`（2）、`kernel-api`（2）、`alarm-backends`（1）、`metadata`（1） 等 6 个模块 |
| `alarm_strategy_v2` | 5 | `monitor-web`（38）、`kernel-api`（9）、`alarm-backends`（4）、`fta-web`（3）、`bkmonitor`（1） |
| `bkmonitor_metriclistcache` ⚠︎默认命名 | 5 | `monitor-web`（24）、`fta-web`（3）、`alarm-backends`（1）、`bkmonitor`（1）、`kernel-api`（1） |
| `alarm_query_config_v2` | 5 | `monitor-web`（20）、`kernel-api`（2）、`bkmonitor`（1）、`metadata`（1）、`fta-web`（1） |
| `user_group` | 5 | `monitor-web`（10）、`kernel-api`（7）、`apm-web`（5）、`alarm-backends`（2）、`bkmonitor`（1） |
| `alarm_strategy` | 5 | `alarm-backends`（12）、`kernel-api`（5）、`monitor-web`（4）、`bkmonitor`（1）、`fta-web`（1） |
| `action_config` | 5 | `fta-web`（7）、`monitor-web`（5）、`kernel-api`（4）、`alarm-backends`（1）、`bkmonitor`（1） |
| `dashboard` | 5 | `monitor-web`（13）、`apm-ebpf`（1）、`bk-dataview`（1）、`bkmonitor`（1）、`kernel-api`（1） |
| `monitor_applicationconfig` ⚠︎默认命名 | 5 | `monitor-web`（12）、`apm`（2）、`apm-web`（1）、`monitor`（1）、`rum-web`（1） |
| `alarm_shield` | 5 | `monitor-web`（9）、`alarm-backends`（4）、`bkmonitor`（1）、`kernel-api`（1）、`fta-web`（1） |
| `action_plugin` | 5 | `fta-web`（8）、`alarm-backends`（3）、`monitor-web`（2）、`bkmonitor`（1）、`kernel-api`（1） |
| `bkmonitor_alertassigngroup` ⚠︎默认命名 | 5 | `fta-web`（4）、`monitor-web`（3）、`kernel-api`（2）、`alarm-backends`（1）、`bkmonitor`（1） |
| `bkmonitor_alertassignrule` ⚠︎默认命名 | 5 | `fta-web`（3）、`monitor-web`（3）、`kernel-api`（2）、`alarm-backends`（1）、`bkmonitor`（1） |
| `monitor_web_customeventgroup` ⚠︎默认命名 | 5 | `kernel-api`（2）、`bkmonitor`（1）、`metadata`（1）、`fta-web`（1）、`monitor-web`（1） |
| `action_instance` | 4 | `alarm-backends`（19）、`fta-web`（5）、`bkmonitor`（1）、`kernel-api`（1） |
| `apm_datalink` ⚠︎默认命名 | 4 | `metadata`（9）、`kernel-api`（4）、`monitor-web`（2）、`apm`（1） |
| `alarm_item_v2` | 4 | `monitor-web`（10）、`fta-web`（2）、`bkmonitor`（1）、`kernel-api`（1） |
| `metadata_bcsclusterinfo` ⚠︎默认命名 | 4 | `monitor-web`（6）、`apm`（3）、`kernel-api`（2）、`metadata`（1） |
| `org` | 4 | `monitor-web`（8）、`kernel-api`（2）、`bk-dataview`（1）、`bkmonitor`（1） |
| `alarm_cacherouter` | 4 | `kernel-api`（5）、`alarm-backends`（4）、`bkmonitor`（1）、`monitor-web`（1） |
| `strategy_action_relation` | 4 | `monitor-web`（5）、`kernel-api`（3）、`fta-web`（2）、`bkmonitor`（1） |
| `alarm_cachenode` | 4 | `alarm-backends`（5）、`kernel-api`（2）、`bkmonitor`（1）、`monitor-web`（1） |
| `apm_apmapplication` ⚠︎默认命名 | 4 | `monitor-web`（6）、`apm`（1）、`kernel-api`（1）、`metadata`（1） |
| `duty_arrange` | 4 | `monitor-web`（4）、`kernel-api`（3）、`alarm-backends`（1）、`bkmonitor`（1） |
| `duty_rule` | 4 | `monitor-web`（5）、`kernel-api`（2）、`alarm-backends`（1）、`bkmonitor`（1） |
| `metadata_esstorage` ⚠︎默认命名 | 4 | `monitor-web`（5）、`apm`（2）、`alarm-backends`（1）、`metadata`（1） |
| `monitor_web_collectorpluginmeta` ⚠︎默认命名 | 4 | `bkmonitor`（4）、`kernel-api`（3）、`metadata`（1）、`monitor-web`（1） |
| `report` | 4 | `alarm-backends`（3）、`monitor-web`（3）、`kernel-api`（2）、`bkmonitor`（1） |
| `bkmonitor_issue_merge_relation` | 4 | `kernel-api`（5）、`alarm-backends`（1）、`bkmonitor`（1）、`fta-web`（1） |
| `bkmonitor_reportitems` ⚠︎默认命名 | 4 | `monitor-web`（4）、`alarm-backends`（2）、`bkmonitor`（1）、`kernel-api`（1） |
| `apm_ebpf_deepflowworkload` ⚠︎默认命名 | 4 | `monitor-web`（3）、`kernel-api`（2）、`apm`（1）、`apm-ebpf`（1） |
| `bkmonitor_querytemplate` ⚠︎默认命名 | 4 | `monitor-web`（4）、`bkmonitor`（1）、`apm-web`（1）、`profile`（1） |
| `bkmonitor_statisticsmetric` ⚠︎默认命名 | 4 | `monitor-web`（3）、`apm-web`（2）、`alarm-backends`（1）、`bkmonitor`（1） |
| `alarm_action` | 4 | `kernel-api`（2）、`monitor-web`（2）、`bkmonitor`（1）、`fta-web`（1） |
| `report_channel` | 4 | `alarm-backends`（2）、`monitor-web`（2）、`bkmonitor`（1）、`kernel-api`（1） |
| `alarm_notice_group` | 4 | `monitor-web`（2）、`alarm-backends`（1）、`bkmonitor`（1）、`fta-web`（1） |
| `alarm_strategy_history` | 4 | `monitor-web`（2）、`alarm-backends`（1）、`bkmonitor`（1）、`kernel-api`（1） |
| `metadata_spaceresource` ⚠︎默认命名 | 4 | `monitor-web`（2）、`apm-ebpf`（1）、`kernel-api`（1）、`metadata`（1） |
| `user` | 4 | `kernel-api`（2）、`bk-dataview`（1）、`bkmonitor`（1）、`monitor-web`（1） |
| `calendar` | 4 | `alarm-backends`（1）、`bkmonitor`（1）、`calendars`（1）、`monitor-web`（1） |
| `alarm_alert` | 3 | `alarm-backends`（8）、`monitor-web`（2）、`bkmonitor`（1） |
| `alarm_strategy_label` | 3 | `monitor-web`（7）、`bkmonitor`（1）、`kernel-api`（1） |
| `api_auth_token` | 3 | `kernel-api`（5）、`monitor-web`（3）、`bkmonitor`（1） |
| `alarm_event` | 3 | `monitor-web`（4）、`alarm-backends`（3）、`bkmonitor`（1） |
| `converge_relation` | 3 | `alarm-backends`（5）、`fta-web`（2）、`bkmonitor`（1） |
| `monitor_uptimechecktask` ⚠︎默认命名 | 3 | `monitor-web`（6）、`kernel-api`（1）、`monitor`（1） |
| `event_plugin` | 3 | `fta-web`（5）、`bkmonitor`（1）、`monitor-web`（1） |
| `metadata_datasourceresulttable` ⚠︎默认命名 | 3 | `monitor-web`（5）、`bkmonitor`（1）、`metadata`（1） |
| `apm_web_profileuploadrecord` ⚠︎默认命名 | 3 | `profile`（3）、`monitor-web`（2）、`apm-web`（1） |
| `bkmonitor_reportcontents` ⚠︎默认命名 | 3 | `monitor-web`（3）、`alarm-backends`（2）、`bkmonitor`（1） |
| `bkmonitor_strategy_issue_config` | 3 | `alarm-backends`（4）、`bkmonitor`（1）、`kernel-api`（1） |
| `monitor_uptimechecknode` ⚠︎默认命名 | 3 | `monitor-web`（4）、`kernel-api`（1）、`monitor`（1） |
| `monitor_web_customtstable` ⚠︎默认命名 | 3 | `bkmonitor`（3）、`kernel-api`（2）、`monitor-web`（1） |

（共 286 张，完整见 `tables.md`）

## 4. 专家资产（11 个）

| 专家 | 路径 | 关联模块 |
|------|------|----------|
| UnifyQuery查询专家 | `/root/bk-monitor/.module-experts/UnifyQuery查询专家` | `apm`、`bkmonitor`、`apm-web`、`rum` |
| issue专家 | `/root/bk-monitor/.module-experts/issue专家` | `alarm-backends`、`apm`、`bkmonitor`、`kernel-api`、`fta-web` |
| kernel_api网关专家 | `/root/bk-monitor/.module-experts/kernel_api网关专家` | `alarm-backends`、`apm`、`bkmonitor`、`drf-resource`、`kernel-api`、`metadata`、`fta-web`、`monitor`、`monitor-api`、`monitor-web`、`core`（⚠️ 误关联，见 `modules/core.md`）（⚠️ 误关联，见 `modules/core.md`）、`rum` |
| 元数据管理专题 | `/root/bk-monitor/.module-experts/元数据管理专题` | `metadata`（人工指认） |
| 前端专题 | `/root/bk-monitor/.module-experts/前端专题` | **未关联** |
| 告警屏蔽专家 | `/root/bk-monitor/.module-experts/告警屏蔽专家` | `alarm-backends`、`bkmonitor`、`kernel-api`、`fta-web`、`monitor-web`、`core`（⚠️ 误关联，见 `modules/core.md`）（⚠️ 误关联，见 `modules/core.md`） |
| 告警查询专家 | `/root/bk-monitor/.module-experts/告警查询专家` | `bkmonitor`、`drf-resource`、`kernel-api`、`fta-web`、`monitor-web`、`core`（⚠️ 误关联，见 `modules/core.md`）（⚠️ 误关联，见 `modules/core.md`） |
| 场景视图专家 | `/root/bk-monitor/.module-experts/场景视图专家` | `apm`、`bkmonitor`、`apm-web`、`monitor-web`、`performance` |
| 外部API集成专题 | `/root/bk-monitor/.module-experts/外部API集成专题` | `bkmonitor`（人工指认，范围 `bkmonitor/api/`） |
| 性能场景专家 | `/root/bk-monitor/.module-experts/性能场景专家` | `bkmonitor`、`monitor-web`、`performance` |
| 数据源查询构造专家 | `/root/bk-monitor/.module-experts/数据源查询构造专家` | `apm`、`bkmonitor`、`metadata`、`rum` |

> 关联按专家资产文本里出现的模块名/slug 机械判定；「未关联」不代表无关（专家名可能用中文业务名，与代码标识无字面重叠）。

## 5. 待确认（1 → 已复核）

| 类型 | 位置 | 内容 | 复核结论 |
|------|------|------|----------|
| 默认命名表名（框架规范） | 183 张 | 未显式 `db_table` 的模型 | **已核对成立**：Django 默认命名 `{app_label}_{模型小写}`；核对 `label` 覆盖——仅 `packages/weixin/core` 覆盖为 `weixin_core`（其 `BkWeixinUser` 显式声明 `db_table="bk_weixin_user"`），其余模块 label 与目录名一致。表名可信。 |

## 6. 未归属说明

### 6.1 顶层 `core/` 公共包

顶层公共包 `core/`（drf_resource、errors、prometheus、statistics、unit…）：**不是 Django app**，无 apps.py；`from core.*` 全仓 1062 个文件，其中 `core.drf_resource` 已按导入路径归入 `core.drf_resource`（drf-resource 模块），其余不归属任何模块

> 影响：「改 core/ 下的东西」无法通过本索引反查（它不是模块）；`core.drf_resource` 的引用已归入 `drf-resource`。

### 6.2 其他未归属代码

| 路径 | 是什么 | 为何不是模块 |
|------|--------|--------------|
| `packages/apm_trace/` | 挂在 `/trace/` 的纯路由包（`urls.py` + `views.py`） | 无 `apps.py` / `models.py`，不进 `INSTALLED_APPS` |
| `config/` | Django 配置与角色（`role/{web,api,worker}.py` → 不同 `INSTALLED_APPS` 子集） | 配置而非应用 |
| `blueapps` / `monitor_adapter` / `version_log` / `notice` | 外部依赖或平台内置 app（非本仓源码） | 代码不在本仓 |

## 7. 挂载前缀口径（读前缀列前必看）

索引的「挂载前缀」列 = **全仓 `urls*.py` 里的路径声明**（应用**内**的子路由前缀 + 被 include 时的挂载点），**不含父级拼装**。对外真实路径 = 根 `urls.py` 挂载 + 应用内子前缀。

| 模块 | 根 `urls.py` 挂载（`urls.py:59-88`） | 例：真实对外路径 |
|------|--------------------------------------|------------------|
| `monitor-web` | `/rest/v2/`、`/query-api/rest/v2/` | 前缀 `/commons` → `/rest/v2/commons/...`（与前端 `rest/v2/commons/*` 对应） |
| `apm-web` | `/apm/`、`/apm_log_forward/`（log_proxy） | 前缀 `/profile_api` → `/apm/profile_api/...` |
| `fta-web` | `/fta/` | 前缀 `/alert` → `/fta/alert/...` |
| `rum-web` | `/rum/` | 前缀 `/metric` → `/rum/metric/...` |
| `monitor-api` | `/rest/v1/` | — |
| `ai-whale` | `/ai_whale/` | — |
| `core`（weixin） | `/weixin/` | — |
| `calendars` | `/`（根，与 `monitor_adapter` 同挂） | — |
| `kernel-api` | **动态**：`kernel_api/urls.py:55` 由 router 拼前缀（v4） | 前缀列显示 `-`；查具体路径看该文件 |
| 非本仓：`apm_trace` `/trace/`、`notice` `/notice/`、`account` `/account/` | — | — |

> 全局前缀：`config` 未设置 `setGlobalPrefix` 类配置 → 「（未探测到）」；根 `urls.py` 直接挂载各应用。

## 8. 语义标注与历史缺陷记录

本节由 `temp/be-index-bkmonitor-build.py` 追加（**只做语义标注，不做机械修正**）：模块中文职责、专家人工指认、未归属说明、前缀口径、待确认复核。

| # | 历史缺陷（已在 `scan_backend.py` v2.1.0 修复） | 位置（修复前） | 影响 |
|---|------------------------------------------|----------------|------|
| 1 | **幽灵表**：基类含 `model` 即当模型 + 4000 字符窗口兜底扫到邻居类 `db_table` | `:932,936` | 32 张假表（`metadata_spacemanager`、`monitor_api_basedictobj`…） |
| 2 | **「被依赖」恒为空**：用 AppConfig 类名匹配包名 | `build_dependents()` | 「改这个模块影响谁」静默答不出（24/24 模块为空） |
| 3 | **`core` 同名歧义**：`app_names` 取 basename（顶层 `core/` vs `packages/weixin/core`） | `:915,1044` | 微信模块凭空 19 个被依赖；嵌套 app 拿不到依赖边 |
| 4 | **`--check` 不看 `exclude`** | `run_check()` | 前端改动误报后端索引过期 |
| 5 | **`--emit-tree` 吞 `--format json --out`** | `:1861-1869` | JSON 静默不生成 |
| 6 | **`expertsDir` 按 cwd 解析** | `merge_config()` | 同一声明从不同目录调用，专家关联 10 → 0 |
| 7 | **上层声明覆盖 CLI `--root`**（可把范围放大到祖先目录） | `find_config()` + `merge_config()` | 实测 24→31 模块，混入整仓其它工程 |

> 历史缺陷已在 `scan_backend.py` v2.1.0 修复（含 `--check` 的 exclude pathspec、`--emit-tree` 与 `--out` 并存、`expertsDir` 声明目录基准）；后处理脚本已同步简化为纯标注。
> 重建顺序见 `/root/bk-monitor/.fe-index/INDEX.md`「重建」节。
