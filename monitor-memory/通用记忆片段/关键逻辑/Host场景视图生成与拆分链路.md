Host 场景视图生成与拆分链路：GetSceneViewResource 查询视图配置后，经 HostBuiltinProcessor 读取 host.json/process.json 并调用 get_auto_view_panels 返回 panels 与 order 元组，拆分新接口时可直接复用。

- 符号: `GetSceneViewResource.perform_request(params)`、`get_view_config`、`HostBuiltinProcessor.get_view_config`、`get_auto_view_panels`、`get_panels`、`get_order_config`、`sort_panels`
- 位置: `bkmonitor/packages/monitor_web/scene_view/resources/view.py`

## 核心链路

1. `perform_request` → 查询 `SceneViewModel` 视图配置
2. `get_view_config(view, params)` → 分发到 `HostBuiltinProcessor`
3. `HostBuiltinProcessor.get_view_config` → 读取 `host.json`/`process.json`，调用 `get_auto_view_panels(view)`
4. `get_auto_view_panels` → `get_panels(view)` + `get_order_config(view)` + `sort_panels(...)`

## 关键发现

`get_auto_view_panels` 已天然按 `view.id`（`"host"`/`"process"`）区分，返回 `(panels, order)` 元组。拆分 4 个新接口时可直接复用，分别取 `panels` 或 `order`。

## 相关文件

- 位置: `bkmonitor/packages/monitor_web/scene_view/builtin/host.py` — `HostBuiltinProcessor`、`get_auto_view_panels`
- 位置: `bkmonitor/packages/monitor_web/scene_view/builtin/utils.py` — `sort_panels`
