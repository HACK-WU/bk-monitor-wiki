---
groupPath: 专题记忆/Issue
relation: IssueViewSet 权限控制模式
keywords: [IssueViewSet, 权限控制, IAM, READ_ONLY, MANAGE_EVENT]
exportedAt: "2026-07-06T04:01:03.964Z"
---
# IssueViewSet 权限控制模式

## 入口
- `packages/fta_web/issue/views.py` → `IssueViewSet`
- `ResourceRouter` 注册：`register(r"", IssueViewSet, basename="issue")`

## 核心机制
```python
READ_ONLY_ENDPOINTS: Set[str] = {
    "issue/search",
    "issue/detail",
    "issue/round_robin/notify",
}
NO_BIZ_REQUIRED_ENDPOINTS: Set[str] = {
    "issue/search",
    "issue/top_n",
    "issue/recent_assignees",
}
```

### 权限规则
| 端点 | 权限类型 | 说明 |
|------|---------|------|
| `READ_ONLY_ENDPOINTS` | `VIEW_EVENT` | 只读操作，无需 MANAGE 权限 |
| 其他 | `MANAGE_EVENT` | 增删改操作 |
| 全部 | 继承 `BaseBizActionPermission` | 从 `bk_biz_id` 参数提取业务 ID 校验 |

### IssueBusinessActionPermission
自定义 IAM 权限类，从 `issues[*].bk_biz_id` 提取批量业务 ID，用于合并等批量操作。

## 使用场景
- 新增 Issue 端点时，需判断是否放入 `READ_ONLY_ENDPOINTS` 或 `NO_BIZ_REQUIRED_ENDPOINTS`
- 批量操作（合并、批量创建）需确保 IAM 权限覆盖所有涉及业务

## 依赖
- `BaseBizActionPermission`（公共基类）
- `MANAGE_EVENT` / `VIEW_EVENT`（IAM 常量）
