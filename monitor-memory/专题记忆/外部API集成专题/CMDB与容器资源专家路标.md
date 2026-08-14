---
groupPath: 专题记忆/外部API集成专题
relation: CMDB与容器资源专家路标
exportedAt: "2026-08-14T07:51:08.060Z"
---
CMDB与容器资源专家路标：封装 BK-Monitor 对资源与容器监控数据源的调用——CMDB、Kubernetes、BCS 系列、节点管理。
- 负责模块: `bkmonitor/api/{cmdb,kubernetes,bcs,bcs_cluster_manager,bcs_project,bcs_storage,node_man}/`
- 契约层资产: `.module-experts/外部API集成专题/CMDB与容器资源专家/C0-使用总览.md` + `C1-能力契约.md` + `implementation/`
- 核心能力: CMDB主机/拓扑/进程(api.cmdb.* 含client.py 22方法+default.py业务Resource+define.py数据结构) / K8s资源聚合(api.kubernetes.* 非APIResource，数据四路:promql/BCSstorage/K8sSDK/DB) / BCS系列(bcs/bcs_cluster_manager/bcs_project/bcs_storage各自独立网关，Bearer token) / 节点管理(api.node_man.* 36接口，TIMEOUT=300)
- 关键坑: CMDB查询无结果返回空list(perform_request捕获NoRelatedResourceError) / bcs 401需BCS_API_GATEWAY_TOKEN / K8s查询慢(ThreadPool+promql多路并发) / CMDB缓存CC_BACKEND(10min)/CC_CACHE_ALWAYS(1h)