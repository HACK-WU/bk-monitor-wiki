---
name: local-kernel-api-proxy
description: 本地联调 bk-monitor web 进程调用 kernel_api 的解决方案，通过转发代理 + 环境变量覆盖 API base_url，无需真实 APIGW 网关。触发词：kernel_api 本地联调、web 调 kernel_api、BKAPP_NEW_MONITOR_API_BASE_URL、本地 api 进程、Cannot assign requested address
category: integration
tags: [kernel_api, 本地联调, 转发代理, BKAPP_NEW_MONITOR_API_BASE_URL, .env]
created: 2026-08-04
updated: 2026-08-04
---

# 本地 web 进程 → kernel_api 联调（转发代理方案）

## 场景

bk-monitor 开发中，web 角色（`fta_web` / `monitor_web`）里的 Resource 会调用 `api.issue.rename` 这类 `KernelAPIResource`。默认情况下这些调用走真实 APIGW 网关（`BK_COMPONENT_API_URL/api/bk-monitor/{stage}/...`），本地没有网关导致无法联调，报错形如：

```
BKAPIError: 请求系统'issue'错误，返回消息: {...Error response...}
```

需要让 web 进程的 kernel_api 调用直接打到本地 api 角色进程（`python manage.py runserver bkm-dev.paas3-dev.bktencent.com:9000`）。

## 问题

1. **URL 无法直接改**：`api.issue.rename` 的 `base_url` 默认指向真实网关，本地请求会 502/超时。
2. **路径不一致**：web 进程发出的 APIGW 对外路径是 `/app/issue/rename/`，而本地 kernel_api 实际挂载在 `/api/v4/issue/rename/`（映射由 APIGW yaml 完成，本地无网关所以差一层）。
3. **Host 头鉴权**：本地 api 进程用域名启动（`runserver bkm-dev.paas3-dev.bktencent.com:9000`），kernel_api 的鉴权（blueapps login/session）要求请求 `Host` 头匹配该域名；直接用 `127.0.0.1` 做 target 会导致鉴权失败。
4. **IPv6 坑**：`--target http://localhost:...` 可能把 `localhost` 解析到 `::1`，而本地进程监听 IPv4 `127.0.0.1`，报 `[Errno 99] Cannot assign requested address`（这不是鉴权错误，是 TCP 连接层失败）。
5. **Cookie**：本地调用 kernel_api 需要携带会话 Cookie（`bk_monitorv3_sessionid` 等）。

## 解决方案

核心思路：**不改任何主分支代码**，用「环境变量覆盖 base_url」+「本地转发代理」打通链路。

### 1. 官方覆盖项：`BKAPP_NEW_MONITOR_API_BASE_URL`

`api/issue/default.py`（以及 api/monitor、api/metadata、api/rum_api、api/apm_api 共用）：

```python
base_url = (
    settings.NEW_MONITOR_API_BASE_URL
    or f"{settings.BK_COMPONENT_API_URL}/api/bk-monitor/{settings.APIGW_STAGE}/"
)
```

设置环境变量即可把 base_url 指向本地代理，`api.issue.rename` 请求 `http://localhost:18080/app/issue/rename/`。

### 2. 转发代理脚本

脚本位置：`devtools/kernel_api_proxy.py`（项目根 devtools/ 下，不进主分支）。

**本 solution 自带副本**：`scripts/kernel_api_proxy.py`（与 devtools 下版本一致）。部署到新环境时把副本拷贝到目标项目的 `devtools/` 或任意目录，确保它能找到项目根 `.env`（脚本用 `__file__` 向上两层定位 `.env`；若目录层级变化需调整 `env_path`）。

功能：
- `/app/*` 前缀重写为 `/api/v4/*`（`/app/issue/rename/` → `/api/v4/issue/rename/`）
- `localhost`/`::1` 归一化为 `127.0.0.1`（避免 IPv6 `Cannot assign requested address`）
- 透传 method / body / 非 hop-by-hop headers
- 从环境变量附加 Cookie
- 自动从项目根 `.env` 加载配置（不覆盖已存在环境变量）

### 3. 完整配置

`.env`（项目根目录，代理启动时自动加载）：

```bash
KERNEL_API_PROXY_TARGET=http://bkm-dev.paas3-dev.bktencent.com:9000
KERNEL_API_PROXY_COOKIE=bk_biz_id=2; bk_monitorv3_sessionid=...
BKAPP_NEW_MONITOR_API_BASE_URL=http://localhost:18080/
```

启动：

```bash
python3 devtools/kernel_api_proxy.py --listen 18080
```

**注意 target 必须用域名**（不是 127.0.0.1），因为转发时 Host 头取自 target 的 host，鉴权需要域名匹配。

## 关键代码

```python
# devtools/kernel_api_proxy.py 核心转发逻辑
REWRITE_RULES = [("/app/", "/api/v4/")]

# 转发：http.client 连接 target，Host 头自动取自 target_host
conn = http.client.HTTPConnection(self.server.target_host, self.server.target_port, timeout=300)
conn.request(method, path, body=body, headers=headers)
```

```python
# load_dotenv：从项目根 .env 加载，不覆盖已有环境变量
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
```

## 注意事项

1. **target 必须用域名**：kernel_api 鉴权要求 Host 头匹配启动域名（`bkm-dev.paas3-dev.bktencent.com`），用 `127.0.0.1` 会鉴权失败。
2. **`Cannot assign requested address` 是连接层错误不是鉴权**：`localhost` 解析到 `::1` 导致，用 `127.0.0.1` 或确保 hosts 域名解析正确。
3. **`BKAPP_NEW_MONITOR_API_BASE_URL` 影响多个模块**：api/monitor、api/metadata、api/rum_api、api/apm_api 都共用，本地调试时这些调用也会走代理（可接受）。
4. **`/app` → `/api/v4` 映射依赖 APIGW yaml**：新增接口若不同步 `support-files/apigw/resources/**/*.yaml` 的 backend.path，代理重写会 404。
5. **`direct_request` 另一条路**：`KernelAPIResource`（`core/drf_resource/contrib/nested_api.py`）在 `settings.ROLE == "api"` 时走进程内 `direct_request`（不经 HTTP、不鉴权），适合纯逻辑测试；但 web 角色 HTTP 链路联调仍需本代理方案。
6. 脚本纯 Python 标准库，无第三方依赖；配置全部走 `.env`/环境变量，不写死。
