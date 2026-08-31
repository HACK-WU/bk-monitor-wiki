---
groupPath: 决策记录/告警查询
relation: 架构设计-可组合查询管线与query_fields白名单
exportedAt: "2026-08-31T03:18:06.719Z"
---
【决策记录｜告警查询 可组合查询管线加 query_fields 白名单：新增可查询字段必须注册】
- 分类：架构设计
- 动机：可维护性（新增查询维度不需要改管线，只改声明式配置）
- 决策：查询管线固定为 get_search_object 到 add_conditions 到 add_query_string 到 add_ordering 到 add_pagination 到可选 add_overview 与 add_aggs 到 execute；所有可搜索字段必须在 AlertQueryTransformer.query_fields 中用 QueryField 声明（field 展示名、display 中文名、es_field、agg_field、is_char、searchable、alias_func）
- 背景约束：add_conditions 与 add_query_string 的字段映射全部来自该白名单；它是 AlertQueryTransformer 的翻译中心
- 被否决方案：按 ES 字段直接查询（不做映射），否决理由为展示字段名与 ES 字段名不一致（如 ip 与 event.ip），且无聚合字段与值翻译能力
- 已知代价：新增可查询字段必须同时维护 query_fields，否则前端字段查不到（实现层技术债已列）；searchable=False 的纯计算字段不进 ES，需走 alias_func
- 重新评估触发条件：字段映射改为从元数据自动生成（可移除手工注册）
- 关联代码：query_fields 与 AlertQueryTransformer @ packages/fta_web/alert/handlers/alert.py；QueryField、BaseQueryTransformer、build_query_string_q、add_conditions @ handlers/base.py
- 证据来源：代码注释（base.py：可供查询的ES字段配置；NESTED_KV_FIELDS：例如 "tags.": "event.tags"）；实现层 02-实现.md（新增可查询字段必须在此注册；查询管线高度可组合，新增查询维度通常只需扩展 query_fields 与 conditions 支持，无需改动管线本身）
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 12