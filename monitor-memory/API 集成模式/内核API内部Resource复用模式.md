---
groupPath: API 集成模式
relation: 内核API内部Resource复用模式
keywords: [kernel_api, 内部调用, Resource, 复用, 批发场景]
exportedAt: "2026-06-24T08:54:48.852Z"
---
### 内部 Resource 复用模式（kernel_api/resource/）
- **设计目的**: `kernel_api/resource/` 下的 Resource 不是给前端直接调用的，而是作为**批发场景**使用，通常在其他 Resource 内部被复用
- **与 `kernel_api/views/` 的区别**:
  - `views/` 下的 `ResourceViewSet` → 对外暴露给 API 网关（前端/其他系统调用）
  - `resource/` 下的 `Resource` → 仅内部调用（被其他 Resource 的 `perform_request` 使用）
- **封装模式**: 常做一层薄封装，适配内部调用参数
  - 例如 `ListAlertResource` 内部调用 `SearchAlertResource().request(...)`，可能帮忙补全一些协议头或别名映射
- **使用场景**: 当某个查询/操作在多个对外的 ViewSet 中都需要用到时，抽成 `kernel_api/resource/` 下的独立 Resource，供多 ViewSet 在 `perform_request` 中复用
  - `kernel_api/resource/alert.py` 中的 3 个 Resource 就是封装给 MCP/AI 请求使用的