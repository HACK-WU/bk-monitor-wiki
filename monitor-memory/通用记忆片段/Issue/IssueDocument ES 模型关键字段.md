---
groupPath: 通用记忆片段/Issue
relation: IssueDocument ES 模型关键字段
keywords: [IssueDocument, IssueActivityDocument, fingerprint, merge_status, activity]
exportedAt: "2026-06-23T08:08:27.268Z"
---
# IssueDocument ES 模型关键字段

## 入口
- `bkmonitor/documents/issue.py` → `IssueDocument`、`IssueActivityDocument`

## IssueDocument 关键字段
```python
class IssueDocument(Document):
    id = field.Keyword()           # Issue 唯一标识
    event_id = field.Keyword()     # 关联 Event ID
    title = field.Text()           # 标题（全文搜索）
    description = field.Text()     # 描述（全文搜索）
    fingerprint = field.Keyword()  # 指纹，用于关联相似 Issue（合并的关联键）
    merge_status = field.Keyword() # 合并状态：active / split / member
    status = field.Keyword()       # 状态（new/ack/resolved等，走 StatusTranslator）
    priority = field.Keyword()     # 优先级（P1/P2/P3等，走 PriorityTranslator）
    assignee = field.Keyword()     # 处理人
    dimensions = field.Object(...) # 影响范围维度（多维 OR 条件查询）
    create_time = field.Date()
    update_time = field.Date()
    bk_biz_id = field.Integer()    # 业务 ID（IAM 权限校验）
```

## IssueActivityDocument 设计
```python
class IssueActivityDocument(Document):
    id = field.Keyword()
    issue_id = field.Keyword()     # 关联 Issue
    operator = field.Keyword()     # 操作人
    activity_type = field.Keyword() # 操作类型（create/update/merge/split/assign等）
    content = field.Text()         # 操作内容描述
    create_time = field.Date()
```

## 特殊方法
- `issue_merge(parent, issue_ids)`：类方法，批量合并 Issue，修改 `merge_status` 和关联关系
- `issue_split()`：实例方法，拆分已合并的 Issue
- `save()`：继承自 ES Document，自动索引

## merge_status 状态机
| 状态 | 含义 |
|------|------|
| `active` | 正常 Issue，未被合并也未合并其他 |
| `member` | 已被合并到其他 Issue（子 Issue）|
| `split` | 从合并状态拆分出来 |

## 依赖
- Elasticsearch Document（django-elasticsearch-dsl 或类似库）
- `ImpactDimensionsTranslator`（dimensions 字段翻译）

## 使用场景
- 新增 Issue 字段时，需同步更新 Document 定义、Serializer、QueryFieldMap
- 合并/拆分操作需理解 `merge_status` 状态流转
- 全文搜索（title/description）依赖 `Text` 类型字段
