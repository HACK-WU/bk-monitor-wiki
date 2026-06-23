---
name: url-view-resolver
description: 通过运行 django-url-view-resolver.py 脚本，解析 Django URL 最终命中的视图对象和 Resource 类。当用户询问某个 URL/接口对应的处理逻辑、视图类、Resource 类时使用。触发短语包括：'这个接口对应什么视图'、'这个 URL 命中哪个处理函数'、'查看接口处理逻辑'、'定位接口代码'。
---

# Django URL 视图解析器

当需要查看某个接口 URL 最终命中的 Django 视图对象时，**必须优先运行脚本**，不要先凭代码搜索猜测。

## 命令格式

```bash
/root/bk-monitor/bkmonitor/.venv/bin/python /root/bk-monitor/django-url-view-resolver.py "<目标URL>" "<HTTP方法>"
```

### 参数说明

| 参数 | 必选 | 说明 |
|------|------|------|
| `<目标URL>` | 是 | 要解析的接口路径，如 `/rest/v2/duty_plan/preview_duty_rule_plan/` |
| `<HTTP方法>` | 否 | HTTP 方法（get/post/put/delete），指定后可追踪到最终的 Resource 类 |

## 输出示例

```text
输入 URL: /rest/v2/duty_plan/preview_duty_rule_plan/
解析 Path: /rest/v2/duty_plan/preview_duty_rule_plan/
路由名称: monitor_web:duty_plan-preview-duty-rule-plan
最终视图对象: <function DutyPlanViewSet at 0x7f58997ff9c0>
视图模块: monitor_web.user_group.views
视图限定名: DutyPlanViewSet
视图类: monitor_web.user_group.views.DutyPlanViewSet

--- HTTP POST 处理链分析 ---
action: preview_duty_rule_plan
resource_mapping key: ('POST', 'monitor_web.user_group.views.DutyPlanViewSet-preview_duty_rule_plan')
Resource 类: <class 'monitor_web.user_group.resources.PreviewDutyRulePlanResource'>
Resource 模块: monitor_web.user_group.resources
Resource 限定名: PreviewDutyRulePlanResource
```

## 返回信息

脚本执行成功后，应返回以下信息：

- **路由名称**：Django URL 路由的命名（如 `monitor_web:duty_plan-preview-duty-rule-plan`）
- **最终视图对象**：resolve() 返回的视图函数
- **视图模块**：视图所在的 Python 模块
- **视图限定名**：视图的 `__qualname__`
- **视图类**（view_class）：DRF ViewSet 类的完整路径
- **参数信息**：URL 中的位置参数和关键字参数（如果有）
- **Resource 类及限定名**：指定 HTTP 方法后追踪到的最终处理类

## 后续操作

要查看具体的视图处理代码，**直接搜索输出中的「Resource 限定名」即可**。

例如输出为 `Resource 限定名: PreviewDutyRulePlanResource`，则直接搜索该类名：

```bash
grep -rn "class PreviewDutyRulePlanResource" bkmonitor/
```

该类就是最终处理请求的 Resource 对象，其中的 `perform_request` 方法是核心业务逻辑入口。

## 使用流程

```text
1. 运行脚本，获取 URL 对应的视图和 Resource 类
   ↓
2. 从输出中提取「Resource 限定名」（如 PreviewDutyRulePlanResource）
   ↓
3. 搜索该类名，定位到源码文件
   ↓
4. 阅读 perform_request 方法，理解业务逻辑
```

## 注意事项

1. **优先运行脚本**：不要先凭代码搜索猜测接口对应的处理逻辑
2. **指定 HTTP 方法**：如果需要追踪到最终的 Resource 类，必须指定第二个参数
3. **执行失败处理**：如果脚本执行失败，直接说明失败原因和关键报错，不要臆测结果
4. **脚本依赖 Django 环境**：脚本通过 `import hello` 初始化 Django 环境，必须使用项目虚拟环境的 Python 解释器运行

## 适用场景

- 用户提供了一个 API URL，想知道对应的处理代码
- 需要定位某个接口的 Resource 类以分析业务逻辑
- 排查接口问题时，需要确认请求最终由哪个类处理
- 需要了解某个 URL 的路由注册信息

## 不适用场景

- 已知 Resource 类名，只需查看其实现 → 直接 grep 搜索类名
- 需要了解 `resource.xxx.yyy` 格式的路径引用 → 使用 `resource-locator` skill
