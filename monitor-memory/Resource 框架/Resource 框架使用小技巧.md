Resource 框架使用小技巧集，涵盖线程安全、批量请求、线程池上下文继承、异步任务、采样记录、Serializer 自动发现、批量校验、MCP 请求处理、命名映射、文档生成等常用模式。

入口位置：
- 符号: `bkmonitor/core/drf_resource/base.py` → `Resource`（基类）
- 位置: `bkmonitor/core/drf_resource/management/root.py`（ResourceManager / ResourceShortcut，自动注册）
- 位置: `bkmonitor/utils/thread_backend.py`（ThreadPool，继承 InheritParentThread，线程池）
- 位置: `bkmonitor/core/drf_resource/models.py`（ResourceDataManager，请求记录）

resource.xxx.yyy() 天然线程安全，全局入口调用会创建新的临时实例转发请求，多线程并发安全。
- 符号: `Resource.__call__`
- 位置: `bkmonitor/core/drf_resource/base.py`
- 用法: `result = resource.alert.search_alert({"id": "xxx", "limit": 10})`
- 注意：背后 `Resource.__call__` 会执行 `tmp_resource = self.__class__()` 创建**新的临时实例**，再通过 `ResourceData.objects.request()` 转发。即使同一个全局入口被多线程并发调用，也是线程安全的。
- 注意：如果**直接持有 Resource 实例**（如 `resource_instance = SomeResource()`）再多次调用 `resource_instance.request(...)`，这时候是**同一个实例**，需要自行保证实例级状态安全。

bulk_request 并行批量请求，内部使用 ThreadPool 真多线程并发执行多个请求。
- 用法: `results = resource.issue.issue_top_n_result.bulk_request([{"start_time": t0, "end_time": t1, "bk_biz_id": 2}, {"start_time": t1, "end_time": t2, "bk_biz_id": 2}])`

| 参数 | 说明 |
|------|------|
| `request_data_iterable` | `list` / `tuple`，每个元素是一份 `request_data`（dict） |
| `ignore_exceptions` | `True` 时跳过失败的单个请求，结果位置上填 `None` |

- 边界行为：全部报错 → 抛出第一个异常（不会静默吞掉）；内部使用 `ThreadPool.apply_async()` + `future.get()`，非协程，是真多线程。

线程池自动继承主线程上下文，包括 local 对象、timezone、language、trace_context。
- 符号: `ThreadPool.get_func_with_local()`
- 位置: `bkmonitor/utils/thread_backend.py`
- 同步内容：
  - `local` 对象中的所有数据（Django request/session/thread-local变量）
  - `timezone`（当前时区）
  - `language`（当前语言）
  - `trace_context`（OpenTelemetry trace 上下文）
- 注意：在 Resource 里可以直接 `get_request_username()`、`get_request_tenant_id()`，即使在 `bulk_request` 的子线程中也能正确拿到值。
- 注意：如果 Resource 在**定时任务 / Celery / 命令行**中调用（无 HTTP request），这些函数会返回默认值或报错，需要显式传参兜底。

delay / apply_async 异步任务，通过 Celery 后台执行 Resource 请求。
- 用法: `task_info = resource.alert.some_resource.delay({"id": "xxx"})` → `{"task_id": "celery-task-id-xxx"}`
- 用法: `task_info = resource.alert.some_resource.apply_async({"id": "xxx"}, countdown=60, queue="high")`
- 符号: `core.drf_resource.tasks.run_perform_request`
- 自动注入：`(resource, username, bk_tenant_id, request_data)`

请求采样记录（调试用），开启 ENABLE_RESOURCE_DATA_COLLECT 后自动把 Resource 输入输出记录到 resource_data 表。
- 配置: `settings.ENABLE_RESOURCE_DATA_COLLECT = True`
- 规则：
  - 首次访问某个 Resource → **必定记录**
  - 后续访问 → 按 `RESOURCE_DATA_COLLECT_RATIO`（默认 0）采样
  - 如果 Resource 设置 `support_data_collect = False` → 跳过记录
- 用法：排查线上问题时可以直接查 `resource_data` 表看历史入参和返回。

Serializer 自动发现规则：不显式定义时按命名规则自动查找 RequestSerializer / ResponseSerializer。
- 规则：

| Resource 类名 | 自动查找的 RequestSerializer | 自动查找的 ResponseSerializer |
|--------------|---------------------------|----------------------------|
| `SearchAlertResource` | `SearchAlertRequestSerializer` | `SearchAlertResponseSerializer` |

- 通过 `serializers_module` 配置可以指定搜索模块范围。

many_request_data / many_response_data 批量校验，配合 DRF many=True 的 serializer 行为用于批量创建/更新场景。
- 用法:
```python
class BatchCreateResource(Resource):
    many_request_data = True   # 入参是 list，每个元素走 RequestSerializer 校验
    many_response_data = True  # 返回是 list，每个元素走 ResponseSerializer 校验
```

MCP 请求特殊处理：Resource 框架内置 MCP 请求检测（`HTTP_X_BK_REQUEST_SOURCE == bkm-mcp-client`），自动上报 Prometheus 指标。
- 自动上报 Prometheus 指标：`mcp_resource_requests_total`（状态/异常类型/是否有数据）
- 自动上报耗时：`mcp_resource_requests_cost_seconds`
- 失败时也会上报（不吞异常）
- 注意：对普通业务开发是透明的，无需关心。

全局入口命名映射：resource.alert.search_alert 的命名规则。
- 命名规则：
  - `resource` → 各模块 `resources.py`
  - `api` → `api/xxx/default.py`（封装远程 ESB/APIGW）
  - `adapter` → `xxx/adapter/default.py`（按平台差异覆盖）
- 通过 `ResourceFinder` 在 Django `AppConfig.ready()` 时自动扫描注册，懒加载（首次访问才 import）。

generate_doc() 自动生成接口文档，从 Serializer fields 自动生成 OpenAPI 风格的参数列表。
- 符号: `ResourceClass.generate_doc()`
- 返回: `{"request_params": [...], "response_params": [...]}`
- 配合 API 文档工具使用。

依赖关系速查：
```
Resource
├── views.ResourceViewSet (HTTP 暴露)
├── models.ResourceDataManager (请求采样记录)
├── management.root.ResourceShortcut (懒加载代理)
│   └── management.finder.ResourceFinder (自动发现)
└── utils.thread_backend.ThreadPool (多线程并发)
```

使用场景：
- 需要批量并行调用多个 Resource → 用 `bulk_request`
- 需要异步后台执行 → 用 `delay` / `apply_async`
- 需要在线上排查入参 → 开 `ENABLE_RESOURCE_DATA_COLLECT`
- 需要自动文档生成 → 显式定义 Serializer + `generate_doc()`
