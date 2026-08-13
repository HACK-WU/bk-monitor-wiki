---
groupPath: 关联关系/告警屏蔽
relation: ShieldStatusChecker-AlertShieldConfigShielder-ShieldObj
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] ShieldStatusChecker 状态检测器 与 AlertShieldConfigShielder 屏蔽器/ShieldObj 匹配结果
强度：必改——改 AlertShieldConfigShielder 的匹配逻辑或 ShieldObj.is_match 返回结构时，ShieldStatusChecker.check 必须跟着改；改 ShieldStatusChecker 的状态更新逻辑，Shielder/ShieldObj 不用管
原因：ShieldStatusChecker 调用 AlertShieldConfigShielder 检测告警屏蔽状态，根据匹配结果更新 AlertDocument 的 is_shielded/shield_id/shield_left_time 字段，并触发解除屏蔽通知

源端（状态检测器）:
- `ShieldStatusChecker.check(alert)` @ `bkmonitor/alarm_backends/service/alert/manager/checker/shield.py`
- `ShieldStatusChecker.push_actions()` @ `bkmonitor/alarm_backends/service/alert/manager/checker/shield.py`（QoS 限流后 create_actions.delay 异步推送解除通知）

目标端（屏蔽器+匹配对象）:
- `AlertShieldConfigShielder(alert)` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/saas_config.py`（初始化时完成全部匹配：ShieldCacheManager 加载→ALERT_SHIELD_SNAPSHOT 缓存查→未命中则遍历 AlertShieldObj.is_match）
- `AlertShieldConfigShielder.is_matched()` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/saas_config.py`（优先级链：GlobalShielder→HostShielder→shield_objs 非空）
- `AlertShieldObj.is_match(alert)` @ `bkmonitor/alarm_backends/service/converge/shield/shield_obj.py`（时间+维度双校验）
- `AlertShieldConfigShielder.get_shield_left_time()` / `list_shield_ids()` 供状态检测器使用