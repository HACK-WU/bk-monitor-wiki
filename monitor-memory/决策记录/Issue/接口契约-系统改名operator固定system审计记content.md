---
groupPath: 决策记录/Issue
relation: 接口契约-系统改名operator固定system审计记content
exportedAt: "2026-09-01T08:35:17.233Z"
---
【决策记录｜Issue 系统自动改名的 operator 固定为 system，审计人另记 content】
- 分类：接口契约
- 动机：避坑（把审计人写进 operator 会污染下游是否为系统改名的判据）
- 决策：rename 增加可选 content 参数用于写入 NAME_CHANGE 活动日志。LLM 标题生成路径下 operator 固定为 system（保证是否系统改名的判据稳定），非 system 的真实发起人标识另记于 content，而不是写进 operator。用户手工改名不传 content
- 背景约束：下游功能（如是否系统改名判断、标题来源判别）依赖 operator 取值稳定；而审计需要知道真实发起人
- 被否决方案：把真实发起人写进 operator，否决理由为 docstring 原文「避免把审计人写进 operator 污染下游标题来源判别」
- 已知代价：审计信息分散在两个字段（operator 与 content），查询活动日志时需按场景解析
- 重新评估触发条件：活动日志模型增加独立的 source 或 initiator 字段（可移除 content 承载审计的约定）
- 关联代码：IssueDocument.rename @ bkmonitor/documents/issue.py；IssueActivityType.NAME_CHANGE @ constants/issue.py
- 证据来源：rename 方法 docstring 的 content 参数说明段
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 9