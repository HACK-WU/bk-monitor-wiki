---
groupPath: 技术栈选型
relation: Kafka客户端依赖
exportedAt: "2026-09-20T08:17:41.192Z"
---
BK-Monitor 同时依赖两个 Kafka Python 客户端（均在 pyproject.toml 主 dependencies 中，非可选依赖）：confluent-kafka（Confluent 维护的 librdkafka 绑定，Kafka 官网推荐客户端）与 kafka-python（dpkp 社区纯 Python 实现，1.4.6 为 2019 年版本，已很旧）。

- 符号: `confluent-kafka==2.4.0` / `kafka-python==1.4.6`
- 位置: `bkmonitor/pyproject.toml`
- 分工:
  - confluent-kafka（生产端为主）：alarm_backends/core/alarmd/publisher.py 的 Producer（lru_cache 进程内复用、自定义分区键）；alarm_backends/service/fta_action/message_queue/client.py 的 KafKaClient（支持 DSN 与 dict 配置、SASL/SCRAM）；metadata/models/storage.py 与 metadata/task/config_refresh.py 的 AdminClient（建 topic、TopicCollection）；metadata/resources/resources.py 的 Consumer
  - kafka-python（消费端与 Admin 主体）：alarm_backends/core/storage/kafka.py（KafkaQueue/KafkaOffsetManager）与 kafka_v2.py（KafkaQueueV2 消费池）；service/access/data/processor.py、service/access/event/event_poller.py；service/alert/handler.py；management/story/* 运维脚本；metadata/service/data_source.py、service/storage_details.py、models/data_source.py（KafkaAdminClient 建 topic/扩分区）；packages/fta_web/event_plugin/kafka.py
- 关键点: opentelemetry-instrumentation-kafka-python 只埋点 kafka-python，confluent-kafka 产出的生产链路不被该 instrumentation 采集；改消费侧代码需注意 kafka-python 1.4.6 API 与新版（2.x）有差异