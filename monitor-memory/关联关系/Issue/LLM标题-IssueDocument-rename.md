---
groupPath: 关联关系/Issue
relation: LLM标题-IssueDocument-rename
exportedAt: "2026-08-13T08:55:56.523Z"
---
[强关联] LLM 标题任务 与 IssueDocument.rename 方法
强度：必改——改 IssueDocument.rename 的参数/CAS 逻辑/enforce_unique 语义时，LLM 标题任务必须跟着改；改 LLM 标题生成逻辑，rename 方法不用管
原因：LLM 标题通过 rename 方法 CAS 写入（检查 default_name），rename 的 enforce_unique=False 是系统路径专用，参数/语义变更会级联影响标题生成

源端（LLM 标题任务）：
- `dispatch_llm_title` @ `alarm_backends/service/fta_action/llm_title.py`
- `generate_issue_llm_title(issue_id, bk_biz_id, default_name, alert_id)` @ `alarm_backends/service/fta_action/tasks/issue_tasks.py`
- `regenerate_issue_llm_title(issue_id, bk_biz_id, *, alert_id=None, operator="system")` @ `alarm_backends/service/fta_action/tasks/issue_tasks.py`
- 队列: celery_llm_task

目标端（rename 方法）：
- `IssueDocument.rename(new_name, operator, enforce_unique=False, content=None)` @ `bkmonitor/documents/issue.py`
- CAS 保护: 写入前检查当前 name 是否仍为 default_name
- operator 恒为 system，enforce_unique=False（系统路径专用）