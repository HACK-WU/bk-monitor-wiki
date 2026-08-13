---
groupPath: 专题记忆/Issue
relation: LLM 标题生成
exportedAt: "2026-08-13T08:53:50.704Z"
---
LLM 标题生成模块在新建 Issue 后异步生成可读标题。独立队列 celery_llm_task，两级闸门控制，CAS 保护防覆盖用户改名，失败静默不重试。支持运维显式补偿重生成和周期预计算 few-shot 示例。

## 关键符号
- 符号: `dispatch_llm_title(issue)`
- 位置: `alarm_backends/service/fta_action/llm_title.py`
- 用途: 新建 Issue 后异步派发 LLM 标题生成任务
- 符号: `generate_issue_llm_title(issue_id, bk_biz_id, default_name, alert_id, alert_retry_attempt=0)`
- 符号: `regenerate_issue_llm_title(issue_id, bk_biz_id, *, alert_id=None, operator="system")`
- 符号: `refresh_issue_llm_title_examples()`
- 位置: `alarm_backends/service/fta_action/tasks/issue_tasks.py`

## 两级闸门
1. 部署级 env: `ENABLE_ISSUE_LLM_TITLE`
2. 运行时业务白名单: `ISSUE_LLM_TITLE_BIZ_WHITE_LIST`
- regenerate_issue_llm_title 绕过这两级闸门（运维显式发起），但仍保留业务级限流

## CAS 保护
- 写入前检查当前 name 是否仍为默认名（default_name 参数）
- 防止覆盖用户抢先改名
- rename 时 operator 恒为 system，enforce_unique=False

## 失败策略
- 所有失败静默处理，保留默认名
- 不入队重试
- 只有 alert_not_found 会按 1s/3s 延迟重试

## 生成条件
- 仅日志类告警且关联内容非空
- 业务在白名单内
- 未触发限流
- Issue 非活跃/为活跃合并 member 时跳过（regenerate 路径）

## few-shot 示例
- refresh_issue_llm_title_examples 周期预计算缓存
- 队列 celery_action_cron
- 缓存 24h 过期后自动退静态示例
- 白名单为空时直接跳过

## 标题校验规则
- 拒绝多行、md5、IP、trace_id
- 管理命令: `regenerate_issue_llm_title`（强制显式模式、dry-run 去重、超 20 个唯一 Issue 拒绝）
- 位置: `bkmonitor/management/commands/regenerate_issue_llm_title.py`