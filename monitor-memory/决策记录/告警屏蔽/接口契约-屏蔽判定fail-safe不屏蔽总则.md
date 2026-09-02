---
groupPath: 决策记录/告警屏蔽
relation: 接口契约-屏蔽判定fail-safe不屏蔽总则
exportedAt: "2026-09-01T08:42:46.387Z"
---
【决策记录｜告警屏蔽 屏蔽判定一律 fail-safe：无法判定时选择不屏蔽（贯穿原则）】
- 分类：接口契约
- 动机：避坑（过度屏蔽导致漏告警，漏告警代价高于多告警）
- 决策：模块内所有无法判定的分支都选择不屏蔽，三处实现方向一致：shield_obj 中 dimension_condition 解析失败替换为永不命中占位条件；shielder 中 HostShielder.is_matched 捕获异常后返回 False（主机屏蔽判定异常时按未屏蔽处理）；shield_conditions 中 PromQL 指标换算或表达式搜索不成立一律返回未命中
- 背景约束：屏蔽是抑制告警的能力，判定失效的方向决定后果，判定失败时若按屏蔽处理会静默吞掉真实告警
- 被否决方案：判定失败时忽略该条件继续匹配（fail-open），否决理由为条件被静默丢弃后屏蔽范围被动扩大等于漏告警，代码注释写明过度屏蔽导致漏告警比屏蔽不生效更危险
- 已知代价：配置写错时表现为屏蔽不生效，排障时易被误认为功能缺陷；失败原因只在日志
- 重新评估触发条件：出现因配置解析失败导致屏蔽不生效且用户无感知的反馈累计大于等于 2 次（届时需考虑在列表页暴露配置健康状态）
- 关联代码：_NeverMatchCondition 与 _parse_dimension_conditions @ converge/shield/shield_obj.py；HostShielder.is_matched @ converge/shield/shielder/saas_config.py；PromqlAwareMetricIdCondition @ converge/shield_conditions.py
- 证据来源：代码注释（_NeverMatchCondition docstring：确保解析失败不会让屏蔽范围被动扩大，过度屏蔽导致漏告警比屏蔽不生效更危险）；commit 719abff350（body：屏蔽范围扩大等于漏告警比屏蔽不生效更危险；换算或搜索不成立一律返回未命中，维持不屏蔽）
- 完整上下文：.module-experts/告警屏蔽专家/C5-关键决策.md 决策 1