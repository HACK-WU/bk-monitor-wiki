---
groupPath: 决策记录/UnifyQuery查询
relation: 接口契约-排序用虚拟时间字段_time
exportedAt: "2026-08-31T02:05:27.218Z"
---
【决策记录｜UnifyQuery 排序统一用虚拟时间字段 _time，由统一查询后端按 time_field 替换】
- 分类：接口契约
- 动机：避坑（时间字段硬编码导致排序被静默丢弃或查询报错）
- 决策：get_unify_query_params 的 order_by 未显式传入时默认负号 _time，使用统一查询的虚拟时间字段 _time，而不是各数据源真实时间字段名（如 time 或 dtEventTimeStamp）
- 背景约束：bkdata 与 bklog 等索引以 dtEventTimeStamp 为时间字段，硬编码 time 时统一查询后端要么静默丢弃排序条件降级为不排序，要么命中 keyword 类型导致查询报错
- 被否决方案：按数据源 DEFAULT_TIME_FIELD 取真实字段名拼 order_by，否决理由为跨源场景下硬编码或直取真实字段名不可靠
- 已知代价：依赖统一查询后端的虚拟字段替换能力，后端不替换则排序失效
- 重新评估触发条件：统一查询后端取消虚拟字段 _time 支持；或某数据源的时间字段无法被正确替换
- 关联代码：UnifyQuery.get_unify_query_params @ unify_query/query.py
- 证据来源：代码注释（query.py：使用 unify-query 虚拟时间字段 _time 会按 query_list 中的 time_field 替换为真实时间字段，背景是在 bkdata 与 bklog 等以 dtEventTimeStamp 为时间字段的索引上硬编码为 time 要么被 uq 静默丢弃降级为不排序要么命中 keyword 导致查询报错）
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 3