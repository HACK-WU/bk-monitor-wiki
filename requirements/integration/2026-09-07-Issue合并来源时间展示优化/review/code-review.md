# Code Review 报告：merge_sources 成员条目新增告警时间字段（REQ-20260907-001）

> 审查日期：2026-09-07　|　模式：快速紧凑（净增 111 行：生产 5 + 测试 106；2026-09-04 同型改动二次复用）　|　关联需求：REQ-20260907-001
> 结论性质：**已验证**（单测实跑：`test_issue_resources.py` 34 passed 1 skipped，web 角色）

## 变更概览

| 文件 | 改动 |
|---|---|
| `packages/fta_web/issue/resources.py` | ES source 补 `last_alert_time`；`last_alert_time_map` 构建；成员 item 输出 `first_alert_time`/`last_alert_time`（`or 0` 兜底）+ 语义注释 |
| `packages/fta_web/tests/issue/test_issue_resources.py` | 新增 `TestListMergeSourcesAlertTimes` 3 用例（两列表携带字段 / ES 缺失兜底 0 / None 兜底 0） |

## 七维度速评

| 维度 | 结论 | 依据 |
|---|---|---|
| 语义一致性 | ✅ 10 | 需求=子 Issue 时间展示，实现=成员条目补两时间字段，意图完全对齐；无搭车变更 |
| 安全 | ✅ 10 | 无注入/敏感面；纯响应新增字段 |
| Bug 风险 | ✅ 9 | 兜底链 `int(getattr(x, k, 0) or 0)` 覆盖缺失/None；与既有 first 同型，无新路径 |
| 规范 | ✅ 9 | 注释说明语义与兜底；map 命名/结构与上下文一致 |
| 架构 | ✅ 9 | 契约纯新增向后兼容；split_history 同带字段属超集供给，无副作用 |
| 性能 | ✅ 9 | 复用同一次 terms 查询，零额外 ES 往返；dict 构建为既有模式等量复制 |
| 测试覆盖 | ✅ 9 | 3 用例覆盖正常/缺失/None 三态；实跑通过（34 passed 1 skipped，skip 为存量） |

## 整体评分：A

**🎯 合入结论：✅ 可直接合入（后端范围）。**

**回归说明**：`packages/fta_web/tests/issue` 目录全量 37 passed + 1 failed（`test_issue_trend_contract.py`，读取 webpack 前端文件断言过期）——git 确认本次前端文件零触碰，属存量失败，与本次改动无关。

**关键决策实证**：
1. 字段语义「成员合并前冻结的真实告警时间线」成立——成员 `first/last_alert_time` 由周期任务维护、合并后文档冻结（方案 A cascade follow），恰为需求要的"子 Issue 实际时间"。
2. `first_alert_time` 复用：原接口取该字段本用于 anomaly 时间窗，本次顺手输出到响应，无额外查询成本。
3. 测试桩须带 `STATUS_SPLIT` 常量（生产代码访问 `IssueMergeRelation.STATUS_SPLIT`），首轮运行已实证修正。

**合入后跟进（P2）**：
| # | 事项 |
|---|---|
| 1 | 前端适配（`MergeSourceMemberBase` 补声明 + split-content 渲染，0 占位）——已移交 [api-changes 文档](/root/bk-monitor/docs/api-changes/2026-09-04-issue-merge-sources-alert-times.md)，防死字段 |
| 2 | ES 整体查询 fail-open 加固（存量，如做建议统一覆盖 anomaly/名称/时间三类字段） |

**二次质疑**：challenger 自动接力（贯通两问/守恒三问/异常归宿/全局回扣/搭车变更），无阻塞级质疑，详见 [challenge-report.md](challenge-report.md)。
