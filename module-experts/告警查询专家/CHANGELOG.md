# 变更日志

> 由 expert-team 初始化，expert-lookup 增量更新时写入。

## 2026-07-27 - 重建（新格式）
- 由 expert-team 重建为「契约层 + 实现层」分离的新格式
- 迁移旧实现层文档至 `implementation/`（01-架构 / 02-实现 / 03-数据流转 / 05-接口 / 06-测试）
- 新增契约层：`C0-使用总览.md`、`C1-能力契约.md`、`C2-使用流程.md`
- 实现层基于 git commit：310f13e（源码快照）

## 2026-07-27 - 补充 AlertQueryTransformer 说明
- 在 `implementation/02-实现.md` 新增「查询字符串翻译器（AlertQueryTransformer）」章节：字段白名单 `query_fields`、嵌套 KV、`assign_tags` 回退、`VALUE_TRANSLATE_FIELDS` 值翻译、`visit_search_field`/`visit_word` 特殊分支，及 en locale 下 `action_id` 失效缺陷。
- `02-实现.md` 目录与「关键类与函数」表同步补充 `AlertQueryTransformer`。
- `03-数据流转.md` 参数变换说明增加交叉引用。
