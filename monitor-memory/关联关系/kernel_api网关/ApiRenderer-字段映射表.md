---
groupPath: 关联关系/kernel_api网关
relation: ApiRenderer-字段映射表
exportedAt: "2026-08-13T09:12:08.190Z"
---
[强关联] ApiRenderer/ApiModelFilterSet 字段适配 与 API_FIELD_FORMATED_MAPPINGS 映射表
强度：必改——改 API_FIELD_FORMATED_MAPPINGS 映射表时，ApiRenderer（响应侧）+ ApiModelFilterSet（请求侧）双向映射必须跟着改，前端消费方也要改；改渲染逻辑，映射表不用动
原因：字段映射是双向契约：响应侧内核字段→蓝鲸规范字段，请求侧蓝鲸规范参数→内核字段，映射表是两端共享的唯一真源

源端（字段适配）：
- `ApiRenderer.format_field(result, level=0)` @ `bkmonitor/kernel_api/adapters.py`（响应渲染时递归映射，level=0 不转最外层 envelope）
- `ApiModelFilterSet` @ `bkmonitor/kernel_api/adapters.py`（请求参数反向映射后交 DjangoFilterBackend）
- MCP 请求注入 trace_id（get_mcp_trace_id）@ `bkmonitor/kernel_api/adapters.py`

目标端（映射表 + 前端消费）：
- `API_FIELD_FORMATED_MAPPINGS` @ `bkmonitor/kernel_api/adapters.py`（biz_id→bk_biz_id、app_code→bk_app_code、plat_id→bk_cloud_id、company_id→bk_supplier_id）
- 前端/调用方按蓝鲸规范字段消费响应（bk_biz_id 等）