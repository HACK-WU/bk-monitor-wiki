---
groupPath: 通用记忆片段/Issue
relation: Issue API Resource 业务逻辑模板
keywords: [SearchResource, DetailResource, CreateResource, MergeResource, issue_merge]
exportedAt: "2026-06-23T08:08:04.158Z"
---
# Issue API Resource 业务逻辑模板

## 入口
- `packages/fta_web/issue/resources.py` → 各 Resource 类

## Resource 结构
| Resource | 端点 | 核心逻辑 |
|-----------|------|---------|
| `IssueSearchResource` | `POST issue/search/` | 调用 `IssueQueryHandler`，从 serializer 提取 `limit`/`page`/`sort`/`conditions` |
| `IssueDetailResource` | `GET issue/detail/` | 从 serializer 取 `id`，直接 `IssueDocument.get(id=id)` |
| `IssueCreateResource` | `POST issue/` | `IssueDocument(**issue_info).save()`，返回 document |
| `IssueUpdateResource` | `PUT issue/` | 从 serializer 取 `id`、`update_fields`，partial update |
| `IssueDeleteResource` | `DELETE issue/` | 从 serializer 取 `id`，删除文档 |
| `IssueMergeResource` | `POST issue/merge/` | `IssueDocument.issue_merge(parent, issue_ids)`，批量合并 |
| `IssueSplitResource` | `POST issue/split/` | `IssueDocument.get(id=id).issue_split()` |
| `IssueSearchQSearchResource` | `POST issue/search/qsearch/` | 调用 `build_condition_query_v2`，返回 `query_dict` |
| `IssueRoundRobinResource` | `POST issue/round_robin/notify` | 轮询通知逻辑 |
| `IssueOauthTokenGetResource` | `POST fta/issue/tapd/oauth/token` | TAPD 授权：获取 token → 保存 → `try_bind_importable()` |
| `IssueRelatedIssuesResource` | `POST issue/related` | 同 `issue/merge` |
| `IssueTopNResource` | `POST issue/top_n` | TopN 聚合查询 |
| `IssueRecentAssigneesResource` | `POST issue/recent_assignees` | 最近处理人查询 |
| `IssueServiceResource` | `POST issue/service` | 服务信息 |

## 通用模式
1. 所有 Resource 继承 `Resource`，接受 `request` + `form_data`
2. 序列化器统一使用 `IssueSearchSerializer` 或对应的特定 Serializer
3. ES 操作走 `IssueDocument`（`bkmonitor/documents` 下的 Document 类）
4. 返回直接是 document dict 或构造后的响应 dict

## 关键代码模板（Create）
```python
class IssueCreateResource(Resource):
    """创建 Issue"""
    def perform_request(self, validated_request_data):
        serializer = IssueCreateSerializer(data=validated_request_data)
        serializer.is_valid(raise_exception=True)
        issue_info = serializer.validated_data
        issue_document = IssueDocument(**issue_info)
        issue_document.save()
        return issue_document
```

## 关键代码模板（Merge）
```python
class IssueMergeResource(Resource):
    """合并 Issue"""
    def perform_request(self, validated_request_data):
        serializer = IssueMergeSerializer(data=validated_request_data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.pop("parent")
        children = serializer.validated_data.pop("children")
        IssueDocument.issue_merge(parent, children)
        return {"message": "success"}
```

## 依赖
- `IssueDocument`（ES 文档模型）
- `IssueQueryHandler`（搜索查询构建）
- 各 Serializer（序列化/反序列化）

## 使用场景
- 新增 Issue 端点时，复制对应 Resource 模板
- 修改搜索逻辑时，检查 `IssueSearchResource` 和 `IssueQueryHandler`
