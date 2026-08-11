# 已知单元测试失败：kernel_api 网关专家

> 切面级汇总：父专家汇总各子专家条目。维护者：code-review 阶段 8 / expert-lookup 增量更新。
> **当前状态（2026-08-06）**：专家创建时未在本环境实际执行测试（静态检查），**暂无已确认的已知失败条目**。以下为各子专家测试的执行方式，供验证与后续追加。

## 认证与安全子专家

- 无对应单测文件（`middlewares/authentication.py` 测试缺口，见 implementation/06-测试.md），无可执行用例。

## RPC 函数注册子专家

### 通用执行方式

```bash
cd /root/bk-monitor/bkmonitor
/root/bk-monitor/bkmonitor/.venv/bin/python -m pytest bkmonitor/kernel_api/rpc/tests/ \
    --override-ini "filterwarnings=" -o addopts=""
```

- 环境依赖：Django settings 初始化（api 角色）+ `.venv` + 显式 `BKAPP_DEPLOY_PLATFORM=community` 等环境变量。
- 已知风险（未实证）：`test_admin_rpc.py`（137KB）覆盖极广，存在因全局注册表状态 / DB 残留导致的不稳定可能——若实际跑出失败，请按下面模板追加条目。

## 内部 Resource 复用子专家

### 通用执行方式

```bash
cd /root/bk-monitor/bkmonitor
/root/bk-monitor/bkmonitor/.venv/bin/python -m pytest bkmonitor/kernel_api/tests/test_alert_mcp.py \
    bkmonitor/kernel_api/tests/test_log_search.py \
    bkmonitor/kernel_api/tests/test_log_extract.py \
    bkmonitor/kernel_api/tests/test_scene_log_search_resource.py \
    bkmonitor/kernel_api/tests/test_k8s_resource_candidates.py \
    --override-ini "filterwarnings=" -o addopts=""
```

## v4 API 视图子专家

### 通用执行方式

```bash
cd /root/bk-monitor/bkmonitor
/root/bk-monitor/bkmonitor/.venv/bin/python -m pytest bkmonitor/kernel_api/tests/test_issue_v4.py \
    --override-ini "filterwarnings=" -o addopts=""
```

---

## 追加模板（code-review 阶段 8 / expert-lookup 使用）

### {切面/子专家名}

### {测试文件路径}:{测试函数名}

- **执行方式**：{运行该测试的完整命令}
- **失败时间**：{date}
- **失败原因**：{断言错误摘要}
- **修复尝试**：{尝试了什么，为什么未修复}
- **影响**：{对使用/验证的影响}
- **来源**：code-review 阶段 8 测试验证 / expert-lookup 增量更新
