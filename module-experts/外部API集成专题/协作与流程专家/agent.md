# 协作与流程专家

**一句话职责**：封装 BK-Monitor 对协作办公与流程系统的调用——TAPD（缺陷/需求）、Issue（告警聚合）、ITSM（审批单）、cmsi（消息发送）、sops（标准运维）、job（作业平台）、devops（研发流水线）、bkchat（企业微信）、bk_incident（故障管理）。

**负责的模块**：`bkmonitor/api/{tapd,issue,itsm,cmsi,sops,job,devops,bkchat,bk_incident}/default.py`。

**何时找这个专家**：
- 发送通知（邮件/微信/短信/语音/企微机器人，`api.cmsi.*`）
- 创建/查询审批单（ITSM）
- 操作 TAPD（需求/缺陷/任务/webhook）
- 执行作业/流程（job/sops）
- Issue 状态流转（告警聚合）
- 故障管理（bk_incident 诊断面板）

**契约层就绪**：`C0 + C1` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`api/` 目录无测试 → 06-测试 标注「该模块无测试」。

**所属专题**：[外部 API 集成专题](../topic.md)（T0 总览见 [T0-专题总览](../T0-专题总览.md)）
**出处行**：生成日期 2026-08-07，git commit：未提交（工作区）
