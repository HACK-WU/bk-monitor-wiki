# Host 页面接口拆分重构

> **需求编号**: REQ-20260707-001
> **创建日期**: 2026-07-07
> **需求状态**: 已确认
> **需求类型**: feat / refactor
> **关联模块**: monitor_web.performance, monitor_web.scene_view
> **原始文档**: [Host 页面 Service API 文档](https://iwiki.woa.com/p/4024333340)

---

## 1. 背景

前端 Host 页面（`src/trace/pages/host/`）之前通过少量聚合接口一次性获取所有数据。随着页面复杂度增加，前端需要将接口拆分为更细粒度的独立接口，实现：

- **首屏快速渲染**：基础信息先返回，指标数据异步加载
- **按需加载**：进程列表、面板配置等仅在需要时请求
- **缓存策略**：部分稳定配置（如面板排序）可模块级缓存

前端已完成接口拆分设计和 Service 层改造，后端需要同步提供对应接口。

---

## 2. 现状分析

### 2.1 当前后端接口

| 接口 | Resource 类 | 路由 | 当前返回 |
|------|------------|------|---------|
| `host_performance` | `HostPerformanceResource` | `GET /performance/host_performance/` | 主机列表 + 指标 + 进程 + 告警（大聚合） |
| `search_host_info` | `SearchHostInfoResource` | `POST /performance/search_host_info/` | 主机基础信息列表 ✅ |
| `search_host_metric` | `SearchHostMetricResource` | `POST /performance/search_host_metric/` | 主机指标数据 ✅ |
| `get_host_process_list` | `GetHostProcessListResource` | `POST /scene_view/get_host_process_list/` | 进程名称列表（字段不全） |
| `get_scene_view` | `GetSceneViewResource` | `GET /scene_view/get_scene_view/` | 完整视图配置（含 panels + order） |

### 2.2 现有问题

1. **panels 和 order 没有独立接口**：当前通过 `get_scene_view` 返回完整视图配置，前端需要单独获取面板配置和排序配置
2. **进程列表字段严重不足**：`GetHostProcessListResource` 仅返回 `status`, `name`, `id` 三个字段，前端期望 `pid`, `port`, `bindIp`, `cpuUsage`, `memUsage`, `startCommand` 等 11 个字段
3. **缺少进程视图的面板配置接口**：进程详情页需要独立的面板配置（`process` 视图）

---

## 3. 目标

将后端接口与前端文档对齐，提供以下 8 个接口：

### 3.1 已有接口（需调整或保持）

| 序号 | 接口名 | HTTP 方法 | 路由 | 状态 |
|------|--------|----------|------|------|
| 1 | `getHostInfoList` | POST | `/performance/search_host_info/` | ✅ 已存在，保持兼容 |
| 2 | `getHostMetricInfoList` | POST | `/performance/search_host_metric/` | ✅ 已存在，保持兼容 |
| 3 | `getHostTopoTreeByBizId` | POST | `/commons/get_topo_tree/` | ✅ 已存在，保持兼容 |

### 3.2 需改造接口

| 序号 | 接口名 | HTTP 方法 | 路由 | 改造点 |
|------|--------|----------|------|--------|
| 4 | `getHostProcessList` | POST | `/scene_view/get_host_process_list/` | 补全字段：pid, port, bindIp, cpuUsage, memUsage, startCommand 等 |

### 3.3 需新建接口

| 序号 | 接口名 | 类型 | 来源 | 说明 |
|------|--------|------|------|------|
| 5 | `getHostViewsPanels` | 图表面板配置 | 从 `get_scene_view` 的 `host` 视图拆分 | 返回主机详情页的图表(panel)配置 |
| 6 | `getProcessViewsPanels` | 图表面板配置 | 从 `get_scene_view` 的 `process` 视图拆分 | 返回进程详情页的图表(panel)配置 |
| 7 | `getHostMetricGroupPanelOrder` | 排序与显隐 | 从 `get_scene_view` 的 `host` 视图拆分 | 返回主机指标分组排序与显隐配置 |
| 8 | `getProcessMetricGroupPanelOrder` | 排序与显隐 | 从 `get_scene_view` 的 `process` 视图拆分 | 返回进程指标分组排序与显隐配置 |

---

## 4. 接口详细说明

> 注：详细接口契约（请求参数、返回类型、示例）参考 `references/frontend-api-wiki.md`（前端 Wiki 落盘文档）。

### 4.1 getHostProcessList 改造

**当前问题**：仅返回 `status`, `name`, `id`

**期望字段**（来自前端文档）：
- `bindIp`: 绑定 IP
- `cpuUsage`: CPU 使用率
- `hostIp`: 主机 IP
- `id`: 唯一标识（进程名@IP）
- `memRss`: 物理内存使用量
- `memUsage`: 内存使用率
- `name`: 进程名
- `pid`: 进程 ID
- `port`: 端口号
- `portStatus`: 端口状态（0=正常，1=异常）
- `protocol`: 协议（TCP/UDP）
- `startCommand`: 启动命令
- `uptime`: 运行时长
- `user`: 运行用户
- `instanceCount`: 进程实例数（取自 CMDB `proc_num` 字段）
- `fdNum`: 文件句柄数量
- ~~`threadConnected`: 连接数——已放弃，CMDB/指标库均无对应指标~~

**后端数据来源分析**：
- 当前 `GetHostProcessListResource` 调用 `resource.cc.get_process_info()` 获取进程信息
- 需要调研 `get_process_info` 的原始返回结构，确认能否提供上述字段
- 部分字段（如 `cpuUsage`, `memUsage`, `uptime`）可能需要从指标库查询
- **新增字段数据源（2026-07-20 补充，2026-07-21 定稿）**：
  - `instanceCount`：取自 CMDB 进程 `proc_num` 字段（进程实例数）。实现：`Process` 模型（`bkmonitor/api/cmdb/define.py`）新增 `proc_num` 属性，`get_process_info` 透出，前端映射为 `instanceCount`。**不再按 display_name 分组计数**（原方案废弃）
  - `fdNum`：`system.proc` 表 `fd_num` 字段（`bk-monitor-base/src/bk_monitor_base/metadata/data/init_resulttable.json` 行 6100-6108，描述"进程文件句柄数"，unit=short），加入 `get_process_runtime_metrics` 的 `METRIC_FIELDS`
  - ~~`threadConnected`（连接数）：已放弃。经核查 CMDB 与指标库（`system.proc`/`mysql.net`）均无对应指标字段，无法提供，前端移除该列即可~~

### 4.2 面板配置接口（4 个新接口）

**数据来源**：
- 当前 `monitor_web/scene_view/builtin/host.py` 中的 `get_auto_view_panels()` 函数生成 panels + order
- `HostBuiltinProcessor.get_view_config()` 返回 `"panels"` 和 `"order"`

**拆分逻辑**：
- `getHostViewsPanels` → 复用 `get_auto_view_panels(view)` 中 `view.id == "host"` 的 panels
- `getProcessViewsPanels` → 复用 `get_auto_view_panels(view)` 中 `view.id == "process"` 的 panels
- `getHostMetricGroupPanelOrder` → 复用 `get_auto_view_panels(view)` 中 `view.id == "host"` 的 order
- `getProcessMetricGroupPanelOrder` → 复用 `get_auto_view_panels(view)` 中 `view.id == "process"` 的 order

**路由规划**（建议放入 `scene_view` 模块）：
- `GET /scene_view/get_host_views_panels/`
- `GET /scene_view/get_process_views_panels/`
- `GET /scene_view/get_host_metric_group_panel_order/`
- `GET /scene_view/get_process_metric_group_panel_order/`

---

## 5. 验收标准

- [ ] `getHostProcessList` 返回字段与前端文档完全一致
- [ ] `getHostViewsPanels` 返回 `HostViewsRowPanel[]` 结构，与前端文档一致
- [ ] `getProcessViewsPanels` 返回 `HostViewsRowPanel[]` 结构，进程面板 id 前缀为 `process.{指标 id}`
- [ ] `getHostMetricGroupPanelOrder` 返回 `MetricGroupPanelOrder[]` 结构
- [ ] `getProcessMetricGroupPanelOrder` 返回 `MetricGroupPanelOrder[]` 结构（进程默认分组为 `__UNGROUP__`）
- [ ] 所有新接口与前端 Service 层成功联调
- [ ] 已有接口保持向后兼容

---

## 6. 依赖与风险

### 6.1 依赖
- `monitor_web/scene_view/builtin/host.py` 中的 panels/order 生成逻辑
- `resource.cc.get_process_info()` 的数据源能力

### 6.2 风险
| 风险 | 等级 | 说明 |
|------|------|------|
| 进程字段数据源不足 | 中 | 底层 `get_process_info` 可能无法提供全部期望字段，需调研确认 |
| panels 结构变更影响 | 低 | 需确保拆分后的 panels 格式与现有 `get_scene_view` 返回一致 |
| 缓存策略 | 低 | 前端期望进程面板配置使用模块级缓存，后端需确认是否支持 |

---

## 7. 备注

- 前端文档中标注"**数据不太够，需要安装设计稿中补充字段**"的 `getHostProcessList`，需要与前端确认最终字段定义
- 前端文档中标注"**新 API 根据原 host scene panel配置拆分**"的面板接口，需保证与现有 `get_scene_view` 返回的 panels/order 格式兼容
- **[2026-07-20 ~ 2026-07-21]** `getHostProcessList` 字段扩展定稿：新增 `fdNum`（来自 `system.proc` 的 `fd_num`）、`instanceCount`（来自 CMDB 进程 `proc_num` 字段，需在 `Process` 模型新增 `proc_num` 属性）；`threadConnected`（连接数）经核查无对应指标，**已放弃**。另：`get_process_runtime_metrics` 支持 `start_time`/`end_time` 区间查询，`get_process_port_health` 端口健康聚合由 AVG 改为 MIN。代码要点见项目记忆 `项目踩坑点/GetHostProcessListResource 三字段扩展数据来源`
