---
groupPath: 关联关系/外部API集成专题
relation: CommonBaseResource-各系统基类-APIResource
exportedAt: "2026-08-14T07:54:15.386Z"
---
[强关联] CommonBaseResource 公共基类 与各系统 APIResource 子类继承体系
强度：必改——改 CommonBaseResource 的 perform_request/get_request_url/__init__ 逻辑时，选用该基类的系统受影响；但多数系统自建基类不受影响
原因：CommonBaseResource 提供动态URL渲染(Jinja2Renderer) + BKAPIError统一包装模板，是 api/ 下的通用基类，但实际多数系统自建基类直接继承 APIResource

源端（公共基类）:
- `CommonBaseResource` @ `bkmonitor/api/common/default.py`
- 关键行为: `__init__` 用 Jinja2Renderer 渲染 url 占位符（占位符置空用于报错展示，base_url 用 BK_COMPONENT_API_URL/BK_PAAS_HOST/BK_ITSM_V4_API_URL 替换用于实际请求）；`perform_request` 注入 `_origin_user=get_global_user()` + 捕获 BKAPIError 后以 `system_name=plugin_key, url=url_path` 重写异常；`get_request_url` 返回完整渲染的 base_url

目标端（直接继承 APIResource 的系统自建基类）:
- `BkUserApiResource`(bk_login) / `BkPaaSAPIGWResource`(bk_paas) / `TapdAPIResource`(tapd) / `CMDBBaseResource`(cmdb) / `BkDataAPIGWResource`(bkdata) / `BkApiGatewayResource`(bk_apigateway) 等
- 这些系统基类大多直接继承 `core.drf_resource.APIResource`，不经过 CommonBaseResource
- CommonBaseResource 是可选模板，非强制基类