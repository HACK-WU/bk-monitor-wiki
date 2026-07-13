# S02 进程字段设计更新（CMDB 优先 / TSDB 兜底）

> 关联需求：REQ-20260707-001（Host 页面接口拆分重构 · S02 进程字段补全）
> 本文档为设计**更新记录**，不修改 `requirement.md` 及其他既有文档。
> 背景：提交 `5c33c8f` 的 Code Review 发现 TSDB 字段名/维度错误，并据此调整 S02 字段来源策略。

---

## 1. 设计原则变更

| 项 | 原方案 | 新方案（本文档） |
|----|--------|------------------|
| 主数据源 | 运行时字段优先从 TSDB 取，CMDB 仅兜底 `user` | **CMDB 配置数据为主源**，TSDB 运行时数据作为增强 |
| 两源都有时 | TSDB 优先（`user` 取 TSDB） | **CMDB 优先，TSDB 兜底** |
| 查询失败处理 | 无兜底，TSDB 异常会拖垮整个接口 | TSDB 查询 `try/except` 兜底，`runtime_data={}`，CMDB 基础字段照常返回 |

**理由**：CMDB 返回的是确定性配置数据（启动命令、绑定、用户），列表不应因运行时采集缺失/超时而丢掉基础信息。运行时指标（cpu/mem/pid/uptime/portStatus）仅在 TSDB 有，缺失时置 `None` 即可。

---

## 2. 前端 ProcessItem 14 字段来源优先级

| 前端字段 | CMDB 来源（`list_service_instance_detail`） | TSDB 来源 | 策略 |
|---------|--------------------------------------------|-----------|------|
| `id` | `process.bk_process_id` | — | 纯 CMDB（建议改回 `bk_process_id`，当前误用 `name`） |
| `name` | `process.bk_process_name` / `bk_func_name` | `system.proc.display_name` | CMDB 优先（两者应一致） |
| `hostIp` | 主机 IP（经 `bk_host_id` 关联） | — | 纯 CMDB |
| `bindIp` | `bind_info.ip` | — | 纯 CMDB |
| `port` | `bind_info.port` | — | 纯 CMDB |
| `protocol` | `bind_info.protocol` | — | 纯 CMDB |
| `startCommand` | `process.start_cmd` | — | 纯 CMDB |
| `user` | `process.user`（启动用户，配置值） | `system.proc.username`（运行用户，实际值） | **CMDB 优先，TSDB 兜底** |
| `portStatus` | — | `system.proc_port.port_health` | 纯 TSDB（无则 `None`） |
| `cpuUsage` | — | `system.proc.cpu_usage_pct` | 纯 TSDB（无则 `None`） |
| `memUsage` | — | `system.proc.mem_usage_pct` | 纯 TSDB（无则 `None`） |
| `memRss` | — | `system.proc.mem_res` | 纯 TSDB（无则 `None`） |
| `pid` | ⚠️ 仅 `bk_process_id`（≠操作系统 PID） | `system.proc.pid`（操作系统进程号） | **必须用 TSDB，不可用 CMDB 兜底** |
| `uptime` | — | `system.proc.uptime` | 纯 TSDB（无则 `None`） |

> ⚠️ **`pid` 关键约束**：CMDB 的 `bk_process_id` 是进程**配置**ID，与操作系统进程号（`system.proc.pid`）语义完全不同。即使 CMDB 有值，也不能用它兜底前端的 `pid`，否则返回错误数据。

---

## 3. CMDB 接口返回信息（`list_service_instance_detail`）

### 3.1 接口链路
- 业务封装：`bkmonitor/api/cmdb/default.py` → `GetProcess` Resource
- 底层调用：`client.list_service_instance_detail`（蓝鲸 CC 组件 API）
  - 路径：`/api/v3/findmany/proc/service_instance/details`（apigw）/ `/list_service_instance_detail/`（ESB）
  - 封装注册：`bkmonitor/blueking/component/apis/cc.py:419`（`ComponentAPI`）
- `GetProcess` 内部已按 `bk_host_id` 过滤，遍历 `process_instances`，把 `process` + `relation` 合并，并把 `bind_info[]` 展开为 `bind_ip` / `port` / `protocol` / `bk_enable_port`，封装成 `Process(**process_params)`。

### 3.2 响应结构（节选自接口示例）
```
data.info[]                          # 服务实例列表
 ├─ bk_biz_id, id, name, bk_host_id, bk_module_id, service_category_id, ...
 └─ process_instances[]
     ├─ process   # 进程配置属性
     └─ relation  # 关联信息（bk_host_id / bk_process_id / service_instance_id / process_template_id）
```
`process` 对象字段（来自 CMDB `process_instances[x].process`）：

| CMDB 字段 | 类型 | 说明 | 映射到前端 |
|-----------|------|------|-----------|
| `bk_process_id` | int | 进程配置ID | `id` |
| `bk_func_name` | string | 进程名称 | `name` |
| `bk_process_name` | string | 进程别名 | `name` |
| `start_cmd` | string | 启动命令 | `startCommand` |
| `user` | string | 启动用户 | `user`（CMDB 优先） |
| `bind_info[]` | object[] | 绑定信息 | — |
| `bind_info[].ip` | string | 绑定IP | `bindIp` |
| `bind_info[].port` | string | 绑定端口 | `port` |
| `bind_info[].protocol` | string | 协议 | `protocol` |
| `bind_info[].enable` | bool | 端口是否启用 | 控制端口是否展示 |

> 注：`process.user` 是 **启动用户**（CMDB 配置值）；运行时实际运行用户在 TSDB `system.proc.username`。两源都有时按 §1 取 CMDB 优先。

### 3.3 字段完整性结论
CMDB 接口**已覆盖**需求 S02 中前端 `ProcessItem`（frontend-api-wiki.md）所需的全部配置侧字段（`id`/`name`/`bindIp`/`port`/`protocol`/`startCommand`/`user`），无需另起查询。运行时指标（§2 纯 TSDB 列）CMDB 不提供，继续走 TSDB。

> 注：CMDB `process` 还提供 `work_path`/`priority`/`proc_num`/`auto_start` 等配置字段，但前端 `ProcessItem` 契约（14 字段）未使用，故后端 `Process`/`get_process_info` 仅显式透传 `user`/`start_cmd`，其余仍走 `_extra_attr` 兜底，不纳入响应。

---

## 4. TSDB 字段定义来源（`init_resulttable.json`）

### 4.1 文件位置
- **绝对路径**：`/root/bk-monitor/bk-monitor-base/src/bk_monitor_base/metadata/data/init_resulttable.json`
- **相对路径（仓库根 `bk-monitor/`）**：`bk-monitor-base/src/bk_monitor_base/metadata/data/init_resulttable.json`
- **仓库归属**：该文件属于 **`bk-monitor-base` 子仓库**（独立 Git，不与主工程 `bkmonitor` 共用），是元数据初始化表定义，声明各 `result_table` 的字段名、类型、单位及 `tag`（`dimension` / `metric` / `timestamp`）。所有 TSDB 查询字段名必须与这里一致，否则查不到或语义错。

### 4.2 `system.proc` 表（table_id: `system.proc`，文件行 5982 起）
进程运行时指标表。关键字段（`tag` 决定能否做 `AVG` 指标、还是按列名返回的维度）：

| 字段 | 类型 | tag | 说明 | S02 用途 |
|------|------|-----|------|---------|
| `username` | string | **dimension** | 进程用户名 | `user`（TSDB 兜底，按列名读） |
| `pid` | int | **dimension** | 进程id（操作系统号） | `pid`（按列名读） |
| `uptime` | int | **metric** | 进程运行时间（s） | `uptime`（AVG） |
| `cpu_usage_pct` | double | metric | 进程CPU使用率 | `cpuUsage`（AVG） |
| `mem_usage_pct` | double | metric | 进程内存使用率 | `memUsage`（AVG） |
| `mem_res` | int | metric | 进程使用物理内存（bytes） | `memRss`（AVG） |
| `display_name` | string | dimension | 进程显示名称 | 关联 key |
| `bk_host_id` / `bk_target_ip` / `bk_target_cloud_id` | — | dimension | 主机定位维度 | 分组/关联 |

> ❌ **易错**：`system.proc` 表中**不存在** `user` 字段（那是其他表的 CPU 指标），也**不存在** `mem_rss` 字段（正确名是 `mem_res`）。原提交 `5c33c8f` 的 `METRIC_FIELDS` 用了这两个错误名，必须修正。

### 4.3 `system.proc_port` 表（table_id: `system.proc_port`，文件行 6327 起）
进程端口状态表。关键字段：

| 字段 | 类型 | tag | 说明 | S02 用途 |
|------|------|-----|------|---------|
| `proc_exists` | int | metric | 进程存活状态 | `status`（AGENT_STATUS 判定） |
| `port_health` | int | metric | 进程端口状态 | `portStatus` |
| `display_name` | string | dimension | 进程显示名称 | 关联 key |
| `bk_host_id` / `bk_target_ip` / `bk_target_cloud_id` | — | dimension | 主机定位维度 | 分组/关联 |

> ⚠️ `system.proc_port` 表中**无 `pid` 字段**，操作系统 PID 只能从 `system.proc` 取。

---

## 5. 原提交（5c33c8f）需修正点（来自 Code Review P0-1）

1. **`get_process_runtime_metrics`（`cc/resources/cmdb.py:247`）字段名错误**
   - `mem_rss` → `mem_res`（物理内存，见 §4.2）
   - `user` → `username`，并改为 **dimension**（按列名 `record["username"]` 读，不能进 `metrics` 做 `AVG`）
   - `pid` 是 **dimension**，按列名 `record["pid"]` 读
   - `uptime` 是 **metric**，可 `AVG`
2. **`expression` 不能再用乘积**
   - 原 `expression="*".join([f"A{i}"...])` 对异构量（含字符串维度 `username`）乘积无意义且可能报错
   - 单数据源多指标时改用 `expression="a"`，引擎按别名各自返回
3. **`pid` 不可 CMDB 兜底**（见 §2 约束）
4. **`user` 字段优先级反转**（见 §1/§2）：`CMDB.user or TSDB.username`

---

## 6. 待确认项（未在本轮改动，需跨端对齐）

| # | 待确认 | 影响 |
|---|--------|------|
| Q1 | `port_health` 原始极性（1=健康 or 1=异常）？需与前端 Service 层对齐 `portStatus`（0=Normal/1=Abnormal） | 决定 `get_process_port_health` 返回值是否需反转 |
| Q2 | 前端 `id` 究竟期望 `bk_process_id` 还是其他？当前实现用 `process["name"]`，建议改 `bk_process_id` | `id` 字段稳定性 |
| Q3 | TSDB 查询超时/降级阈值（commit TODO 提到 >3s） | 兜底健壮性实现细节 |
