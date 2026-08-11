signed_state 签名密钥依赖 SECRET_KEY（APP_TOKEN）的潜在问题与未来优化方向。
- 符号: `generate_signed_state`, `verify_signed_state`
- 位置: `bkmonitor/packages/fta_web/issue/utils/tapd.py`

场景：`generate_signed_state` 和 `verify_signed_state` 使用 `settings.SECRET_KEY`（即 APP_TOKEN）作为 HMAC 签名密钥。

潜在问题：
1. 密钥复用：APP_TOKEN 同时用于蓝鲸组件 API 鉴权和 OAuth state 签名，泄露一边影响另一边
2. 分布式部署：如果不同节点的 APP_TOKEN 不同（非标准部署），signed_state 跨节点验证会失败

现状：标准蓝鲸 SaaS 部署下，同一应用所有实例共享同一个 `BKPAAS_APP_SECRET`，所以当前无实际问题。

未来优化方向：如果需要多租户隔离或跨环境部署，应派生专用密钥：
```python
import hashlib
SIGNING_KEY = hashlib.sha256(settings.SECRET_KEY.encode("utf-8") + b"tapd-oauth-state").digest()
```
当前不需要改，记录备忘。
