---
groupPath: 决策记录/告警屏蔽
relation: 接口契约-通知幂等Redis锁与调度层遗留TODO
exportedAt: "2026-08-31T02:32:39.253Z"
---
【决策记录｜告警屏蔽 通知幂等用 Redis 锁（开始 set、结束 delete、无锁不发结束），但任务调度层仍未加锁】
- 分类：接口契约
- 动机：避坑（定时扫描周期性执行，同一屏蔽的开始或结束通知被重复发送）
- 决策：ShieldObj.check_and_send_notice 中开始通知前 set 锁键为 __lock__ 并带 ttl；can_send_end_notice 先检查锁是否存在，无锁直接返回 False（即只有发过开始通知的屏蔽才可能发结束通知）；结束通知发出后 delete 锁
- 背景约束：屏蔽通知由 Celery 定时任务周期性扫描触发（check_and_send_shield_notice 分片为 do_check_and_send_shield_notice），同一配置会被反复扫描到
- 被否决方案：无（未找到相关记录）
- 已知代价与遗留：shield/tasks.py 仍保留 TODO 注释「确定是否需要加锁，防止重复通知」，幂等只在 ShieldObj 层，任务调度层（分片重复执行、多实例并发扫描）未加锁；锁有 TTL，屏蔽时长超过 TTL 的边界场景需额外注意
- 重新评估触发条件：出现重复通知的线上反馈；或屏蔽周期可能超过锁 TTL 时需评估锁有效期
- 关联代码：ShieldObj.check_and_send_notice、can_send_end_notice、notice_lock_key @ converge/shield/shield_obj.py；do_check_and_send_shield_notice @ converge/shield/tasks.py
- 证据来源：代码实现（shield_obj.py 的 set、get、delete 锁逻辑）；shield/tasks.py 第 55 行 TODO 注释
- 完整上下文：.module-experts/告警屏蔽专家/C5-关键决策.md 决策 7