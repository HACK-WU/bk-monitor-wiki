---
groupPath: 关联关系/外部API集成专题
relation: kubernetes-数据四路-非APIResource聚合
exportedAt: "2026-08-14T07:53:01.837Z"
---
[强关联] kubernetes 数据四路聚合模式 与非 APIResource 继承
强度：必改——改 kubernetes Resource 的数据源路径或聚合逻辑时，所有 K8s 资源查询接口的行为全变
原因：kubernetes 不走 APIResource，继承 Resource/CacheResource，数据来源四路：promql/BCS storage/K8s SDK/本地 DB

源端（非标准基类与四路数据源）:
- 基类: 继承 `Resource`/`CacheResource`（非 `APIResource`） @ `bkmonitor/api/kubernetes/default.py`
- `cache_type = CacheType.BCS`（5min 缓存）
- 数据四路:
  1. promql 指标（`UnifyQuery`/`load_data_source(PROMETHEUS)` 多线程）
  2. BCS storage（`api.bcs_storage.fetch`）
  3. K8s SDK（`BCSCluster.api_client` 的 core_v1_api/apps_v1_api）
  4. 本地 DB（BCSBase/BCSCluster 模型）

目标端（代表性 Resource 与消费）:
- `FetchK8sClusterListResource`/`FetchK8sNodeListByClusterResource`/`FetchK8sPodListByClusterResource`/`FetchK8sWorkloadListByClusterResource` — 按集群拉取资源列表
- `FetchKubernetesConsistencyCheckResource` + 5 子类 — 三方一致性校验
- 内部用 `ThreadPool` + promql 多路并发，预期耗时较长