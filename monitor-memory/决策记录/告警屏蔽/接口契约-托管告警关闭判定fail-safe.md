---
groupPath: 决策记录/告警屏蔽
relation: 接口契约-托管告警关闭判定fail-safe
exportedAt: "2026-09-15T01:46:33.578Z"
---
【决策记录｜托管告警关闭判定一律 fail-safe】
- 分类：接口契约
- 动机：避坑（判定失败时误关闭告警 → 静默终结真实告警，用户再也看不到；漏关只是告警多留一段时间）
- 决策：close 型屏蔽托管的告警，关闭的唯一前提是该屏蔽被明确判定为已不在屏蔽中（active is False）；归属屏蔽缺失（Shield.origin_objects.in_bulk 查不到）、时间配置不可读（shield_is_active 抛异常）、SQL 异常三类情形一律保留告警不关闭
- 背景约束：屏蔽结束关闭是替用户把告警收尾的动作，判错方向决定后果；origin_objects 含软删除记录，因此查不到无法区分明确删除与查询异常
- 被否决方案：
  - 查不到归属即视为已删除并关闭：否决理由 —— 软删除与数据缺失无法区分，误关会静默终结真实告警
- 重新评估触发条件：出现「屏蔽已结束但告警长期不关闭」的反馈累计 ≥ 2 次
- 关联代码：check_shield_end_close_finished / shield_is_active @ alarm_backends/service/alert/manager/shield_tasks.py
- 证据来源：代码注释（shield_tasks.py：「原始 manager 包含软删除记录。缺失并不等价于明确删除，保留告警并告警日志。SQL 异常直接抛出，整批不执行关闭」）