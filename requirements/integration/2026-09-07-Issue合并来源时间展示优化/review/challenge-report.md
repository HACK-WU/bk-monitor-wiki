# 质疑报告：merge_sources 成员条目新增告警时间字段（REQ-20260907-001）

> 质疑对象：2026-09-07 后端变更（`fta_web/issue/resources.py` ListMergeSourcesResource + test_issue_resources.py）
> 质疑模式：challenger 代码变更模式（新增功能策略），由 code-review 阶段 7 自动接力
> 质疑日期：2026-09-07

## 质疑详情

### Q1 数据贯通（正向）：新增字段沿链路到最终落点了吗？

| 跳 | 证据 | 结果 |
|---|---|---|
| ES source 取回 | diff：`.source([... "last_alert_time"])`，`IssueDocument` mappings 61-62 行确认两字段均映射 | ✅ |
| map 构建 | `last_alert_time_map`（`int(getattr(...) or 0)`），与既有 `first_alert_time_map` 同模式 | ✅ |
| item 输出 | `active_members`/`split_history` 共用 item 构造，两字段在公共段 | ✅ |
| 最终落点 | API 响应 JSON（views 路由 `issue/merge_sources` 直通 Resource 返回值） | ✅ |

**结论：后端链路贯通，质疑不成立。**

### Q2 数据贯通（反向）：新增产出有消费方吗？

前端 TS `MergeSourceMemberBase` 未声明两字段，当前**无前端消费方**。判定：**分阶段铺垫**——用户 2026-09-07 拍板「只负责后端」，前端适配已移交 [api-changes 文档](/root/bk-monitor/docs/api-changes/2026-09-04-issue-merge-sources-alert-times.md)。**质疑不成立（已确认的有意分阶段），但合入后前端长期不跟进会退化为死字段，建议跟进。**（🟢 非阻塞）

### Q3 守恒三问（存量数据）

- **流向**：响应新增 2 个 key，`merge_sources` 全仓调用点仅 views 路由 + 前端 `split-content.tsx` 一处；旧消费方不读新 key，零影响。✅
- **数量**：不改变任何列表条数与条目存在性。✅
- **内容**：旧字段逐字节不变（diff 核对，插入位置在 `merge_time` 与 `status` 之间，纯新增）。✅

**结论：守恒成立。**

### Q4 异常归宿：ES 整体查询失败会怎样？

`member_hits` 查询无 try/except，ES 不可用时整个接口异常——这是**存量行为**（原代码同样无保护），本次未改变语义，且 `member_name`/`member_es_status` 等同源字段均依赖该查询，单独为新增字段加 fail-open 意义有限。**质疑不成立（存量一致），如需加固建议独立需求统一处理 anomaly/名称/时间三类字段的 fail-open。**（🟢 非阻塞）

### Q5 全局回扣

- **目标回扣**：需求=子 Issue 时间展示。后端数据供给完整达成；展示侧移交前端（范围决策已获用户确认）。✅
- **位置回扣**：`IssueQueryHandler`、合并/拆分执行路径、bkm_cli 均不消费 merge_sources 响应，无放大效应。✅
- **判据回扣**：旧字段契约不变（测试 34 passed 含全部存量契约用例）；`split_history` 额外携带新字段属超范围提供、前端不消费无副作用。✅

### Q6 搭车变更

diff 仅含目标改动（source 补字段 + map + item 两行 + 注释 + 测试），无顺手优化。✅

## 结论

**无阻塞级质疑，维持合入结论 ✅ 可直接合入（后端范围）。**

| # | 质疑点 | 等级 | 处置 |
|---|--------|------|------|
| 1 | 前端未消费新增字段（移交项） | 🟢 | 已移交 api-changes 文档，建议前端排期跟进防死字段 |
| 2 | ES 整体查询无 fail-open（存量） | 🟢 | 与本次无关，如加固走独立需求 |
