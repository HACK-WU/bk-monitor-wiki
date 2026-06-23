---
groupPath: 通用记忆片段
relation: Monitor API资源自动暴露到OpenAI
keywords: [monitor_api, OpenAI]
exportedAt: "2026-06-23T09:13:14.682Z"
---
### Monitor API 资源自动暴露到 OpenAI
- **自动注册机制**: `monitor_web/monitor_api/views/` 下新增的 `ResourceViewSet`（继承 `ResourceViewSet`）
  - 每个新类默认自动生成一个 OpenAI entry point / `resource` 路径入口
  - `endpoint` 注册后，AI/OpenAI 可直接通过 `resource.xxx.yyy()` 调用
- **场景控制**: 若某模块不希望暴露给 OpenAI（如 Issue 相关资源仅走 API 网关，不走 AI 调用）
  - 可在 `monitor_api` 配置中排除该模块，或在 ViewSet 中设置 `exclude_from_openai = True`
  - 否则新加的每一个 ResourceViewSet 都会自动被 OpenAI 发现并注册
- **核心逻辑**: `monitor_web/monitor_api/views/` 目录下的所有 `ResourceViewSet` 子类，通过自动扫描注册到 `ResourceRouter`，同步生成 OpenAI resource entry
- **影响**: 新增 `IssueViewSet` 或其他 ViewSet 时，需确认是否需要暴露给 OpenAI；不需要时应主动排除，避免意外暴露