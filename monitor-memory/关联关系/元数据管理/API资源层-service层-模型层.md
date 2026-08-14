---
groupPath: 关联关系/元数据管理
relation: API资源层-service层-模型层
exportedAt: "2026-08-14T01:46:33.763Z"
---
[强关联] API 资源层/service 服务层 与 模型层（DataSource/ResultTable/Storage/Space）
强度：必改——改模型层字段定义时，Resource 层经 Service 层的读写逻辑必须跟着改；改 service 接口契约，模型层不用管
原因：Resource 层（resources/resources.py 152KB）通过 Service 层读写 DataSource/ResultTable/Storage/Space/CustomReport 等模型，模型字段变更级联影响所有 API 接口

源端（API 资源层+服务层）:
- `resources/resources.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/resources/resources.py`（~3495行，数据源CRUD/结果表CRUD/字段管理/BCS集成）
- `resources/cluster.py` / `entity_relation.py` / `bkdata_link.py` / `log_datalink.py` / `space.py` / `vm.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/resources/`
- `service/data_source.py` / `storage_details.py` / `sync_metadata.py` / `space_redis.py` / `es_storage.py` / `vm_storage.py` @ `bk-monitor-base/src/bk_monitor_base/metadata/service/`

目标端（模型层）:
- `DataSource` / `ResultTable` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/data_source.py` / `result_table.py`
- `Storage` 系列模型 @ `bk-monitor-base/src/bk_monitor_base/metadata/models/storage.py`
- `Space` / `CustomReport` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/space/` / `custom_report/`
- 契约边界: service/ 接口契约归 API与工具库专家，实现细节归对应功能域子专家