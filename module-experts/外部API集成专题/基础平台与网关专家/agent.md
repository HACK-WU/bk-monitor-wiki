# 基础平台与网关专家

**一句话职责**：封装 BK-Monitor 对蓝鲸 PaaS 基础能力的调用——用户/租户（bk_login）、应用（bk_paas）、插件（bk_plugin）、权限中心（iam）、API 网关（bk_apigateway）、文档中心（docs），并提供公共基类 `CommonBaseResource`。

**负责的模块**：`bkmonitor/api/{common,bk_login,bk_paas,bk_plugin,iam,bk_apigateway,docs}/default.py`。

**何时找这个专家**：
- 查询租户/用户/部门（`api.bk_login.*`）
- 获取 apigw 公钥（`api.bk_apigateway.get_public_key`，kernel_api 认证依赖）
- 插件调用（bk_plugin：meta/detail/invoke/schedule）
- 批量实例授权（iam.batch_instance）
- 需要动态 URL 渲染 + 统一错误包装（复用 `CommonBaseResource`）

**契约层就绪**：`C0 + C1` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`api/` 目录无测试 → 06-测试 标注「该模块无测试」。

**所属专题**：[外部 API 集成专题](../topic.md)（T0 总览见 [T0-专题总览](../T0-专题总览.md)）
**出处行**：生成日期 2026-08-07，git commit：未提交（工作区）
