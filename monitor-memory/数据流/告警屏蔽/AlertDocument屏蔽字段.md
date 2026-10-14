---
groupPath: 数据流/告警屏蔽
relation: AlertDocument屏蔽字段
exportedAt: "2026-09-15T01:51:10.486Z"
---
【数据流｜AlertDocument 屏蔽字段（ES）】
- 实体类型：ES 文档字段（AlertDocument）
- 结构：is_shielded(Boolean)、shield_id(list)、shield_left_time、shield_end_close(Boolean，close 型屏蔽接管标记)
- 生产方：AddShieldResource（alert 类型建屏蔽时置 is_shielded=True）；ShieldStatusChecker.check（回写 is_shielded / shield_id / shield_left_time）；CloseShieldMatcher._match（置 shield_end_close=True + is_shielded=True + shield_id=[id]）@ converge/shield/close.py；check_shield_end_close_finished（关闭时 set_end_status → CLOSED 并落盘）@ alert/manager/shield_tasks.py
- 主要消费方：前端告警列表/详情展示；告警查询链路（is_shielded 过滤）；check_abnormal_alert / check_blocked_alert（ES 查询排除 shield_end_close）@ alert/manager/tasks.py；shield_tasks 扫描（status=ABNORMAL 且 shield_end_close=True）
- 业务用途：告警的屏蔽状态标记与托管归属，供展示、查询过滤与状态机分流
- 详细流向：见 .module-experts/告警屏蔽专家/implementation/03-数据流转.md