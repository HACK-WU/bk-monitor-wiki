---
groupPath: 专题记忆/Issue
relation: IssueMergeResolver 合并拆分
exportedAt: "2026-09-02T10:25:22.607Z"
---
IssueMergeResolver 负责 Issue 的合并与拆分，关系持久化在 MySQL IssueMergeRelation 表。合并后源 Issue 冻结并级联状态随主 Issue 变更；拆分恢复为独立 Issue。查询路径通过 Resolver 进行 display_id 折叠、member 排除、聚合数据 union。
- 符号: `IssueMergeResolver.merge(main_issue_id, source_issue_ids, operator)`
- 符号: `IssueMergeResolver.split(issue_id, operator, split_alert_ids=None)`
- 位置: `bkmonitor/issue_merge.py`
- 异常: `IssueFrozenError`（目标 Issue 已归档/已解决/已是合并 member）

合并语义：
- 主 Issue 继承被合并 Issue 的告警关联
- 被合并 Issue 状态冻结，记录 MERGED_INTO 活动日志
- 不可再单独操作
- 跨业务禁止合并

拆分语义：
- 将子 Issue 从主 Issue 拆分恢复为独立 Issue
- 可选指定 split_alert_ids 带走特定告警
- 拆分后原 member 状态恢复为拆分前状态或 unresolved

批量拆分（2026-09-02 REQ-20260901-001 新增，kernel_api SplitResource 双参数二选一）：
- 入参二选一：member_issue_id（旧单条契约不变，apigw issue.yaml isPublic 外部消费者依赖）与 member_issue_ids（新批量 ≤50，去重保序；单条拆分传长度 1 列表）
- web SplitIssueResource 仅透传：单次转发 api.issue.split，operator 由 get_request_username() 注入；旧单条契约原样透传兼容保留至前端适配完成
- 批量逐条独立执行、无跨条目事务、部分失败不阻塞其余条目
- _mark_split 条件 UPDATE（WHERE status=active）幂等防并发/重复拆分：rowcount=0 记 skipped（message: relation not active）
- 单条异常隔离：failed 条目统一通用文案 split failed，内部细节仅日志不下发（SplitNotFoundError 单独接住记 skipped）
- ES 重置按主 Issue 分组合并调用 bulk_reset_for_split（同组明细通常一个主 → 1 次 bulk）
- 批量响应 shape: {"status": "ok", "results": [{"member_issue_id", "status": "ok|skipped|failed", "message"?}]}

级联状态同步：
- 主 Issue 状态变更（resolve/archive/reopen/restore）会级联同步所有 active member 的 ES status
- 被拆分的 member 状态保持当前状态不变

Web 层转发：
- 合并/拆分写操作由 Web 层 MergeIssueResource/SplitIssueResource 转发到 api role 的 MergeResource/SplitResource 执行
- 符号: `MergeIssueResource` / `SplitIssueResource`
- 位置: `bkmonitor/packages/fta_web/issue/resources.py`
- api role: `kernel_api/views/v4/issue.py`（MergeResource/SplitResource，SplitResource 位于 559 行附近）

MySQL 模型：
- 表名: `bkmonitor_issue_merge_relation`
- 符号: `IssueMergeRelation`
- 记录主 Issue 与子 Issue 关系，支持拆分恢复

测试注意：
- 合并/拆分测试需 api 角色（conf.api.development.community），worker/web 角色下会假失败
- 测试文件: `alarm_backends/tests/service/fta_action/test_issue_merge.py`（75 用例，api 角色 75 全过，含 TestSplitBatch 3 用例：全部成功+ES 按主分组 / 去重保序+skipped / 异常隔离+通用文案）
- web 契约: `packages/fta_web/tests/issue/test_issue_resources.py` TestSplitIssueBatchContract 8 用例（批量透传/二选一必传/双传拒绝/超 50/非法 ID/旧参合法与透传）