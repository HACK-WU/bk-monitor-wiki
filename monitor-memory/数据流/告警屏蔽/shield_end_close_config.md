---
groupPath: 数据流/告警屏蔽
relation: shield_end_close_config
exportedAt: "2026-09-15T01:51:10.486Z"
---
【数据流｜shield_end_close_config（告警 extra_info 结构）】
- 实体类型：数据结构（Alert 的 extra_info 内嵌，非独立存储）
- 结构：{shield_id: int, window_begin: int, window_end: int}（窗口边界为 inclusive 的 epoch 秒）
- 生产方：CloseShieldMatcher._match @ converge/shield/close.py（接管时随 alert.update_extra_info 写入）
- 主要消费方：check_shield_end_close_finished @ alert/manager/shield_tasks.py——只消费 shield_id（定位归属屏蔽）；window_begin / window_end 当前无消费方，仅作排障溯源（到期判定以 DB 当前配置实时计算为准）
- 业务用途：托管告警的归属溯源，是关闭任务定位 owner shield 的唯一依据
- 详细流向：见 .module-experts/告警屏蔽专家/implementation/03-数据流转.md