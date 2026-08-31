---
groupPath: 决策记录/Issue
relation: 架构设计-指纹粒度Redis锁与Token锁防误删
exportedAt: "2026-08-31T03:10:17.255Z"
---
【决策记录｜Issue 并发控制用 fingerprint 粒度 Redis 锁加 Token 锁 Lua 脚本防误删】
- 分类：架构设计
- 动机：避坑（并发创建同一 fingerprint 的 Issue，导致同策略同维度出现多个活跃 Issue）
- 决策：_acquire_lock 按 fingerprint 加锁（不同 fingerprint 互不阻塞），一次性尝试 SET NX EX（失败即返回 None，不等待不重试）；获锁后二次确认无活跃 Issue 才创建；释放走 _TokenLock 的 Lua 脚本，仅当 value 与自身 token 相等才 del
- 背景约束：告警处理是多 worker 并发，同一 fingerprint 的告警可能同时到达；锁 TTL 过期后若直接 del 会误删其他 worker 持有的锁
- 被否决方案：全局锁或按策略加锁，否决理由为不同 fingerprint 互相阻塞、吞吐下降；普通 del 释放锁，否决理由为 TTL 过期后可能误删其他 worker 持有的锁
- 已知代价：抢锁失败即跳过本次聚合（该告警本次不进 Issue），依赖周期任务 backfill_unlinked_alerts 补偿；锁 TTL 内 worker 崩溃需等 TTL 自然过期
- 重新评估触发条件：出现抢锁失败导致告警长期未关联的反馈（需评估补偿任务的覆盖度与时效）
- 关联代码：_acquire_lock 与 _TokenLock @ alarm_backends/service/fta_action/issue_processor.py
- 证据来源：Wiki《Issue 聚合引擎》「并发控制」节（锁粒度、获取方式、释放安全、TTL 表加 Lua 脚本，避免 TTL 过期后误删其他 worker 持有的锁）
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 6