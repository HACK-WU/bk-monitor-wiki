---
groupPath: 专题记忆/Issue
relation: IssueDocument 数据模型与状态机
exportedAt: "2026-08-13T08:53:09.065Z"
---
IssueDocument 是 Issue 的 ES 文档模型，封装状态机方法（assign/resolve/archive/reopen/restore/rename/add_comment/update_priority），所有状态流转由模型方法控制并返回活动日志。状态机有 4 个状态：pending_review（待审核/活跃）、unresolved（未解决/活跃）、resolved（已解决/非活跃）、archived（归档/非活跃）。

## 状态流转规则
- pending_review → unresolved（assign 首次指派 / add_comment / update_priority 自动流转）
- pending_review/unresolved → resolved（resolve，幂等 no-op）
- pending_review/unresolved → archived（archive）
- resolved → unresolved（reopen，清空 resolved_time）
- archived → pending_review/unresolved（restore，从活动日志推断归档前状态）

## 关键方法
- 符号: `IssueDocument.get_issue_or_raise(issue_id, bk_biz_id=None)`
- 位置: `bkmonitor/documents/issue.py`
- 用途: 按 ID 查询单条 Issue，使用 all_indices=True 避免跨天漏查；bk_biz_id 不匹配按不存在处理
- 异常: `IssueNotFoundError`
- 符号: `IssueDocument.to_cache_dict()`
- 用途: 生成 Redis 缓存字典，使用 skip_empty=False 保留空字段
- 符号: `IssueDocument.assign(assignees, operator)` → pending_review 专用，调后转为 unresolved
- 符号: `IssueDocument.reassign(assignees, operator)` → 任意状态改派，不触发流转
- 符号: `IssueDocument.resolve(operator)` → 幂等，级联同步 active member
- 符号: `IssueDocument.archive(operator)` → 级联同步 active member
- 符号: `IssueDocument.rename(new_name, operator, enforce_unique=True, content=None)`
- 异常: `IssueNameDuplicatedError`（enforce_unique=True 且同业务同名）、`IssueFrozenError`（合并 member）
- 注意: LLM 标题等系统路径应传 enforce_unique=False

## ES 索引字段
- id（Keyword，{timestamp}{uuid8}）、strategy_id、bk_biz_id、name（Text raw:Keyword）、status、assignee（Keyword multi）、priority（P0/P1/P2）、alert_count、first_alert_time、last_alert_time、fingerprint（count_md5）、dimension_values（Flattened）、impact_scope（Flattened）、is_regression

## 异常类
- `IssueNotFoundError`、`IssueFrozenError`（合并 member 不可操作）、`IssueNameDuplicatedError`
- 位置: `bkmonitor/documents/issue.py`