错误码段冲突（UpgradeError 已占 3318001，issue 改用 3327xxx 段）与 web 网关 HTTPError 响应体字符串化导致上游错误码丢失的问题。
- 符号: `IssueError`, `IssueRenameConflictError`, `APIResource.perform_request`
- 位置: `core/errors/issue.py`, `core/drf_resource/contrib/api.py`, `metadata/models/data_link/data_link.py`

错误码段冲突：`core/errors/upgrade.py` 的 UpgradeError 已占 code=3318001，issue 曾误用 3318001 冲突，改用未占用段 3327xxx（`core/errors/issue.py` IssueError=3327000 / IssueRenameConflictError=3327001）。新增错误码前先 grep 全局占用（搜索 code = 33）。

HTTP 状态码网关透传丢失：web 网关 `core/drf_resource/contrib/api.py` 的 `APIResource.perform_request` 原用 `str(err.response.content)` 把响应体字符串化，上游错误码丢失（BKAPIError.data 变 `{"message": str}`）；已改为 `err.response.json()` 优先透传，非 JSON 退回字符串。

消费方影响：消费 `BKAPIError.data.code`/`message` 的调用方 `metadata/models/data_link/data_link.py` 的 `_is_remote_component_not_found` — data 结构变化会影响其判断逻辑，改框架错误分支需回归。
