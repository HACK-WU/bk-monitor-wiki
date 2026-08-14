---
groupPath: 专题记忆/元数据管理
relation: API与工具库专家
exportedAt: "2026-08-14T01:46:06.511Z"
---
API与工具库专家管理元数据的 API 接口（Resource 层）、服务层接口契约、通用工具函数库、BCS 容器服务集成。含 2 个子专家（API资源/BCS与工具库）。

- 符号: `MetadataResource`、`ClusterResource`、`EntityRelationResource`、`DataLinkResource`、`service/*`、`models/bcs/BCSClusterInfo`
- 位置: `bk-monitor-base/src/bk_monitor_base/metadata/resources/`、`service/`、`utils/`、`models/bcs/`

覆盖文件:
- resources/(8文件): resources.py(152KB~3495行) 核心 Resource 类（数据源/结果表/字段/BCS）、cluster.py(18KB) 集群管理、bkdata_link.py(51KB) 计算平台数据链路、datalink_operation.py(18KB)、entity_relation.py(21KB) 实体关系声明式API、log_datalink.py(39KB)、space.py(18KB)、vm.py(13KB)
- service/(7文件): data_source.py/storage_details.py(18KB)/sync_metadata.py(12KB)/space_redis.py(3KB)/es_storage.py/vm_storage.py(9KB)/influxdb_instance.py
- utils/(34文件): 加密哈希(cipher/hash_util/hashring)、时间(time_tools/time_format)、Redis(redis_tools)、Consul(consul)、请求上下文(request/local/user/tenant)、并发锁(lock.py)、数据库(db.py)、ES(es_tools/es_curator)、BCS/K8S(bcs/k8s_metric)、外部集成(bkbase/gse/data_link)
- models/bcs/(4文件): BCSClusterInfo(29KB) 集群注册、BCSResource 抽象基类、ServiceMonitorInfo/PodMonitorInfo、ReplaceConfig

子专家:
- API资源子专家: resources/ 全包 + service/ 服务层（resources.py 152KB 第二大单文件）
- BCS与工具库子专家: models/bcs/ + utils/ 全包

与其他专家关系:
- 上游依赖: 专家1/2/3（Resource 层经 Service 层读写 DataSource/ResultTable/Storage/Space/CustomReport）
- 下游被依赖: api/metadata/default.py（外部API网关）+ kernel_api（内核直连）
- 契约边界: service/ 接口契约归本专家，实现细节归对应功能域子专家（如 space_redis.py 实现归空间管理子专家）
- 公共依赖: core/drf_resource（框架基类）+ constants.py(139KB) + serializers.py