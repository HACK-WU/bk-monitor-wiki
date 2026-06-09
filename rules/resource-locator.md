---
name: resource-locator
description: 解析 resource.xxx.xxx 或 api.xxx.xxx 格式的路径引用，定位到对应的Resource类代码位置。当用户提到类似 resource.alert.alert_date_histogram_result 或 api.monitor.data_query 格式的路径时使用此skill。
---

# Resource/API 定位器

## 功能说明

当遇到特定格式的路径引用时，自动转换为类名并定位代码位置。

## 解析规则

### 1. `resource` 开头的路径

**格式**: `resource.xxx.xxx.class_name_in_snake_case`

**转换规则**:
- 取最后一个部分（下划线分隔的名称）
- 将 snake_case 转换为 PascalCase（每个单词首字母大写）
- 添加 `Resource` 后缀
- 在整个代码库中查找

**示例**:
- `resource.alert.alert_date_histogram_result` → `AlertDateHistogramResultResource`
- `resource.strategy.list` → `ListResource`
- `resource.alarm.handling_record` → `HandlingRecordResource`

### 2. `api` 开头的路径

**格式**: `api.xxx.xxx.class_name_in_snake_case`

**转换规则**:
- 同样的命名转换规则
- **固定在 `bkmonitor/api/` 目录下查找**

**示例**:
- `api.monitor.data_query` → `DataQueryResource`（在 `bkmonitor/api/` 下查找）
- `api.alert.push` → `PushResource`

## 转换流程

```
resource.alert.alert_date_histogram_result
                    ↓
         alert_date_histogram_result (提取最后一部分)
                    ↓
         AlertDateHistogramResult (snake_case → PascalCase)
                    ↓
         AlertDateHistogramResultResource (添加Resource后缀)
                    ↓
         在代码库中搜索 class AlertDateHistogramResultResource
```

## 使用方法

当遇到此类路径时，按以下步骤操作：

1. **识别路径类型**: 判断是 `resource` 还是 `api` 开头
2. **提取类名部分**: 取最后一个下划线分隔的部分
3. **转换命名**: snake_case → PascalCase
4. **添加后缀**: 添加 `Resource` 后缀
5. **定位代码**:
    - `resource` 开头：在整个代码库中搜索
    - `api` 开头：在 `bkmonitor/api/` 目录下搜索
6. **忽略大小写**: 搜索时忽略大小写

## 搜索命令

### resource 开头的路径
```bash
# 在整个代码库中搜索
grep -ri "class ClassNameResource" /root/bk-monitor/bkmonitor/
```

### api 开头的路径
```bash
# 固定在 bkmonitor/api 目录下搜索
grep -ri "class ClassNameResource" /root/bk-monitor/bkmonitor/api/
```

## 常见变体

某些情况下可能存在以下变体：

| 路径格式 | 转换结果 | 说明 |
|---------|---------|------|
| `resource.xxx.xxx.list` | `ListResource` | 通用列表资源 |
| `resource.xxx.xxx.detail` | `DetailResource` | 通用详情资源 |
| `resource.xxx.xxx.batch` | `BatchResource` | 批量操作资源 |

## 注意事项

- 转换时忽略大小写进行查找
- 如果找不到精确匹配，尝试模糊搜索
- 部分Resource类可能带有数字或特殊命名，需要灵活处理
