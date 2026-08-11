# 认证与安全子专家

**一句话职责**：kernel_api 网关的请求认证与授权——apigw JWT、API Token（Bearer）、MCP 请求三种认证，以及用户自动创建与租户上下文注入。

**负责的模块**：`bkmonitor/kernel_api/middlewares/authentication.py`（27KB，单文件）+ `config/role/api.py` 中认证相关配置。

**何时找这个专家**：
- 排查内核 API 认证失败（403 / JWT 验签失败 / Token 无效 / MCP 权限拒绝）
- 新增 API Token 授权范围（`ApiAuthToken` namespaces）
- 新增 MCP 服务权限动作映射
- 理解 apigw JWT 公钥获取与缓存
- 排查用户自动创建 / 多租户租户 ID 不匹配

**契约层就绪**：`C0 + C1` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`middlewares/authentication.py` **无对应单测文件**（测试缺口，见 06-测试.md）；所属父专家整体 ⚠️ 依赖外部环境。

**所属专家**：[kernel_api 网关专家](../../agent.md)
**出处行**：生成日期 2026-08-06，git commit：未提交（工作区）
