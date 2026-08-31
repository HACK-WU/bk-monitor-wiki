---
groupPath: 决策记录/场景视图
relation: 性能取舍-视图列表panel_count分级计算
exportedAt: "2026-08-31T01:50:02.299Z"
---
【决策记录｜场景视图列表 panel_count 分级计算：轻量占位面板 + 未覆盖场景返回 0】
- 分类：性能取舍
- 动机：避坑（collect 场景 SceneView 列表慢查询）、避坑（custom_event_* 与 custom_metric_* 未兜底导致 GetSceneViewList 直接报错）
- 决策：CollectBuiltinProcessor.get_view_config 在 params.only_simple_info 为真时返回 N 个占位面板（N 来自 get_simple_panel_count），跳过完整面板渲染与 MetricListCache 查询；get_simple_panel_count 仅对 collect_* 与 plugin_* 场景精确计数，其他场景返回 0
- 背景约束：列表接口只需要有哪些视图加大致面板数；完整渲染需查 MetricListCache 并按业务拼装 panels，成本高
- 被否决方案：所有场景统一走完整渲染计算 panel_count，否决理由为 collect 场景已出现列表慢查询（commit 7eada2ad26）；未覆盖场景抛异常，否决理由为会导致整个列表接口报错（commit 5b8992aff9）
- 已知代价：非 collect_* 与 plugin_* 场景列表的 panel_count 恒为 0，前端需接受无面板数展示
- 重新评估触发条件：产品要求 custom_metric_* 或 custom_event_* 也展示 panel_count；或出现新的列表慢查询场景
- 关联代码：get_simple_panel_count @ scene_view/builtin/collect.py；CollectBuiltinProcessor.get_view_config @ scene_view/builtin/collect.py
- 证据来源：commit 7eada2ad26、5b8992aff9；docstring（collect.py get_simple_panel_count：用于 SceneViewList 仅请求基础信息时避免触发完整面板渲染和 MetricListCache 查询，其他场景直接返回 0）
- 完整上下文：.module-experts/场景视图专家/C5-关键决策.md 决策 8