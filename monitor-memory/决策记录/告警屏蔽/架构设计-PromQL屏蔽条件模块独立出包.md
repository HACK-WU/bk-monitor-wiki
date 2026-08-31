---
groupPath: 决策记录/告警屏蔽
relation: 架构设计-PromQL屏蔽条件模块独立出包
exportedAt: "2026-08-31T02:32:04.254Z"
---
【决策记录｜告警屏蔽 PromQL 屏蔽条件模块放在 shield 包外，保证可独立导入与测试】
- 分类：架构设计
- 动机：可测试性（独立模块无需 Django 环境即可单测）
- 决策：新增 alarm_backends/service/converge/shield_conditions.py（包外），而不是放进 shield 包内
- 背景约束：shield 包的 __init__ 会加载 ShieldManager 及全部 shielder，导入即依赖 Django settings；而屏蔽匹配逻辑本身只依赖 bkmonitor.utils
- 被否决方案：放进 shield 包内，否决理由为导入即依赖 Django settings，无法脱离 DB、Redis 与 app registry 单独导入与测试
- 已知代价：屏蔽条件相关代码分散在两个包，需靠命名与文档维持归属认知
- 重新评估触发条件：shield 包的导入副作用被消除（可独立导入）
- 关联代码：shield_conditions.py @ alarm_backends/service/converge/；shield/__init__.py
- 证据来源：commit 719abff350（body：放在 shield 包外，该包 __init__ 会加载 ShieldManager 及全部 shielder，导入即依赖 Django settings，独立模块只依赖 bkmonitor.utils 可单独导入与测试；测试段落说明 19 项测试无需数据库、Redis 或 app registry）
- 完整上下文：.module-experts/告警屏蔽专家/C5-关键决策.md 决策 4