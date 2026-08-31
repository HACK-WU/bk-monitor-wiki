---
groupPath: 决策记录/性能场景
relation: 兼容处理-分享与显式ID保留目标下推
exportedAt: "2026-08-31T02:23:39.117Z"
---
【决策记录｜性能场景 分享与显式 ID 场景保留目标下推，全量场景才跳过】
- 分类：兼容处理
- 动机：安全合规（分享链接只能看到被授权的主机，不能因为性能优化扩大数据范围）
- 决策：_resolve_hosts 用返回值第一个元素显式表达是否下推 host target：显式 bk_host_ids、单主机分享 bk_host_id、拓扑分享 bk_obj_id 加 bk_inst_id 三种场景返回 True（下推精确集合）；只有全业务全量场景返回 False（跳过下推）。另外 bk_host_ids 显式传空列表时直接返回空字典，不因空而扩大为全量
- 背景约束：性能优化不能以放宽数据范围为代价，跳过 target 意味着由服务端 CMDB 解析决定范围，只能用于业务全量这种本身没有额外限制的场景
- 被否决方案：全量场景与分享场景统一处理（一律下推或一律跳过），否决理由为一律下推则请求体膨胀（万级 ID），一律跳过则分享场景会越权暴露业务全部主机
- 已知代价：_resolve_hosts 的分支语义必须严格维护，新增查询场景时容易漏判是否下推
- 重新评估触发条件：新增分享形态（如按集群分享）时必须同步判定下推策略
- 关联代码：SearchHostMetricResource._resolve_hosts 与 perform_request（空列表短路）@ monitor_web/performance/resources.py
- 证据来源：代码 docstring（解析查询主机集，返回是否下推 host target、CMDB hosts、输出 host id）；commit 4faf55fb50（body：显式 ID、单主机分享和拓扑分享继续目标下推，bk_host_ids 为空列表仍表示空集合，不扩大 scope）
- 完整上下文：.module-experts/性能场景专家/C5-关键决策.md 决策 4