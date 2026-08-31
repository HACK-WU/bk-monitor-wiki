---
groupPath: 决策记录/场景视图
relation: 接口契约-进程按display_name分组而非进程ID
exportedAt: "2026-08-31T01:49:25.791Z"
---
【决策记录｜场景视图主机进程维度以 CMDB 进程名 display_name 分组，而非 CMDB 进程 ID 或单 PID】
- 分类：接口契约
- 动机：避坑（以 CMDB 进程 ID 作为列表 id → 前端拿该 ID 去过滤 display_name 维度 → 图表查询无数据）
- 决策：进程列表以 process.name（display_name）作为稳定 row key 与图表查询变量；同名进程的多个 CMDB 配置合并为一组，组内保留全部端口绑定 portBindings，单值字段取排序最小的代表配置；CPU 与内存按同名进程组汇总，uptime 固定取 MAX
- 背景约束：TSDB 进程指标以 display_name 为维度上报，无 PID 维度时无法按单实例区分；CMDB 同名进程可存在多条配置（多端口绑定、不同启动命令）
- 被否决方案：以 CMDB 进程 ID 作为列表 id，否决理由为与 TSDB 的 display_name 维度不匹配导致图表无数据（commit aa68990ea2 记录的线上故障）；按单 PID 查看进程组指标，否决理由为 commit 4ca8b24a00 明确列为边界外
- 已知代价：同名进程组的 CPU 与内存为合计值；单值字段只代表组内一条 CMDB 配置；uptime 只展示组内最大值
- 重新评估触发条件：TSDB 进程指标稳定带上 PID 维度且产品要求按实例下钻；或出现同名进程不同配置需独立展示的需求
- 关联代码：group_process_configs @ scene_view/process_group.py；GetHostProcessListResource.perform_request @ scene_view/resources/host.py；get_metric_panel @ scene_view/builtin/host.py
- 证据来源：commit aa68990ea2、08d008d995、4ca8b24a00（PR 描述边界段）；代码注释（host.py：分组后继续使用进程名作为稳定 row key）
- 完整上下文：.module-experts/场景视图专家/C5-关键决策.md 决策 4