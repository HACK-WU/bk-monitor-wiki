# 已知单元测试失败：Issue 专家

> 记录在**当前开发环境**（稀疏检出 43%、Django 4.2.27、pyenv 3.11.10 + 项目 `.venv`）下运行 Issue 测试时遇到的失败与规避方式。
> 逐切面标注：哪些失败属于**环境问题**（换角色/完整检出可消除），哪些属于**测试本身限制**。

---

## 全局前置（所有切面）

| # | 问题 | 影响 |
|---|------|------|
| G1 | `pyproject.toml` 的 `filterwarnings` 引用 `RemovedInDjango51Warning`，Django 4.2.27 无此属性 | pytest 启动即解析失败（EXIT=4），任何测试需追加 `--override-ini "filterwarnings="` |
| G2 | 环境变量需显式注入（`D:` 前缀在变量已置空时不生效） | 需 `export BKAPP_DEPLOY_PLATFORM=community DJANGO_CONF_MODULE=<角色> USE_DYNAMIC_SETTINGS=0` |
| G3 | 系统 Python 缺 `bkcrypto` | 必须使用 `.venv/bin/python` |

---

## 1. kernel_api RPC 切面（bkm-cli Issue 诊断）

### `kernel_api/rpc/tests/test_bkm_cli_inspect_issue.py`（收集期失败）

- **执行方式**：
  ```bash
  cd /root/bk-monitor/bkmonitor
  BKAPP_DEPLOY_PLATFORM=community DJANGO_CONF_MODULE=conf.worker.development.community USE_DYNAMIC_SETTINGS=0 \
    .venv/bin/python -m pytest kernel_api/rpc/tests/test_bkm_cli_inspect_issue.py -q --override-ini "filterwarnings="
  ```
- **失败时间**：2026-08-03
- **失败原因**：`RuntimeError: Model class monitor_web.extend_account.models.UserAccessRecord doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.`——该文件 import 链经 `kernel_api.rpc.functions.bkm_cli` 包 `__init__` 引入 `admin/collect_config.py` → `monitor_web.models.collecting.CollectConfigMeta`，而 worker 角色 INSTALLED_APPS 不含 monitor_web。
- **修复尝试**：改用 web 角色 → 报 `AttributeError: DEFAULT_CRONTAB`（web 角色不含 alarm_backends 相关设置）。改用 **api 角色**（同时挂 monitor_web + alarm_backends）应可通过，未在本环境完成全量验证。
- **影响**：bkm-cli Issue 诊断 20 个用例当前无法运行，需 api 角色或完整部署环境。
- **来源**：expert-audit 测试验证

---

## 2. Issue 查询切面（趋势契约）

### `packages/fta_web/tests/issue/test_issue_trend_contract.py::test_issue_list_renders_before_trend_is_loaded`

- **执行方式**：
  ```bash
  cd /root/bk-monitor/bkmonitor
  BKAPP_DEPLOY_PLATFORM=community DJANGO_CONF_MODULE=conf.web.development.community USE_DYNAMIC_SETTINGS=0 \
    .venv/bin/python -m pytest packages/fta_web/tests/issue/test_issue_trend_contract.py -q --override-ini "filterwarnings="
  ```
- **失败时间**：2026-08-03
- **失败原因**：`FileNotFoundError: .../webpack/src/trace/pages/alarm-center/services/issues-services.ts`——用例读取前端 TS 源文件验证"前端先渲染列表再加载趋势"契约，当前稀疏检出（43%）缺少该前端文件。
- **修复尝试**：未尝试（需完整检出前端源码）。
- **影响**：仅该 1 条用例失败，其余 3 条通过；完整检出后可过。
- **来源**：expert-audit 测试验证

---

## 3. 状态聚合切面（合并/拆分）——角色选择注意

### `alarm_backends/tests/service/fta_action/test_issue_merge.py`（worker/web 角色下部分失败）

- **执行方式**（正确姿势：**api 角色**）：
  ```bash
  cd /root/bk-monitor/bkmonitor
  BKAPP_DEPLOY_PLATFORM=community DJANGO_CONF_MODULE=conf.api.development.community USE_DYNAMIC_SETTINGS=0 \
    .venv/bin/python -m pytest alarm_backends/tests/service/fta_action/test_issue_merge.py -q --override-ini "filterwarnings="
  ```
- **失败时间**：2026-08-03（仅记录错误角色下的失败现象）
- **失败原因**：该文件部分用例同时 `import kernel_api.views.v4.issue.MergeResource` 与 `fta_web.issue.resources.MergeIssueResource`，需要 monitor_web + alarm_backends 同时注册。**worker 角色**（8 failed）报 `UserAccessRecord`/`SearchHistory` app_label 错误；**web 角色**（5 failed）报 `DEFAULT_CRONTAB` 缺失。
- **修复尝试**：改用 **api 角色** → **72 passed 全绿**。确认非逻辑问题，是角色选择错误。
- **影响**：无——按 api 角色运行即可全过。本文档记录以防他人误用 worker/web 角色。
- **来源**：expert-audit 测试验证

---

## 结论

- **✅ 全绿（当前环境可跑）**：`test_issue_fingerprint.py`（64）、`test_issue_llm_title.py` + `test_regenerate_issue_llm_title_command.py`（93）、`test_issue_resources.py`（21）、`test_issue_merge_expand.py`（10）、`test_issue_activities_contract.py`（7，AST 免依赖）、`test_issue_v4.py`、`test_issue_merge.py`（72，**需 api 角色**）。
- **✅ 全绿（本次新增）**：`test_issue_rename_conflict.py`（REQ-20260803-001 专有状态码）——**自包含环境**（顶部 `import hello` 加载 Django 环境，无需手动配置），两种角色：
  - web 角色（默认）→ 7 passed, 2 skipped（仅 kernel_api `RenameResource` 用例因角色环境自动 skip；`api_exception_handler` 渲染用例依赖轻量，web 角色下同样可执行）
  - api 角色（`BK_ISSUE_TEST_ROLE=api`）→ 9 passed 全绿
  - 已覆盖：错误类常量 / kernel_api 抛专有错误 / web 端转码（mock 对齐真实 `api_exception_handler` data 白名单）/**渲染契约锁定**（HTTP 200 + body code=3327001 + data 白名单拦截 name）
  - 运行：`bkmonitor/.venv/bin/python -m pytest -p no:django .module-experts/issue专家/test/test_issue_rename_conflict.py -q`
- **⚠️ 环境受限**：`test_bkm_cli_inspect_issue.py`（需 api 角色/完整环境）、`test_issue_trend_contract.py` 1 条（需前端完整检出）。
- **全局前置**：`--override-ini "filterwarnings="` + 显式环境变量 + `.venv` + **按切面选择角色**（worker/web/api），角色选错会出现"假失败"。
