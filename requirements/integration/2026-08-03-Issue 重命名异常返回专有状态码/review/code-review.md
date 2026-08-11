# 📋 Code Review Report

**Commit**: `94ad79d` — feat: Issue 重命名冲突返回专有错误码(3327001)与HTTP 409，前端可识别转页面提示
**变更文件**: `core/errors/issue.py`（新增 35 行）/ `kernel_api/views/v4/issue.py`（12 行）/ `packages/fta_web/issue/resources.py`（20 行）
**关联需求**: `REQ-20260803-001《Issue 重命名异常返回专有状态码》`（匹配依据：提交语义 ↔ 需求名称 🟢）
**整体评分**: **A**（8.86/10）
**审查模式**: 深度模式（67 行）
**审查时间**: 2026-08-04

## 🎯 功能意图推测（阶段 3）

**🌍 全局图景**：业务目标 = 前端可稳定识别「同业务重名」错误并转页面友好提示｜系统位置 = 前端 → web `RenameIssueResource` → `api.issue.rename`(APIResource) → kernel_api `RenameResource` → `IssueDocument.rename()` 抛 `IssueNameDuplicatedError` → 转 `IssueRenameConflictError` 逐级透传｜整体成功判据 = ① 前端收到 HTTP 409 + code 3327001 + 中文 message；② 其他错误原样传播不误转码；③ 成功路径行为不变

| 代码位置 | 推测的功能意图 | 确认状态 | 置信度 |
|----------|---------------|----------|--------|
| `core/errors/issue.py` `IssueRenameConflictError` | 定义专有错误类：code=3327001 + 语义注释 HTTP 409 | ⏩ 免确认（需求文档锚定） | 🟢 |
| `kernel_api/views/v4/issue.py:215-217` `RenameResource` | 捕获 `IssueNameDuplicatedError` 改抛专有错误（不再抛 ValidationError） | ⏩ 免确认 | 🟢 |
| `fta_web/issue/resources.py:968-981` `RenameIssueResource` | 捕获 `BKAPIError`，识别 `data.code==3327001` 后重抛专有错误 + 中文 message | ⏩ 免确认 | 🟢 |

## 📊 维度评分概览

| 维度 | 评分 | 状态 |
| ---- | ---- | ----- |
| 🔑 语义一致性 | 8.5/10 | ⚠️ |
| ⚠️ 安全性 | 9/10 | ✅ |
| 🐛 Bug 风险 | 8.5/10 | ⚠️ |
| 📐 代码规范 | 9/10 | ✅ |
| 🏗️ 架构设计 | 8.5/10 | ⚠️ |
| ⚡ 性能 | 10/10 | ✅ |
| 🧪 测试覆盖 | 8.5/10 | ⚠️ |

## 🔑 语义一致性分析

**[M1]** `status_code=409` 跨角色隐式契约（🟡 P2）——`IssueRenameConflictError.status_code=409` 被 kernel_api 与 web 两处共用：kernel_api 端经 `api_exception_handler`（`Response(json_data)` 无 status → 默认 HTTP 200）忽略该值，web 端经 `custom_exception_handler` 生效返回 409。主链路经源码逐行推演**确认可达**（web 网关走 body 检查分支而非 HTTPError 分支），但依赖隐式默认行为，未来 `api_exception_handler` 变更或错误在 custom_exception_handler 上下文被抛出将导致 409 穿透 → 识别失败。建议类注释显式声明。

**[M2]** api 端 `data={"name": ...}` 为死字段 + 测试 mock 与真实链路不符（🟡 P2）——`api_exception_handler` 的 data 白名单（error_code/next_actions）丢弃 name，web 端 `e.data.get("data")` 恒为 `{}`；`test_issue_rename_conflict.py` 的 `_conflict_body()` mock `data={"name":"dup"}` 并断言 `err.data == {"name":"dup"}` 与真实行为不符。

**[M3]** 重名冲突从"静默"变"ERROR 级日志"（🟢 P2）——`api_exception_handler:30-31` 对非 ValidationError 固定 `logger.exception`，每次重名误操作产生 ERROR traceback。

## 🛤️ 条件路径与数据流分析

**参数路径（0.7）**：web 端 `e.data` 为 dict 且 code 匹配 → 转码重抛；非 dict/缺 code → `str(None)!=str(3327001)` → `raise` 原样传播 ✅ 健壮

**数据流守恒（0.9）**：

| 数据实体 | 流向变化 | 数量变化 | 内容变化 | 异常路径归宿 | 结论 |
|----------|----------|----------|----------|--------------|------|
| 重名错误响应 | ❌ code 3300004/3301001 → 3327001 | ✅ 无 | ✅ message 英文→中文、data 收缩 | ✅ web 端转码后渲染 409 | ✅ |

**新增数据贯通（0.9）**：

| 新增数据元素 | 正向贯通 | 反向消费 | 结论 |
|--------------|----------|----------|------|
| `code=3327001` | ✅ api role → HTTP 200 body → web body 检查分支 → 识别 → web 409 | ✅ 前端（仓库外，需人工确认） | ✅ |
| `data.name` | ❌ 断链于 `api_exception_handler` 白名单 | 🟡 死字段（需求文档已知接受） | ⚠️ |

**搭车变更审计（0.10）**：

| 搭车变更位置 | 改动性质 | 围栏检查 | 正确性 | 结论 |
|--------------|----------|----------|--------|------|
| `RegenerateTitleResource` 两处格式化 | 纯格式化（多行→单行） | ✅ 原写法非故意 | ✅ 无语义变化 | ✅ 放行 + 建议拆独立提交 |

## 🔴 严重问题（P0）

无。

## 🟡 建议改进（P1/P2）

1. **[M1] `IssueRenameConflictError` 类注释补充跨角色行为说明**——显式声明"kernel_api 端经 `api_exception_handler` 返回 HTTP 200，status_code=409 仅 web 端生效"
2. **[M2] 对齐测试 mock 与真实链路**——`_conflict_body()` 的 `data` 应为 `{}`；或需求层面明确是否要透传 name（若要则扩展 `api_exception_handler` 白名单）
3. **[M3] 重名 ERROR 日志噪音**——评估降级方案
4. **搭车变更拆分**——`RegenerateTitleResource` 格式化拆独立提交
5. **链路核心契约补测试**（challenger C1）——补 `api_exception_handler(IssueRenameConflictError)` 渲染测试，锁定 HTTP 200 + body code + data 白名单
6. **前端消费确认**（challenger C2）——人工确认前端已按 code 3327001 转页面提示，建议 api-testing 端到端验证

## 🟢 亮点

- 错误码段 3327xxx 经 grep 确认未占用，避开 upgrade 3318001 段
- 跨角色状态码设计巧妙：同一错误类在不同部署角色下（api_exception_handler 返回 200 / custom_exception_handler 返回 409）恰好满足需求设计的双态链路
- web 端识别逻辑健壮：`isinstance(e.data, dict)` 前置判断 + `str()` 双端比较，非 dict/缺 code 安全 fallthrough
- 中文 message 用 gettext，支持 i18n
- 测试资产完备（7 用例，两种角色运行方式文档化）

## 📝 总结与行动项

**🎯 合入结论**：✅ **可直接合入**（无 P0；主链路经源码逐行推演确认可达）

**📌 合入后跟进**：

| 优先级 | 行动项 | 关联语义 |
| ------ | ------ | -------- |
| P2 | 补充 `IssueRenameConflictError` 跨角色 status_code 行为注释（M1） | #S3 |
| P2 | 对齐 `test_issue_rename_conflict.py` mock 与真实 `api_exception_handler` 行为（M2） | #A1 |
| P2 | 补链路核心契约渲染测试（challenger C1） | #A1 |
| P2 | 人工确认前端消费 code 3327001 + api-testing 端到端验证（challenger C2） | #A2 |
| P2 | 评估重名 ERROR 日志噪音（M3/C4） | #A1 |
| P2 | `RegenerateTitleResource` 格式化搭车变更拆独立提交（0.10/C3） | - |
| P3 | 专家契约增量更新：`RenameIssueResource` 参数名 `name`→`new_name`、异常清单补 `IssueRenameConflictError` | #S5 |

---

### 🧨 阶段 7 结论（challenger 接力）

自动质疑已执行（`review/challenge-report.md`）：无 🔴 高风险质疑，所有质疑点均非阻塞级 → **维持 ✅ 合入结论**。质疑点 C1/C2/C4 已并入上方 P2 清单。

### 🧪 阶段 8 测试验证

**测试建议区项**：① 真实 kernel_api → `api_exception_handler` 输出（HTTP 200 + body 结构 + data 白名单）；② 端到端 `POST /issue/rename` 重名 → web 409 + code 3327001。
**执行情况**：环境受限（需 api 角色 + 完整检出，`.module-experts` 测试已 7 passed 验证错误类/转码逻辑），动态端到端验证**建议接力 api-testing / e2e-testing**（需求文档已推荐）。已知测试 `test_api_gateway_error.py` 源码被稀疏检出排除（仅 pyc 缓存），当前不可运行，建议完整检出后补跑。
