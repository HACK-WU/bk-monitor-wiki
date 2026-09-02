---
groupPath: 专题记忆/Issue
relation: ListMergeSourcesResource 合并来源接口契约
exportedAt: "2026-09-01T06:43:44.790Z"
---
# ListMergeSourcesResource 合并来源接口契约（PR12234 更新）

契约来源：`packages/fta_web/issue/resources.py` `ListMergeSourcesResource`（路由 GET `/issue/merge_sources`，resource.issue.list_merge_sources）。2026-08-31 commit 438a146（已合并主 Issue 支持继续合并）新增返回字段 `via_issue_id`，其余字段未变。

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
- via_issue_id 同字段另在两处暴露：bkm_cli inspect-issue detail 的 merge_status.active_members（_inject_member_via_issue_ids fail-open 注入）、关系模型 IssueMergeRelation.via_issue_id（迁移 0203）。
- 前端消费现状：TS 类型 MergeSourceMemberBase 未声明该字段（断链，PR12234 review P1-3）。

完整前端对接文档：.module-experts/issue专家/review/api-change-PR12234.md