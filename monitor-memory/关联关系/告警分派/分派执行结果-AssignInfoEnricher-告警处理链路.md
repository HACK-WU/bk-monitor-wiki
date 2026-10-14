---
groupPath: 关联关系/告警分派
relation: 分派执行结果-AssignInfoEnricher-告警处理链路
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] 分派规则配置（后端执行结果）与 告警处理链路（下游消费者）
强度：建议改——改分派规则配置的数据结构或分派动作语义（actions 类型扩展、等级/标签调整语义变化）时，需评估后端分派结果在告警链路的下游消费（告警查询 / 展示 / 后续处理）连带影响；改下游消费逻辑不影响本模块配置面
原因：本模块配置的规则由后端 AssignInfoEnricher 在告警构建链执行，分派结果落到告警处理链路；托管告警（shield_end_close）场景下该富化器被直接跳过（告警屏蔽 7 处副作用隔离点中的第 2 处，见 ki 关联关系/告警屏蔽 的 Alert-shield_end_close-7个副作用隔离点）

配置面：
- AlarmDispatchConfig.handleStartDebug / DebuggingResult @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/

执行面：
- AssignInfoEnricher @ bkmonitor/alarm_backends/service/alert/enricher/rule_assign.py

证据：grep 实证（rule_assign.py 与测试；托管告警跳过逻辑已见于告警屏蔽专家资产与 ki 强关联）