---
groupPath: 关联关系/kernel_api网关
relation: authentication-bk_apigateway公钥
exportedAt: "2026-08-13T09:12:28.704Z"
---
[强关联] 认证中间件 与 api.bk_apigateway 公钥获取（JWT 验签依赖）
强度：建议改——改 get_apigw_public_keys 获取逻辑或 FROM_APIGW_NAME 配置时，JWT 验签链路受影响；改 apigw 公钥发布机制，认证中间件需适配
原因：apigw JWT 验签依赖从 api.bk_apigateway 获取的 RS512 公钥，公钥缺失/缓存失效会导致所有 apigw JWT 认证失败，是认证链路的外部依赖契约

源端（认证中间件）：
- `AuthenticationMiddleware.get_apigw_public_keys()` @ `bkmonitor/kernel_api/middlewares/authentication.py`（functools.lru_cache(maxsize=1) + login_db cache 缓存公钥，公钥为空时 120s 短缓存防抖）
- `BkJWTClient.validate()`（RS512 验签，取 app.app_code/user.username）@ `bkmonitor/kernel_api/middlewares/authentication.py`
- `FROM_APIGW_NAME` 配置（apigw 名称列表）@ `bkmonitor/config/role/api.py`

目标端（公钥来源）：
- `api.bk_apigateway.get_public_key` @ `bkmonitor/api/bk_apigateway/`（经蓝鲸 API 网关获取公钥）
- 公钥缓存于 `login_db` cache