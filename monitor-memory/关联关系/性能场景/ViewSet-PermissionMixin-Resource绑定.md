---
groupPath: 关联关系/性能场景
relation: ViewSet-PermissionMixin-Resource绑定
exportedAt: "2026-08-13T12:07:32.331Z"
---
[强关联] 6 个 Resource 类 与 6 个 ViewSet/PermissionMixin 权限绑定
强度：必改——改 ViewSet 的 ResourceRoute 绑定或 PermissionMixin 的权限声明时，对应 Resource 类必须跟着改；改 Resource 类签名，ViewSet 不用管
原因：ViewSet 通过 resource_routes 把 endpoint 绑定到 resource.performance.*，PermissionMixin 统一加 VIEW_HOST 权限，绑定关系变更级联影响所有接口路由和权限

源端（ViewSet 路由+权限）:
- 6 个 ViewSet @ `bkmonitor/packages/monitor_web/performance/views.py`（HostPerformanceViewSet/HostPerformanceDetailViewSet/HostTopoNodeDetailViewSet/TopoNodeProcessStatusViewSet/SearchHostInfoViewSet/SearchHostMetricViewSet）
- `PermissionMixin` @ `bkmonitor/packages/monitor_web/performance/views.py`（统一 VIEW_HOST 权限，5/6 个 ViewSet 继承）
- `SearchHostInfoViewSet` 未继承 PermissionMixin（无 VIEW_HOST 权限）
- `ResourceRouter.register_module(performance_views)` @ `bkmonitor/packages/monitor_web/performance/urls.py`

目标端（Resource 类）:
- `HostPerformanceResource` / `HostPerformanceDetailResource` / `HostTopoNodeDetailResource` / `TopoNodeProcessStatusResource` / `SearchHostInfoResource` / `SearchHostMetricResource` @ `bkmonitor/packages/monitor_web/performance/resources.py`