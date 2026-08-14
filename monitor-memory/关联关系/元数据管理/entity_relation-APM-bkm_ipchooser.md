---
groupPath: 关联关系/元数据管理
relation: entity_relation-APM-bkm_ipchooser
exportedAt: "2026-08-14T01:46:33.763Z"
---
[强关联] entity_relation 实体关系模型 与 APM/bkm_ipchooser 跨模块消费
强度：必改——改 entity_relation.py 的 EntityMeta/ResourceDefinition/RelationDefinition 模型定义时，APM 层和 bkm_ipchooser 的消费逻辑必须跟着改；改 APM 拓扑构建逻辑，模型定义不用管
原因：entity_relation.py 是 metadata 中唯一跨三模块组件，APM 层做拓扑构建和服务依赖分析，bkm_ipchooser 做主机选择器集成，模型定义变更级联影响两个外部模块

源端（模型定义）:
- `EntityMeta` / `ResourceDefinition` / `RelationDefinition` / `CustomRelationStatus` @ `bk-monitor-base/src/bk_monitor_base/metadata/models/entity_relation.py`（8KB）
- `EntityRelationResource` @ `bk-monitor-base/src/bk_monitor_base/metadata/resources/entity_relation.py`（声明式 API）

目标端（跨模块消费）:
- `apm/views.py` / `apm/models/config.py` @ `bk-monitor-base/src/bk_monitor_base/apm/`（拓扑构建、服务依赖分析）
- `bkm_ipchooser/` @ `bkmonitor/bkm_ipchooser/`（主机选择器集成）
- 本专题仅覆盖 metadata 侧模型定义，APM 层拓扑构建不在专题范围