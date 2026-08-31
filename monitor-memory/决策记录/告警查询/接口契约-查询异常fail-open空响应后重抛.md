---
groupPath: 决策记录/告警查询
relation: 接口契约-查询异常fail-open空响应后重抛
exportedAt: "2026-08-31T03:17:23.270Z"
---
【决策记录｜告警查询 查询异常 fail-open：返回空响应但携带部分结果后重抛】
- 分类：接口契约
- 动机：可用性（ES 抖动或 DSL 错误时整页 500 的体验劣于降级展示）
- 决策：AlertQueryHandler.search 捕获异常后 logger.exception 记录 search alerts error，用 make_empty_response 构造空响应，把已构造的 result 挂到 exc.data 后重新抛出
- 背景约束：告警列表是高频主入口，短时故障不应直接返回错误页
- 被否决方案：异常直接向上抛（整页 500），无相关记录；现状选择的是降级数据加保留异常，让前端既能展示又能感知
- 已知代价：前端看到的是无数据而不是报错，极易被误判为查询条件写错；排查必须看日志 search alerts error 或 exc.data；异常仍会抛，若调用方未处理仍可能 500
- 重新评估触发条件：出现因 fail-open 掩盖真实故障的反馈；或需要把降级状态显式返回给前端
- 关联代码：AlertQueryHandler.search @ packages/fta_web/alert/handlers/alert.py
- 证据来源：代码实现（try 与 except 加 make_empty_response 加 exc.data = result 加 raise exc）；C0 已知坑 4；实现层结论段
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 4