---
groupPath: 项目踩坑点
relation: GetHostProcessListResource 三字段扩展数据来源
keywords: [GetHostProcessListResource, instanceCount, fd_num, system.proc, proc_num, UnifyQuery, get_process_instance_count, Process]
exportedAt: "2026-07-23T01:49:15.746Z"
---
# GetHostProcessListResource 字段扩展（定稿 2026-07-21，2026-07-23 修正 instanceCount 来源）

> 文件: `bkmonitor/packages/monitor_web/scene_view/resources/host.py` → `GetHostProcessListResource.perform_request`
> 关联需求: REQ-20260707-001

## 最终实现字段

### fdNum（文件句柄数）— 已实现
- 表: `system.proc`（`bk-monitor-base/src/bk_monitor_base/metadata/data/init_resulttable.json` 行 6100-6108）
- 字段: `fd_num`, 描述"进程文件句柄数", unit=short
- 实现: `get_process_runtime_metrics` 的 `METRIC_FIELDS` 新增 `fd_num`；`host.py` 的 `runtime_metric_map` 加 `{"fdNum": "fd_num"}`
- 函数: `bkmonitor/packages/monitor_web/cc/resources/cmdb.py` → `get_process_runtime_metrics`

### instanceCount（实例数）— 已实现，来源已修正
- 数据来源: **UnifyQuery 实时查询**，按 `(bk_target_ip, bk_target_cloud_id, display_name)` 维度对 `system.proc` 做 `COUNT` 聚合，得到进程实际运行实例数。
- 实现链路:
  1. `bkmonitor/packages/monitor_web/cc/resources/cmdb.py` → **新增 `get_process_instance_count`**，使用 `UnifyQuery.query_data` 查询 `system.proc`，返回 `{bk_host_id: {display_name: count}}`
  2. `bkmonitor/packages/monitor_web/scene_view/resources/host.py` → `GetHostProcessListResource.perform_request` 调用 `get_process_instance_count`，返回结构为 `{"instanceCount": instance_counts.get(process["name"], 0)}`
- 注意事项: 默认值为 `0`（无运行实例），不要与 CMDB 配置实例数 `proc_num` 混淆。
- 已移除: `bkmonitor/api/cmdb/define.py` → `Process.__init__` 的 `proc_num` 参数；`bkmonitor/packages/monitor_web/cc/resources/cmdb.py` → `get_process_info` 不再透出 `proc_num`；`bkmonitor/packages/monitor_web/collecting/resources/frontend.py` 删除对应变量示例。

### threadConnected（连接数）— 已放弃
- 经核查 CMDB 与指标库（`system.proc`/`mysql.net`）均无对应指标字段，无法提供
- 前端移除该列即可

## 附带改动
- `get_process_runtime_metrics` 新增 `start_time`/`end_time`（秒级时间戳，可选）；同时传入时按区间查询（×1000 转毫秒，instant=True 取单值），否则保持最近三分钟默认行为。由 `host.py` RequestSerializer 透传
- `get_process_port_health` 端口健康聚合由 `AVG` 改为 `MIN`（窗口内任一时刻异常即判异常）