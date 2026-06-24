---
name: api-tester
description: 在 Django 进程内直接调用 Resource 类测试监控平台接口，实现自动化 Postman 功能：URL+方法自动解析出 Resource 类、自动提取请求参数 schema 与示例、支持只校验/完整执行两种模式。当用户要求测试接口、调用接口验证、跑一下某个 URL、模拟请求某个 API、接口联调、验证接口参数是否正确时使用。触发短语包括：'测试这个接口'、'调用一下这个 API'、'跑一下这个 URL'、'验证接口参数'、'接口联调'、'测一下接口返回'。
---

# 接口测试器（api-tester）

## 概述

**目的**：无需登录态/CSRF/网关，在 Django 进程内直接调用 Resource 类，对监控平台接口做真实业务逻辑测试

**功能**：
- 给定 URL + HTTP 方法，自动解析出对应的 Resource 类（复用 `django-url-view-resolver` 的 resolve 机制）
- 从 `Resource.RequestSerializer` 自动提取参数 schema 并生成示例参数（类似 Postman 参数面板）
- 支持三种模式：`inspect`（只解析）/ `dry-run`（只校验参数）/ `run`（完整执行）

**使用场景**：
- 用户说"测试这个接口"、"跑一下这个 URL"、"调用一下这个 API"
- 接口联调时验证参数是否合法、返回是否符合预期
- 排查接口问题时，需要确认 Resource 业务逻辑的实际输出

## 原理

监控平台对外接口均通过 `ResourceViewSet` 注册，每个 URL 最终映射到一个 `Resource` 子类。`Resource.request()` 完整走"请求校验 → `perform_request` 业务逻辑 → 响应校验"链路。本 skill 绕过 HTTP/认证层，在进程内直调 `Resource.request()`，测试的是纯业务逻辑（参数校验 + perform_request + 响应校验）。

> 与真实 HTTP 测试的差异：不经过认证、权限、限流、CSRF 等中间件；依赖 HTTP 请求上下文（如 `get_request_username()`）的接口会报错，详见 [reference.md](reference.md)。

## 命令格式

```bash
/root/bk-monitor/bkmonitor/.venv/bin/python /root/bk-monitor/bk-monitor-wiki/skills/api-tester/scripts/api_tester.py <子命令> "<URL>" "<METHOD>" [-p '<参数JSON>'] [--confirm]
```

| 参数 | 必选 | 说明 |
|------|------|------|
| `<子命令>` | 是 | `inspect` / `dry-run` / `run` |
| `<URL>` | 是 | 接口路径，如 `/rest/v2/duty_plan/preview_duty_rule_plan/` |
| `<METHOD>` | 否 | HTTP 方法（GET/POST/PUT/DELETE），默认 GET |
| `-p` / `--params` | 否 | 请求参数 JSON 字符串，不传则用自动生成的示例参数 |
| `--confirm` | run 模式且非 GET 时必选 | 确认执行写操作 |

## 三种模式

| 模式 | 作用 | 是否执行业务逻辑 | 副作用风险 |
|------|------|------------------|-----------|
| `inspect` | 解析接口，输出 Resource 信息 + 参数 schema + 示例参数 | 否 | 无 |
| `dry-run` | 仅校验请求参数合法性（`RequestSerializer`） | 否 | 无 |
| `run` | 完整执行 `Resource.request()`（校验+业务+响应校验） | 是 | 非 GET 可能有写副作用 |

## 使用流程

```text
1. inspect：先用 inspect 模式查看接口参数结构，拿到 example_params
   ↓
2. 填充参数：根据 example_params 模板，结合实际场景填入真实参数值
   ↓
3. dry-run（可选）：用填好的参数做一次校验，确认参数合法
   ↓
4. run：执行接口，查看真实返回数据 / 异常堆栈 / 耗时
```

### 步骤 1：inspect

```bash
/root/bk-monitor/bkmonitor/.venv/bin/python /root/bk-monitor/bk-monitor-wiki/skills/api-tester/scripts/api_tester.py inspect /rest/v2/data_explorer/get_graph_query_config/ POST
```

输出含 `param_schema`（字段名/类型/是否必填/描述/默认值/枚举选项）和 `example_params`（可直接用的示例参数 JSON）。

### 步骤 2：填充参数

从输出的 `example_params` 复制，按 `param_schema` 中的 `description` 和 `required` 标记填入真实值。

### 步骤 3：run

```bash
/root/bk-monitor/bkmonitor/.venv/bin/python /root/bk-monitor/bk-monitor-wiki/skills/api-tester/scripts/api_tester.py run /rest/v2/duty_plan/preview_duty_rule_plan/ POST -p '{"days":7,"bk_biz_id":2}' --confirm
```

## 输出解读

所有输出为 JSON，顶层 `status` 字段：

| status | 含义 |
|--------|------|
| `ok` | 正常返回（`mode` 区分 inspect/dry-run/run） |
| `resolve_failed` | URL 未匹配到视图或非 ResourceViewSet |
| `params_error` | `-p` 的 JSON 解析失败 |
| `confirm_required` | 非 GET 的 run 未加 `--confirm`，已拦截 |
| `env_error` | Django 环境初始化失败 |
| `usage_error` | 命令格式错误 |

`run` 模式的 `result` 字段：

| result.status | 含义 |
|---------------|------|
| `success` | 执行成功，`data` 为返回数据，`cost_seconds` 为耗时 |
| `error` | 执行抛异常，含 `exception_type`/`exception_message`/`traceback` |

`dry-run` 模式的 `result` 字段：

| result.status | 含义 |
|---------------|------|
| `valid` | 参数校验通过，`validated_data` 为校验后数据 |
| `invalid` | 参数校验失败，含异常信息 |

## 安全约束

1. **非 GET 的 run 必须 `--confirm`**：脚本会拦截未确认的写操作，返回 `confirm_required`
2. **AI 执行写操作前须向用户确认**：即使加了 `--confirm`，AI 在执行非 GET 的 run 前，应向用户说明将调用哪个接口、可能产生什么副作用，征得同意
3. **无事务回滚**：进程内直调不经过 Django 事务中间件，写操作不可自动回滚，涉及 DB/外部 API 的写操作尤需谨慎

## 不适用场景

- 需要测试认证/权限/限流/CSRF 等中间件层 → 需真实 HTTP 请求或 Django Test Client
- 接口的 `perform_request` 依赖 HTTP 请求上下文（如当前登录用户 `get_request_username()`、租户 ID）→ 直调会报错，参考 [reference.md](reference.md) 的限制说明
- 已知 Resource 类名只想看代码 → 直接 grep 类名，无需本 skill
- 只想定位 URL 对应的视图代码 → 用 `url-view-resolver` skill

## 更多资源

- 限制说明、参数类型对照、常见错误排查，参见 [reference.md](reference.md)
