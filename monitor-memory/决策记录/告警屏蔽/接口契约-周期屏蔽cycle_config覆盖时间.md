---
groupPath: 决策记录/告警屏蔽
relation: 接口契约-周期屏蔽cycle_config覆盖时间
exportedAt: "2026-08-31T02:32:39.254Z"
---
【决策记录｜告警屏蔽 周期屏蔽的时间语义：cycle_config 的时分秒覆盖 begin_time 与 end_time 的日期时间】
- 分类：接口契约
- 动机：一致性（周期屏蔽表达的是每天或每周的某段时间，而非一段绝对时间）
- 决策：handle_shield_time 对周期类型不等于 1 的屏蔽配置，用 cycle_config 中的时间部分（begin_time 与 end_time 的时分秒）替换 begin_time 与 end_time 的日期时间部分；单次屏蔽（周期类型等于 1）则按绝对时间处理
- 背景约束：周期屏蔽需要按天或周重复生效，必须把重复的时间片段叠加到具体日期上
- 被否决方案：无（未找到相关记录）
- 已知代价：单次屏蔽与周期屏蔽的时间语义不同，跨类型复用时间字段易出错；历史上有两轮修复（commit 40c0c40403、393ce1df90）
- 重新评估触发条件：周期屏蔽的时间表达改造（如支持多个时间段）
- 关联代码：handle_shield_time @ monitor_web/shield/resources/backend_resources.py
- 证据来源：C0 已知坑 4；commit 40c0c40403（屏蔽相关接口支持时区）、393ce1df90 与 f7c57f65a2（屏蔽时间处理逻辑问题）
- 完整上下文：.module-experts/告警屏蔽专家/C5-关键决策.md 决策 10