---
groupPath: 专题记忆/APM
relation: Profile采集与上报链路
exportedAt: "2026-09-07T03:43:18.232Z"
---
Profile 数据采集上报链路：应用或探针生成 pprof 二进制 → gzip 压缩 → multipart/form-data 上报 bk-collector 的 /pyroscope/ingest 端点。
- 入口: `CollectorHandler.send_to_builtin_datasource(profile_id, service_name, profile)`
- 位置: `bkmonitor/packages/apm_web/profile/collector.py`
- 核心步骤:
  1. 经 `api.apm_api.query_builtin_profile_datasource()` 获取内置 Profile 数据源 token 与 app_name
  2. pprof 二进制写入 gzip 压缩流
  3. 手工构造 multipart/form-data（encode_multipart_form_data）
  4. 上报地址取 BKAPP_PROFILING_COLLECTOR_HTTP_HOST，缺省回退 BKAPP_OTLP_HTTP_HOST 去掉 /v1/traces 后缀
  5. 模拟 pyroscope agent 参数：name={app_name}{service_name=xxx}、from/until（ns 转秒）、spyName=gospy、sampleRate=100、units 取 profile.sample_type[0].unit 对应字符串表项
- 关键点：最多重试 3 次，全部失败抛异常；仅支持 CPU 类型（TODO 注释预留 sample_type_config 扩展其他类型）