---
groupPath: 通用记忆片段/关键逻辑
relation: Host场景视图生成与拆分链路
keywords: [HostBuiltinProcessor, get_auto_view_panels, panels, order]
exportedAt: "2026-07-07T07:55:08.710Z"
---
### Host 场景视图生成与拆分链路
- **入口**: `GetSceneViewResource.perform_request(params)`
- **路径**: `bkmonitor/packages/monitor_web/scene_view/resources/view.py`
- **核心链路**:
  1. `perform_request` → 查询 `SceneViewModel` 视图配置
  2. `get_view_config(view, params)` → 分发到 `HostBuiltinProcessor`
  3. `HostBuiltinProcessor.get_view_config` → 读取 `host.json`/`process.json`，调用 `get_auto_view_panels(view)`
  4. `get_auto_view_panels` → `get_panels(view)` + `get_order_config(view)` + `sort_panels(...)`
- **关键发现**: `get_auto_view_panels` 已天然按 `view.id`（`"host"`/`"process"`）区分，返回 `(panels, order)` 元组。拆分 4 个新接口时可直接复用，分别取 `panels` 或 `order`。
- **文件**: `builtin/host.py`（`HostBuiltinProcessor`、`get_auto_view_panels`）, `builtin/utils.py`（`sort_panels`）