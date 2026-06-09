---
description: Django URL 解析脚本使用规则 - 通过 URL 路径定位最终视图和 Resource 类
alwaysApply: true
---

# Django URL → View / Resource 解析脚本

当需要从 HTTP 接口 URL 反推出最终处理代码（视图函数、视图类、Resource 类）时，使用仓库提供的解析脚本。

## 脚本位置

```
/root/bk-monitor/django-url-view-resolver.py
```

## 前置依赖

脚本第一行 `import hello` 会触发 Django 环境初始化。`hello.py` 位于仓库根目录 `/root/bk-monitor/hello.py`，负责：

1. 将 `bkmonitor/` 和 `bkmonitor/packages/` 加入 `sys.path`
2. 设置 `DJANGO_SETTINGS_MODULE` 并加载 `.env`
3. 调用 `django.setup()` 完成 Django 启动

**不要修改 `hello.py`**，除非用户明确要求。

## 执行方式

使用项目 venv 的 Python，在仓库根目录下执行：

```bash
cd /root/bk-monitor && /root/bk-monitor/bkmonitor/.venv/bin/python django-url-view-resolver.py "<URL>" "<METHOD>"
```

- `URL`（必填）：Django path，如 `/rest/v2/data_explorer/get_graph_query_config/`
- `METHOD`（可选，默认 POST）：HTTP 方法，如 `GET`、`POST`、`PUT`、`DELETE`

## URL 路由前缀映射

bk-monitor 的 URL 按以下前缀分发到不同模块，构造 URL 时必须使用正确的前缀：

| 前缀 | 目标模块 | 说明 |
|------|----------|------|
| `rest/v2/` | `monitor_web` | 监控平台主接口 |
| `query-api/rest/v2/` | `monitor_web` | 查询专用 API |
| `fta/` | `fta_web` | 故障自愈（告警、事件、处理等） |
| `apm/` | `apm_web` | APM 应用性能监控 |
| `trace/` | `apm_trace` | Trace 链路追踪 |
| `rest/v1/` | `monitor_api` | 旧版 API |

**注意**：fta 下的子模块路径直接接在前缀后面，如 `fta/alert/`（不是 `fta/rest/v2/alert/`）。

## 实际输出示例

### 示例 1：monitor_web 模块（ResourceViewSet）

```bash
cd /root/bk-monitor && /root/bk-monitor/bkmonitor/.venv/bin/python django-url-view-resolver.py "/rest/v2/data_explorer/get_graph_query_config/" "POST"
```

输出：

```
输入 URL: /rest/v2/data_explorer/get_graph_query_config/
解析 Path: /rest/v2/data_explorer/get_graph_query_config/
路由名称: monitor_web:data_explorer-get-graph-query-config
最终视图对象: <function DataExplorerViewSet at 0x...>
视图模块: monitor_web.data_explorer.views
视图限定名: DataExplorerViewSet
视图类: monitor_web.data_explorer.views.DataExplorerViewSet

--- HTTP POST 处理链分析 ---
action: get_graph_query_config
resource_mapping key: ('POST', 'monitor_web.data_explorer.views.DataExplorerViewSet-get_graph_query_config')
Resource 类: <class 'monitor_web.data_explorer.resources.GetGraphQueryConfig'>
Resource 模块: monitor_web.data_explorer.resources
Resource 限定名: GetGraphQueryConfig
```

### 示例 2：fta_web 模块（ResourceViewSet）

```bash
cd /root/bk-monitor && /root/bk-monitor/bkmonitor/.venv/bin/python django-url-view-resolver.py "/fta/alert/alert/search/" "POST"
```

输出：

```
输入 URL: /fta/alert/alert/search/
解析 Path: /fta/alert/alert/search/
路由名称: fta_web:alert-alert/search
最终视图对象: <function AlertViewSet at 0x...>
视图模块: fta_web.alert.views
视图限定名: AlertViewSet
视图类: fta_web.alert.views.AlertViewSet

--- HTTP POST 处理链分析 ---
action: alert/search
resource_mapping key: ('POST', 'fta_web.alert.views.AlertViewSet-alert/search')
Resource 类: <class 'fta_web.alert.resources.SearchAlertResource'>
Resource 模块: fta_web.alert.resources
Resource 限定名: SearchAlertResource
```

## 输出字段说明

### 基础输出（所有视图类型）

| 字段 | 说明 |
|------|------|
| 输入 URL | 原始输入 |
| 解析 Path | Django `resolve()` 使用的 path |
| 路由名称 | URLConf 中注册的 name（格式：`namespace:viewset-endpoint`） |
| 最终视图对象 | `resolve()` 返回的 callable |
| 视图模块 | 视图所在 Python 模块路径 |
| 视图限定名 | ViewSet 类名 |
| 视图类 | 完整的 `module.ClassName` |

### HTTP 方法处理链分析（提供 METHOD 时）

脚本按视图类型分三条路径分析：

1. **ResourceViewSet**（bk-monitor 自研框架）：通过 `resource_mapping` 字典查找最终 `Resource` 类，输出 Resource 类名、模块、限定名
2. **标准 DRF ViewSet**：通过 `view_func.actions` 映射找到 HTTP 方法对应的 action 方法
3. **普通 APIView / Django View**：直接按 HTTP 方法名取类上对应的处理方法（如 `get`、`post`）

## 使用场景

### 场景 1：从 API URL 定位 Resource 类

当已知一个接口 URL（如前端请求、日志中的 URL、API 文档中的路径），需要找到后端实际处理逻辑时，执行脚本获取 Resource 类和模块路径，然后打开对应源码文件。

### 场景 2：排查 URL 路由问题

当 URL 返回 404 或命中了意外的视图时，用脚本确认路由实际走向。

### 场景 3：理解接口调用链

在阅读代码或排查问题时，快速了解一个 URL 从路由到视图到 Resource 的完整处理链。

## 解析失败处理

- 如果输出 `URL 未匹配到任何视图`，说明该 path 在 Django URLConf 中没有注册，检查 URL 前缀和路径拼写
- 如果脚本报 `ImportError` 或 `ModuleNotFoundError`，通常是缺少运行时依赖，需确认 `.env` 配置正确
- 如果 `resource_mapping 中未找到 key`，脚本会回退列出该 ViewSet 下所有候选 Resource

## 与 resource-locator 规则的关系

- `resource-locator` 规则：从代码中的 `resource.xxx.yyy` 调用路径 → 定位 Resource 类（静态分析）
- 本脚本：从 HTTP URL → 定位视图和 Resource 类（运行时解析）

两者互补。如果只有 URL 没有代码引用，用本脚本；如果只有 `resource.xxx.yyy` 路径，用 `resource-locator` 规则。
