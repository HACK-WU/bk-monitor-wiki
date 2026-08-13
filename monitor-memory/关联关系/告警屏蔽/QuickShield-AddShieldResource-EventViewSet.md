---
groupPath: 关联关系/告警屏蔽
relation: QuickShield-AddShieldResource-EventViewSet
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] QuickShield 快捷屏蔽适配层 与 AddShieldResource 完整屏蔽入口/EventViewSet 认证
强度：必改——改 AddShieldResource 的参数签名/handle_* 逻辑时，QuickShield 的 handle_scope/handle_strategy/handle_event 必须跟着改；改 EventViewSet 认证方式，QuickShield 不用管
原因：QuickShield 是适配层，把移动端简单输入（type+event_id+end_time）翻译成 add_shield 需要的复杂 dimension_config，同时绕过 CSRF（NoCsrfSessionAuthentication）和 IAM（get_permissions 返回 []），参数变更级联影响适配逻辑

源端（快捷屏蔽适配层）:
- `QuickShield` @ `bkmonitor/packages/weixin/event/resources.py`（handle_scope/handle_strategy/handle_event 自动推导 dimension_config）
- `QuickAlertShield` @ `bkmonitor/packages/fta_web/alert/resources.py`（token 验权，逐条调 add_shield）
- `EventViewSet` @ `bkmonitor/packages/weixin/event/views.py`（NoCsrfSessionAuthentication，get_permissions 返回 []）

目标端（完整屏蔽入口）:
- `AddShieldResource` @ `bkmonitor/packages/monitor_web/shield/resources/backend_resources.py`
- QuickShield 调用 resource.shield.add_shield(is_quick=True, shield_notice=False, cycle_config={type:1})
- QuickAlertShield 调用 resource.shield.add_shield(category=alert, end_time=now+3h)
- 关键差异：quick_shield 不更新 ES is_shielded、不检查重复、不校验 MANAGE_DOWNTIME