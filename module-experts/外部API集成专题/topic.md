# 外部 API 集成专题

**一句话职责**：BK-Monitor 访问第三方/内部系统的全部外部 API 调用层——34 个外部系统集成（蓝鲸 PaaS 平台/CMDB/容器/数据平台/协作办公/监控生态），统一基于 `APIResource` 封装。

**专题范围**：`bkmonitor/api/`（34 个系统子目录 + `common/` 公共基类，约 50 个源文件、650KB+）。

**何时找这个专题**：
- 需要调用某个外部系统能力（CMDB 主机查询、bkdata 数据、tapd 缺陷、kubernetes 资源等）
- 新增一个外部系统集成（建 `api/{system}/default.py`）
- 排查第三方调用失败（认证/URL/响应格式/错误包装）
- 理解 `resource.xxx.yyy()` 与 `api.xxx.yyy` 全局入口的差异

**专家清单**：
- **基础平台与网关专家**：bk_login / bk_paas / bk_plugin / iam / bk_apigateway / common / docs —— 蓝鲸 PaaS 基础能力与认证基座
- **CMDB 与容器资源专家**：cmdb / kubernetes / bcs / bcs_cluster_manager / bcs_project / bcs_storage / node_man —— 资源与容器监控数据源
- **数据平台专家**：bkdata / metadata / unify_query / log_search / aiops_sdk —— 数据计算/存储/查询链路
- **协作与流程专家**：tapd / issue / itsm / cmsi / sops / job / devops / bkchat / bk_incident —— 协作办公与流程
- **监控生态专家**：monitor / grafana / apm_api / rum_api / aidev / bmw —— 监控周边系统

**专题就绪**：`T0` 就绪（T0-专题总览.md）

**包含的资产**：T0-专题总览.md + 5 个专家（各含 agent.md + C0/C1 + implementation/）

**出处行**：生成日期 2026-08-07，git commit：未提交（工作区）
