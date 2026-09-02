---
groupPath: 待生效变更/Issue
relation: 拆分接口批量契约变更-ki专题记忆更新
exportedAt: "2026-09-02T06:46:18.703Z"
---
【待生效变更｜拆分接口批量契约变更-ki专题记忆更新】
- 触发来源：REQ-20260901-001 Issue拆分支持批量操作（工作区未提交变更，2026-09-02 code review 登记）
- 资产类型：ki 记忆
- 影响资产：monitor-memory 专题记忆/Issue 的「合并拆分」relation
- 变更类型：修改
- 当前内容：拆分链路描述为单条：SplitIssueResource（web 薄壳）→ api.issue.split → kernel_api SplitResource → 查 active 关系 + 单条 UPDATE status=split + bulk_reset_for_split([member_id])
- 合并后应为：追加批量路径：web 仅收 member_issue_ids ≤50 透传；kernel_api 批量逐条独立（_mark_split 条件 UPDATE 幂等，skipped/failed 单条隔离），ES 重置按主 Issue 分组合并调用（同组 1 次 bulk）；旧单条契约保留（外部兼容）。合入后更新该 relation，并评估新增决策记忆「拆分批量逐条独立、无跨条目事务、部分失败不阻塞，rejected 整批事务方案」
- 状态：待生效
- 登记时间：2026-09-02