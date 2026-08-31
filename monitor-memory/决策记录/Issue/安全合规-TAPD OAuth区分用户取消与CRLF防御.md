---
groupPath: 决策记录/Issue
relation: 安全合规-TAPD OAuth区分用户取消与CRLF防御
exportedAt: "2026-08-31T03:11:25.323Z"
---
【决策记录｜Issue TAPD OAuth 回调：区分用户主动取消与系统错误，并防御 CRLF 日志注入】
- 分类：安全合规
- 动机：避坑（用户取消授权被误判为系统错误，用户看到错误页且无法区分原因）、安全（外部回调参数直接进日志）
- 决策：三条约定：signed_state 验签前置（确保 error_url 来自受信任签名）；检测到 error 参数时识别为用户主动取消，友好重定向到 error_url 并记 info 日志，不当作系统错误；记录 error_description 前剔除 CRLF 防御日志注入。缺少 code 的非取消场景同样重定向到 error_url
- 背景约束：用户取消授权时 TAPD 重定向回 redirect_uri 并携带 error=access_denied（无 code），原逻辑把无 code 统一重定向到根路径，误判为参数缺失
- 被否决方案：维持无 code 即重定向根路径，否决理由为无法区分用户主动取消与真实系统错误，排障与体验都受损
- 已知代价：error_url 依赖签名校验，签名配置错误会导致取消流程不可用；signed_state 的签名截断为 hex 16 字符（兼顾安全性与 URL 长度），是安全强度与可用性的折中
- 重新评估触发条件：TAPD 回调参数协议变化；或需要把用户取消计入运营指标
- 关联代码：tapd_user_oauth_callback @ packages/fta_web/issue/resources.py；verify_signed_state 与 generate_signed_state @ packages/fta_web/issue/utils/tapd.py；tapd_app_install_callback（应用态授权回调，同为验签前置）@ resources.py
- 证据来源：commit 9bd1cf3213（body 四条改动）；代码注释（用户主动取消授权：TAPD 重定向回 redirect_uri 并携带 error=access_denied，属正常业务分支，重定向到 error_url 展示友好提示，不当作系统错误）；generate_signed_state docstring（签名截断至 hex 16 字符兼顾安全性与 URL 长度，payload 必须包含 exp 建议 TTL 15min）；相关 commit 30df862d4d
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 14