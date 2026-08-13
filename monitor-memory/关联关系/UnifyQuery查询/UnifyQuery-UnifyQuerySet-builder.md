---
groupPath: 关联关系/UnifyQuery查询
relation: UnifyQuery-UnifyQuerySet-builder
exportedAt: "2026-08-13T10:01:18.353Z"
---
[强关联] UnifyQuery 门面 与 UnifyQuerySet Builder 链式构建
强度：必改——改 UnifyQuery 的 instant/end_time/step 参数语义时，UnifyQuerySet.instant(align_interval=) 必须跟着改；改 Builder 的链式 API，UnifyQuery 不用管
原因：UnifyQuerySet.instant(align_interval=N) 在设 instant=True 同时把 end_time 前移 N 毫秒，依赖 UnifyQuery 的 instant 参数行为语义（step强制1m+保留边界点），参数语义变更级联影响 Builder 的对齐补偿逻辑

源端（门面）:
- `UnifyQuery.query_data(instant=...)` @ `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `UnifyQuery._query_unify_query`（instant→step="1m"）@ `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `process_unify_query_data`（非instant丢弃end_time边界点）@ `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

目标端（Builder）:
- `UnifyQuerySet` @ `bkmonitor/bkmonitor/data_source/unify_query/builder.py`
- `UnifyQuerySet.instant(align_interval=...)` @ `bkmonitor/bkmonitor/data_source/unify_query/builder.py`
- `UnifyQuerySet.time_agg` / `limit` 等链式方法 @ `bkmonitor/bkmonitor/data_source/unify_query/builder.py`