---
groupPath: 关联关系/Issue
relation: MergeResource合并校验-bkm_cli合并对账
exportedAt: "2026-09-01T07:21:15.265Z"
---
[强关联] MergeResource 合并校验 与 bkm_cli 合并状态对账

影响线1：改 MergeResource 的校验集合（增删校验、放宽阈值、移除某条不变量校验）→ _list_merge_conflicts 必改；原因：写入侧不再拦截的不变量必须在对账侧可观测，否则静默腐化
影响线2：改 _list_merge_conflicts 的桶定义或判定 SQL → MergeResource 必改；原因：对账判定依赖与写入侧相同的关系表语义（status=active、main/member 方向、via_issue_id 溯源），口径不一致会持续误报

原因：PR#12234 移除 member 端防链式校验后，系统不再在写入侧阻止嵌套，改由运维对账侧发现深度违例——校验移除与对账补位是同一件事的两端

写入校验端：
- MergeResource（校验 1-5，含待改挂成员一致性校验与组规模上限）@ bkmonitor/kernel_api/views/v4/issue.py
- IssueMergeRelation（via_issue_id 字段、关系深度恒为 1 的 docstring 约定）@ bkmonitor/bkmonitor/models/issue.py

运维对账端：
- _list_merge_conflicts（四类桶；第 4 类 depth_violations 为 PR#12234 新增，不加 create_time 窗口）@ bkmonitor/kernel_api/rpc/functions/bkm_cli/issue.py
- _inject_member_via_issue_ids（detail 取证补 via_issue_id）@ bkmonitor/kernel_api/rpc/functions/bkm_cli/issue.py