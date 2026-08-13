---
groupPath: 专题记忆/Issue
relation: IssueMergeResolver 合并拆分
exportedAt: "2026-08-13T08:53:32.215Z"
---
IssueMergeResolver 负责 Issue 的合并与拆分，关系持久化在 MySQL IssueMergeRelation 表。合并后源 Issue 冻结并级联状态随主 Issue 变更；拆分恢复为独立 Issue。查询路径通过 Resolver 进行 display_id 折叠、member 排除、聚合数据 union。

## 关键符号
- 符号: `IssueMergeResolver.merge(main_issue_id, source_issue_ids, operator)`
- 符号: `IssueMergeResolver.split(issue_id, operator, split_alert_ids=None)`
- 位置: `bkmonitor/issue_merge.py`
- 异常: `IssueFrozenError`（目标 Issue 已归档/已解决/已是合并 member）

## 合并语义
- 主 Issue 继承被合并 Issue 的告警关联
- 被合并 Issue 状态冻结，记录 MERGED_INTO 活动日志
- 不可再单独操作
- 跨业务禁止合并

## 拆分语义
- 将子 Issue 从主 Issue 拆分恢复为独立 Issue
- 可选指定 split_alert_ids 带走特定告警
- 拆分后原 member 状态恢复为拆分前状态或 unresolved

## 级联状态同步
- 主 Issue 状态变更（resolve/archive/reopen/restore）会级联同步所有 active member 的 ES status
- 被拆分的 member 状态保持当前状态不变

## Web 层转发
- 合并/拆分写操作由 Web 层 MergeIssueResource/SplitIssueResource 转发到 api role 的 MergeResource/SplitResource 执行
- 符号: `MergeIssueResource` / `SplitIssueResource`
- 位置: `bkmonitor/packages/fta_web/issue/resources.py`
- api role: `kernel_api/views/v4/issue.py`（MergeResource/SplitResource）

## MySQL 模型
- 表名: `bkmonitor_issue_merge_relation`
- 符号: `IssueMergeRelation`
- 记录主 Issue 与子 Issue 关系，支持拆分恢复

## 测试注意
- 合并/拆分测试需 api 角色（conf.api.development.community），worker/web 角色下会假失败
- 测试文件: `alarm_backends/tests/service/fta_action/test_issue_merge.py`（72 用例，api 角色 72 全过）