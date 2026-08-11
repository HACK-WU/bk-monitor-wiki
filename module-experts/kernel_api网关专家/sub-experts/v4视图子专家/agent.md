# v4 API 视图子专家

**一句话职责**：kernel_api 对外 v4 API 层——`views/v4/` 下 40+ 文件的 `ResourceViewSet` 与独立 Resource，是当前内核 API 主版本（告警/策略/事件/日志/Issue/APM/RPC 等）。

**负责的模块**：`bkmonitor/kernel_api/views/v4/`（40 个 .py）。

**何时找这个专家**：
- 需要新增/修改 v4 对外 endpoint
- 排查某个 `/api/v4/xxx/` 接口的行为
- 理解 v4 视图如何复用内部 Resource 与挂载 app
- 告警事件中心 / 策略 / 日志 / Issue 等 v4 接口问题

**契约层就绪**：`C0 + C1 + C2` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约 / C2-使用流程；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`kernel_api/tests/`（test_alert_mcp / test_issue_v4 等）间接覆盖；⚠️ 依赖外部环境。

**所属专家**：[kernel_api 网关专家](../../agent.md)
**出处行**：生成日期 2026-08-06，git commit：未提交（工作区）
