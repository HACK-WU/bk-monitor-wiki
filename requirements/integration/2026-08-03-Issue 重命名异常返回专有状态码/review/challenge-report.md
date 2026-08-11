# 🎯 质疑报告：Issue 重命名冲突返回专有错误码（REQ-20260803-001）

> 调用方：code-review 阶段 7（无阻塞项自动接力）
> 质疑对象：提交 `94ad79d`（代码变更 · 新增功能）
> 输入上下文：diff + 权威语义（需求文档）+ 全局图景 + code-review 报告结论（A / ✅ 可合入）
> 生成时间：2026-08-04

## 结论摘要

| 质疑点 | 等级 | 质疑是否成立 | 主 review 是否覆盖 |
|--------|------|--------------|--------------------|
| C1 链路核心隐式契约无测试锁定（api_exception_handler 返回 200） | 🟡 中 | ⚠️ 部分成立（测试缺陷） | 已指出 mock 偏差，未升级为「契约无测试锁定」 |
| C2 消费端（前端）端到端闭环未验证 | 🟡 中 | ⚠️ 成立（`[待确认]`） | 已标注"消费方在仓库外" |
| C3 搭车变更（RegenerateTitleResource 格式化）审查缺全局回扣论证 | 🟢 低 | ⚠️ 轻微成立 | 已立案（0.10），缺全局论证 |
| C4 kernel_api message 含英文+内部字段 | 🟢 低 | ⚠️ 不成立（无消费方受影响） | 已覆盖 |
| C5 测试 mock 与真实 api_exception_handler 行为不符 | 🟡 中 | ⚠️ 成立 | 已覆盖（M2） |

**总体风险**：🟢 低风险 —— 无 🔴 高风险质疑，无阻塞项；所有质疑点均不推翻主 review 的 ✅ 合入结论，并入「合入后跟进」清单。

---

## 阶段0：需求确认

- **功能目标**：重命名冲突（同业务重名）返回专有状态码（code 3327001），前端稳定识别并转页面友好提示
- **功能输入**：`POST /issue/rename`（bk_biz_id, issue_id, new_name）
- **功能输出**：重名时 HTTP 409 + `{code: 3327001, message: "已存在同名 Issue，请更换名称"}`
- **触发条件**：同业务下已存在同名 Issue
- **需求来源**：REQ-20260803-001 需求文档（✅ 可靠，书面落盘）
- **需求理解**：开发者理解与需求文档一致（✅ 无偏差）——主链路「kernel_api HTTP 200 + body code → web body 检查分支 → 识别重抛 → web 409」经源码逐行推演确认成立

## 阶段1：变更概述

- **新增文件**：`core/errors/issue.py`（IssueError 基类 + IssueRenameConflictError）
- **修改文件**：`kernel_api/views/v4/issue.py`（RenameResource 抛专有错误）、`packages/fta_web/issue/resources.py`（RenameIssueResource 识别转码）
- **搭车变更**：`kernel_api/views/v4/issue.py` RegenerateTitleResource 两处纯格式化
- **变更规模**：54 增 + 13 删 = 67 行

## 阶段2-4：需求覆盖 / 边界 / 兼容性验证（对抗式复核）

主 review 已逐项覆盖，质疑者复核结论：

- **主流程**：✅ 完整——web 端重名时「识别 3327001 → 重抛 → 409 + 中文」链路可达
- **分支流程**：✅ 完整——非重名 BKAPIError 原样传播；`e.data` 非 dict / code 缺失时安全 fallthrough
- **异常流程**：✅ 已处理——api role 经 `api_exception_handler` 返回 HTTP 200（`Response(json_data)` 无 status 参数，DRF 默认 200），web 网关走 body 检查分支而非 HTTPError 分支
- **输入边界**：✅ `new_name` strip 校验（api 端 + web 端 serializer 双校验）
- **接口兼容**：⚠️ 对外契约从「HTTP 500 + code 3301001/3300004」变为「HTTP 409 + code 3327001」——这是**有意的行为变化**（需求目标），且 web 端是唯一对外入口，无其他后端消费方依赖旧行为
- **数据兼容**：✅ 无持久化数据变化
- **行为影响**：⚠️ 重名冲突从「不记日志的 ValidationError」变为「记 ERROR traceback 的 IssueRenameConflictError」（见 C6，主 review M3 已覆盖）

## 阶段5：风险验证

- **依赖风险**：🟢 低——无新增第三方依赖
- **安全风险**：🟢 低——无注入/越权/泄露；api 端 message 含 `bk_biz_id`/`name`（业务数据，非敏感）
- **性能风险**：🟢 低——无性能影响
- **维护风险**：🟡 中——跨角色状态码隐式契约（M1）+ 链路核心无测试锁定（C1）

## 阶段5.5：体验质量质疑

- **正向体验**：✅ 重名时前端可转友好页面提示（需求目标达成，前提是前端消费 code，见 C2）
- **负向体验**：⚠️ 用户重名误操作时，kernel_api 端会产生 ERROR 级日志 + 全量 traceback（C6，主 review M3）——预期业务异常记 ERROR 会造成日志噪音

## 阶段6：极端条件验证（核心推演）

### 核心变化1：api role 错误响应从 HTTP 200+code 400 变为 HTTP 200+code 3327001

**推演场景**：

| 场景 | 条件 | 预期行为 | 风险 |
|------|------|----------|------|
| 正常 | api role 返回 HTTP 200 + body code=3327001 | web 网关 body 检查分支 → BKAPIError(data=完整 dict) → web 端识别 → 409 | ✅ 无 |
| 隐式契约被破坏 | 未来 `api_exception_handler` 增加 `status=exc.status_code` 或 `IssueRenameConflictError` 在 web 端 custom_exception_handler 上下文被抛出 | 409 穿透到 HTTP 层 → web 网关 `raise_for_status` → HTTPError 分支 → `e.data` 变字符串 → **识别失败**，前端回到旧体验（500 + 通用错误） | 🟡 **链路静默降级**，无报错但需求失效 |
| 前端未消费 | 前端仍按旧逻辑判断 | 前端拿到 409 + 3327001 但无对应分支 → 可能仍展示通用错误 | 🟡 需求未闭环 |

**核心变化2：data.name 透传**

| 场景 | 条件 | 预期行为 | 风险 |
|------|------|----------|------|
| 正常 | api 端 `data={"name": ...}` | `api_exception_handler` 白名单仅透传 error_code/next_actions → name 丢弃 → web 端 data={} | 🟡 死字段，需求文档已知接受 |

## 阶段7：风险评估与建议

### 成立质疑（非阻塞级）

| # | 质疑点 | 等级 | 证据 | 建议 |
|---|--------|------|------|------|
| C1 | **链路核心隐式契约无有效测试锁定**：`api_exception_handler` 返回 HTTP 200 + data 白名单是整条链路的命脉，但可运行测试（`test_issue_rename_conflict.py`）只 mock 理想链路响应（`data={"name":"dup"}`），未覆盖 api_exception_handler 的真实渲染（data={}）；`test_api_gateway_error.py` 源码被稀疏检出排除，当前不可运行 | 🟡 中 | pyc 缓存存在但源码不在工作区；mock 与真实行为不符（主 review M2） | 补一个针对 `api_exception_handler(IssueRenameConflictError)` 的渲染测试（断言 HTTP 200 + body code + data 白名单），将隐式契约显式锁定 |
| C2 | **消费端（前端）端到端闭环未验证**：本次提交只完成后端「生产端」，前端是否已按 code=3327001 消费无法确认（仓库外/稀疏检出不含）；若前端未同步，本次改动对用户体验零影响 | 🟡 中 | webpack/src 下 grep `3327001` 无命中 | 人工确认前端分支已按 code 3327001 转页面提示；建议 api-testing 端到端验证真实 `POST /issue/rename` 重名 |
| C3 | **搭车变更审查缺全局回扣论证**：主 review 对 RegenerateTitleResource 两处格式化给出了正确性判断（✅ 纯格式化），但未做全局回扣论证（改动点 → 调用链 → 判据） | 🟢 低 | 语法等价性可证（多行↔单行无 AST 差异） | 拆独立提交，保持变更原子性 |
| C4 | **重名冲突 ERROR 日志噪音**：api_exception_handler 对非 ValidationError 固定 `logger.exception`（ERROR + traceback），重名属预期业务异常 | 🟡 中 | `kernel_api/exceptions.py:30-31` | 团队确认是否接受；评估将 IssueRenameConflictError 纳入 IGNORE_EXCEPTIONS 或降级日志 |

### 不成立质疑（已被主 review 覆盖 / 证据排除）

| # | 质疑点 | 不成立依据 |
|---|--------|-----------|
| C5 | HTTP 409 穿透导致 web 网关识别失败 | 已排除——api role 用 `api_exception_handler`（非 custom_exception_handler），`Response(json_data)` 无 status → 默认 HTTP 200，web 网关走 body 检查分支 |
| C6 | 错误消息泄露内部信息 | api role message 含 bk_biz_id/name 属正常业务数据，非敏感；web 端转码后最终用户只见中文 |

### 🌍 全局回扣质疑

| 全局质疑 | 结论 |
|----------|------|
| **目标回扣** | 需求目标「前端识别重名并转友好提示」在后端链路**可达**（✅），但**闭环依赖前端消费**（C2，`[待确认]`） |
| **位置回扣** | 调用链「前端 → web RenameIssueResource → HTTP → kernel_api → ES」中，改动点在中段错误处理，无放大风险（✅） |
| **判据回扣** | ① 成功路径不变 ✅；② 其他错误不误转码 ✅；③ 重名可识别 ⚠️——依赖 api_exception_handler 隐式 200 行为（C1，脆弱但当前成立） |

### 行动建议

**建议处理（🟡）**：
1. 补 `api_exception_handler(IssueRenameConflictError)` 渲染测试，显式锁定 HTTP 200 + body code + data 白名单契约（C1）
2. 人工确认前端已按 code=3327001 消费；建议 api-testing 端到端验证真实重名链路（C2）
3. 评估重名冲突 ERROR 日志噪音处理方案（C4）

**可选处理（🟢）**：
4. RegenerateTitleResource 搭车格式化拆独立提交（C3）

## 质疑对主 review 结论的影响

所有质疑均非阻塞级（无 🔴）→ **维持 code-review 结论：✅ 可直接合入**。质疑点 C1/C2/C4 并入「合入后跟进」P2 清单，C3 并入 P2。
