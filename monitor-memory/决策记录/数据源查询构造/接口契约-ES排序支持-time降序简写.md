---
groupPath: 决策记录/数据源查询构造
relation: 接口契约-ES排序支持-time降序简写
exportedAt: "2026-08-31T02:15:35.033Z"
---
【决策记录｜数据源查询构造 ES 排序支持 -time 降序简写】
- 分类：接口契约
- 动机：一致性（与 Django ORM 及本模块其它查询入口的负号字段降序写法保持统一）
- 决策：ES compiler 的 _parser_order_by 支持三种排序写法：负号 time（单字段带前导负号）解析为 time 降序；单字段无前缀为升序；带空格的 field desc 形式按空格拆分
- 背景约束：调用方（尤其从 ORM 侧迁移过来的代码）习惯用负号字段名表示降序
- 被否决方案：无（未找到相关记录）
- 已知代价：字段名本身含前导负号的边缘场景会被误判为降序（实践中字段名不含负号）
- 重新评估触发条件：出现字段名含负号的排序需求
- 关联代码：_parser_order_by @ data_source/backends/elastic_search/compiler.py；process_sort_fields @ data_source/utils/query.py
- 证据来源：commit d66983ce0c（ESDataQuery 支持 order_by 的 -time 格式）；代码注释（compiler.py：支持 -time 转为 time 降序；utils/query.py docstring：原始排序字段列表如负号 time 与 name 转为 time desc 与 name）
- 完整上下文：.module-experts/数据源查询构造专家/C5-关键决策.md 决策 9