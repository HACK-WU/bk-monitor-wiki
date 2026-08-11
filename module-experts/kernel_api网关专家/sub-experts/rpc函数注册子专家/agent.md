# RPC 函数注册子专家

**一句话职责**：kernel_api 的 RPC 函数注册与执行层——`KernelRPCRegistry` 注册"函数"（admin 运维巡检 / bkm-cli 只读命令 / 平台信息），经 `KernelRPCResource` 统一暴露；含 bkm-cli op 白名单与租户推断。

**负责的模块**：`bkmonitor/kernel_api/rpc/`（registry.py / tenant.py / bkm_cli_registry.py + functions/ 子包：admin 31 文件、bkm_cli 18 文件、biz_scene / info / metadata / resources）。

**何时找这个专家**：
- 新增/修改内核 RPC 函数（admin.* 运维巡检、bkm-cli.* 只读命令、平台信息）
- 调用 `KernelRPCResource`（`func_name + params` 协议，含 `__meta__` 渐进披露）
- bkm-cli op_id 白名单映射与审计元数据
- 排查 RPC 调用租户推断（`inject_bk_tenant_id`）
- 排查 `未找到可调用函数` 错误

**契约层就绪**：`C0 + C1 + C2` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约 / C2-使用流程；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`rpc/tests/` 22 文件（test_admin_rpc 137KB / test_bkm_cli_* 系列）；⚠️ 依赖外部环境（Django settings 初始化）。

**所属专家**：[kernel_api 网关专家](../../agent.md)
**出处行**：生成日期 2026-08-06，git commit：未提交（工作区）
