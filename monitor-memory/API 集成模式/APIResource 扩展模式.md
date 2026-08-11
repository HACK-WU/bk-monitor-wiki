TapdAPIResource 是第三方 API 封装模板，继承 APIResource 并覆写 base_url/认证/响应解析以适配非标准接口格式。
- 符号: `api.tapd.default.TapdAPIResource`
- 位置: `api/tapd/default.py`
- 继承: `core.drf_resource.contrib.api.APIResource`
- 核心覆写:
  - `base_url = settings.TAPD_API_BASE_URL`
  - `INSERT_BK_USERNAME_TO_REQUEST_DATA = False` — 不自动插入 bk_username
  - `IS_STANDARD_FORMAT = False` — 响应不是标准 BlueKing 格式（无 result/code/data 外层）
  - `get_headers()` — 构造 Basic Auth Header：`client_id:client_secret` Base64 → `Authorization: Basic {encoded}`
  - `render_response_data()` — 防御性解析 TAPD 响应 `{status, data, info}`：status != "1" 时抛 `BKAPIError`
- 用法: 封装任何第三方 API 时，继承 `APIResource`，覆写上述 4 个属性/方法即可适配非标准接口格式。

APIResource 与 Resource 的区分：APIResource 封装远程 ESB/APIGW 调用（perform_request 发 HTTP），Resource 封装本地业务逻辑（perform_request 实现业务）。
- 位置: `core/drf_resource/contrib/api.py`（APIResource）、`core/drf_resource/base.py`（Resource）
