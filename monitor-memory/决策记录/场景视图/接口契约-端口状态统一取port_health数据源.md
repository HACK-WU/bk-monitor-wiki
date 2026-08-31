---
groupPath: 决策记录/场景视图
relation: 接口契约-端口状态统一取port_health数据源
exportedAt: "2026-08-31T01:49:25.792Z"
---
【决策记录｜场景视图主机进程端口状态统一取 system.proc_port 的 port_health，三态简化为二态】
- 分类：接口契约
- 动机：避坑（PromQL 指标 system:proc_port:proc_exists 查询恒无数据 → 端口状态图表始终为空）
- 决策：GetHostProcessPortStatusResource 改用 resource.cc.get_process_port_health，与 GetHostProcessListResource 同数据源；状态映射只保留 0 正常与 1 异常（不再区分 nonlisten）；时间范围改为可传 start_time 与 end_time（秒级），不传时保持最近 5 分钟默认行为
- 背景约束：端口健康是进程级指标，图表按同名 CMDB 进程的端口展开，端口共享该进程的健康状态
- 被否决方案：继续用 PromQL system:proc_port:proc_exists，否决理由为实测查询无数据、图表恒空（commit 8eb7d38599）；保留三态含 nonlisten，否决理由为数据源只提供 0/1 健康值无第三态支撑
- 已知代价：无 listen 与 nonlisten 区分；查询窗口被收敛为最长 5 分钟
- 重新评估触发条件：system:proc_port:proc_exists 恢复上报且产品要求区分 nonlisten；或需要查询超过 5 分钟窗口的端口状态趋势
- 关联代码：GetHostProcessPortStatusResource.perform_request @ scene_view/resources/host.py
- 证据来源：commit 8eb7d38599（body：实际测试该指标查询均无数据返回，因此改用 get_process_port_health 统一数据源；端口状态从三态简化为二态）；代码注释（host.py：端口健康是进程级指标）
- 完整上下文：.module-experts/场景视图专家/C5-关键决策.md 决策 5