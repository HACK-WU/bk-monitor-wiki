---
groupPath: 关联关系/外部API集成专题
relation: metadata-MetaDataAPIGWResource-KernelAPIResource
exportedAt: "2026-08-14T07:52:30.763Z"
---
[强关联] metadata MetaDataAPIGWResource 与 KernelAPIResource 自身网关模式
强度：必改——改 MetaDataAPIGWResource 的 base_url/module_name 或 KernelAPIResource 基类时，所有 metadata 接口路由全变
原因：metadata 走 bk-monitor 自身网关（非外部 ESB/APIGW），继承 KernelAPIResource，module_name=metadata_v3

源端（自身网关基类）:
- `MetaDataAPIGWResource(KernelAPIResource)` @ `bkmonitor/api/metadata/default.py`
- `base_url = NEW_MONITOR_API_BASE_URL` 或 `api/bk-monitor/{APIGW_STAGE}/`
- `module_name = metadata_v3`
- action 形如 `/app/metadata/...`
- 约 70 个 Resource 类（数据源/结果表/存储/集群/事件分组/时序分组/空间）
- 序列化: `MetadataBaseSerializer`（去 None 字段）、`UsernameSerializer`（自动补用户名）

目标端（消费方）:
- `alarm_backends/core/cache/result_table.py` 等消费 `api.metadata.list_result_table` 等
- 与 api.monitor 同走 KernelAPIResource（module_name=mointor_v3）为同一自身网关模式