---
name: itsm-v4-integration-config
description: 排查监控平台对接 ITSM V4 时环境变量漏配导致「服务名称下拉暂无选项」与「前往IT服务管理中心跳 404」两类问题。触发词：ITSM V4、系统不存在、system_workflow/list、处理套餐服务名称为空、前往IT服务管理中心 404、BK_ITSM_V4_SYSTEM_ID、BK_ITSM_V4_HOST、create_itsm_v4_system、BKAPIError 3301001
category: integration
tags: [ITSM, ITSM_V4, 处理套餐, 环境变量, 系统不存在, BK_ITSM_V4_SYSTEM_ID, BK_ITSM_V4_HOST, 404]
created: 2026-10-23
updated: 2026-10-23
version: 1
---

# 监控平台对接 ITSM V4 的环境变量配置排查

## 场景

监控平台（bk-monitor）「处理套餐」的「IT 服务管理中心」插件通过新版 ITSM V4 接口拉取服务/流程列表。新环境部署或环境变量漏配时，会出现两类**看起来像前端 bug、实际是配置缺失**的现象：

- 现象 A：新建处理套餐时，「服务名称」下拉框显示「暂无选项」，接口报 `系统不存在`
- 现象 B：点击下拉框底部「前往IT服务管理中心」链接，跳到监控平台自己的 `/exception` 404 页

两者根因不同，必须分别修，只修一个另一个仍坏。

## 问题

### 现象 A：下拉框「暂无选项」

后端返回的原始错误（`bytes` 转义已解码）：

```json
{
  "result": false,
  "code": 200,
  "message": "请求系统'common'错误，返回消息: {'message': 'b'{\"result\":false,\"code\":\"40000\",\"message\":\"系统不存在\",\"data\":{\"detail\":\"系统不存在\"}}''}",
  "error_details": {
    "type": "BKAPIError",
    "code": 3301001,
    "overview": "请求系统'common'错误，",
    "detail": "b'{\"result\":false,\"code\":\"40000\",\"message\":\"系统不存在\",\"data\":{\"detail\":\"系统不存在\"}}'",
    "popup_message": "warning"
  }
}
```

`error_details.code = 3301001` 是 `BKAPIError`（`bkmonitor/core/errors/api.py:26`），`message_tpl` 为 `请求系统'{system_name}'错误，`（同文件 `:33`）。外层 `code: 200` 说明 HTTP 层正常，**监控平台自身没故障**，失败发生在对 ITSM 的调用。

真实失败点：请求 `/api/v1/system_workflow/list/`，ITSM 返回 `40000 系统不存在`。

**关键点：`BK_ITSM_V4_SYSTEM_ID` 未配置时不会报错，而是静默回退到 `APP_CODE`**（`bkmonitor/config/default.py:1345`），于是代码照常发起请求，ITSM 侧自然找不到该 code 的系统。排查时极易误判为接口 bug。

### 现象 B：跳转 404

点击「前往IT服务管理中心」后，浏览器地址变为 `https://<监控域名>/#/system/processList`（或最终落到 `#/exception`），渲染监控自己的「页面不存在」兜底页。

这不是 ITSM 挂了，而是 `BK_ITSM_V4_HOST` 为空串，模板渲染出的是**相对路径**，浏览器把相对路径拼到了监控平台域名上。监控前端没有 `/system/processList` 路由，路由匹配失败后走 `router.ts:77` 的 `redirect: '/exception'`，最终由 `exception-page.vue` 以默认 `type='404'` 渲染。

## 根因

| 现象 | 根因变量 | 变量默认值 | 后果 |
|---|---|---|---|
| A 下拉暂无选项 | `BK_ITSM_V4_SYSTEM_ID` | `APP_CODE`（非空！） | 请求打到 ITSM，但系统不存在 |
| B 跳转 404 | `BK_ITSM_V4_HOST` | `""` | 链接变相对路径，跳到监控自己域下 |

同一段配置还有第三个变量 `BK_ITSM_V4_API_URL`，默认 `{BK_COMPONENT_API_URL}/api/cw-aitsm/prod`，一般能通，不是这两个现象的原因。

## 解决方案

### Step 1：先确认三个变量的**生效值**

不要只看环境变量，`settings` 里才是运行时真正用的值（可能被 `BKAPP_SETTINGS_` 前缀覆盖）。

```python
from django.conf import settings
import os

APP_CODE = getattr(settings, "APP_CODE", None)
print("APP_CODE =", APP_CODE)
print("-" * 72)

for key in ("BK_ITSM_V4_SYSTEM_ID", "BK_ITSM_V4_API_URL", "BK_ITSM_V4_HOST"):
    print(key)
    print("  生效值     :", repr(getattr(settings, key, "<未定义>")))
    print("  环境变量   :", repr(os.getenv(key)))
    print("  BKAPP 覆盖 :", repr(os.getenv("BKAPP_SETTINGS_" + key)))
    print()

sid = getattr(settings, "BK_ITSM_V4_SYSTEM_ID", None)
if sid == APP_CODE:
    print("[注意] SYSTEM_ID 等于 APP_CODE，极可能未配置而走了默认回退")
```

执行方式（容器内通常无需手动指定 `DJANGO_CONF_MODULE`）：

```bash
cd bkmonitor
python manage.py shell < check_itsm_vars.py
```

若在容器外手动跑，必须补齐角色配置，否则 `settings` 加载失败：

```bash
DJANGO_CONF_MODULE=conf.web.development.community python manage.py shell
```

判定：`生效值 == APP_CODE`（常见 `bk_monitorv3`）基本可确定是未配置。

### Step 2：修现象 A —— 在 ITSM 侧创建系统

先取当前实际生效的 `system_id`，再执行创建。`--code` **必须显式写成该值**：

```bash
python manage.py create_itsm_v4_system --name "蓝鲸监控平台" --code bk_monitorv3
```

执行位置：监控平台后端的 Python 容器，工作目录为 `bkmonitor/`（`manage.py` 所在目录）。命令依赖 `settings.BK_ITSM_V4_API_URL` 与后台用户身份（`CommonBaseResource.perform_request` 会注入 `_origin_user`，来自 `get_global_user()`），这些都由容器环境提供。

首次执行预期输出：

```text
✓ 系统 [bk_monitorv3] 不存在，准备创建...
正在创建系统...
✓ 系统创建成功！
```

该命令内部用同一个 `system_workflow/list/` 接口探测，并把「系统不存在」当正常分支继续创建，所以命令能跑通即代表该报错会消失。

### Step 3：修现象 B —— 补 `BK_ITSM_V4_HOST`

在部署配置中补上 ITSM V4 的**站点**地址（注意不是接口网关）：

```bash
BK_ITSM_V4_HOST=https://apps.paas3-dev.bktencent.com/cw--aitsm
```

末尾带不带 `/` 都行，代码会 `.rstrip("/")`。但**不能是 `None`**，否则 `rstrip` 直接抛异常。

提测/生产环境要填该环境自己的 ITSM 站点域名，不能照抄 dev 的值。

### Step 4：重启并验证

改环境变量后必须**重启服务**，因为 `settings` 在进程启动时加载。

插件配置本身是落库的：`packages/fta_web/handlers.py` 的 `register_builtin_plugins` 用 `update_or_create` 把 `support-files/fta/action_plugin_initial.json` 写入 `ActionPlugin` 表。但 `itsm_v4_site_url` 等值属于 `ActionPlugin.PUBLIC_PARAMS`，**在渲染时从 `settings` 实时读取**，所以重启后新值自动生效，通常无需重新同步插件。

验证顺序：

1. 再跑一次创建命令，返回「系统ID [...] 已存在，无需重复创建」→ 系统已就位
2. 回到处理套餐页，服务名称下拉应能拉到列表
3. 点击「前往IT服务管理中心」，应跳到 ITSM 站点而非监控的 404

## 关键代码

变量定义（`bkmonitor/config/default.py:1342-1345`）：

```python
# 新版ITSM
BK_ITSM_V4_HOST = os.getenv("BK_ITSM_V4_HOST", "")
BK_ITSM_V4_API_URL = os.getenv("BK_ITSM_V4_API_URL", f"{BK_COMPONENT_API_URL}/api/cw-aitsm/prod")
BK_ITSM_V4_SYSTEM_ID = os.getenv("BK_ITSM_V4_SYSTEM_ID", APP_CODE)
```

注入模板上下文（`bkmonitor/models/fta/action.py:190-200`）：

```python
PUBLIC_PARAMS = {
    # ...
    "itsm_v4_site_url": settings.BK_ITSM_V4_HOST.rstrip("/"),
    "itsm_v4_api_url": settings.BK_ITSM_V4_API_URL.rstrip("/"),
    "itsm_v4_system_id": settings.BK_ITSM_V4_SYSTEM_ID,
    # ...
}
```

插件模板（`support-files/fta/action_plugin_initial.json`）：

```json
// :721  按钮跳转
"url": "{{itsm_v4_site_url}}/#/system/processList"
// :731  流程链接
"url": "{{itsm_v4_site_url}}/#/ticket/ticketInfo?workflowId={{key}}&type=create"
// :726  拉列表（现象 A 的失败点）
"init_kwargs": { "url": "{{itsm_v4_api_url}}/api/v1/system_workflow/list/" }
// :736  传入 system_id
"request_data_mapping": { "is_enable": "True", "system_id": "{{itsm_v4_system_id}}" }
```

创建命令内的两个接口（`bkmonitor/bkmonitor/management/commands/create_itsm_v4_system.py`）：

```python
class ItsmSystemCreateResource(CommonBaseResource):
    def __init__(self):
        super().__init__(url="{{itsm_v4_api_url}}/api/v1/system/create/", method="POST")

class ItsmSystemWorkflowListResource(CommonBaseResource):
    def __init__(self):
        super().__init__(url="{{itsm_v4_api_url}}/api/v1/system_workflow/list/", method="GET")
```

排查用完整脚本见 `scripts/check_itsm_vars.py`。

## 注意事项

1. **`--code` 不能省**。`create_itsm_v4_system` 的 `_parse_system_info` 在未传 `--code` 时执行 `code = name`。若只写 `--name "蓝鲸监控平台"`，建出来的 code 就是中文名，与 `settings.BK_ITSM_V4_SYSTEM_ID` 对不上，报错依旧。要么显式 `--code`，要么两个参数都不传（此时 name 和 code 都取 `settings.BK_ITSM_V4_SYSTEM_ID`）。

2. **`SYSTEM_ID` 的默认值不是空**。它是 `APP_CODE`，所以漏配不会立刻报「未配置」，而是变成「系统不存在」，这个误导性很强。判据就一条：生效值是否等于 `APP_CODE`。

3. **两个域名别混用**。`BK_ITSM_V4_API_URL` 是接口网关（`bkapi.` 开头，带 `/api/cw-aitsm/prod`），`BK_ITSM_V4_HOST` 是页面站点（`apps.` 开头，如 `.../cw--aitsm`）。把网关地址填进 `HOST` 会导致跳转落到 API 路径。

4. **`.env` 不随代码发布**。仓库根的 `.env` 被 `.gitignore` 忽略，属于本地私有文件。生产/提测环境的这些变量必须在部署配置里单独声明，否则拿到的是代码默认值（`HOST` 为空、`SYSTEM_ID` 回退 `APP_CODE`）。

5. **同类变量的默认值不一致，别类推**。同一段配置里 `BK_ITSM_HOST`、`BK_SOPS_HOST`、`BK_INCIDENT_SAAS_HOST` 都给了 `{BK_PAAS_HOST}/o/xxx/` 这类可用默认值，唯独 `BK_ITSM_V4_HOST` 留空，说明它依赖部署侧显式注入，不能靠默认值兜底。

6. **只建系统不补 host，现象 B 依然存在**；只补 host 不建系统，现象 A 依然存在。两个都要改才算完整修复。
