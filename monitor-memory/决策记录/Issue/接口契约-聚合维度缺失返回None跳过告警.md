---
groupPath: 决策记录/Issue
relation: 接口契约-聚合维度缺失返回None跳过告警
exportedAt: "2026-08-31T03:09:42.907Z"
---
【决策记录｜Issue 聚合维度缺失时指纹返回 None，跳过该告警而非降级聚合】
- 分类：接口契约
- 动机：避坑（维度凑不齐的告警若降级聚合，会混入不相关的 Issue 池，污染聚合语义）
- 决策：gen_issue_fingerprint 遍历 sorted(aggregate_dimensions) 时，任一维度取值为 None 或空串立即返回 None；调用方据此跳过该告警，不创建也不关联任何 Issue。空 aggregate_dimensions 是唯一例外，退化为 count_md5([strategy:{id}]) 的一策略一 Issue catch-all 路径
- 背景约束：同一具体问题的判定依赖完整维度组合，缺一维就无法确认是同一个问题
- 被否决方案：维度缺失时用空值占位继续计算，否决理由为会让不同维度完整度的告警算出同一指纹
- 已知代价：告警静默不聚合——策略配置了告警中不存在的聚合维度时，该策略下所有告警都不会产生 Issue 且不报错，排查成本高
- 重新评估触发条件：需要维度缺失的可观测手段（当前只在指纹层静默跳过）
- 关联代码：gen_issue_fingerprint @ alarm_backends/service/fta_action/issue_processor.py
- 证据来源：Wiki《Issue 聚合引擎》「关键设计决策」表（维度缺失返回 None、空 aggregate_dimensions 退化为 catch-all）；C0 已知问题 1
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 3