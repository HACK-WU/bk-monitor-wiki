---
groupPath: 决策记录/告警查询
relation: 性能取舍-track_total_hits用10000非True
exportedAt: "2026-08-31T03:18:06.718Z"
---
【决策记录｜告警查询 搜索主链路 track_total_hits 用 10000 而非 True】
- 分类：性能取舍
- 动机：优化（track_total_hits=True 会强制 ES 精确全量计数，大索引下开销显著）
- 决策：搜索主链路 search_object.params(track_total_hits=10000)；page_size 上限 5000（serializers 约束）；导出走 export_alert（全量 scan，page_size=0 语义）
- 背景约束：列表展示只需要够用的总数精度，超过 1 万的精确总数对分页体验无实际价值
- 被否决方案：track_total_hits=True（精确计数），否决理由为 commit 明写避免大索引强制全量计数
- 已知代价：total 超过 1 万时不精确（C0 能力边界已声明）；依赖总数做业务判断的调用方会拿到截断值
- 重新评估触发条件：出现需要超过 1 万的精确总数的诉求；或 ES 集群规格变化使精确计数不再成为瓶颈
- 关联代码：AlertQueryHandler.search_raw @ packages/fta_web/alert/handlers/alert.py；page_size 约束 @ serializers.py；get_bucket_count（仍用 True）@ resources.py
- 证据来源：commit a564b3f73c（perf: track_total_hits=True 改为 10000，避免大索引强制全量计数）；C0 能力边界与已知坑 5
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 6