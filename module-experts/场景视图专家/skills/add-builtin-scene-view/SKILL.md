---
name: add-builtin-scene-view
description: 为蓝鲸监控 scene_view 模块新增或修改内置场景视图配置（新增场景、新增视图页签、调整默认面板/排序）。当用户说"给主机监控加个视图""新增一个内置场景""改默认面板顺序""scene_view 加内置视图"时使用。
---

# 新增/修改内置场景视图

## 适用场景
- 为已有内置场景（host / kubernetes / uptime_check / apm / custom_metric / alert 等）新增一个视图页签或调整其默认面板/排序
- 新增一个全新的内置场景（scene_id）
- 修改内置视图的 JSON 骨架配置

## 前置定位
- 处理器注册表：`bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`（`get_builtin_processors` / `BUILTIN_SCENES`）
- 各场景处理器：`builtin/{scene}.py`（如 `builtin/host.py`）
- 内置视图骨架：`builtin/view_configs/{scene_id}-{view_id}.json`
- 数据模型：`bkmonitor/packages/monitor_web/models/scene_view.py`

## 执行步骤

### A. 为已有场景新增视图页签
1. 在 `builtin/view_configs/` 新增 `{scene_id}-{view_id}.json`，字段参考同场景已有 JSON（`name/mode/variables/panels/list/order/options`），需国际化的字符串用 `"_(文案)"` 包裹。
2. 在对应处理器（如 `HostBuiltinProcessor`）的 `filenames` 列表中登记新文件名 `{scene_id}-{view_id}`。
3. 若需自定义默认排序，更新处理器内的默认 order（如 `builtin/host.py` 的 `DEFAULT_HOST_ORDER`）或 `create_default_order`。
4. 确认 `create_default_views` 的差异同步会自动 `bulk_create` 新视图——注意它同时会 `delete` 骨架中不存在的旧视图，勿误删。

### B. 新增全新内置场景
1. 新建 `builtin/{new_scene}.py`，继承 `BuiltinProcessor`（多数场景可复用 `NormalProcessorMixin`）。
2. 实现抽象方法：`is_builtin_scene`、`get_view_config`、`create_or_update_view`、`create_default_views`（用 Mixin 时声明 `SCENE_ID` 与 `filenames` 即可）。
3. 在 `builtin/__init__.py` 的 `get_builtin_processors()` 返回列表中注册该类；若需在场景分类接口出现，补 `BUILTIN_SCENES`。
4. 在 `builtin/view_configs/` 放置 `{new_scene}-*.json` 骨架。

### C. 修改默认面板/排序
1. 直接改对应 `view_configs/*.json` 的 `panels` / `order`，或处理器内的默认 order 常量。
2. 面板输出结构对齐 `base.py` 的 `Panel.to_dict`（id/title/sub_title/targets/options/grid_pos）。

## 校验
- 确认新增 endpoint（若有）已在 `views.py` 的 `resource_routes` 注册。
- 本地构造请求核对 `get_scene_view` / `get_scene_view_list` 返回的 panels 与顺序符合预期。
- 检查 `create_default_views` 差异同步不会误删既有用户视图（骨架 view_id 集合是否完整）。

## 边界与注意
- 内置 JSON 每次读盘无缓存，避免在骨架里堆过大配置。
- `SceneViewModel.mode` 模型值为 `auto/custom`，对外序列化值为 `tile/custom`，注意映射。
- apm/kubernetes/alert 场景的 `type` 会被 `validate_scene_type` 置空，视图唯一键随之变化。
