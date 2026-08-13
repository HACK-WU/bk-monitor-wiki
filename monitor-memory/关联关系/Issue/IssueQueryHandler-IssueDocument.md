---
groupPath: 关联关系/Issue
relation: IssueQueryHandler-IssueDocument
exportedAt: "2026-08-13T08:55:36.777Z"
---
[强关联] IssueQueryHandler/IssueQueryTransformer 与 IssueDocument ES 索引结构
强度：必改——改 IssueDocument 的 ES 索引字段定义/映射时，查询处理器和转换器必须跟着改；改查询逻辑，索引结构不用管
原因：查询处理器直接消费 IssueDocument 的 ES 索引字段（含 name.raw、strategy_name.raw、dimension_values、impact_scope 等映射），字段结构变更会导致查询失败

源端（查询层）：
- `IssueQueryHandler` @ `bkmonitor/packages/fta_web/issue/handlers/issue.py`
- `IssueQueryTransformer` @ `bkmonitor/packages/fta_web/issue/handlers/issue.py`
- `SearchIssueResource` / `IssueTopNResource` / `IssueTrendResource` @ `bkmonitor/packages/fta_web/issue/resources.py`

目标端（ES 索引结构）：
- `IssueDocument` @ `bkmonitor/documents/issue.py`
- ES 索引 `bkfta_issue` 字段映射: name(Text raw:Keyword)、strategy_name(text raw)、fingerprint(Keyword)、dimension_values(Flattened)、impact_scope(Flattened)
- 字段映射表: name→name.raw、strategy_name→strategy_name.raw、impact_scope.{dim}→impact_scope.{dim}.instance_list.{id_field}