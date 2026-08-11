system.proc display_name 维度的真实数据格式说明。display_name 维度真实值 = 进程名（即 CMDB 的 bk_process_name），是自由文本字符串（如 "nginx"/"redis"/"java"），不含 IP/端口。

- 位置: `bkmonitor/packages/monitor_web/scene_view/builtin/view_configs/process.json`

`system.proc` result table（table_id: "system.proc"，label: "host_process"）的 `display_name` 维度（field_type: string，description: "进程显示名称"）真实值 = **进程名**，即 CMDB 的 `bk_process_name`，是自由文本字符串（如 "nginx"/"redis"/"java" 或用户自定义进程名），**不含 IP/端口**。

### 关键代码证据

- 位置: `bkmonitor/packages/monitor_web/scene_view/builtin/view_configs/process.json`
- 视图把 `display_name` 当 `bk_process_name` 传详情接口：`"bk_process_name": "$display_name"`

- 符号: `get_process_runtime_metrics`
- 位置: `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`
- 查 `system.proc`，`group_by` 含 `"display_name"`，docstring 示例值 `"nginx"`/`"redis"`；运行时指标按 `record["display_name"]` 为 key 索引

- 位置: `bkmonitor/packages/monitor_web/cc/resources/cmdb.py`
- `get_process_exists`/`get_process_port_health` 同样按 `display_name` 分组索引

- 符号: `GetHostProcessListResource.perform_request`
- 位置: `bkmonitor/packages/monitor_web/scene_view/resources/host.py`
- `name = process["name"]`（来自 CMDB `pp.bk_process_name`），运行时按 `process["name"]` 索引；`id = f"{process['name']}@{host.ip}"`（@host.ip 仅属于 id 字段，非 display_name 本身）

- 位置: `bkmonitor/packages/monitor_web/scene_view/resources/host.py`
- `runtime_metric_map` — UI 字段↔system.proc 字段映射（cpuUsage→cpu_usage_pct 等）

### 易混淆字段（同一条进程数据）

| 字段 | 来源 | 格式 |
|------|------|------|
| display_name | system.proc 维度 = CMDB bk_process_name | 进程名字符串，如 "nginx" |
| proc_name | system.proc 维度 | 进程二进制文件名 |
| API name | CMDB bk_process_name | 同 display_name |
| API id | 代码拼接 | "进程名@主机IP"（复合，仅前端选中/去重） |

### 注意

- display_name 值由 CMDB 配置决定，无固定正则格式，可能为空（代码用 `record.get("display_name")` 真值过滤，空值跳过）。
- 补全 get_host_process_list 时，display_name 直接返回进程名即可，不要自拼 @ip。
