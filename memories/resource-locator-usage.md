---
title: resource-locator Skill 使用场景
usage_scenario: ["代码中出现resource.xxx.yyy路径引用", "代码中出现api.xxx.yyy路径引用", "需要定位Resource类源码位置"]
keywords: ["resource-locator", "resource路径", "api路径", "Resource类定位", "代码引用定位"]
---

当用户在代码中遇到 `resource.xxx.yyy` 或 `api.xxx.yyy` 格式的路径引用，需要定位其对应的 Python Resource 类源码时，使用 `resource-locator` skill。

## 核心转换规则

1. 提取路径最后一段（snake_case 格式）
2. 转换为 PascalCase
3. 添加 `Resource` 后缀

## 转换示例

| 路径引用 | 提取 | PascalCase | 最终类名 |
|----------|------|------------|----------|
| `resource.alert.list_alert_log` | `list_alert_log` | `ListAlertLog` | `ListAlertLogResource` |
| `api.metadata.get_label` | `get_label` | `GetLabel` | `GetLabelResource` |

## 定位流程

1. 转换类名（snake_case → PascalCase + Resource）
2. 全局搜索类定义
   - `resource.` 前缀 → 整个代码库 `bkmonitor/`
   - `api.` 前缀 → `bkmonitor/api/` 目录
3. 查看类实现，阅读 `perform_request` 方法

## 适用场景

- 代码中出现了 `resource.alert.list_alert_log` 这类引用，想知道具体实现
- 需要查看 `api.metadata.get_label` 对应的接口处理类
- 搜索代码定位 Resource 类定义和 `perform_request` 方法

## 注意事项

当用户提供了一个 HTTP URL 路径时，应该优先使用 `url-view-resolver`，而非 `resource-locator`。
