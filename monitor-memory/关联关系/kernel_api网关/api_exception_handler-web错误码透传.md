---
groupPath: 关联关系/kernel_api网关
relation: api_exception_handler-web错误码透传
exportedAt: "2026-08-13T09:12:01.207Z"
---
[强关联] api_exception_handler 异常渲染 与 web 端 APIResource/BKAPIError 错误识别
强度：必改——改 api_exception_handler 的 body.code 语义或 data 白名单键时，web 端所有经 APIResource 调用 kernel_api 的错误识别逻辑必须跟着改（双向契约）；改 web 端识别逻辑，异常渲染不用动
原因：kernel_api 层 HTTP 恒 200 + body.code，web 端经 APIResource 调用时 BKAPIError 默认包装为 500，需捕获后按 e.data.code 重抛专有错误，形成跨角色错误码契约

源端（异常渲染）：
- `api_exception_handler(exc, context)` @ `bkmonitor/kernel_api/exceptions.py`
- HTTP 恒 200；code = getattr(exc, "code", 500)；data 白名单仅透传 `error_code`/`next_actions`
- 错误码段约定：3 开头蓝鲸平台错误（3301xxx=外部API、3300xxx=业务逻辑）；issue 用 3327xxx；需避免与 core/errors/upgrade.py 3318001 冲突

目标端（web 端错误识别）：
- `APIResource`（core.drf_resource.contrib.api）@ web 端 packages/*/resources.py
- `BKAPIError`（调用失败抛出，含 e.data.code/message）
- `RenameIssueResource` 识别 code==3327001 重抛 IssueRenameConflictError @ `bkmonitor/packages/fta_web/issue/resources.py`（示例）
- 前端认 body.code 而非 HTTP 状态码