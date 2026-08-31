---
groupPath: 决策记录/UnifyQuery查询
relation: 架构设计-类ORM Builder替代dict拼装
exportedAt: "2026-08-31T02:06:21.187Z"
---
【决策记录｜UnifyQuery 后台查询提供类 ORM Builder（QueryConfigBuilder），替代 dict 拼装】
- 分类：架构设计
- 动机：可维护性（各场景重复拼装查询 dict，冗长且易错）
- 决策：新增 unify_query/builder.py，提供 QueryConfigBuilder 与 UnifyQuerySet，复用已有 datasource 模块，让后台以类 ORM 链式调用（table、metric、group_by、conditions）构造查询，再由 Builder 转成 query_list 或 query_configs
- 背景约束：统一查询结构原本由前端拼接参数，后台只负责解析；APM 存在预计算路由、服务接口统计等需要后台对多结果表做聚合查询的复杂场景
- 被否决方案：继续在各场景手写 dict 拼装，否决理由为模块文档明确每个场景的查询都在进行相似的数据结构拼装，过于重复冗长
- 已知代价：新增一层抽象，简单查询也要走 Builder；两套构造方式（直接构造 UnifyQuery 与 Builder）并存
- 重新评估触发条件：Builder 无法表达某类查询（需回退手写 dict）；或 dict 直构方式被完全取代
- 关联代码：QueryConfigBuilder、UnifyQuerySet @ unify_query/builder.py
- 证据来源：模块级文档字符串（builder.py：做了什么——复用已有 datasource 模块支持使用类 ORM 模式进行 UnifyQuery 查询；背景——APM 存在预计算路由、服务接口统计等复杂查询场景；解决了什么问题——每个场景的查询都在进行相似的数据结构拼装，过于重复冗长，基于 unify query_configs 场景进行类 ORM 的封装）
- 完整上下文：.module-experts/UnifyQuery查询专家/C5-关键决策.md 决策 12