---
groupPath: Resource 框架
relation: Resource框架自动发现与使用
keywords: [ResourceManager, 自动发现, resource, api, adapter]
exportedAt: "2026-06-24T08:54:48.851Z"
---
### Resource 框架自动发现与使用方式
- **自动发现入口**: `core/drf_resource/management/root.py`
  - `ResourceManager` 自动扫描各模块的 resource/adapter/api 目录
  - 扫描规则：`resource.模块名 → 模块/resources.py`（如 `resource.cc`→`cc/resources.py`）
  - 变体：`adapter.模块名 → 模块/adapter/default.py`；如存在 `模块/adapter/${platform}/resources.py`，覆盖 default
  - 全部导出：
    - `from core.drf_resource import Resource` — 基类
    - `from core.drf_resource import APIResource, CacheResource, FaultTolerantResource` — 扩展
    - `from core.drf_resource import adapter, api, resource` — 自动发现管理器
- **两种使用方式**:
  1. `resource.xxx.yyy()` → 线程安全，自动完成请求/响应序列化
  2. `from api.tapd import SomeResource; SomeResource().request(params)` → 显式导入
- **TLS 参数透传**: HTTP 请求自动携带 `bk_app_code`/`bk_app_secret`/`bk_username`（由 `api.Resource` 基类注入）
- **关键特性**:
  - `bulk_request()` — 并行批量请求
  - `delay()` / `apply_async()` — 异步任务
  - ThreadPool 自动继承上下文
  - 全局入口命名映射（`endpoint` → resource 路径）
- **内部调用复用**:
  - `kernel_api/resource/某模块.py` 中常封装 `kernel_api` 专用的 resource，内部调用其他模块的 resource（如 `ListAlertResource` 内部调用 `SearchAlertResource`）
  - 前端不直接调用 `kernel_api/resource/` 的内容，而是通过 `kernel_api/views/` 中的 `ResourceViewSet` 暴露