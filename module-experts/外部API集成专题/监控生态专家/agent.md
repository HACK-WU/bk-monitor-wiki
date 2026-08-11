# 监控生态专家

**一句话职责**：封装 BK-Monitor 对监控周边系统的调用——监控自身网关（monitor）、Grafana（仪表盘/数据源，含导出工具）、APM（apm_api）、RUM（rum_api）、AI 开发平台（aidev，LLM/知识库）、监控 Worker（bmw 常驻任务）。

**负责的模块**：`bkmonitor/api/{monitor,grafana,apm_api,rum_api,aidev,bmw}/`。

**何时找这个专家**：
- 调用监控自身网关能力（采集配置/拨测/报表/自定义指标，`api.monitor.*`）
- Grafana 仪表盘/数据源/组织管理（`api.grafana.*`）
- APM/RUM 应用与链路查询（`api.apm_api.*` / `api.rum_api.*`）
- LLM 对话 / 知识库问答（`api.aidev.*`）
- APM 预计算常驻任务（`api.bmw.*`）

**契约层就绪**：`C0 + C1` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`api/` 目录无测试 → 06-测试 标注「该模块无测试」。

**所属专题**：[外部 API 集成专题](../topic.md)（T0 总览见 [T0-专题总览](../T0-专题总览.md)）
**出处行**：生成日期 2026-08-07，git commit：未提交（工作区）
