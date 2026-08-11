蓝鲸监控应用凭证配置获取工具，区分 Web 角色和 Backend 角色从不同环境变量读取 APP_CODE/SECRET_KEY/APP_TOKEN，并供蓝鲸组件 SDK 使用。

- 位置: `bkmonitor/config/default.py`

Web 角色（ROLE == "web"）：
- `APP_ID = APP_CODE = get_env_or_raise("BKPAAS_APP_ID", "APP_ID", "APP_CODE", default="bk_monitorv3")`
- `APP_TOKEN = SECRET_KEY = get_env_or_raise("BKPAAS_APP_SECRET", "APP_TOKEN", "SECRET_KEY", default="")`
- `BACKEND_APP_CODE = os.getenv("BK_MONITOR_APP_CODE") or "bk_bkmonitorv3"`

非 Web 角色（API/Backend）：
- `APP_ID = APP_CODE = get_env_or_raise("BK_MONITOR_APP_CODE", default="bk_bkmonitorv3")`
- `APP_TOKEN = SECRET_KEY = get_env_or_raise("BK_MONITOR_APP_SECRET", default="")`
- `BACKEND_APP_CODE = APP_CODE`

蓝鲸组件客户端配置，从 Django settings 二次提取，供蓝鲸组件 SDK 使用。
- 位置: `bkmonitor/blueking/component/conf.py`
- 配置项:
  - `APP_CODE = settings.APP_ID`
  - `SECRET_KEY = settings.APP_TOKEN`
  - `COMPONENT_SYSTEM_HOST`: 优先取 `BK_COMPONENT_API_URL`，回退 `BK_PAAS_INNER_HOST`，最后 `BK_PAAS_HOST`
  - `DEFAULT_BK_API_VER`: 默认 `v2`
  - `CLIENT_ENABLE_SIGNATURE = False`

注意事项：
- Web 和 Backend 使用不同的环境变量前缀（`BKPAAS_` vs `BK_MONITOR_`）
- `SECRET_KEY` 实际是 APP_TOKEN，不是 Django 的 SECRET_KEY
- `conf.py` 是给蓝鲸组件 SDK 用的，值来自 Django settings 的 `APP_ID` 和 `APP_TOKEN`
