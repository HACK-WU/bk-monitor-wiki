---
groupPath: 决策记录/数据源查询构造
relation: 兼容处理-未切换场景复刻日志平台query_string处理
exportedAt: "2026-08-31T02:15:35.032Z"
---
【决策记录｜数据源查询构造 未切换统一查询的场景复刻日志平台的 query_string 处理逻辑】
- 分类：兼容处理
- 动机：一致性（切换前后检索语法行为一致，避免切回原生后检索结果变化）
- 决策：_get_unify_query_string 对未走统一查询的场景复刻 bklog 日志平台的 query_string 构造规则：先 html.unescape，空串返回通配符星号；命中 QUERY_SPECIAL_REGEX（特殊字符集合或 AND、OR、TO、NOT）则原样返回；否则两端包通配符（星号关键词星号）
- 背景约束：日志平台对 query_string 有自己的 DSL 处理规则（含 ES 语法特殊字符判定），原生路径直调其 API，必须在 SaaS 侧还原同样处理，否则检索语义不一致
- 被否决方案：无（未找到相关记录）
- 已知代价：需跟随日志平台实现演进维护（注释中给出 Ref 链接指向 bklog 的 query_string_builder.py）；SaaS 侧与日志平台侧存在隐式行为耦合
- 重新评估触发条件：全部业务切换至统一查询（该兼容分支可移除）；或日志平台调整 query_string 处理规则
- 关联代码：LogSearchTimeSeriesDataSource._get_unify_query_string、QUERY_SPECIAL_REGEX、WILDCARD_PATTERN @ data_source/data_source/__init__.py
- 证据来源：代码注释（背景：没有切换 UnifyQuery 的场景直调日志平台 API，此处对其日志平台对 query_string 的处理逻辑，Ref 指向 bklog 的 query_string_builder.py）；commit ca2a2e841e（优化告警详情日志查询，对 query string 中的特殊字符进行转义）、18ada779fc（修复 SQLCompiler 中对 query_string 转义报错问题）
- 完整上下文：.module-experts/数据源查询构造专家/C5-关键决策.md 决策 8