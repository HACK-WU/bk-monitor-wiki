---
groupPath: 通用记忆片段
relation: 外部API调用模式
keywords: [外部API, APIResource, base_url, action, module_name, get_headers, render_response_data]
exportedAt: "2026-06-23T09:17:42.269Z"
---
### 外部API调用模式（api/ 目录）
- **目录**: `api/` — 封装 monitor 访问第三方/内部其他系统的 API 接口
- **目录结构**: 每个外部系统一个子目录（`tapd/`、`cmdb/`、`cmsi/`、`node_man/`、`grafana/` 等）
- **基类模式**: `class XXXResource(APIResource)`
  - `base_url` — 远端基地址
  - `module_name` — 模块标识
  - `method` / `action` — HTTP 方法和 API 路径
  - `INSERT_BK_USERNAME_TO_REQUEST_DATA = False` — 不自动注入蓝鲸认证
  - `IS_STANDARD_FORMAT = False` — 非标准格式（覆写 `render_response_data()`）
- **非标准响应处理**: 覆写 `render_response_data()` 做格式适配
- **自定义认证**: `get_headers()` 中实现（如 TAPD Basic Auth）
- **数据定义**: 嵌套 `RequestSerializer` / `ResponseSerializer`
- **使用方式**:
  - 自动注册：`resource.xxx.yyy()`（如 `resource.tapd.get_workspaces()`）
  - 直接实例化：`SomeResource().request(params)`