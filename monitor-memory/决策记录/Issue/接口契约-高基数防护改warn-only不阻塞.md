---
groupPath: 决策记录/Issue
relation: 接口契约-高基数防护改warn-only不阻塞
exportedAt: "2026-08-31T03:09:42.907Z"
---
【决策记录｜Issue 高基数防护改为 warn-only，超阈值不阻塞新建】
- 分类：接口契约
- 动机：避坑（原实现触达阈值即阻塞新建，导致超阈值后该策略的告警永久失联）
- 决策：单策略活跃 Issue 数超过 ISSUE_MAX_ACTIVE_PER_STRATEGY 时仅上报 metric 与 warning，不阻塞新建；通过 bkmonitor_issue_fingerprint_blocked{reason=high_cardinality} 速率告警让运维发现。ES count 结果缓存到 Redis，5 分钟 TTL 带正负 20% jitter 打散 thundering herd，缓存 miss 时用 SET NX EX 10s 短锁让一个 worker 探 ES，其他 worker 跳过
- 背景约束：高基数（维度组合爆炸）会拖垮 ES 与聚合链路，但阻塞新建的代价比高计数更严重
- 被否决方案：历史实现为触达阈值时 return False 阻塞新建，否决理由为 Wiki 明写「这会导致超阈值后该策略所有告警永久失联」
- 已知代价：阈值失效后高基数风险靠监控发现而非系统自保护；ES 仍需承受高基数的查询压力
- 重新评估触发条件：出现高基数把 ES 打挂的生产事件（届时需引入真正的限流或降级，而非简单恢复阻塞）
- 关联代码：_check_active_issue_count @ alarm_backends/service/fta_action/issue_processor.py
- 证据来源：Wiki《Issue 聚合引擎》「高基数防护 → 设计决策」段（含历史实现与其否决理由、缓存与短锁参数）
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 4