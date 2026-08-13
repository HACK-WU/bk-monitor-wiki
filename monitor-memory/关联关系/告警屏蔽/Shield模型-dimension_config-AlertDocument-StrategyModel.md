---
groupPath: 关联关系/告警屏蔽
relation: Shield模型-dimension_config-AlertDocument-StrategyModel
exportedAt: "2026-08-13T11:42:33.568Z"
---
[强关联] Shield 模型 dimension_config 结构 与 AlertDocument/StrategyModel 逻辑引用
强度：必改——改 AlertDocument 维度字段结构或 StrategyModel ID 命名时，ShieldObj._calculate_alert_dimension 和 handle_alert 必须跟着改；改 dimension_config JSON 结构，序列化器和 handle_* 都要适配
原因：Shield 的 dimension_config 通过 JSON 字段中的 ID 关联 AlertDocument（_alert_id）和 StrategyModel（strategy_id），是逻辑引用非外键，字段变更级联影响维度提取和匹配

源端（Shield 模型 dimension_config）:
- `Shield.dimension_config` @ `bkmonitor/bkmonitor/models/base.py`（JSON 字段，结构随 category 变化）
- alert 类型: dimension_config._alert_id 引用 AlertDocument.id
- strategy 类型: dimension_config.strategy_id 引用 StrategyModel.id
- dimension 类型: dimension_config._strategy_id 重命名后不参与匹配
- scope 类型: dimension_config 含 scope_type+target（service_instance_id/bk_target_ip/bk_topo_node/dynamic_group）

目标端（逻辑引用模型）:
- `AlertDocument` @ `bkmonitor/documents/alert.py`（alert 类型屏蔽创建时更新 is_shielded=True）
- `StrategyModel` @ `bkmonitor/bkmonitor/models/base.py`（strategy 类型屏蔽引用策略 ID）
- `Shield.status` 计算属性: 根据 is_enabled 和 end_time 动态计算 SHIELDED/EXPIRED/REMOVED