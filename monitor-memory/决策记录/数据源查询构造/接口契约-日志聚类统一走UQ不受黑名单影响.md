---
groupPath: 决策记录/数据源查询构造
relation: 接口契约-日志聚类统一走UQ不受黑名单影响
exportedAt: "2026-08-31T02:15:04.764Z"
---
【决策记录｜数据源查询构造 日志聚类场景统一走统一查询，不受黑名单影响】
- 分类：接口契约
- 动机：一致性（聚类结果只在统一查询侧存在，原生路径查不到）
- 决策：LogSearchTimeSeriesDataSource.switch_unify_query 中，若结果表名以 _clustered 结尾（由 _get_unify_query_table_suffix 从条件中解析），直接返回 True，短路后续黑名单判定
- 背景约束：日志聚类产生的结果表结构与原始索引不同，只有统一查询后端支持
- 被否决方案：无（未找到相关记录）
- 已知代价：黑名单无法对聚类场景止损，业务命中黑名单时普通日志查询走原生，聚类查询仍走统一查询
- 重新评估触发条件：原生路径支持聚类结果表查询；或聚类场景出现需要按业务豁免的故障
- 关联代码：LogSearchTimeSeriesDataSource.switch_unify_query 与 _get_unify_query_table_suffix @ data_source/data_source/__init__.py
- 证据来源：commit 3bef9aeffb（日志聚类场景统一通过 UnifyQuery 查询）；代码实现（_clustered 后缀短路分支）
- 完整上下文：.module-experts/数据源查询构造专家/C5-关键决策.md 决策 4