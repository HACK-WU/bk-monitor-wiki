# 内部 Resource 复用子专家

**一句话职责**：kernel_api 的"批发场景"内部 Resource 层——`resource/` 下的 Resource 不直接暴露前端，而是被 `views/` 的 ViewSet 或 MCP/AI 请求在 `perform_request` 中复用；含 operation 运营指标体系。

**负责的模块**：`bkmonitor/kernel_api/resource/`（28 文件 + operation/ 子目录），含 MCP 告警/日志/APM/事件、日志提取、K8s、AI 制品仓库、运营指标等。

**何时找这个专家**：
- 复用告警/日志/事件等内部查询能力（批发场景）
- 新增一个被多 ViewSet 复用的 Resource
- MCP/AI 请求接入（alert.py 的 MCP 系列 Resource）
- operation 运营指标查询（ListOperationMetricsResource 等）
- 排查日志搜索 / 日志提取 / K8s candidates 查询问题

**契约层就绪**：`C0 + C1 + C2` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约 / C2-使用流程；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`kernel_api/tests/` 6 个测试覆盖（test_alert_mcp / test_log_search / test_log_extract / test_scene_log_search_resource / test_k8s_resource_candidates）；⚠️ 依赖外部环境。

**所属专家**：[kernel_api 网关专家](../../agent.md)
**出处行**：生成日期 2026-08-06，git commit：未提交（工作区）
