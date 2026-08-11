# 需求文档：Issue 重命名异常返回专有状态码

- **需求 ID**：REQ-20260803-001
- **创建时间**：2026-08-03
- **状态**：已完成
- **分类**：integration

## 背景与目标

**背景**：Issue rename 接口发生重名冲突时，前端无法区分「重命名报错」与其他错误——重名异常经 `ValidationError`(3300004) → `BKAPIError`(3301001) 两层包装后，前端拿到的是 HTTP 500 + 冗长报错信息，无法据此做页面信息提示，体验差。

**目标**：重命名冲突（同业务下已存在同名 Issue）返回**专有状态码**（业务码 `3327001` + HTTP `409`），前端可稳定识别并转为友好页面提示。

## 需求描述

web 端 `POST /issue/rename` 在同业务重名时返回：

```json
HTTP 409
{ "result": false, "code": 3327001, "name": "Issue 重名",
  "message": "已存在同名 Issue，请更换名称" }
```

前端只需判断 `code === 3327001` 即可转页面信息提示，而非展示报错信息。

## 需求拆分清单

| REQ | 需求描述 | 验收标准 | 依赖 |
|-----|----------|----------|------|
| REQ-01 | 定义 issue 专有错误码段（3327xxx）与重名错误类 | `IssueRenameConflictError.code == 3327001`；`status_code == 409` | 无 |
| REQ-02 | api role `RenameResource` 重名异常改抛专有错误 | 捕获 `IssueNameDuplicatedError` 抛 `IssueRenameConflictError`（不再抛 `ValidationError`） | REQ-01 |
| REQ-03 | ~~web 网关透传结构化错误响应体~~（**已废弃**） | ~~`APIResource` HTTPError 分支优先 `err.response.json()`~~ | 无 |
| REQ-04 | web 端 `RenameIssueResource` 识别重名 code 转码 | 捕获 `BKAPIError`，`data.code == 3327001` 时重抛 `IssueRenameConflictError` + 中文 message | REQ-02 |

## 非功能性约束

- 成功路径行为不变（rename 成功仍返回 `{bk_biz_id, issue_id, status, name, update_time, activities}`）
- 其他错误（参数校验 / Issue 不存在等）原样传播，不误转码
- 链路：kernel_api 返回 HTTP 200 + body `{code: 3327001, message: 中文}`；web 网关走 `APIResource` body 检查分支（`result=false && code!=0`）抛 `BKAPIError`（data 为完整响应 dict）；web 端 REQ-04 识别 code 重抛 `IssueRenameConflictError`，由 web `custom_exception_handler` 渲染 **HTTP 409** + 中文 message。**前端认 body.code 而非 HTTP 状态码**
- 不修改 `api_exception_handler`：其 data 白名单仅透传 `error_code`/`next_actions`，`data.name` 不透出（非需求验收项，可接受）

## 潜在风险与注意事项

1. **错误码唯一性**：`3318xxx` 段已被 `core/errors/upgrade.py`（`UpgradeError`=3318001）占用，本次改用未占用段 `3327xxx`；新增错误码前必须先 grep 全局占用。
2. **REQ-03 已回退**：`APIResource` HTTPError 分支保持原样（`str(err.response.content)`），避免影响所有 api 网关错误展示及 `metadata/models/data_link/data_link.py` 的 `_is_remote_component_not_found`（消费 `BKAPIError.data.code/message`）。issue 重名链路不依赖 HTTPError 分支（kernel_api 返回 200），走 body 检查分支即可识别 code。
3. **遗留项**：`IssueNotFoundError`（Issue 不存在）仍走通用 500 + `UnknownError`(3300003)，后续可映射为专有错误码（建议 3327002）。

## 变更清单

| 文件 | 变更 |
|------|------|
| `core/errors/issue.py`（新建） | `IssueError`(3327000) 基类 + `IssueRenameConflictError`(3327001, HTTP 409) |
| `kernel_api/views/v4/issue.py` | `RenameResource` 重名异常改抛 `IssueRenameConflictError` + 中文 message |
| `packages/fta_web/issue/resources.py` | `RenameIssueResource` 识别 `data.code==3327001` 重抛专有错误 + 中文 message |

> 已回退：`core/drf_resource/contrib/api.py` 的 REQ-03 改动（HTTPError 分支 json 透传）经评估为无效改动且影响框架级回归，已撤销，保持提交前原状。

## 测试验证

- 测试代码已编写（`TestRenameIssueError` / `TestRenameResourceErrorCode` / `test_api_gateway_error.py`），TC-01（错误码常量）运行验证通过
- web 侧用例依赖 web 角色 settings（`DJANGO_CONF_MODULE=conf.web.*`），默认 pytest（worker 角色）下与现有 fta_web 测试同样受限
- 端到端建议：api-testing 验证真实 `POST /issue/rename` 重名 → HTTP 409 + code=3327001
