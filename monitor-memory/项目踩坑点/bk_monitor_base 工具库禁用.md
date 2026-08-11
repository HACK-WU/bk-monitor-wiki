bk_monitor_base 工具库的 `get_request`/`get_request_username`/`local` 在标准请求中不可用，必须使用 `bkmonitor.utils` 下的同名工具。
- 位置: `bkmonitor/bkmonitor/utils/`
- 错误工具位置: `bk-monitor-base/src/bk_monitor_base/metadata/utils/`
- 请求上下文设置: `bkmonitor/bkmonitor/middlewares/request_provider.py`
- 命名空间配置: `bkmonitor/urls.py`

问题现象：在 `fta_web/issue/views.py` 的 `TAPDAuthPermission.has_permission` 中调用 `get_request_username()` 时，报错 `get_request(): current thread hasn't request`。

根本原因：项目中存在两个独立的 `Local()` 对象：
1. `bkmonitor.utils.local.local` — 被 `RequestProvider` 中间件正确设置
2. `bk_monitor_base.metadata.utils.local.local` — 从未被任何中间件设置

当代码从 `bk_monitor_base` 导入 `get_request()`/`get_request_username()` 时，使用的是第二个 `local` 对象，因此永远无法获取到 request。

正确做法：一律使用 `bkmonitor/bkmonitor/utils/` 下的工具，禁止使用 `bk-monitor-base` 中的同名工具。

| 错误导入 | 正确导入 |
|----------|----------|
| `from bk_monitor_base.metadata.utils.request import get_request_username` | `from bkmonitor.utils.request import get_request_username` |
| `from bk_monitor_base.metadata.utils.request import get_request` | `from bkmonitor.utils.request import get_request` |
| `from bk_monitor_base.metadata.utils.local import local` | `from bkmonitor.utils.local import local` |
