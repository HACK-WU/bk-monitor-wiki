# 数据平台专家

**一句话职责**：封装 BK-Monitor 对数据平台链路的调用——BKData 计算平台（数据接入/查询/DataFlow）、监控元数据（metadata，走 bk-monitor 自身网关）、统一查询（unify-query，自建 HTTP 网关）、日志检索（bk-log-search）、AIOps 模型推理（aiops_sdk）。

**负责的模块**：`bkmonitor/api/{bkdata,metadata,unify_query,log_search,aiops_sdk}/default.py`。

**何时找这个专家**：
- 查询监控数据（`api.bkdata.query_data`、`api.unify_query.*`）
- 查询/创建元数据（结果表、数据源、事件分组）
- 日志检索与索引集管理（`api.log_search.*`）
- AIOps 模型推理（时序/异常检测/离群）
- 理解 token/user 双鉴权、SaaS 认证注入（UseSaaSAuthInfoMixin）

**契约层就绪**：`C0 + C1` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`api/` 目录无测试 → 06-测试 标注「该模块无测试」。

**所属专题**：[外部 API 集成专题](../topic.md)（T0 总览见 [T0-专题总览](../T0-专题总览.md)）
**出处行**：生成日期 2026-08-07，git commit：未提交（工作区）
