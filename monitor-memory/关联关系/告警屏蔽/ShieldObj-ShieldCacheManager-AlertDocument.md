---
groupPath: 关联关系/告警屏蔽
relation: ShieldObj-ShieldCacheManager-AlertDocument
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] ShieldObj 引擎匹配核心 与 ShieldCacheManager 缓存/AlertDocument ES 文档
强度：必改——改 ShieldCacheManager 缓存结构/序列化方式时，ShieldObj/ShieldStatusChecker 必须跟着改；改 AlertDocument 维度字段结构时，AlertShieldObj._calculate_alert_dimension 必须跟着改
原因：引擎层从 Redis 缓存读取屏蔽配置构建 ShieldObj，从 AlertDocument 提取告警维度做匹配，缓存结构或文档字段变更级联影响整个匹配链路

源端（引擎匹配）:
- `ShieldObj.is_match` / `_parse_dimension_config` / `_clean_dimension` / `_parse_dimension_conditions` @ `bkmonitor/alarm_backends/service/converge/shield/shield_obj.py`
- `AlertShieldObj._calculate_alert_dimension` / `get_dimension` @ `bkmonitor/alarm_backends/service/converge/shield/shield_obj.py`
- `ShieldStatusChecker.check` @ `bkmonitor/alarm_backends/service/alert/manager/checker/shield.py`

目标端（缓存+ES文档）:
- `ShieldCacheManager.get_shields_by_biz_id` / `refresh` @ `bkmonitor/alarm_backends/core/cache/shield.py`（Redis key=shield.biz_{bk_biz_id}）
- `AlertDocument` @ `bkmonitor/documents/alert.py`（is_shielded/shield_id/shield_left_time 字段由 ShieldStatusChecker 更新）
- `ALERT_SHIELD_SNAPSHOT` 缓存（key=strategy_id+alert_id，存匹配到的屏蔽配置 ID 列表）