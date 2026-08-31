---
groupPath: 决策记录/数据源查询构造
relation: 兼容处理-cmdb层级表走bk_sql临时方案
exportedAt: "2026-08-31T02:15:35.032Z"
---
【决策记录｜数据源查询构造 cmdb 层级表查询走 bk_sql 直查计算平台，代码注释标注为临时方案】
- 分类：兼容处理
- 动机：一致性（与统一查询侧的 cmdb 层级判定保持一致）
- 决策：数据源构造阶段，若 table 含 _cmdb_level 后缀则剥离该后缀并调用 to_bk_data_rt_id 转成计算平台结果表，用 bk_sql 直查；同时 UnifyQuery.use_unify_query 对「cmdb 层级查询加表名命中 BKDATA_CMDB_LEVEL_TABLES 白名单」的组合直接返回 False 走原生路径，两条路径判定逻辑刻意保持一致
- 背景约束：cmdb 层级聚合表由计算平台侧维护，统一查询当前不支持该查询形态
- 被否决方案：无（未找到相关记录）
- 已知代价：被代码注释标注为临时方案，注释写明「后续此逻辑去掉，直接将结果表传递给 unify-query 即可」；当前需维护 BKDATA_CMDB_LEVEL_TABLES 白名单与表名后缀约定
- 重新评估触发条件：统一查询支持直接查询 cmdb 层级结果表（即注释所述后续此逻辑去掉的时机），届时需同步移除 use_unify_query 中的豁免分支
- 关联代码：BkdataTimeSeriesDataSource 表名转换分支 @ data_source/data_source/__init__.py；UnifyQuery.use_unify_query 的 cmdb 层级豁免分支 @ data_source/unify_query/query.py；BKDATA_CMDB_LEVEL_TABLES @ config/default.py
- 证据来源：代码注释（通过 is_cmdb_level_query 判定是否查询 cmdb 层级表，和 unify-query 判定逻辑保持一致；如果是层级表查询则转到计算平台查询；后续此逻辑去掉，直接将结果表传递给 unify-query 即可；在 UnifyQuery.use_unify_query 判定中，如果是 cmdb-level 查询并且在白名单 BKDATA_CMDB_LEVEL_TABLES 里会走到这个逻辑）；config 注释（强制使用数据平台查询的 cmdb 层级表）；commit 79f2823bac（补齐 cmdb 层级查询判定逻辑注释）
- 完整上下文：.module-experts/数据源查询构造专家/C5-关键决策.md 决策 6