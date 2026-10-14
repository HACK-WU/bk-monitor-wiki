---
groupPath: 关联关系/告警屏蔽
relation: Alert-shield_end_close-7个副作用隔离点
exportedAt: "2026-09-15T01:48:14.173Z"
---
[强关联] Alert.shield_end_close 标记 与 7 处副作用消费方
强度：必改——新增/修改托管告警的副作用切断点时，必须同步检查这 7 处；改标记名称或语义时 7 处全部要改；漏掉任一处会让托管告警漏出副作用（发通知/建动作/被状态机终结）
原因：shield_end_close 是跨模块的“接管标记”，消费方分散在通知、分派、复合、动作、状态检查五个子系统，无统一收口点

标记定义侧：
- Alert.shield_end_close 属性 / update() 中的托管分支 / should_send_signal() @ alarm_backends/core/alert/alert.py

消费方（7 处）：
1. Alert.should_send_signal（返回 False）@ core/alert/alert.py
2. AssignInfoEnricher.enrich_alert（跳过分派）@ service/alert/enricher/rule_assign.py
3. BaseAlertProcessor.send_signal（跳过信号下发）@ service/alert/processor.py
4. check_action_and_composite（跳过复合）@ service/composite/tasks.py
5. 动作创建过滤（self.alerts）@ service/fta_action/tasks/create_action.py
6. check_abnormal_alert / check_blocked_alert 查询条件排除 + manager/processor.py 二次过滤 @ service/alert/manager/tasks.py、manager/processor.py
7. 独立扫描入口 @ service/alert/manager/shield_tasks.py