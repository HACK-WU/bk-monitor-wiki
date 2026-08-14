---
groupPath: 关联关系/外部API集成专题
relation: bk_apigateway-GetPublicKeyResource-kernel_api认证
exportedAt: "2026-08-14T07:54:15.386Z"
---
[强关联] bk_apigateway GetPublicKeyResource 与 kernel_api 认证体系
强度：必改——改 GetPublicKeyResource 的 action/base_url/返回结构时，kernel_api 认证依赖会断裂
原因：kernel_api 的 ApiAuthToken 认证依赖 bk_apigateway 提供的公钥验证 JWT 签名，是跨模块认证契约

源端（API提供方）:
- `GetPublicKeyResource` @ `bkmonitor/api/bk_apigateway/default.py`
- 基类: `BkApiGatewayResource`（base_url=APIGATEWAY_API_BASE_URL 或 api/bk-apigateway/prod/）
- action: `/api/v1/apis/{api_name}/public_key/`
- cache_type: USER（缓存公钥避免重复请求）
- 调用: `api.bk_apigateway.get_public_key({"api_name": "bk-monitor", "bk_tenant_id": "default"})["public_key"]`

目标端（认证消费方）:
- `ApiAuthToken` 认证类 @ `bkmonitor/kernel_api/authentication.py`
- 用公钥验证请求中的 JWT 签名，确认请求来自已授权的 API 网关
- 参见 kernel_api 网关专家「认证与安全」章节