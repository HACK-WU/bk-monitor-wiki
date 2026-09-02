---
groupPath: 关联关系/Issue
relation: worker配置常量-MergeResource组规模门禁
exportedAt: "2026-09-01T07:21:15.265Z"
---
[强关联] worker 角色配置常量 与 MergeResource 合并组规模门禁
强度：必改——改 ISSUE_MAX_MERGE_GROUP_SIZE 的语义/阈值/默认值时，MergeResource 校验 5 必须跟着改；改 MergeResource 的组规模判定口径（计数范围含待改挂成员）时，常量的注释与规模模型说明必须同步
原因：常量定义在 worker 角色配置文件、消费方却是 web 接口层的 MergeResource，两端不同目录、无 import 关系，靠 settings 字符串弱耦合，改动时极易只改一端

风险点（务必留意）：
- 消费方用 getattr(settings, "ISSUE_MAX_MERGE_GROUP_SIZE", 0) or 0 兜底，常量被删/改名时门禁**静默关闭**（fail-open），不报错不告警，规模上限形同虚设
- 0 = 关闭门禁，>0 才生效

常量定义端：
- ISSUE_MAX_MERGE_GROUP_SIZE 及与 ISSUE_MAX_ACTIVE_PER_STRATEGY 的取向对照注释 @ bkmonitor/config/role/worker.py

消费端：
- MergeResource 校验 5（组规模上限，须排在任何写入之前）@ bkmonitor/kernel_api/views/v4/issue.py
- MergeGroupTooLargeError（错误码 3337110）@ bkmonitor/bkmonitor/issue_merge/errors.py
- 异常导出声明 @ bkmonitor/bkmonitor/issue_merge/__init__.py