---
groupPath: 决策记录/Issue
relation: 接口契约-LLM标题两级闸门仅新建静默失败
exportedAt: "2026-08-31T03:10:17.255Z"
---
【决策记录｜Issue LLM 标题派发：两级闸门加仅新建触发加延迟导入加异常静默】
- 分类：接口契约
- 动机：可维护性（避免启动期依赖未就绪模块）、可观测性（失败不影响主链路）
- 决策：四项约定：两级闸门——部署级 env ENABLE_ISSUE_LLM_TITLE（由 helm chart 按 llmWorker 有效容量派生注入，env 不存在即不派发）加运行时业务白名单 is_llm_title_enabled_for_biz；仅新建时派发（created=True），查找已有 Issue 不触发；导入延迟化（from ... import 写在函数内）避免启动时依赖未就绪的 LLM 模块；异常全捕获 logger.warning 记录不影响主链路
- 背景约束：LLM 依赖是可选的外部能力，且其模块启动顺序晚于聚合链路
- 被否决方案：模块顶层 import LLM 依赖，否决理由为启动时依赖未就绪的 LLM 模块
- 已知代价：标题生成失败对用户不可见（只有日志）；两级闸门意味着默认关闭，需部署与业务白名单同时放行
- 重新评估触发条件：LLM 能力成为默认依赖（可移除 env 闸门）；或需要向用户暴露标题生成失败状态
- 关联代码：_maybe_dispatch_llm_title @ issue_processor.py；generate_issue_llm_title 与 refresh_issue_llm_title_examples @ tasks/issue_tasks.py
- 证据来源：Wiki《Issue 聚合引擎》「LLM 标题派发 → 两级闸门表加设计决策三条」
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 7