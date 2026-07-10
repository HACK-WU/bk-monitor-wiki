# 代码骨架生成状态 (Skeleton Status)

> **Requirement:** [REQ-20260707-001] Host 页面接口拆分重构  
> **Design Doc:** `/root/bk-monitor/bk-monitor-wiki/requirements/integration/2026-07-07-Host页面接口拆分重构/design/`  
> **Generated At:** 2026-07-09  

---

## 总览

| 子需求 | 文件名 | 行数 | 状态 | 批次 |
|------|--------|------|------|------|
| S-01 | `host.py`, `views.py` | ~120 | ✅ **编码完成** | Batch 1 |
| S-02 | `cmdb.py`, `host.py`, `api/cmdb/define.py` | ~130 | ✅ **编码完成** | Batch 2 |

**整体进度：编码实施已完成** → 待进入稳定验证（契约核对/集成测试）

---

## S-01: Panels/Order 接口拆分

### 新增 Resource 类

| Resource 类 | 所在文件 | 方法 | 路由 |
|-------------|---------|------|------|
| `GetHostViewsPanelsResource` | `host.py` | `perform_request` | `get_host_views_panels` |
| `GetHostViewsPanelsOrderResource` | `host.py` | `perform_request` | `get_host_views_panels_order` |
| `GetProcessViewsPanelsResource` | `host.py` | `perform_request` | `get_process_views_panels` |
| `GetProcessViewsPanelsOrderResource` | `host.py` | `perform_request` | `get_process_views_panels_order` |

### 路由注册

- 文件: `views.py`
- 位置: `SceneViewViewSet.resource_routes` 列表末尾追加 4 条 POST 路由
- 新增 import 语句从 `monitor_web.scene_view.resources.host` 导入 4 个 Resource 类

### 实现完成检查

- ✅ `GetHostViewsPanelsResource` — `perform_request` 完整实现（复用 `create_default_views` → `SceneViewModel.objects.filter` → `get_auto_view_panels(view)[0]`）
- ✅ `GetProcessViewsPanelsResource` — 同上，取 `[0]`
- ✅ `GetHostViewsPanelsOrderResource` — 同上，取 `[1]`
- ✅ `GetProcessViewsPanelsOrderResource` — 同上，取 `[1]`
- ✅ `id` 字段语义修正 — CharField 视图 ID（`"host"` / `"process"`），与 `SceneViewModel.id` 对齐
- ✅ 4 个 Resource 均添加 `validate_bk_biz_id` 权限校验
- ✅ `views.py` 路由注册完成 — `SceneViewViewSet.resource_routes` 追加 4 条 POST 路由
- ✅ 全部语法校验通过

---

## S-02: 进程列表字段补全

### 修改函数

| 函数/类 | 所在文件 | 修改内容 |
|---------|---------|---------|
| `Process.__init__` | `api/cmdb/define.py` | **P0 修复**：注入 `_extra_attr = kwargs` + `__getattr__` 兜底 |
| `get_process_info` | `cmdb.py` | 扩展返回字段: `bindIp`, `port`, `startCommand`, `protocol`, `workPath`, `autoStart`, `priority`, `procNum`, `user`, `portStatus`；通过 `getattr(pp, "x", None)` 提取，nullable |
| `GetHostProcessListResource.perform_request` | `host.py` | 透传 15 字段到前端响应（含运行时数据合并） |

### 新增函数

| 函数 | 所在文件 | 职责 |
|------|---------|------|
| `get_process_runtime_metrics` | `cmdb.py` | 查询 `system.proc` 6 项指标（`cpu_usage_pct`, `mem_rss`, `mem_usage_pct`, `pid`, `uptime`, `user`），返回 `{bk_host_id: {display_name: {field: value}}}` |
| `get_process_port_health` | `cmdb.py` | 查询 `system.proc_port.port_health`，返回 `{bk_host_id: {display_name: 0/1/None}}`（0=Normal, 1=Abnormal） |

### 字段来源（分层结构）

| 字段 | 来源 | 类型 | 可空性 | 备注 |
|------|------|------|--------|------|
| `id` | CMDB `bk_process_name` | string | ❌ | 与 `name` 相同 |
| `name` | CMDB `bk_process_name` | string | ❌ | |
| `status` | `get_process_status`（`system.proc_port:proc_exists`）| string | ❌ | ON / OFF / UNKNOWN |
| `hostIp` | 入参主机 `host.ip` | string | ❌ | 前端展示用 |
| `protocol` | CMDB `protocol` | string | ✅ | TCP / UDP / None |
| `bindIp` | CMDB `bind_ip` | string | ✅ | |
| `port` | CMDB 端口首值 | string | ✅ | `str(ports[0]) if ports else None` |
| `startCommand` | CMDB `start_cmd` | string | ✅ | |
| `user` | `system.proc` `user` > CMDB `user` | string | ✅ | 运行时覆盖 CMDB |
| `portStatus` | `system.proc_port.port_health` | int | ✅ | 0=Normal, 1=Abnormal, None=unknown |
| `cpuUsage` | `system.proc` `cpu_usage_pct` | float | ✅ | % |
| `memUsage` | `system.proc` `mem_usage_pct` | float | ✅ | % |
| `memRss` | `system.proc` `mem_rss` | int | ✅ | bytes |
| `pid` | `system.proc` `pid` | int | ✅ | |
| `uptime` | `system.proc` `uptime` | int | ✅ | 秒 |

### 实现完成检查

- ✅ `Process.__init__` P0 修复 — `api/cmdb/define.py`
- ✅ `get_process_info` 字段扩展 — 10 个 CMDB 字段（含 portStatus）
- ✅ `get_process_runtime_metrics` 新建 — 6 项 system.proc 指标
- ✅ `get_process_port_health` 新建 — port_health 查询
- ✅ `GetHostProcessListResource` 响应重构 — 15 字段完整透出
- ✅ 字段名对齐前端文档 — `cpuUsage`/`memUsage`（非 `cpuUsagePct`/`memUsagePct`）
- ✅ 全部文件语法校验通过 — `host.py`, `cmdb.py`, `views.py`, `api/cmdb/define.py`

### 遗留性能优化

- `get_process_status` + `get_process_port_health` 共同查询 `system.proc_port`，Phase 2 可合并为单次 UnifyQuery 减少 TSDB 往返
- TODO：`get_process_port_health` 添加 `>3s 超时降级为 None`（当前仅标注，未实现）

---

## 设计文档索引

| 文档 | 路径 |
|------|------|
| 设计父文档 | `design/host_view_split_DESIGN.md` |
| S-01 子文档 | `design/host_view_split_S01_panels_order_DESIGN.md` |
| S-02 子文档 | `design/host_view_split_S02_process_fields_DESIGN.md` |
| 评审报告 | `design/design-review.md` |

---

## Challenger 审查记录

### 审查结果

| 质疑 | 类型 | 等级 | 处理状态 |
|------|------|------|----------|
| #1 S-01 Resource 缺少权限校验 | 架构 | 🟡 中 | **已修复** — 为 4 个新 Resource 的 RequestSerializer 添加 `validate_bk_biz_id` |
| #2 `Process` kwargs 未存储 | 业务逻辑 | 🔴 高 | **已修复** — `Process.__init__` 添加 `self._extra_attr = kwargs` + `__getattr__` 方法 |
| #3 双查询性能问题 | 性能 | 🟡 中 | **已标记** — `get_process_port_health` 添加 PERFORMANCE NOTE，Phase 2 合并 |
| #4 端口健康查询无超时保护 | 异常 | 🟡 中 | **已标记** — 添加 TODO (`>3s 降级为 None`) |
| #5 `portStatus` 语义混淆 | 接口 | 🟡 中 | **已标记** — `GetHostProcessListResource` 响应中添加详细语义注释 |
| #6 旧字段兼容 | 兼容 | 🟢 低 | 💤 延后 — 原有字段顺序未变 |
| #8 循环依赖风险 | 架构 | 🟢 低 | 💤 延后 — 当前无循环，保持监控 |

### 修复详情

#### Fix #1: `Process.__init__` kwargs 存储 (P0 阻断项)

**文件**: `api/cmdb/define.py`  
**问题**: `Process` 类丢弃 `**kwargs`，导致 `getattr(pp, "work_path", "")` 永远返回 `''`  
**修复**: 在 `__init__` 末尾添加 `self._extra_attr = kwargs`，并新增 `__getattr__` 方法委托到 `_extra_attr` (与 `ServiceInstance` 模式一致)  
**验证**: `getattr(p, 'work_path', '') == '/data'` 通过

#### Fix #2: S-01 Resource 权限校验

**文件**: `packages/monitor_web/scene_view/resources/host.py`  
**修复**: 4 个新 Resource 的 inner `RequestSerializer` 均添加 `def validate_bk_biz_id(self, value)` 方法  
**模式**: 参照 `GetHostProcessPortStatusResource.validate_bk_biz_id`

#### Fix #3: 性能与超时注释

**文件**: `packages/monitor_web/cc/resources/cmdb.py`  
**修复**: `get_process_port_health` docstring 中添加 PERFORMANCE NOTE；`query.query_data` 调用处添加 TODO 标注超时降级需求

#### Fix #4: portStatus 语义注释

**文件**: `packages/monitor_web/scene_view/resources/host.py`  
**修复**: `GetHostProcessListResource` 响应中 `portStatus` 字段新增详细注释，说明与 `status` 字段的区别及三个返回值含义

---

## 验收检查清单

- [ ] S-01: 4 个新 Resource `perform_request` 均实现完毕（当前为 `pass` 占位）
- [ ] S-01: `HostBuiltinProcessor.get_auto_view_panels` 调用正确，仅取部分返回值
- [ ] S-02: `get_process_port_health` 函数实现并验证查询语句
- [ ] S-02: CMDB 原始字段通过 `getattr` 正确提取（Phase 1 兼容模式）— **已修复 `Process` kwargs 存储**
- [ ] S-02: 端口健康查询 3s 超时降级机制实现
- [ ] S-02: 前端响应兼容旧字段（`status`, `name`, `id` 不变）
- [ ] 单元测试通过
- [ ] 联调测试通过
- [ ] **联调 checklist: 核对 endpoint 名称与前端 Wiki 完全一致**
