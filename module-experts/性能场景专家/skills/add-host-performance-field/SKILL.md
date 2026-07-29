---
name: add-host-performance-field
description: 为 monitor_web.performance 模块的主机列表/指标聚合接口新增一个聚合字段（指标/进程/告警/状态类）的标准操作步骤。当需要"给主机性能列表加个字段""扩展 search_host_metric 返回""新增主机拓扑/进程展示字段"时使用。
---

# 新增主机性能聚合字段

## 适用场景
- 给 `host_performance`（主机列表）或 `search_host_metric`（指定主机指标）的返回结构新增一个字段
- 新增字段的数据来自 `resource.cc.*` 或 `api.cmdb.*` 等外部聚合源
- 涉及 `performance/resources.py` 中 `HostPerformanceResource` / `SearchHostMetricResource`

## 触发短语
- "给主机性能列表加个字段"
- "新增主机性能指标 / 进程字段"
- "扩展 search_host_metric 返回"
- "host_performance 返回里加个 xxx"

## 前置知识
模块采用「字典就地填充 + ThreadPool 并行」范式（详见 `01-架构.md` / `02-实现.md`）：
- `host_dict` 先放默认值（多为 `None` / `[]`）
- 每个数据源是一个**静态方法** fetch 单元，按 `bk_host_id` 写入 `host_dict`
- `perform_request` 用 `ThreadPool.apply_async` 并行注册，最后 `join`

## 执行步骤

### 步骤 1：在 host_dict 加默认值
在目标 Resource 的 `perform_request` 中，给 `host_dict` 构造字典新增字段，初值 `None`（列表类用 `[]`）。
- 列表接口：`HostPerformanceResource.perform_request`（resources.py 约 L79-L114）
- 指标接口：`SearchHostMetricResource.perform_request`（resources.py 约 L402-L414）

### 步骤 2：新增/复用 fetch 静态方法
在 Resource 内新增静态方法（参考 `get_process_status` / `get_alarm_count` 写法）：
```python
@staticmethod
def get_xxx(bk_biz_id: int, hosts: list[Host], data: dict[int, dict]):
    result = resource.cc.get_xxx(bk_biz_id=bk_biz_id, hosts=hosts)
    for bk_host_id in result:
        if bk_host_id not in data:
            continue
        data[bk_host_id]["xxx"] = result[bk_host_id]
```
若数据源已存在对应 `resource.cc.*` 方法，直接复用即可，无需新建。

### 步骤 3：ThreadPool 注册
在 `perform_request` 的 `pool = ThreadPool()` 之后、`pool.close()` 之前，新增：
```python
pool.apply_async(self.get_xxx, args=(bk_biz_id, hosts, host_dict))
```
（注意：必须在 `pool.join()` 之前注册，否则不会被调度）

### 步骤 4：进程类字段需同步两处
若新增的是**进程级字段**（如 `component` 列表内的子字段），需同时修改：
- `HostPerformanceResource.get_process_status`（约 L34-L56）的 `component` 构造
- `SearchHostMetricResource.get_process_status`（约 L377-L398）的 `component` 构造
两者目前代码重复，需保持一致。

### 步骤 5：评估缓存影响（仅列表接口）
`HostPerformanceResource` 是 `CacheResource`（`CacheType.HOST`），结果被缓存。若新字段是**实时**数据，需确认缓存刷新时机（缓存 TTL 或主动失效），否则前端可能看到旧值。

## 边界与注意
- 各 fetch 方法必须对 `bk_host_id not in data` 做 `continue`，避免写入不存在的主机
- 单源异常不要抛到 `perform_request` 外层，否则整份列表 500（参考 challenger 对 `proc_num` 的防御性建议）
- 新增字段后，前端契约（`ProcessItem` / 主机列表结构）需同步，否则字段不会被展示

## 示例
需求：给主机列表新增「进程实例数 `instanceCount`」（来自 `resource.cc.get_process_info` 的 `proc_num`）
1. `host_dict` 加 `"instanceCount": None`
2. 复用 `get_process_status`，在 `component` 构造中加 `"instanceCount": process.get("proc_num")`
3. 列表接口已在 `pool.apply_async(self.get_process_status, ...)` 注册，无需新增 apply_async
4. 同步 `SearchHostMetricResource.get_process_status` 的 `component` 结构
5. 列表接口走 HOST 缓存，`proc_num` 来自 CMDB（非实时），缓存可接受

## 参考
- 架构与实现：`01-架构.md`、`02-实现.md`
- 接口契约：`05-接口.md`
- 外部数据源：`bkmonitor/packages/monitor_web/cc/resources/cmdb.py`（get_process_info L141、get_host_performance_data L418 等）
