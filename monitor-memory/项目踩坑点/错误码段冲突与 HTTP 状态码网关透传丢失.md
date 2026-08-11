---
groupPath: 项目踩坑点
relation: 错误码段冲突与 HTTP 状态码网关透传丢失
keywords: [3318001, 3327, data_link, BKAPIError.data]
exportedAt: "2026-08-03T07:24:15.282Z"
---
- `core/errors/upgrade.py` UpgradeError 已占 code=3318001，issue 曾误用 3318001 冲突，改用未占用段 3327xxx（`core/errors/issue.py` IssueError=3327000 / IssueRenameConflictError=3327001）。新增错误码前先 grep 全局占用（搜索 code = 33）。
- web 网关 `core/drf_resource/contrib/api.py` APIResource.perform_request 原用 str(err.response.content) 把响应体字符串化，上游错误码丢失（BKAPIError.data 变 {"message": str}）；已改为 err.response.json() 优先透传，非 JSON 退回字符串。
- 消费 BKAPIError.data.code/message 的调用方：`metadata/models/data_link/data_link.py` _is_remote_component_not_found——data 结构变化会影响其判断逻辑，改框架错误分支需回归。