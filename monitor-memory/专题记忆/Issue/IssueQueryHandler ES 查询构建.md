---
groupPath: 专题记忆/Issue
relation: IssueQueryHandler ES 查询构建
keywords: [IssueQueryHandler, QUERY_FIELD_MAP, fingerprint]
exportedAt: "2026-07-06T04:01:13.569Z"
---
# IssueQueryHandler ES 查询构建

## 入口
- `packages/fta_web/issue/handlers/issue.py` → `IssueQueryHandler`
- 继承 `BaseBizQueryHandler[IssueDocument]`
- 查询条件继承自：`IssueSearchSerializer` → `BaseSearchSerializer`

## 核心字段映射
```python
QUERY_FIELD_MAP: Dict[str, QueryField] = {
    "id": QueryField("id", field_action=field_value_filter, operator="in"),
    "event_id": QueryField("event_id", field_action=field_value_filter, operator="in"),
    "query": QueryField("query"),   # 全文搜索 title / description
    "fingerprint": QueryField("fingerprint"),
    "merge_status": QueryField("merge_status", AllowBlankString),  # 合并状态过滤
    # 维度过滤
    "assignee": QueryLimitedField("assignee", LimitedStringField, transform=transform_value_filter),  # 按用户名 in 过滤
    "status": QueryLimitedField("status", StatusTranslator, transform=transform_value_filter, exact=True),
    "priority": QueryLimitedField("priority", PriorityTranslator, transform=transform_value_filter),
    "dimensions": QueryField("dimensions", ImpactDimensionsTranslator),  # 多维影响范围，OR 条件
}
```

## 特殊逻辑

### 1. QSearch 查询（关键词模式）
`search/qsearch/` 端点使用 `build_condition_query_v2`：
- 仅搜索当前一天的数据（性能优化）
- `is_merge_process = SHOW_ALL`
- 直接返回 `query_dict`（不走完整 limit/sort/hits 构建）

### 2. 排序规则
- 默认 `_id` 逆序
- 支持 `priority`、`update_time` 等字段

### 3. 合并查询
- `fingerprint` 按指纹精确过滤同名 Issue（合并的关联键）
- `merge_status` 标记合并状态：`active`/`split`/`member`
- `is_merge_process` 在 QSearch 中 = `SHOW_ALL`

## 依赖
- `IssueDocument`（ES 文档模型）
- `BaseQueryTransformer`（查询构建基类）
- `StatusTranslator` / `PriorityTranslator` / `ImpactDimensionsTranslator`

## 使用场景
- 新增 Issue 搜索维度时，需在 `QUERY_FIELD_MAP` 注册 `QueryField`
- 全文搜索（title/description）走 `query` 字段的 `query_string`
