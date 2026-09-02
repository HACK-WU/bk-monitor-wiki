---
groupPath: 专题记忆/Issue
relation: IssueAggregationProcessor 聚合引擎
exportedAt: "2026-09-01T08:43:03.576Z"
---
IssueAggregationProcessor 是告警→Issue 的聚合入口，在 fta_action 告警处理链路中执行。每条告警触发一次 process()，根据策略配置的聚合维度计算指纹，三级查找活跃 Issue，不存在则加锁创建。新建后异步派发 LLM 标题任务。

## 核心流程
1. 配置校验：issue_config.is_enabled + alert_levels 匹配 + conditions 过滤
2. 指纹计算：gen_issue_fingerprint(strategy_id, agg_dims, data_dims)
3. 三级查找活跃 Issue：Redis 缓存 → ES 标准查找 → Legacy 兜底
4. 不存在则创建（分布式锁保护，按 fingerprint 粒度）
5. 告警关联：AlertDocument.issue_id UPSERT
6. 新建后异步 dispatch_llm_title

## 关键符号
- 符号: `IssueAggregationProcessor(alert, strategy).process() -> bool`
- 位置: `alarm_backends/service/fta_action/issue_processor.py`
- 返回: True=成功关联/创建，False=未进入 Issue 池（策略未开启/级别不匹配/缺维度/抢锁失败）
- 异常: 内部捕获 ES/Redis 异常并打日志，不阻断 fta_action 主流程

## 指纹计算
- 符号: `gen_issue_fingerprint(strategy_id, aggregate_dimensions, data_dimensions) -> str|None`
- 位置: `alarm_backends/service/fta_action/issue_processor.py`
- 算法: count_md5，payload=["strategy:{id}"] + sorted dims 的 "{key}={value}"
- 维度缺失/为空/全空白 → 返回 None（告警不进入任何 Issue）
- 空 aggregate_dimensions 退化为按 strategy_id 隔离
- 值做 str(...).strip() 归一化
- ⚠️ 维度取值来自 alert.event.extra_info.origin_alarm.data.dimensions，不是 alert.dimensions

## 并发控制
- 锁粒度: 按 fingerprint
- 获取方式: SET NX EX 一次性尝试
- 释放安全: Lua 脚本 Token 锁，只释放自己持有的锁
- 获取失败: 跳过该告警，不阻塞主链路

## 高基数防护
- 单策略活跃 Issue 数超阈值时: 仅 metric + warning，不阻塞新建
- ES count 结果缓存 Redis，5 分钟 TTL（±20% jitter）

## 双写策略
- 先 ES 后 Redis（ES 为唯一持久化存储）
- ES 写入失败重试 1 次，仍失败抛异常
- Redis 操作 fail-silent（只 log 不阻塞）
- 活跃 Issue 写缓存，非活跃删缓存