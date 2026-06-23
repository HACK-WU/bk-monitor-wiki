---
groupPath: 通用记忆片段
relation: Resource 框架使用小技巧
keywords: [Resource, drf_resource, core.drf_resource, perform_request, bulk_request, ResourceManager, ResourceShortcut, thread_backend, ThreadPool]
exportedAt: "2026-06-23T08:20:19.555Z"
---
# Resource 框架使用小技巧

## 入口
- 基类：`bkmonitor/core/drf_resource/base.py` → `Resource`
- 自动注册：`bkmonitor/core/drf_resource/management/root.py` → `ResourceManager` / `ResourceShortcut`
- 线程池：`bkmonitor/utils/thread_backend.py` → `ThreadPool`（继承 `InheritParentThread`）
- 请求记录：`bkmonitor/core/drf_resource/models.py` → `ResourceDataManager`

## 1. 🚀 `resource.xxx.yyy()` 天然线程安全

```python
# 全局入口调用（推荐）
result = resource.alert.search_alert({"id": "xxx", "limit": 10})
```

> 背后 `Resource.__call__` 会执行 `tmp_resource = self.__class__()` 创建**新的临时实例**，再通过 `ResourceData.objects.request()` 转发。即使同一个全局入口被多线程并发调用，也是线程安全的。

**但注意**：如果**直接持有 Resource 实例**（如 `resource_instance = SomeResource()`）再多次调用 `resource_instance.request(...)`，这时候是**同一个实例**，需要自行保证实例级状态安全。

---

## 2. ⚡ `bulk_request` 并行批量请求

```python
# 批量并发（内部 ThreadPool）
results = resource.issue.issue_top_n_result.bulk_request([
    {"start_time": t0, "end_time": t1, "bk_biz_id": 2},
    {"start_time": t1, "end_time": t2, "bk_biz_id": 2},
])
```

| 参数 | 说明 |
|------|------|
| `request_data_iterable` | `list` / `tuple`，每个元素是一份 `request_data`（dict） |
| `ignore_exceptions` | `True` 时跳过失败的单个请求，结果位置上填 `None` |

**边界行为**：
- 全部报错 → 抛出第一个异常（不会静默吞掉）
- 内部使用 `ThreadPool.apply_async()` + `future.get()`，非协程，是真多线程

---

## 3. 🔀 线程池自动继承主线程上下文

`ThreadPool.get_func_with_local()` 会自动把主线程的以下上下文同步到工作线程：

- `local` 对象中的所有数据（Django request/session/thread-local变量）
- `timezone`（当前时区）
- `language`（当前语言）
- `trace_context`（OpenTelemetry trace 上下文）

**这意味着**：在 Resource 里可以直接 `get_request_username()`、`get_request_tenant_id()`，即使在 `bulk_request` 的子线程中也能正确拿到值。

**但也意味着**：如果 Resource 在**定时任务 / Celery / 命令行**中调用（无 HTTP request），这些函数会返回默认值或报错，需要显式传参兜底。

---

## 4. 📡 `delay` / `apply_async` 异步任务

```python
# 简单异步
task_info = resource.alert.some_resource.delay({"id": "xxx"})
# → {"task_id": "celery-task-id-xxx"}

# 高级异步（传 Celery 参数）
task_info = resource.alert.some_resource.apply_async(
    {"id": "xxx"},
    countdown=60,   # 延迟60秒执行
    queue="high",   # 指定队列
)
```

执行的是 `core.drf_resource.tasks.run_perform_request`，自动注入 `(resource, username, bk_tenant_id, request_data)`。

---

## 5. 📝 请求采样记录（调试用）

`settings.ENABLE_RESOURCE_DATA_COLLECT = True` 时，会自动把 Resource 的输入输出记录到 `resource_data` 表：

- 首次访问某个 Resource → **必定记录**
- 后续访问 → 按 `RESOURCE_DATA_COLLECT_RATIO`（默认 0）采样
- 如果 Resource 设置 `support_data_collect = False` → 跳过记录

**用法**：排查线上问题时可以直接查 `resource_data` 表看历史入参和返回。

---

## 6. 🔍 Serializer 自动发现规则

如果不显式在 Resource 类内定义 `RequestSerializer` / `ResponseSerializer`，会按以下命名规则自动查找：

| Resource 类名 | 自动查找的 RequestSerializer | 自动查找的 ResponseSerializer |
|--------------|---------------------------|----------------------------|
| `SearchAlertResource` | `SearchAlertRequestSerializer` | `SearchAlertResponseSerializer` |

通过 `serializers_module` 配置可以指定搜索模块范围。

---

## 7. 📦 `many_request_data` / `many_response_data` 批量校验

```python
class BatchCreateResource(Resource):
    many_request_data = True   # 入参是 list，每个元素走 RequestSerializer 校验
    many_response_data = True  # 返回是 list，每个元素走 ResponseSerializer 校验
```

配合 DRF `many=True` 的 serializer 行为，用于批量创建/更新场景。

---

## 8. 🎯 MCP 请求特殊处理

Resource 框架内置 MCP 请求检测（`HTTP_X_BK_REQUEST_SOURCE == bkm-mcp-client`）：

- 自动上报 Prometheus 指标：`mcp_resource_requests_total`（状态/异常类型/是否有数据）
- 自动上报耗时：`mcp_resource_requests_cost_seconds`
- 失败时也会上报（不吞异常）

**这对普通业务开发是透明的**，无需关心。

---

## 9. 🗺️ 全局入口命名映射

```
resource.alert.search_alert
        │      │         │
        │      │         └── snake_case（从 SearchAlertResource 去掉 Resource 后转下划线）
        │      └── 模块路径名（fta_web/alert/ → alert）
        └── 全局入口 ResourceManager
```

- `resource` → 各模块 `resources.py`
- `api` → `api/xxx/default.py`（封装远程 ESB/APIGW）
- `adapter` → `xxx/adapter/default.py`（按平台差异覆盖）

通过 `ResourceFinder` 在 Django `AppConfig.ready()` 时自动扫描注册，懒加载（首次访问才 import）。

---

## 10. 🔧 `generate_doc()` 自动生成接口文档

```python
ResourceClass.generate_doc()
# → {"request_params": [...], "response_params": [...]}
```

从 RequestSerializer / ResponseSerializer 的 fields 自动生成 OpenAPI 风格的参数列表，配合 API 文档工具使用。

---

## 依赖关系速查

```
Resource
├── views.ResourceViewSet (HTTP 暴露)
├── models.ResourceDataManager (请求采样记录)
├── management.root.ResourceShortcut (懒加载代理)
│   └── management.finder.ResourceFinder (自动发现)
└── utils.thread_backend.ThreadPool (多线程并发)
```

## 使用场景
- 需要批量并行调用多个 Resource → 用 `bulk_request`
- 需要异步后台执行 → 用 `delay` / `apply_async`
- 需要在线上排查入参 → 开 `ENABLE_RESOURCE_DATA_COLLECT`
- 需要自动文档生成 → 显式定义 Serializer + `generate_doc()`
