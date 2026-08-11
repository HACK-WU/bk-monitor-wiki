---
groupPath: API 集成模式
relation: web 与 kernel_api 异常链路差异与 BKAPIError 捕获
keywords: [异常处理, BKAPIError, 错误码]
exportedAt: "2026-08-04T07:59:13.011Z"
---
# web 与 kernel_api 异常链路差异与 BKAPIError 捕获

> 从 REQ-20260803-001（Issue 重命名异常返回专有状态码）沉淀，同步自 monitor 知识库「核心模块架构」。

## 两套异常处理器差异

| 维度 | web 端（config/role/web.py） | kernel_api（config/role/api.py） |
|------|------------------------------|----------------------------------|
| handler | `core/drf_resource/exceptions.py: custom_exception_handler` | `kernel_api/exceptions.py: api_exception_handler` |
| Error 子类 | 渲染完整 envelope（code/name/message/data/error_details）+ `extra` 平铺，HTTP status 取 `exc.status_code`（409 真实生效） | `failed(str(exc))` 重建，`name`/`error_details.type/code` 均 None |
| data 透传 | `exc.data` 原样输出 | 白名单仅透传 `error_code`/`next_actions`（防 BKAPIError 透出上游响应体泄露） |
| HTTP status | `exc.status_code`（如 409） | 恒为 200（`Response(json_data)` 不带 status，不读 exc.status_code） |

## BKAPIError 捕获方式（web 网关 APIResource）

文件：`bkmonitor/core/drf_resource/contrib/api.py`，定义 `bkmonitor/core/errors/api.py`（code 3301001，`data=上游响应体`）。

1. **HTTPError 分支**（上游 4xx/5xx）：`raise BKAPIError(result=str(err.response.content))`，data 是字符串。REQ-03 曾改 `err.response.json()` 透传 dict，经评估无效（kernel_api 返回 200 不走此分支）且影响 metadata `_is_remote_component_not_found`（消费 data.code/message）→ **已回退**。
2. **body 检查分支**（HTTP 200 但业务失败）：`if not result_json.get("result", True) and ret_code != 0: raise BKAPIError(result=result_json)`，data 是完整 dict。

消费方：`except BKAPIError as e`，用 `e.data.get("code")` 识别上游业务错误码。

## Issue rename 重名冲突实际链路

1. kernel_api `views/v4/issue.py: RenameResource` 捕获 `IssueNameDuplicatedError` → 抛 `IssueRenameConflictError`（code 3327001 + 中文 message）
2. kernel_api `api_exception_handler` → HTTP 200 + body `{code:3327001, result:false, message:中文, data:{}}`
3. web 网关 `APIResource` `raise_for_status()` 通过（200）→ body 检查分支抛 `BKAPIError(result=result_json)`，e.data 含 code=3327001
4. web 端 `packages/fta_web/issue/resources.py: RenameIssueResource` 捕获 BKAPIError，识别 `e.data.code==3327001` → 重抛 `IssueRenameConflictError`（中文 message）
5. web `custom_exception_handler` 渲染 HTTP 409 + code 3327001 + 中文 message

**关键教训**：前端认 body.code 而非 HTTP 状态码；kernel_api 层恒 200+body.code，web 层才转 409。