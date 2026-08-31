---
groupPath: 决策记录/Issue
relation: 接口契约-指纹取值源必须origin_alarm维度
exportedAt: "2026-08-31T03:09:42.907Z"
---
【决策记录｜Issue 指纹取值源必须是 origin_alarm.data.dimensions，不能用 alert.dimensions 或 event 顶层】
- 分类：接口契约
- 动机：避坑（维度取值源选错导致聚合维度取不到值，告警不进任何 Issue）
- 决策：指纹计算与 conditions 匹配统一从 origin_alarm.data.dimensions 取值，即 adapter 收编前的原始 record
- 背景约束：issue_config.aggregate_dimensions 的命名层级与原始告警维度严格一致
- 被否决方案：用 alert.dimensions，否决理由为 trigger 阶段会将主机维度收编为 target_type 与 target，命名层级错位；用 event 顶层字段，否决理由为 adapter 已把 bk_host_id、bk_target_ip 等关键字段 pop 走
- 已知代价：取值路径依赖告警文档内部结构，上游 adapter 若调整结构会直接影响聚合
- 重新评估触发条件：告警文档结构调整（需同步评估所有指纹与条件匹配取值点）
- 关联代码：gen_issue_fingerprint 与 conditions 匹配分支 @ alarm_backends/service/fta_action/issue_processor.py
- 证据来源：Wiki《Issue 聚合引擎》「取值源选型说明」三条（含两条否决理由）
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 2