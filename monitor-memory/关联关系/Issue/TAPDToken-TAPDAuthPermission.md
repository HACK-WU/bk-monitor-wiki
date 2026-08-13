---
groupPath: 关联关系/Issue
relation: TAPDToken-TAPDAuthPermission
exportedAt: "2026-08-13T08:56:07.250Z"
---
[强关联] TAPD token 工具函数 与 TAPDAuthPermission 权限校验
强度：必改——改 Redis key 格式 / token 加密方式 / 存储结构时，TAPDAuthPermission 必须跟着改；改权限校验逻辑，工具函数不用管
原因：TAPDAuthPermission 从 Redis tapd_uat:{tenant}:{user} 读取 token，token 的存取由 utils/tapd.py 的工具函数负责，存储格式变更级联影响权限校验

源端（token 工具函数）：
- `save_tapd_token(tenant_id, username, token_data, expires_in, cipher)` @ `bkmonitor/packages/fta_web/issue/utils/tapd.py`
- `get_tapd_token(bk_tenant_id, username)` @ `bkmonitor/packages/fta_web/issue/utils/tapd.py`
- `delete_tapd_token(tenant_id, username)` @ `bkmonitor/packages/fta_web/issue/utils/tapd.py`
- Redis key: `tapd_uat:{tenant}:{user}`
- AES 加密依赖 SECRET_KEY（密钥轮转需同步处理）

目标端（权限校验）：
- `TAPDAuthPermission` @ `bkmonitor/packages/fta_web/issue/views.py`（IssueViewSet 内嵌类）
- 仅对 TAPD_ENDPOINTS 中的接口生效
- token 失效(422)时自动清理 token 并重新引导授权