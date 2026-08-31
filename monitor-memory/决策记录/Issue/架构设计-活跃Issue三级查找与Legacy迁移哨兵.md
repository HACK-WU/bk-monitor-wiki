---
groupPath: 决策记录/Issue
relation: 架构设计-活跃Issue三级查找与Legacy迁移哨兵
exportedAt: "2026-08-31T03:09:42.907Z"
---
【决策记录｜Issue 活跃 Issue 三级查找加 Legacy 迁移哨兵，保证模型切换窗口期可用】
- 分类：架构设计
- 动机：性能取舍（Redis 缓存最快路径）与兼容处理（部署窗口期旧模型 Issue 仍需可命中）
- 决策：_find_active_issue 三级查找：Step 0 Redis 缓存 ISSUE_ACTIVE_CONTENT_KEY；Step 1 ES 标准查找 fingerprint 加 strategy_id 加 ACTIVE_STATUSES，命中回填缓存；Step 2 Legacy 兜底仅当迁移哨兵未完成时查 strategy_id 加 fingerprint=null 加 ACTIVE_STATUSES，read-only 不写缓存不抢锁。迁移由 post_migrate hook 触发 migrate_legacy_active_issues，全局哨兵 ISSUE_LEGACY_MIGRATION_DONE_KEY 标记完成，周期任务负责续命防 30 天 TTL 失效后 processor 退化到 fallback 全索引查询
- 背景约束：fingerprint 改造把模型从 1:1（strategy 对活跃 Issue）升级为按维度组合切分；存量 fingerprint=null 的活跃 Issue 在新模型下无法可靠归属，必须在新代码生效前强制关闭
- 被否决方案：不做迁移让 legacy Issue 自然过期，否决理由为旧模型活跃 Issue 在新模型下无法归属，会与新 Issue 并存造成同策略双活跃
- 已知代价：迁移哨兵是有状态的 Redis key，续命失败会导致 processor 退化到 fallback ES 查询；Legacy 兜底路径只应在短期窗口触达
- 重新评估触发条件：全量环境迁移完成后移除 Step 2 兜底与哨兵续命任务
- 关联代码：_find_active_issue 与 _legacy_migration_done @ issue_processor.py；migrate_legacy_active_issues @ bkmonitor/documents/issue.py；续命任务 @ tasks/issue_tasks.py
- 证据来源：Wiki《Issue 聚合引擎》「活跃 Issue 查找 → 三级策略说明」与「部署窗口期兼容 → Legacy 迁移机制」；migrate_legacy_active_issues 函数 docstring
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 5