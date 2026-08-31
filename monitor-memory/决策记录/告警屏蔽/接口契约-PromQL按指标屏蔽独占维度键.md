---
groupPath: 决策记录/告警屏蔽
relation: 接口契约-PromQL按指标屏蔽独占维度键
exportedAt: "2026-08-31T02:32:04.254Z"
---
【决策记录｜告警屏蔽 PromQL 策略的按指标屏蔽：独占维度键加专用条件类，不并入 metric_id】
- 分类：接口契约
- 动机：避坑（按标准指标建立的屏蔽对引用同一底层指标的 PromQL 策略不生效，用户以为屏蔽了实际没屏蔽）
- 决策：新增 PromqlAwareMetricIdCondition 作为 metric_id 维度专用条件，等值匹配命中即短路；失败后把屏蔽配置的标准 metric_id 换算成 PromQL 指标名（bk_monitor.system.io.util 转 bkmonitor:system:io:util 或 system:io:util），按 token 边界在原始表达式中搜索，多指标表达式命中任一即命中。原始 PromQL 表达式承载在独立告警维度键 _promql_expressions 上
- 背景约束：PromQL 策略的 metric_id 是整段查询表达式（get_metric_id 对 prometheus 数据源直接返回 promql），与标准指标 bk_monitor.xxx 集合交恒为空；产品语义是屏蔽这个指标，实现却按查询身份字符串比较
- 被否决方案：commit body 明确列出四条：把原始表达式并入 metric_id 维度，否决理由为会让以 metric_id 为 key 的条件多看到一个值，eq、include、issuperset 可能由不命中变命中即屏蔽范围被动扩大，独立键以下划线开头零影响；反方向解析 PromQL 抽取指标名再转标准 metric_id，否决理由为两段式 data_label:field 需查 MetricListCache 才能还原结果表，会把 DB 查询引入屏蔽匹配路径；依赖 QueryConfig.metric_id 做匹配，否决理由为 CharField(128) 截断成 promql[:125] 加省略号，指标名可能整个落在截断之外（实测 4 维度聚合表达式指标名结束于偏移 105，再多一个聚合维度即被切掉）；加长该字段，否决理由为截断是字段约束下的有意兜底
- 已知代价：token 边界限定为不匹配字母数字下划线冒号（避免异数据源同名误命中、更长指标名部分命中、截断残缺前缀命中）；仅在等值失败后才进入新增分支，换算结果按配置 lru_cache
- 重新评估触发条件：PromQL 表达式中出现无法用 token 边界判定的指标命名形式；或出现该命中未命中
 的漏屏蔽反馈
- 关联代码：PromqlAwareMetricIdCondition、PROMQL_EXPRESSION_DIMENSION @ converge/shield_conditions.py；ShieldObj._parse_dimension_config 与 _calculate_alert_dimension @ converge/shield/shield_obj.py；build_promql_metric_names @ bkmonitor/utils/metric_id.py
- 证据来源：commit 719abff350（body 的问题、改动、边界与取舍、性能、测试五段，含全部被否决方案与实测偏移量数据）
- 完整上下文：.module-experts/告警屏蔽专家/C5-关键决策.md 决策 3