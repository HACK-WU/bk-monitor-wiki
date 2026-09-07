---
groupPath: 专题记忆/Issue
relation: ListMergeSourcesResource 合并来源接口契约
exportedAt: "2026-09-07T03:35:01.055Z"
---
# ListMergeSourcesResource 合并来源接口契约（PR12234 + 时间字段更新）

契约来源：`packages/fta_web/issue/resources.py` `ListMergeSourcesResource`（路由 GET `/issue/merge_sources`，resource.issue.list_merge_sources）。2026-08-31 commit 438a146（已合并主 Issue 支持继续合并）新增返回字段 `via_issue_id`；2026-09-07（TAPD 1010158081137884900，REQ-20260907-001「合并后的子issue时间展示优化」）成员条目新增 `first_alert_time` / `last_alert_time`，纯新增向后兼容。

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| bk_biz_id | int | 是 | 业务 ID |
| main_issue_id | str | 是 | 主 Issue ID（IssueIDField，实为 CharField） |

## 返回结构

`{"main_issue_id": str, "active_members": [item], "split_history": [item]}`，无关系时两列表为空。

### item 公共字段

| 字段 | 类型 | 说明 |
|------|------|------|
| member_issue_id | str | 成员 Issue ID |
| member_name | str | 成员名称；ES 不存在时 "{id} (已删除)" |
| anomaly_message | str | 成员最新告警描述；查询失败 fail-open 兜底 "--" |
| merge_reasons | list[str] | 合并依据 |
| merge_operator | str | 合并操作人（关系行 create_user） |
| merge_time | int | 合并时间秒级时间戳，无则 0 |
| first_alert_time | int | **新增（REQ-20260907-001）**。成员最早告警时间秒级时间戳；成员文档合并后冻结，即合并前的真实告警时间；ES 无文档或字段 null 兜底 0 |
| last_alert_time | int | **新增（REQ-20260907-001）**。成员最后告警时间秒级时间戳，兜底规则同上；与 name/status/first_alert_time 同一次 terms 查询取回 |
| status | str | 关系状态 active/split（旧字段，保留一个发布周期向后兼容） |
| relation_status | str | 同义新字段，新代码优先使用 |
| member_es_status | str|null | 成员自身 ES 状态 pending_review/unresolved/resolved/archived；ES 缺失为 null，前端按已删除占位 |
| via_issue_id | str|null | **新增（PR12234）**。上一跳主 Issue ID：成员是"随着某个已成组的主一起被改挂（reparent）并入"时非空，记录它此前所属的主；直接合并的成员为 null。纯溯源标签，可能指向已不在本组的 Issue（上一跳主随后被拆分），不得假设它仍是本组成员 |

### split_history 条目额外字段

| 字段 | 类型 | 说明 |
|------|------|------|
| split_reasons | list[str] | 拆分依据，default=None 统一 or [] 兜底 |
| split_operator | str | 拆分操作人（关系行 update_user） |
| split_time | int | 拆分时间秒级时间戳 |
| split_kind | str|null | 拆分触发类型；新写入固定 manual，历史可能为 by_main_resolve/by_main_archive |

## 行为约束

- 排序按关系行 create_time 降序。
- anomaly_message 批量查询失败仅 warning，不影响主返回。
- first/last_alert_time 取自成员 ES 文档，缺失兜底 0；split_history 条目同样携带（前端当前不消费，无副作用）。
- via_issue_id 同字段另在两处暴露：bkm_cli inspect-issue detail 的 merge_status.active_members（_inject_member_via_issue_ids fail-open 注入）、关系模型 IssueMergeRelation.via_issue_id（迁移 0203）。
- 前端消费现状：TS 类型 MergeSourceMemberBase 未声明 first/last_alert_time 与 via_issue_id（断链，PR12234 review P1-3）；时间字段前端适配项已移交 `docs/api-changes/2026-09-04-issue-merge-sources-alert-times.md`（渲染「最早发生时间/最后出现时间」，0 时占位）。

完整前端对接文档：.module-experts/issue专家/review/api-change-PR12234.md