---
groupPath: 通用记忆片段
relation: Resource框架使用小技巧
keywords: [Resource, bulk_request, delay, apply_async, ThreadPool, 上下文继承, 请求采样, resource.xxx]
exportedAt: "2026-06-23T09:14:50.327Z"
---
### Resource 框架使用小技巧
- **线程安全调用**: `resource.xxx.yyy()` 线程安全，自动完成请求/响应序列化
- **批量并发请求**: `Resource.bulk_request(resource_cls, params_list, max_workers=10)` — 并行批量请求，加速场景
- **异步任务**: `resource.delay()` / `apply_async()` — Celery 异步执行；`delay_async` 带上下文继承
- **ThreadPool 上下文继承**: ThreadPoolExecutor 中子线程自动继承父线程请求上下文
- **请求采样**: 自动记录请求采样日志，便于后续分析和调试
- **全局命名映射**: `ResourceRouter` 自动将 endpoint 映射到 `resource.xxx.yyy()` 路径
- **两种调用方式**:
  1. `resource.xxx.yyy()` — 自动发现，线程安全，自动序列化
  2. `SomeResource().request(params)` — 显式实例化，直接调用
- **关键类**: `core.drf_resource.base.Resource` 基类，`core.drf_resource.contrib.api.APIResource` 远程调用基类