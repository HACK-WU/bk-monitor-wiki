---
name: resource-locator
description: 根据 resource.xxx.yyy 或 api.xxx.yyy 格式的路径引用，定位到对应的 Python Resource 类源码。当用户提到 resource.xxx、api.xxx 路径，或询问某个接口/资源对应的代码位置时使用。
---

# Resource/API 代码定位

当遇到 `resource.xxx.yyy` 或 `api.xxx.yyy` 格式的路径引用时，按以下流程定位到对应的 Python 类源码。

## 核心转换规则

### 路径格式

```text
resource.<module>.<method_name>
api.<module>.<method_name>
```

### 转换步骤

1. **提取最后一段**：取路径最后一个 `.` 分隔的部分（snake_case 格式）
2. **snake_case → PascalCase**：每个 `_` 分隔的单词首字母大写，去掉下划线
3. **添加 `Resource` 后缀**

### 转换示例

| 路径引用 | 提取 | PascalCase | 最终类名 |
|----------|------|------------|----------|
| `resource.alert.list_alert_log` | `list_alert_log` | `ListAlertLog` | `ListAlertLogResource` |
| `resource.alert.search_alert` | `search_alert` | `SearchAlert` | `SearchAlertResource` |
| `api.metadata.get_label` | `get_label` | `GetLabel` | `GetLabelResource` |
| `resource.alert.alert_date_histogram_result` | `alert_date_histogram_result` | `AlertDateHistogramResult` | `AlertDateHistogramResultResource` |

## 定位流程

### Step 1：转换类名

```text
resource.alert.list_alert_log
                └── list_alert_log → ListAlertLog → ListAlertLogResource
```

### Step 2：全局搜索类定义

根据路径前缀确定搜索范围：

| 前缀 | 搜索范围 | 文件模式 |
|------|----------|----------|
| `resource.` | 整个代码库 `bkmonitor/` | `**/resources.py` |
| `api.` | `bkmonitor/api/` 目录 | `**/default.py` |

搜索命令：

```bash
# resource 类型
grep -rn "class ListAlertLogResource" bkmonitor/

# api 类型
grep -rn "class GetLabelResource" bkmonitor/api/
```

### Step 3：确认模块路径

路径中间部分对应模块目录：

```text
resource.alert.list_alert_log
         │
         └── 对应 fta_web/alert/ 或其他包含 alert 的模块
```

常见模块映射：

| 路径中的模块名 | 实际目录 |
|---------------|----------|
| `alert` | `packages/fta_web/alert/resources.py` |
| `action` | `packages/fta_web/action/resources.py` |
| `monitor_web` 下的子模块 | `packages/monitor_web/<子模块>/resources.py` |
| `apm_web` 下的子模块 | `packages/apm_web/<子模块>/resources.py` |
| `metadata` (api) | `api/metadata/default.py` |

## 完整示例：定位 `resource.alert.list_alert_log`

### 1. 转换类名

```text
list_alert_log → ListAlertLog → ListAlertLogResource
```

### 2. 搜索类定义

```bash
grep -rn "class ListAlertLogResource" bkmonitor/
```

结果：

```text
packages/fta_web/alert/resources.py:2035: class ListAlertLogResource(ApiAuthResource):
```

### 3. 查看类实现

```python
class ListAlertLogResource(ApiAuthResource):
    """获取告警流水记录"""

    class RequestSerializer(serializers.Serializer):
        id = AlertIDField(required=True, label="告警ID")
        offset = serializers.IntegerField(required=False, label="偏移")
        limit = serializers.IntegerField(default=10, label="获取的条数")
        operate = serializers.ListField(default=[], label="记录类型")

    def perform_request(self, validated_request_data):
        alert_id = validated_request_data["id"]
        operate_list = validated_request_data["operate"]
        offset = validated_request_data.get("offset")
        limit = validated_request_data["limit"]

        handler = AlertLogHandler(alert_id)
        result_data = handler.search(operate_list=operate_list, offset=offset, limit=limit)
        return result_data
```

### 4. 查看路由注册（可选）

在对应模块的 `views.py` 中确认 HTTP 端点：

```python
# packages/fta_web/alert/views.py
ResourceRoute("POST", resource.alert.list_alert_log, endpoint="alert/log"),
```

## 背后的原理

### 自动发现与注册

框架启动时（`AppConfig.ready()`）：

1. `ResourceFinder` 扫描所有 Django app 目录，查找 `resources.py` / `default.py` 文件
2. 将发现的模块包装为 `ResourceShortcut`（懒加载代理）
3. 挂载到全局 `resource` / `api` / `adapter` 入口

### 命名转换

`ResourceShortcut._setup()` 加载模块时：

```python
# 对模块中每个 Resource 子类：
# 1. 去掉类名末尾的 "Resource"
cleaned_name = "ListAlertLog"  # 从 "ListAlertLogResource" 去掉 "Resource"
# 2. PascalCase → snake_case
property_name = "list_alert_log"  # camel_to_underscore("ListAlertLog")
# 3. 注册为属性（实例）
setattr(self, "list_alert_log", ListAlertLogResource())
```

因此 `resource.alert.list_alert_log` 实际上访问的是 `ListAlertLogResource` 的一个实例。调用时 `__call__` 会创建新的临时实例执行请求，保证线程安全。

## 快速参考

```text
路径引用:  resource.<module>.<snake_case_name>
类名规则:  snake_case_name → PascalCase + "Resource"
搜索命令:  grep -rn "class <ClassName>" bkmonitor/
文件位置:  resource → **/resources.py | api → api/**/default.py
```