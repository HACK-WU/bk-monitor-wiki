---
groupPath: 决策记录/Issue
relation: 架构设计-合并放开member状态门槛终态不保真
exportedAt: "2026-08-31T03:10:49.492Z"
---
【决策记录｜Issue 合并语义：member 状态门槛放开、main 仍须活跃、合并前终态不保真】
- 分类：架构设计
- 动机：可维护性（member 并入即被冻结，自身状态不再权威，再要求它活跃是无意义的约束）
- 决策：合并校验仅保留 main 必须活跃，移除 member 状态白名单（已解决或已归档 Issue 可并入活跃主）；同时补 ListIssueHistory 的 active 冻结 member 排除（此前是唯一未做排除的列表路径）
- 背景约束：列表隐藏、防链式校验、聚合、级联全部按「关系状态」而非 member 自身 ES status 判断，这是放开门槛不留悬空假设的前提（commit 关键设计判断原文）。main 是存活、对外聚合、吸告警的主体，故保留其活跃约束
- 被否决方案：维持 main 与所有 member 均须活跃，否决理由为 member 一旦并入即冻结，自身状态不再权威，后续由主状态级联与拆分重置接管
- 已知代价与边界（commit 标注为已确认可接受）：member 合并前的终态不保留——合并前已 RESOLVED 或 ARCHIVED 的 member，主 reopen 或 restore 级联会把它复活成 UNRESOLVED、拆出时重置为待审核，不回到合并前的终态，这与「合并等于同根因、拆分等于重新独立评审」语义一致属有意为之，如需保真需在关系表落 pre-merge 状态快照；「同 fingerprint 双活跃」是系统既有、设计容忍的良性状态，路由层 _find_active_issue 按 -create_time 取最新活跃，确定收敛不冲突
- 重新评估触发条件：需要保真 member 合并前终态（需引入 pre-merge 状态快照）
- 关联代码：Issue 合并视图 @ kernel_api/views/v4/issue.py；ListIssueHistory @ packages/fta_web/issue/resources.py；IssueMergeResolver @ bkmonitor/issue_merge/
- 证据来源：commit 4024a7b0b5（body 含背景、改动、关键设计判断、边界说明（行为变化已确认可接受）、测试五段）；相关 commit f851490e11、b26382f4d4、ca6011523f、bd7c598464
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 13