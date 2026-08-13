---
groupPath: 关联关系/告警屏蔽
relation: AddShieldResource-serializers-Shield模型
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] AddShieldResource 后端 CRUD 与 SHIELD_SERIALIZER 序列化器/Shield 模型
强度：必改——改 SHIELD_SERIALIZER 映射表或序列化器 DimensionConfig 字段定义时，AddShieldResource 的 handle_* 方法必须跟着改；改 Shield 模型字段时，序列化器和 Resource 都要适配
原因：AddShieldResource.perform_request 按 category 从 SHIELD_SERIALIZER 选序列化器校验，再分发到 handle_scope/handle_strategy/handle_alert/handle_dimension 组装 dimension_config，序列化器字段结构变更级联影响维度处理逻辑

源端（后端 CRUD）:
- `AddShieldResource` / `BulkAddAlertShieldResource` / `EditShieldResource` / `DisableShieldResource` / `ShieldListResource` @ `bkmonitor/packages/monitor_web/shield/resources/backend_resources.py`
- `handle_scope` / `handle_strategy` / `handle_alert` / `handle_dimension` @ `bkmonitor/packages/monitor_web/shield/resources/backend_resources.py`

目标端（序列化器+模型）:
- `SHIELD_SERIALIZER` 映射表 + `ScopeSerializer`/`StrategySerializer`/`EventSerializer`/`AlertSerializer`/`DimensionSerializer` @ `bkmonitor/packages/monitor_web/shield/serializers.py`
- `Shield` 模型 @ `bkmonitor/bkmonitor/models/base.py`（alarm_shield 表，含 category/scope_type/dimension_config/cycle_config/notice_config/is_enabled 等字段）
- `ShieldCategory`/`ShieldStatus`/`ShieldCycleType`/`ScopeType` 常量 @ `bkmonitor/constants/shield.py`