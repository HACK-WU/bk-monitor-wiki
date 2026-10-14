---
groupPath: 关联关系/告警屏蔽
relation: CloseShieldMatcher-告警builder-AlertShieldObj
exportedAt: "2026-09-15T01:48:14.173Z"
---
[强关联] close 型屏蔽接管链路 与 告警写入链路
强度：必改——改 close 型屏蔽的接管语义（end_policy 判定、窗口口径、多命中择一规则），告警 builder 的调用点与 AlertShieldObj 的 close 时间分支必须连带改；改 AlertShieldObj.is_match 的时间语义会影响所有 close 屏蔽的接管结果
原因：CloseShieldMatcher 依赖 AlertShieldObj 的 end_policy=close 分支（begin_time 落窗判定）与 _parse_cycle_config 的业务时区 matcher；builder/processor.py 的两处 take_over 调用点决定了接管发生在哪一阶段（早于常规 enrichment）

接管侧：
- CloseShieldMatcher.take_over / _take_over / _match @ alarm_backends/service/converge/shield/close.py
- close_time_matcher / matching_window / business_timezone @ alarm_backends/service/converge/shield/window.py

匹配对象侧：
- AlertShieldObj.__init__（business_timezone_name 注入）/ _parse_cycle_config / is_match（close 分支）@ alarm_backends/service/converge/shield/shield_obj.py

调用点侧：
- AlertProcessor（存量告警更新路径、新建告警路径）@ alarm_backends/service/alert/builder/processor.py