---
groupPath: 关联关系/告警分派
relation: getSubmitParams-fta_assign提交体-分派引擎
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] RuleData.getSubmitParams 提交体 与 后端 fta/assign 接口与分派引擎
强度：必改——改提交体任一字段名/结构/语义（user_groups / conditions / actions / alert_severity / additional_tags / is_enabled / settings.public_conditions）时，后端序列化器与分派引擎必须连带评估；改后端内部实现（响应结构与语义不变）前端不用管
原因：前端以 getSubmitParams 生成 batchUpdate / matchDebug 的 rules[] 提交体，后端 fta/assign 持久化并由 AssignInfoEnricher 在告警构建链消费执行；且 matchDebug 与 batchUpdate 必须使用同一份 debugData（源码注释「此为调试数据，保存时也用此数据」）

前端端：
- RuleData.getSubmitParams @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/typing/index.ts
- batchUpdate / matchDebug 调用点 @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/components/debugging-result.tsx

后端端：
- fta/assign/rule_operate/batch_update/ 与 match_debug/（fta 应用）
- AssignInfoEnricher（docstring 告警分派动作）@ bkmonitor/alarm_backends/service/alert/enricher/rule_assign.py

证据：grep 实证（AssignInfoEnricher 源码与测试；debugging-result.tsx 注释与 handleSave 实现）