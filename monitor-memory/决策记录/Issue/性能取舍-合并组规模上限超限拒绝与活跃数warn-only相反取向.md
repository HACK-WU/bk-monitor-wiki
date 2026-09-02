---
groupPath: 决策记录/Issue
relation: 性能取舍-合并组规模上限超限拒绝与活跃数warn-only相反取向
exportedAt: "2026-09-01T08:35:17.233Z"
---
【决策记录｜Issue 合并组规模上限：超限拒绝合并，与活跃数上限的 warn-only 取向刻意相反】
- 分类：性能取舍
- 动机：避坑（把已成组的主并入另一主时成员一起改挂，组规模可成倍增长；ES 查询 size 随成员数线性膨胀 → 慢查询）
- 决策：新增 ISSUE_MAX_MERGE_GROUP_SIZE = 500，合并后组成员总数超限时 MergeResource 抛 MergeGroupTooLargeError（错误码 3337110，HTTP 409）**拒绝合并**；0 = 关闭该门禁。校验 5 排在任何写入之前，避免超限请求留下半写状态
- 背景约束：IssueMergeResolver.hydrate_aggregations 与 IssueDocument.bulk_follow_status 的 ES 查询是 size=len(member_ids)，无界组会退化成慢查询；扁平化改挂（PR#12234）让组规模可以从「成员数」跃升为「成员数之和」
- 被否决方案：无（代码注释只给出与相邻常量的取向对照，未记录其他备选）
- 已知代价与边界：与紧邻的 ISSUE_MAX_ACTIVE_PER_STRATEGY = 500 取向**刻意相反**——那边阻塞会让告警永久失联（属**数据代价**，故放行仅上报 metric）；这里超限只是用户一次交互失败，先拆分再合并即可（**无数据代价**，故直接拒绝）。两个 500 数值相同纯属巧合，语义与处置完全相反，**不可统一**
- 重新评估触发条件：实测证明组规模远超 500 时查询仍无性能退化；或用户频繁因 500 上限合并失败
- 关联代码：ISSUE_MAX_MERGE_GROUP_SIZE @ bkmonitor/config/role/worker.py；MergeResource 校验 5 @ bkmonitor/kernel_api/views/v4/issue.py；MergeGroupTooLargeError @ bkmonitor/bkmonitor/issue_merge/errors.py
- 证据来源：代码注释（config/role/worker.py L560-566，明写「与上面 ISSUE_MAX_ACTIVE_PER_STRATEGY 的 warn-only 取向刻意不同」并给出两边代价对照）；commit 438a146（PR#12234）