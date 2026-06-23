---
title: url-view-resolver Skill 使用场景
usage_scenario: ["用户提供API URL路径需定位处理逻辑", "排查接口问题需确认请求处理类", "查看URL对应的Django视图和Resource类"]
keywords: ["url-view-resolver", "URL解析", "视图定位", "Resource类", "接口处理逻辑"]
---

当用户提供了一个 API URL 路径，需要定位该 URL 对应的 Django 视图、处理逻辑或 Resource 类时，使用 `url-view-resolver` skill。

## 使用命令

```bash
/root/bk-monitor/bkmonitor/.venv/bin/python /root/bk-monitor/django-url-view-resolver.py "<目标URL>" "<HTTP方法>"
```

## 使用流程

1. 运行脚本，获取 URL 对应的视图和 Resource 类
2. 从输出中提取「Resource 限定名」（如 `PreviewDutyRulePlanResource`）
3. 搜索该类名，定位到源码文件
4. 阅读 `perform_request` 方法，理解业务逻辑

## 适用场景

- 用户提供了一个 API URL，想知道对应的处理代码
- 需要定位某个接口的 Resource 类以分析业务逻辑
- 排查接口问题时，需要确认请求最终由哪个类处理

## 不适用场景

- 已知 Resource 类名，只需查看其实现 → 直接 grep 搜索类名
- 需要了解 `resource.xxx.yyy` 格式的路径引用 → 使用 `resource-locator` skill
