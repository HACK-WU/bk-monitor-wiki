---
groupPath: 关联关系/性能场景
relation: HostPerformanceResource-CacheResource-CacheType.HOST
exportedAt: "2026-08-13T12:07:32.331Z"
---
[强关联] HostPerformanceResource 缓存 与 CacheResource/CacheType.HOST 框架
强度：必改——改 CacheResource 框架的缓存机制或 CacheType.HOST 定义时，HostPerformanceResource 必须跟着改；改 HostPerformanceResource 的缓存 key 逻辑，框架不用管
原因：HostPerformanceResource 继承 CacheResource，cache_type=CacheType.HOST，缓存整份主机列表，框架变更级联影响缓存命中和失效逻辑

源端（缓存 Resource）:
- `HostPerformanceResource` @ `bkmonitor/packages/monitor_web/performance/resources.py`（继承 CacheResource，cache_type = CacheType.HOST）
- 缓存 key: CacheType.HOST + bk_biz_id
- 缓存未命中时全量拉取后自动写入缓存
- 缓存命中时直接返回缓存数据

目标端（缓存框架）:
- `CacheResource` 基类 @ `bkmonitor/core/drf_resource/`（自动管理缓存写入/读取/失效）
- `CacheType.HOST` @ `bkmonitor/utils/cache.py`（缓存类型枚举）
- 模块内无主动刷新/失效逻辑（全靠框架自动管理）
- SearchHostMetricResource 不继承 CacheResource，无缓存每次实时查