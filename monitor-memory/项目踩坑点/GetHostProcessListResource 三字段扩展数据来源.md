---
groupPath: 项目踩坑点
relation: GetHostProcessListResource 三字段扩展数据来源
exportedAt: "2026-08-12T09:11:12.513Z"
---
GetHostProcessListResource 字段扩展的数据来源说明，包含 fdNum、instanceCount、threadConnected 三个字段的最终实现与放弃决策（定稿 2026-07-21，2026-07-23 修正 instanceCount 来源，2026-08-12 修正聚合方式与默认值）。
- 符号: `GetHostProcessListResource.perform_request`
- 位置: `bkmonitor/packages/monitor_web/scene_view/resources/host.py`
- 关联需求: REQ-20260707-001

fdNum（文件句柄数）— 已实现。来自 `system.proc` 表（`bk-monitor-base/src/bk_monitor_base/metadata/data/init_resulttable.json`），字段 `fd_num`，描述"进程文件句柄数"，unit=short。
- 符号: `get_process_runtime_metrics`
- 位置: `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`
- 实现: `METRIC_FIELDS` 新增 `fd_num`；`host.py` 的 `runtime_metric_map` 加 `{"fdNum": "fd_num"}`

instanceCount（实例数）— 已实现，聚合方式已修正。数据来源为 UnifyQuery 实时查询，按 `(bk_target_ip, bk_target_cloud_id, display_name)` 维度对 `system.proc` 做 `count_without_time` 聚合，得到进程实际运行实例数。
- 符号: `get_process_instance_count`
- 位置: `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`
- 实现链路:
  1. 新增 `get_process_instance_count`，使用 `UnifyQuery.query_data` 查询 `system.proc`，返回 `{bk_host_id: {display_name: count}}`
  2. `GetHostProcessListResource.perform_request` 调用 `get_process_instance_count`，返回结构为 `{"instanceCount": instance_counts.get(process["name"], 1)}`
- 注意事项: 默认值为 `1`（host.py:570 实际为 `.get(process["name"], 1)`，非 0），不要与 CMDB 配置实例数 `proc_num` 混淆。
- 聚合方式选择: 必须用 `count_without_time` 不能用 `COUNT`。`count_without_time` 只做跨 series 计数（统计分组内 pid series 条数=运行实例数）；`COUNT` 会先 count_over_time 数窗口内采集点个数再 sum，得到的是采集点总数而非实例数（语义错误）。详见「专题记忆/数据源查询机制/count_without_time 与 COUNT 聚合语义差异」。
- 已移除: `bkmonitor/api/cmdb/define.py` 的 `Process.__init__` 的 `proc_num` 参数；`bkmonitor/packages/monitor_web/cc/resources/cmdb.py` 的 `get_process_info` 不再透出 `proc_num`；`bkmonitor/packages/monitor_web/collecting/resources/frontend.py` 删除对应变量示例。

threadConnected（连接数）— 已放弃。经核查 CMDB 与指标库（`system.proc`/`mysql.net`）均无对应指标字段，无法提供，前端移除该列即可。

附带改动：`get_process_runtime_metrics` 新增 `start_time`/`end_time`（秒级时间戳，可选）；同时传入时按区间查询（×1000 转毫秒，instant=True 取单值），否则保持最近三分钟默认行为。由 `host.py` RequestSerializer 透传。`get_process_port_health` 端口健康聚合由 `AVG` 改为 `MIN`（窗口内任一时刻异常即判异常）。