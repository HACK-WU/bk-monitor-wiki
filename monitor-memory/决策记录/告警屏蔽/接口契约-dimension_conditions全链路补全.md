---
groupPath: 决策记录/告警屏蔽
relation: 接口契约-dimension_conditions全链路补全
exportedAt: "2026-08-31T02:32:39.254Z"
---
【决策记录｜告警屏蔽 dimension_conditions 全链路补全，含 regex 与 nregex 正则过滤】
- 分类：接口契约
- 动机：避坑（此前传入的 dimension_conditions 被 serializer 静默丢弃或引擎层不消费，屏蔽范围不符合预期）
- 决策：DimensionConditionSlz 提取到顶层复用，ScopeSerializer、EventSerializer、AlertSerializer 均新增 dimension_conditions 字段；handle_scope 与 handle_alert 透传；ShieldObj._parse_dimension_conditions 增加 SCOPE 与 ALERT 分支，并对单条解析失败做 try 与 except 防御（配合永不命中占位条件）；移动端 QuickShield 新增 dimension_conditions 入参并与屏蔽类型无关地合并进 shield_params
- 背景约束：维度屏蔽需要维度键名白名单（dimension_keys）与维度值匹配方式（dimension_conditions，支持 eq、regex、nregex 条件树）两层能力，此前只有前者
- 被否决方案：无（未找到相关记录）
- 已知代价：BulkAddAlertShieldResource 暂未透传 dimension_conditions（commit 中标注 TODO）；2026-07-30 之前创建的屏蔽配置不含该字段
- 重新评估触发条件：批量屏蔽场景需要维度过滤条件（届时补齐 BulkAddAlertShieldResource 透传）
- 关联代码：ScopeSerializer、EventSerializer、AlertSerializer、DimensionConditionSlz @ monitor_web/shield/serializers.py；handle_scope、handle_alert @ monitor_web/shield/resources/backend_resources.py；_parse_dimension_conditions @ converge/shield/shield_obj.py
- 证据来源：commit 1f109fb8cb（body 列出 serializer、backend_resources、shield_obj、微信 QuickShield 四处改动，并注明已知限制 BulkAddAlertShieldResource 暂未透传已标注 TODO）；C0 已知坑 13
- 完整上下文：.module-experts/告警屏蔽专家/C5-关键决策.md 决策 9