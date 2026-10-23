---
groupPath: 决策记录/IP选择器
relation: 架构设计-拓扑树服务实例数量改读ID索引
exportedAt: "2026-10-21T09:40:35.068Z"
---
【决策记录｜IP 选择器拓扑树 服务实例数量改读 ID 索引而非全量明细】
- 分类：架构设计
- 动机：优化，避坑：拓扑树只需要数量却拉 2.9 万条含 process_instances 的完整明细，端到端 8.37s
- 决策：service_instance 分支改为读 ServiceInstanceModuleIndex（module_id 映射到 service_instance_id 列表），取 len 即数量；索引缺失时回退现有全量拉取，不抛错；fill_host_count_to_tree 的递归聚合逻辑保持不动
- 背景约束：拓扑树入参只有 bk_biz_id，调用方无需知道任何 ID；索引由 cron 后台维护，不在请求路径上；bkm_ipchooser 通过 AbstractBkApi 与主工程解耦，不能直接依赖 api.cmdb，需新增抽象方法（如 get_service_instance_module_index）
- 被否决方案一：提高 batch_request 并发度（20 提到 40）。否决理由：149 页分 8 批，乐观省 3.4s、悲观 0.9s；CMDB 侧已在排队，提并发会把等待转给 CMDB 并可能触发限流；T1 落地后该段直接归零
- 被否决方案二：web 层改 gevent worker 或 asyncio 协程。否决理由：greenlet 在 2.9 万条 dict 反序列化这段 CPU 密集代码不会让出，会阻塞同 worker 内所有并发请求；asyncio 需把 core/drf_resource/contrib/api.py:125 的同步 requests.session 换成 httpx.AsyncClient，影响全部 API 调用层，收益仍是并发度而并发度不是本接口瓶颈
- 已知代价：新鲜度从当前 300s TTL 放宽到约 10~30 分钟（cron RING_NODES 分片）；后台 cron 每轮仍要全量拉一次，成本是转移不是消灭
- 实现陷阱：索引 key 是 str(module_id)，fill_host_count_to_tree 用 node 的 bk_inst_id（int）去 get，不转换会导致所有节点 count 为 0；GetServiceInstanceIdsByTopoNode 在索引缺失时直接抛 CustomError，拓扑树不能沿用该行为
- 前置校验：该业务必须在 StrategyModel 中有策略（active_biz_ids 只覆盖配过策略的业务），否则索引永远不会被 cron 刷新，T1 收益不成立
- 重新评估触发条件：若 CMDB 的 findmany/proc/service_instance/details 支持字段裁剪（不返回 process_instances）或存在不带 details 的轻量接口，则存在不改时效语义的更优方案，届时索引路径可降为备选
- 关联代码：TopoTool.get_topo_tree_with_count（bkm_ipchooser/tools/topo_tool.py:93-103）；fill_host_count_to_tree（同文件 :51-63）；ServiceInstanceModuleIndex（api/cmdb/default.py:183-220）；get_service_instance_by_biz（同文件 :223-234）
- 证据来源：APM trace（2026-10-21，业务 100864，8.37s 端到端、7.26s 应用内、约 149 次 ListServiceInstanceDetail）；本地等价结构基准（0.23MB 与 2.2ms vs 30.45MB 与 580.7ms）；测试 test_get_service_instance_ids_by_topo_node_only_reads_index 断言 ID-only path must not load full details
- 完整上下文：.codebuddy/perf/ip-chooser-topo-trees-20261021.md