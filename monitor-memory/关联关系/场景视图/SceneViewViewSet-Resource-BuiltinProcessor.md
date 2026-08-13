---
groupPath: 关联关系/场景视图
relation: SceneViewViewSet-Resource-BuiltinProcessor
exportedAt: "2026-08-13T11:54:27.102Z"
---
[强关联] SceneViewViewSet 路由聚合 与 Resource 层/BuiltinProcessor 处理器
强度：必改——改 Resource 类签名/行为或 BuiltinProcessor 契约时，SceneViewViewSet 的路由绑定必须跟着改；改 ViewSet 路由注册机制，Resource/Processor 不用管
原因：SceneViewViewSet 通过 resource_routes 把 76 条 endpoint 绑定到 resource.scene_view.*（由 resources/__init__.py 星号导出），Resource 内部调用 get_view_config/create_default_views 分发到 BuiltinProcessor，任一层契约变更级联影响整个视图链路

源端（路由聚合）:
- `SceneViewViewSet` @ `bkmonitor/packages/monitor_web/scene_view/views.py`（76 条 ResourceRoute，权限统一 BusinessActionPermission([VIEW_BUSINESS])）
- 主机场景 4 个拆分接口直接绑定 Resource 类（GetHostViewsPanelsResource 等）
- `ResourceRouter.register_module(views)` @ `bkmonitor/packages/monitor_web/scene_view/urls.py`

目标端（Resource 层+处理器）:
- `GetSceneViewResource` / `GetSceneViewListResource` / `UpdateSceneViewResource` / `DeleteSceneViewResource` @ `bkmonitor/packages/monitor_web/scene_view/resources/view.py`
- `GetHostProcessListResource` / `GetHostViewsPanelsResource` @ `bkmonitor/packages/monitor_web/scene_view/resources/host.py`
- `PageListResource` @ `bkmonitor/packages/monitor_web/scene_view/resources/base.py`
- `BuiltinProcessor` / `NormalProcessorMixin` / 分发函数 @ `bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`