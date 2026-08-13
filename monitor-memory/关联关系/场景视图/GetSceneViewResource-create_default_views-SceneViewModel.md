---
groupPath: 关联关系/场景视图
relation: GetSceneViewResource-create_default_views-SceneViewModel
exportedAt: "2026-08-13T11:54:27.102Z"
---
[强关联] GetSceneViewResource 读路径 与 create_default_views 同步/SceneViewModel 查询
强度：必改——改 create_default_views 的同步逻辑或 SceneViewModel 查询条件时，GetSceneViewResource/GetSceneViewListResource 必须跟着改；改 Resource 的查询逻辑，同步函数不用管
原因：每次读取视图都先调 create_default_views 补齐默认视图（JSON 骨架↔DB 双向同步），再查 SceneViewModel 行，同步逻辑变更级联影响所有读路径

源端（读路径）:
- `GetSceneViewResource.perform_request` @ `bkmonitor/packages/monitor_web/scene_view/resources/view.py`（先 create_default_views，再 SceneViewModel.objects.get，缺失抛 Http404）
- `GetSceneViewListResource.perform_request` @ `bkmonitor/packages/monitor_web/scene_view/resources/view.py`（先 create_default_views，再 filter，按 SceneViewOrderModel.config 排序）
- `get_view_config(view, params)` 分发到 Processor 生成配置

目标端（同步+查询）:
- `create_default_views(scene_id, bk_biz_id, scene_type)` @ `bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`（JSON 骨架↔DB 双向同步）
- `SceneViewModel.objects.filter/get` @ `bkmonitor/packages/monitor_web/models/scene_view.py`（唯一键 bk_biz_id+scene_id+type+id）
- `SceneViewOrderModel.config` @ `bkmonitor/packages/monitor_web/models/scene_view.py`（视图ID有序列表，用于排序）
- 风险：JSON 骨架缺失触发差集删除会物理删除 DB 视图行，影响读取结果