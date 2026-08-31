---
groupPath: 决策记录/UnifyQuery查询
relation: 接口契约-query_log剥离聚合与函数
exportedAt: "2026-08-31T02:05:56.777Z"
---
【决策记录｜UnifyQuery query_log 强制剥离聚合与函数】
- 分类：接口契约
- 动机：一致性（原始日志查询不需要聚合语义）
- 决策：_query_log_using_unify_query 对 query_list 的每一项覆盖 function 为空列表、field_name 为空字符串、time_aggregation 为空字典，再调用 api.unify_query.query_raw
- 背景约束：日志原始记录查询取的是文档本身，聚合与函数无意义且会改变返回结构
- 被否决方案：无（未找到相关记录）
- 已知代价：统一查询路径下 query_log 返回的 total 恒为 0，精确总数只在原生查询分支返回
- 重新评估触发条件：统一查询后端在 query_raw 中支持返回总数
- 关联代码：UnifyQuery._query_log_using_unify_query @ unify_query/query.py
- 证据来源：代码注释（query.py：原始日志查询，无需聚合及函数）；代码实现（query.update 覆盖 function、field_name、time_aggregation）
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 8