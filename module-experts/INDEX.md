# 模块专家包索引
> 由 expert-team 自动维护

## 项目全局（共享资产）
- 资产：PROJECT.md（项目信息/技术栈/架构形态/核心功能/核心服务清单/配套服务关系/架构图/数据流向图/运行环境）
- 说明：所有专家共享的项目全局上下文，创建/使用专家前建议先读
- 维护：expert-team 首次创建/发现全局信息时更新；expert-lookup 使用中发现变化时受限更新

## UnifyQuery查询专家（职责摘要见 agent.md）
- 模块根：bkmonitor/bkmonitor/data_source/unify_query/
- 生成日期：2026-07-27  git commit：host-view-api-split
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 05-接口
- 子专家：无

## 数据源查询构造专家（职责摘要见 agent.md）
- 功能域：load_data_source 工厂、14 组合映射、路径决策、查询描述构造
- 生成日期：2026-07-27  git commit：host-view-api-split
- 契约层：C0-使用总览, C1-能力契约
- 实现层：implementation/01-架构, 02-实现
- 子专家：无

## 场景视图专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/scene_view/
- 重建日期：2026-07-27  git commit：ca831622
- 匹配关键词：场景视图, 视图配置, 内置视图, 主机进程列表, GetHostProcessListResource, memRss, memUsage, 进程指标, mem_usage_pct, PageListResource, 主机拓扑详情, 分屏
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型
- 子专家：无
- 专用技能：skills/add-builtin-scene-view/

## 性能场景专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/performance/
- 重建日期：2026-07-27  git commit：916585db
- 匹配关键词：主机性能, 主机列表, 主机详情, 拓扑节点, 进程状态, 主机指标, HostPerformanceResource, memUsage, mem_usage, psc_mem_usage, cpu_usage, disk_in_use, 内存使用率
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型
- 子专家：无
- 专用技能：skills/add-host-performance-field/

## 告警查询专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/fta_web/alert/
- 重建日期：2026-07-27  git commit：310f13e
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程（暂无 C3）
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 05-接口, 06-测试
- 子专家：无
- 专用技能：skills/query-alert/

## Issue 专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/fta_web/issue/
- 生成日期：2026-07-31
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程, C4-数据流向与消费
- 实现层：implementation/01-架构, 02-实现
- 匹配关键词：Issue, 告警聚合, 状态机, TAPD, LLM标题, IssueAggregationProcessor, IssueDocument, sync_issue_alert_stats, 合并, 拆分
- 子专家：
  - **Issue API 子专家**（sub-experts/issue-api/）：RESTful接口/权限/序列化/批量操作
  - **Issue 查询子专家**（sub-experts/issue-query/）：ES查询构建/时间分片/排序
  - **Issue 状态聚合子专家**（sub-experts/issue-state-aggregation/）：状态机/聚合引擎/周期任务/LLM标题
  - **TAPD 集成子专家**（sub-experts/tapd-integration/）：关联管理/OAuth授权/解绑重绑

## 告警屏蔽专家（职责摘要见 agent.md）
- 模块根：bkmonitor/packages/monitor_web/shield/ + bkmonitor/alarm_backends/service/converge/shield/
- 生成日期：2026-07-28（测试文档补充：2026-08-03）
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程
- 实现层：implementation/01-架构, 02-实现, 03-数据流转, 04-模型, 05-接口, 06-测试
- 测试：test/known-failures.md
- 匹配关键词：告警屏蔽, 屏蔽, scope, strategy, alert, dimension, ShieldObj, AddShieldResource, ShieldCacheManager, 快捷屏蔽, QuickShield, dimension_conditions, 屏蔽通知, HostShielder, ShieldDetectManager
- 子专家：无

## kernel_api 网关专家（职责摘要见 agent.md）
- 模块根：bkmonitor/kernel_api/
- 生成日期：2026-08-06  git commit：未提交（工作区）
- 匹配关键词：kernel_api, API网关, ResourceViewSet, ResourceRouter, JWT鉴权, API Token, MCP认证, apigw, KernelRPCRegistry, RPC函数, ApiRenderer, 字段映射, 内部Resource复用, 批发场景, v2/v3/v4 API
- 契约层：C0-使用总览, C1-能力契约, C2-使用流程, C4-数据流向与消费
- 实现层：implementation/01-架构, 02-实现, 05-接口, 06-测试, 07-运维
- 测试状态：⚠️ 依赖外部环境（kernel_api/tests/ 7 文件 + rpc/tests/ 22 文件）；test/known-failures.md（暂无实测已知失败）
- 子专家：
  - **认证与安全子专家**（sub-experts/认证与安全子专家/）：JWT/API Token/MCP 认证、用户自动创建，匹配关键词：认证, JWT, Token, MCP, 中间件, apigw, 授权, 用户
  - **RPC 函数注册子专家**（sub-experts/rpc函数注册子专家/）：KernelRPCRegistry 函数注册、bkm-cli op 白名单、租户推断，匹配关键词：RPC, KernelRPCRegistry, bkm-cli, op, 租户推断, admin巡检, 只读命令
  - **内部 Resource 复用子专家**（sub-experts/内部resource复用子专家/）：批发场景内部 Resource、operation 运营指标，匹配关键词：Resource复用, 批发场景, MCP告警, 日志检索, 日志提取, 运营指标, OperationMetric
  - **v4 API 视图子专家**（sub-experts/v4视图子专家/）：对外 v4 API 视图集与独立 Resource，匹配关键词：v4视图, ViewSet, endpoint, 告警事件中心, Issue, 策略, 屏蔽

## 外部 API 集成专题（专题）
- 模块根：bkmonitor/api/
- 生成日期：2026-08-07  git commit：未提交（工作区）
- 匹配关键词：外部API, APIResource, 第三方系统, ESB, cmdb, bkdata, kubernetes, tapd, node_man, gse, metadata, unify_query, base_url, get_headers, render_response_data, Basic Auth, Bearer Token, 蓝鲸网关
- 专题层：T0-专题总览（T1 暂无）
- 专家清单：
  - **基础平台与网关专家**（蓝鲸 PaaS 基础：用户/租户/插件/权限/网关公钥/文档）
    - 匹配关键词：bk_login, bk_paas, bk_plugin, iam, bk_apigateway, CommonBaseResource, 租户, 用户, apigw公钥, 插件凭证
    - 契约层：C0-使用总览, C1-能力契约
    - 实现层：implementation/01-架构, 02-实现, 06-测试
  - **CMDB 与容器资源专家**（CMDB/kubernetes/bcs 系列/node_man 资源与容器数据源）
    - 匹配关键词：cmdb, kubernetes, bcs, bcs_cluster_manager, bcs_storage, node_man, 主机, 拓扑, K8s, 容器, batch_request, CacheResource
    - 契约层：C0-使用总览, C1-能力契约
    - 实现层：implementation/01-架构, 02-实现, 06-测试
  - **数据平台专家**（bkdata/metadata/unify_query/log_search/aiops_sdk 数据链路）
    - 匹配关键词：bkdata, metadata, unify_query, log_search, aiops_sdk, 结果表, 数据源, 统一查询, 日志检索, AIOps, token鉴权
    - 契约层：C0-使用总览, C1-能力契约
    - 实现层：implementation/01-架构, 02-实现, 06-测试
  - **协作与流程专家**（tapd/issue/itsm/cmsi/sops/job/devops/bkchat/bk_incident）
    - 匹配关键词：tapd, issue, itsm, cmsi, sops, job, devops, bkchat, bk_incident, 通知, 审批, 流水线, 缺陷
    - 契约层：C0-使用总览, C1-能力契约
    - 实现层：implementation/01-架构, 02-实现, 06-测试
  - **监控生态专家**（monitor/grafana/apm_api/rum_api/aidev/bmw）
    - 匹配关键词：monitor, grafana, apm_api, rum_api, aidev, bmw, 仪表盘, APM, RUM, LLM, 常驻任务
    - 契约层：C0-使用总览, C1-能力契约
    - 实现层：implementation/01-架构, 02-实现, 06-测试
