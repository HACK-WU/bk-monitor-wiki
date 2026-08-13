---
groupPath: 关联关系/告警屏蔽
relation: ShieldManager-Shielder-ShieldObj
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] ShieldManager 调度入口 与 Shielder 屏蔽器组/ShieldObj 匹配对象
强度：必改——改 ShieldManager.shield 的屏蔽器链顺序或 Shielder 接口时，所有 Shielder 子类和 ShieldObj 必须跟着改；改 ShieldObj.is_match 签名/行为，Shielder 不用管
原因：ShieldManager.shield() 按优先级链式执行 GlobalShielder → AlertShieldConfigShielder → AlarmTimeShielder，AlertShieldConfigShielder 内部创建 AlertShieldObj 执行匹配，链路变更级联影响所有屏蔽器

源端（调度入口）:
- `ShieldManager.shield(action_instance, alerts=None)` @ `bkmonitor/alarm_backends/service/converge/shield/manager.py`
- 返回 (bool, shielder) 或 (False, None)

目标端（屏蔽器+匹配对象）:
- `GlobalShielder` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/saas_config.py`（检查 settings.GLOBAL_SHIELD_ENABLED）
- `AlertShieldConfigShielder` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/saas_config.py`（从 ShieldCacheManager 加载配置，创建 AlertShieldObj 逐条匹配）
- `AlarmTimeShielder` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/saas_config.py`（ActionInstance 时间范围）
- `HostShielder` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/saas_config.py`（CMDB 主机 is_shielding/ignore_monitoring）
- `ShieldObj` / `AlertShieldObj` @ `bkmonitor/alarm_backends/service/converge/shield/shield_obj.py`（维度+时间双校验）
- `BaseShielder` @ `bkmonitor/alarm_backends/service/converge/shield/shielder/base.py`（抽象基类，is_matched 接口）