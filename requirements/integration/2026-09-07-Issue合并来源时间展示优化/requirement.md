---
id: REQ-20260907-001
feature: Issue合并来源时间展示优化
status: 进行中
created: 2026-09-07
updated: 2026-09-07
version: 1
tags: [integration, feat, issue, merge_sources, 时间展示]
depends_on: []
author: AI
document_type: requirement
---

# 需求文档：合并后的子 Issue 时间展示优化

- **需求 ID**：REQ-20260907-001
- **TAPD 需求**：1010158081137884900（蓝鲸监控项目，提单人 @edwinwu）
- **创建时间**：2026-09-07
- **状态**：进行中（后端已实施，未提交）
- **分类**：integration

## 背景与目标

**背景**：监控平台 Issues 合并功能中，「已并入但隐藏的 Issue」列表（合并明细抽屉）每个子 Issue 仅展示错误描述与「操作人 · 合并时间」，缺少子 Issue 自身的「最早发生时间」「最后出现时间」，用户难以快速了解各子 Issue 的时间范围与发展趋势。

**目标**：合并明细中每个已并入的子 Issue 明确标注「最早发生时间：xxxx」和「最后出现时间：xxxx」；时间信息准确；不影响现有合并和拆分功能。

## 需求拆分清单

| REQ | 需求描述 | 验收标准 | 负责方 | 状态 |
|-----|----------|----------|--------|------|
| REQ-01 | 后端：merge_sources 成员条目补 `first_alert_time` / `last_alert_time` | active_members 每项含两个秒级时间戳；ES 缺失兜底 0 | 后端（本次范围，用户确认 2026-09-07） | 已实施 |
| REQ-02 | 前端：合并明细条目渲染「最早发生时间 / 最后出现时间」 | 与 TAPD 截图标注一致；时间为 0 时占位渲染 | 前端（移交，见 api-changes 文档） | 待排期 |

**范围决策**：用户明确本次只负责后端（REQ-01），前端适配项已写入 `docs/api-changes/2026-09-04-issue-merge-sources-alert-times.md` 移交。

## 技术要点（调研结论，2026-09-04/07）

- 截图页面=合并明细抽屉「已并入但隐藏的 Issue」，前端组件 `split-content.tsx`（`issues-merge-split-sideslider.tsx` 以 type='split' 渲染），数据源 `ListMergeSourcesResource`（`fta_web/issue/resources.py`，GET `/issue/merge_sources`）。
- 成员 Issue 的 `first/last_alert_time` 由周期任务维护、合并后文档冻结，即合并前的真实告警时间线，语义准确。
- 原接口 ES `source()` 已取 `first_alert_time`（供 anomaly 时间窗），补 `last_alert_time` 取值 + 两处输出即可，零兼容风险。

## 需求验证标准

| 需求 ID | 验证方式 | 验证指标 | 验证时机 |
|---------|----------|----------|----------|
| REQ-01 | 单元测试 | 3 个契约用例（两列表均带字段 / ES 缺失兜底 0 / null 兜底 0）通过 | 开发完成后（已通过，34 passed） |

## 实施记录

- **2026-09-07**：后端实施完成。`resources.py`：ES source 增加 `last_alert_time`、成员条目新增 `first_alert_time`/`last_alert_time`（`or 0` 兜底）；`test_issue_resources.py` 新增 `TestListMergeSourcesAlertTimes` 3 用例。测试：`test_issue_resources.py` 34 passed 1 skipped（web 角色）；issue 目录全量 37 passed，1 失败为存量（`test_issue_trend_contract.py` 读取前端文件断言过期，与本次无关，git 确认前端文件零触碰）。改动未提交，待用户确认。

## 潜在风险与注意事项

1. **兼容性**：纯新增字段，旧前端零影响；split_history 条目同样携带（前端当前不消费，无副作用）。
2. **时间语义**：合并后成员告警时间线冻结（方案 A cascade follow），展示值为合并前真实时间，与需求意图一致。
