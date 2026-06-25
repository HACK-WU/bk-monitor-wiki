---
groupPath: 工具库
relation: MonitorJSONRenderer 响应渲染器
keywords: [MonitorJSONRenderer, 响应格式, CustomException, 渲染器]
exportedAt: "2026-06-25T07:26:53.379Z"
---
### MonitorJSONRenderer — 蓝鲸监控默认 JSON 渲染器

**文件**: `bkmonitor/bkmonitor/views/renderers.py`（继承 `UJSONRenderer`）

全项目默认渲染器，配置在 `config/role/web.py`：
```python
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("bkmonitor.views.renderers.MonitorJSONRenderer",),
    "EXCEPTION_HANDLER": "core.drf_resource.exceptions.custom_exception_handler",
}
```

### 响应格式

**成功 (200-299)**：
```json
{"result": true, "code": 200, "message": "OK", "data": <原始数据>}
```

**失败 (非 200-299)**：根据异常类型分支处理
- `CustomException`：使用 `exc.code` / `exc.message` / `exc.data`
- `PermissionDeniedError`：展平 `extra` 字段
- 普通 dict：提取 `detail` 或 `message`
- 其他：直接作为 message 字符串

### 异常处理链路

1. **`custom_exception_handler`** 优先处理：
   - `Error` 子类（`CustomException` 等）→ 直接构造 `{result, code, message, data}`
   - DRF `APIException` → 转换为 `DrfApiError` 通用格式（code=3300004）
   - 注入 `response.exception_instance` 供渲染器使用
2. **`MonitorJSONRenderer.get_result`** 根据 `exception_instance` 类型二次调整输出

### 关键区别：CustomException vs DRF APIException

| | CustomException | DRF APIException (如 PermissionDenied) |
|---|---|---|
| 分支 | Error 子类，格式可控 | DrfApiError 转换，格式固定 |
| code | 自定义 | 3300004（不可改） |
| message | 自定义 | 异常对象的 str 表示 |
| data | 自定义 dict | 原始 detail |

> **结论**：需要自定义错误格式（如 code=403 + data.auth_url）时必须用 `CustomException`，不能用 DRF 原生异常。