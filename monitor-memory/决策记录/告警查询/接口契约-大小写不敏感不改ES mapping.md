---
groupPath: 决策记录/告警查询
relation: 接口契约-大小写不敏感不改ES mapping
exportedAt: "2026-08-31T03:18:06.719Z"
---
【决策记录｜告警查询 包含匹配的大小写不敏感用 case_insensitive=true，不改 ES mapping】
- 分类：接口契约
- 动机：一致性（UI 模式的包含与不包含应符合用户对大小写不敏感的直觉）
- 决策：UI 模式 include 与 exclude 的 wildcard 查询统一设置 case_insensitive=true，保持现有 *value* 子串、多值 OR 与排除语义
- 背景约束：历史数据已按现有 mapping 写入，改 mapping 需要重建索引
- 被否决方案：调整 ES mapping 或为大小写不敏感新增 analyzer，否决理由为 commit 明写无需调整 Elasticsearch mapping 或迁移历史数据
- 已知代价：依赖 ES 的 wildcard case_insensitive 参数支持；wildcard 查询有额外开销
- 重新评估触发条件：ES 版本升级导致该参数行为变化；或 wildcard 性能问题需改为 ngram 或 normalizer 方案
- 关联代码：include 与 exclude 条件构造 @ packages/fta_web/alert/handlers/base.py
- 证据来源：commit a5326a3bee（body 变更说明三条，含无需调整 Elasticsearch mapping 或迁移历史数据与 94 passed 测试）
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 7