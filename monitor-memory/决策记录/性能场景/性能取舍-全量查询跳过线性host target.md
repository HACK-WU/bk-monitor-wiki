---
groupPath: 决策记录/性能场景
relation: 性能取舍-全量查询跳过线性host target
exportedAt: "2026-08-31T02:23:39.117Z"
---
【决策记录｜性能场景 全量主机指标查询跳过线性 host target，并明确否决五种替代方案】
- 分类：性能取舍
- 动机：优化（普通业务全量查询时浏览器提交上万 bk_host_ids 导致请求体巨大、UQ 线性拼接 target 开销高）
- 决策：全量场景（未显式传 bk_host_ids 且未走分享参数）下，服务端自行解析 CMDB 主机集合用于结果映射与白名单，UQ 侧通过 push_host_target 等于 False 跳过把主机线性编进查询 target；旧版 performance 全量列表同步使用同一优化（HostPerformanceResource 的 skip_linear_target）；空主机集合短路进程 CMDB 与 UQ 查询；大响应启用 gzip
- 背景约束：服务端已持有业务全集 hosts，只需并行回填 host_dict，无需 UQ 再按 target 过滤；分享与显式 ID 场景必须保持精确目标集合，不能扩大 scope
- 被否决方案：commit body 明确列出不引入的五种：主机数阈值（引入分叉逻辑，行为随规模变化难以预期）、Celery 队列异步化（引入任务编排与轮询，列表接口需同步返回）、Redis 快照（引入外部状态与失效问题）、后台常驻缓存（同上且主机集合变动频繁）、轮询状态机（复杂度高收益不抵成本）
- 已知代价：全量场景下 UQ 侧不做主机过滤，返回主机集合完全由服务端 CMDB 解析决定；若 UQ 与 CMDB 主机集合不一致，差异会在映射阶段表现为缺失值
- 重新评估触发条件：单业务主机数大于 5 万导致请求体或 gzip wire size 再次成为瓶颈（commit 的 Verification 中发布后对比请求体、gzip wire size、接口耗时一项当时未完成）
- 关联代码：SearchHostMetricResource._resolve_hosts 与 perform_request @ monitor_web/performance/resources.py；HostPerformanceResource.perform_request（skip_linear_target）@ 同文件
- 证据来源：commit 4faf55fb50（body：普通业务全量 search_host_metric 不再从浏览器提交上万 bk_host_ids，服务端解析 CMDB 主机集合用于映射和白名单，UQ 跳过线性 host target；空主机集合短路进程 CMDB 与 UQ，大响应启用 gzip；不引入主机数阈值、Celery 队列、Redis 快照、后台常驻缓存或轮询状态机；旧版 performance 全量列表同步使用同一免 target 优化）；代码注释（服务端已拿到业务全集 hosts，只并行填 host_dict，UQ 不得再把这批主机编进 target）
- 完整上下文：.module-experts/性能场景专家/C5-关键决策.md 决策 1