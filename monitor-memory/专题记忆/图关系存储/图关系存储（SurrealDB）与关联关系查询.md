---
groupPath: 专题记忆/图关系存储
relation: 图关系存储（SurrealDB）与关联关系查询
exportedAt: "2026-09-18T01:39:26.057Z"
---
监控平台的图数据库是 SurrealDB，用于存储监控对象（资源）之间的关联关系图谱（顶点 + 边），是「资源关联关系查询」能力的数据底座，与 VM/ES/Doris 的时序/日志存储并列，不承载指标/日志本身。

- 图 schema 定义（监控侧负责定义，实际建表/写图由 BKBase 负责）：`ResourceDefinition`（顶点类型 + required 字段拼 UID）、`RelationDefinition`（边类型，static/dynamic、单向 is_directional / 双向、归属 is_belongs_to）经 `convert_to_vertices_and_relations` 转成 vertices/relations，随 `SurrealDBBindingConfig` 下发；同时写 Redis 供 bmw SchemaProvider 消费（Redis 丢失由 task 全量重建）
- 位置: `bkmonitor/metadata/models/entity_relation.py`、`bkmonitor/metadata/models/data_link/data_link_configs.py`、`bkmonitor/metadata/resources/entity_relation.py`、`bkmonitor/metadata/task/entity_relation.py`
- 关系以「指标」形式上报：命名规则 `{from}_to_{to}_flow`（单向）/ `{a}_with_{b}_relation`（双向），见 `get_relation_metric_name`
- 写入链路：DataLink 策略 `GRAPH_RELATION_TIME_SERIES`（RT 形如 `graph_relation_v4.metric.__default__`），Databus 按 `ResultTableOption.graph_relation_v4_data_link` 的 write_targets 双写 VM（时序）+ SurrealDB（图）；CMDB 内置 relation 链路由 `sync_cmdb_relation` 周期任务自动建 RT 并配置双写
- 位置: `bkmonitor/metadata/task/sync_cmdb_relation.py`、`bkmonitor/metadata/models/storage.py`（`SurrealDBStorage`，TYPE_SURREALDB，temporary=图能力表/normal=基础表）
- 查询链路：`api.unify_query.query_multi` / `query_multi_resource_range` → UnifyQuery `/api/v1/relation[/v1beta3]/multi_resource[_range]`（v1beta3 走图版）；对外经 kernel_api `RelationViewSet`（`QueryMultiResourceRelation[Range]Resource`，注释「关联关系MCP」）暴露查询，入参含 source_info/target_type/path_resource（多跳路径）
- 消费方示例：APM 拓扑关联查询（`apm_web/topo/handle/relation/query.py`、`relation_metric.py` 查 apm_service ↔ apm_service_instance）、K8s 资源关联（`GetKubernetesRelationResource`）
- 灰度开关：`GRAPH_RELATION_V4_BIZ_ID_WHITE_LIST`（settings）同时控制双写链路自动 apply 与 v1beta3 查询切流