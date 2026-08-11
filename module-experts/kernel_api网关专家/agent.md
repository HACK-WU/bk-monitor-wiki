# kernel_api 网关专家

**一句话职责**：BK-Monitor 对外暴露内核 API 的独立网关角色（api role），通过 v2/v3/v4 三层版本路由向 API 网关/其他系统暴露 monitor 能力，并作为 web（monitor_saas）→ 告警后台（alarm_backends）的中转层。

**负责的模块**：`bkmonitor/kernel_api/`（Django app），含 URL 路由注册、认证中间件、异常处理、字段适配、DB 路由、扩展点、对外 API 视图（views/v2/v3/v4）、内部复用 Resource（resource/）、RPC 函数注册层（rpc/）。

**何时找这个专家**：
- 需要新增/修改对外内核 API（v2/v3/v4 endpoint）
- 排查 API 认证失败（JWT / API Token / MCP 权限）
- 需要调用内核 RPC 函数（KernelRPCRegistry）或 bkm-cli op
- 排查 web → kernel_api 调用链的错误传播、HTTP 状态码、错误码透传
- 需要理解 api 角色与 web/worker 角色的隔离边界
- 需要在 kernel_api 复用某个内部 Resource（批发场景）

**契约层就绪**：`C0 + C1 + C2 + C4` 就绪
- C0-使用总览.md / C1-能力契约.md / C2-使用流程.md / C4-数据流向与消费.md

**子专家清单**：
- **认证与安全子专家**（sub-experts/认证与安全子专家/）：JWT / API Token / MCP 三种认证与授权、用户自动创建
- **RPC 函数注册子专家**（sub-experts/rpc函数注册子专家/）：KernelRPCRegistry 函数注册、bkm-cli op 白名单、租户推断
- **内部 Resource 复用子专家**（sub-experts/内部resource复用子专家/）：resource/ 下批发场景复用 Resource、operation 运营指标
- **v4 API 视图子专家**（sub-experts/v4视图子专家/）：views/v4/ 对外 API 视图集与独立 Resource

**包含的资产**：
- 契约层：C0-使用总览 / C1-能力契约 / C2-使用流程 / C4-数据流向与消费
- 实现层：implementation/01-架构 / 02-实现 / 05-接口 / 06-测试 / 07-运维

**测试状态**：`kernel_api/tests/`（7 文件） + `rpc/tests/`（22 文件）；⚠️ 依赖外部环境（PROJECT.md 标注）。测试运行需 Django settings 初始化（`cd /root/bk-monitor/bkmonitor` + `.venv` + 显式环境变量 + `--override-ini "filterwarnings="`），详见 implementation/06-测试.md；已知失败清单见 [test/known-failures.md](test/known-failures.md)。

**出处行**：生成日期 2026-08-06，git commit：未提交（工作区）
