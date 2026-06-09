---
description: resource/api 路径定位规则 - 根据 resource.xxx.yyy 或 api.xxx.yyy 路径引用定位到对应 Python Resource 类源码
alwaysApply: true
---

# Resource/API 代码定位规则

当遇到 `resource.xxx.yyy` 或 `api.xxx.yyy` 格式的路径引用时，按以下规则定位到对应的 Python 类源码。

## 路径转换规则

```
resource.<module>.<method_name>  →  <PascalCase(method_name)>Resource
```

1. 提取路径最后一段（snake_case）
2. 转为 PascalCase（每段首字母大写，去下划线）
3. 添加 `Resource` 后缀

| 路径引用 | 类名 |
|----------|------|
| `resource.alert.list_alert_log` | `ListAlertLogResource` |
| `resource.alert.search_alert` | `SearchAlertResource` |
| `api.metadata.get_label` | `GetLabelResource` |

## 搜索范围

| 前缀 | 搜索范围 | 文件模式 |
|------|----------|----------|
| `resource.` | `bkmonitor/` | `**/resources.py` |
| `api.` | `bkmonitor/api/` | `**/default.py` |

搜索命令：
```bash
grep -rn "class ListAlertLogResource" bkmonitor/
```

## 常见模块映射

| 模块名 | 目录 |
|--------|------|
| `alert` | `packages/fta_web/alert/resources.py` |
| `action` | `packages/fta_web/action/resources.py` |
| `monitor_web` 子模块 | `packages/monitor_web/<子模块>/resources.py` |
| `apm_web` 子模块 | `packages/apm_web/<子模块>/resources.py` |
| `metadata` (api) | `api/metadata/default.py` |

## 注册机制

框架启动时 `ResourceFinder` 扫描所有 Django app，将 Resource 子类按 PascalCase→snake_case 注册到全局 `resource`/`api` 入口。例如：

```python
# 类 ListAlertLogResource 注册为：
setattr(self, "list_alert_log", ListAlertLogResource())
# 调用方式：resource.alert.list_alert_log(...)
```

## 快速参考

```
路径: resource.<module>.<snake_case_name>
类名: snake_case → PascalCase + "Resource"
搜索: grep -rn "class <ClassName>" bkmonitor/
文件: resource → **/resources.py | api → api/**/default.py
```
