K8S、GSE 与 BKBase 元数据同步工具集，提供内置指标/事件读取、Kafka 集群注册到 GSE、BkBase 结果表元信息同步等能力。

读取内置 K8S 容器指标与事件，带全局缓存。
- 符号: `get_built_in_k8s_metrics()` / `get_built_in_k8s_events()`
- 位置: `src/bk_monitor_base/metadata/utils/k8s_metric.py`
- 说明:
  - `get_built_in_k8s_metrics()`: 读取 metadata/data/k8s_metrics/*.yaml 获取内置 K8S 容器指标，全局缓存 `K8S_METRICS`
  - `get_built_in_k8s_events()`: 读取 metadata/data/k8s_events.json 获取内置 K8S 事件，全局缓存 `K8S_EVENTS`

Kafka 消息队列信息同步到 GSE 的工具类。
- 符号: `KafkaGseSyncer`
- 位置: `src/bk_monitor_base/metadata/utils/gse.py`
- 方法:
  - `sync_to_gse()`: 遍历 ClusterInfo 注册所有符合条件的 Kafka 集群到 GSE
  - `_get_kafka_sasl_auth(cluster)`: 获取 Kafka SASL 认证信息
  - `register_default_to_gse()` / `register_to_gse()`: 注册集群信息到 GSE
- 注意: GSE 不分租户，使用 `DEFAULT_TENANT_ID`

同步 BkBase RT 元信息到 Metadata。
- 符号: `sync_bkbase_result_table_meta(round_iter, bkbase_rt_meta_list, biz_id_list)`
- 位置: `src/bk_monitor_base/metadata/utils/bkbase.py`
- 说明:
  - 批量比对现有 RT/Field/Option，生成创建/更新操作
  - 使用 `transaction.atomic()` 保证批量写入一致性
  - 支持按 biz_id_list 分批处理
