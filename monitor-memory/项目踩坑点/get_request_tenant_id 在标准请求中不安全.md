`get_request_tenant_id()` 在 Django 标准请求中不可靠，推荐使用 `bk_biz_id_to_bk_tenant_id` 从业务ID反查租户ID。
- 符号: `get_request_tenant_id()`
- 位置: `bkmonitor/utils/request.py`
- 推荐替代: `bk_biz_id_to_bk_tenant_id(bk_biz_id: int) -> str`（位置: `bkmonitor/bkmonitor/utils/tenant.py`）

问题：`get_request_tenant_id()` 有三条取值路径：
1. `request.user.tenant_id` — 依赖用户对象上有 `tenant_id` 属性，不保证存在
2. `get_local_tenant_id()`（即 `local.bk_tenant_id`）— 中间件未设置，走不通
3. 单租户模式兜底 `DEFAULT_TENANT_ID`

根因：`RequestProvider` 中间件（`bkmonitor/bkmonitor/middlewares/request_middlewares.py`）只做了 `local.current_request = _get_request()`，没有调用 `set_request()`，所以 `local.bk_tenant_id` 和 `local.username` 都不会被设置。而 `set_request()` 函数虽然会同时设置三者，但没有被中间件调用。

结论：在 Django 标准请求中，不要依赖 `get_request_tenant_id()` 获取租户ID。推荐使用 `bk_biz_id_to_bk_tenant_id(bk_biz_id)`，`bk_biz_id` 在 Resource 框架中基本都有（从 URL/query/body 提取），比 `request.user.tenant_id` 可靠得多。
