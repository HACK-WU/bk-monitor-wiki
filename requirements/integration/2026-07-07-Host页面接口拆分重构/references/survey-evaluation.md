# 调研结果评估报告

> **需求编号**: REQ-20260707-001
> **评估日期**: 2026-07-08
> **关联文档**: [代码调研报告](code-survey.md)、[API字段映射](api-field-mapping.md)、[UI设计稿](../mockup/host-page-mockup.md)

---

## 一、总体评估

**结论**：调研结果**基本符合预期**，覆盖了UI设计稿中的所有字段需求，并提供了清晰的实现路径。但有**3个技术实现点**需要关注。

## 二、字段覆盖情况对比

| UI设计稿字段 | 调研覆盖状态 | 数据来源 | 备注 |
|-------------|-------------|----------|------|
| **进程名** | ✅ 已覆盖 | CMDB `bk_process_name` | 直接映射 |
| **端口号** | ✅ 已覆盖 | CMDB `protocol` + `bindIp` + `port` | 需组合显示 |
| **用户** | ✅ 已覆盖 | `system.proc` 维度 | 实时查询 |
| **占用CPU** | ✅ 已覆盖 | `system.proc` 指标 `cpu_usage_pct` | 实时查询 |
| **常驻内存(RSS)** | ✅ 已覆盖 | `system.proc` 指标 `mem_usage_pct` + 维度 | 需组合显示 |
| **运行时长** | ✅ 已覆盖 | `system.proc` 维度 | 实时查询 |
| **端口状态** | ✅ 已覆盖 | `system.proc_port` 指标 `port_health` | 区分于进程运行状态 |

## 三、技术实现路径评估

### ✅ **可行且清晰**：
1. **4个新接口实现成本低**：`get_auto_view_panels` 已天然按 `host`/`process` 区分，返回 `(panels, order)` 元组，只需封装4个新Resource类。
2. **CMDB侧直接补全字段**：`bindIp`、`protocol`、`port` 可直接从CMDB获取。
3. **运行时数据查询路径明确**：`system.proc` 和 `system.proc_port` 时序数据可通过标准时序查询接口获取。

### ⚠️ **需关注技术实现细节**：

1. **`startCommand` 字段获取**：
   - **问题**：CMDB原始JSON有 `start_cmd`，但 `Process` 类 `__init__` 无 `_extra_attr` 兜底，构造对象后丢弃。
   - **建议**：需改 `Process.__init__` 增加 `_extra_attr` 或绕过封装直接读取原始JSON。
   - **风险**：中等，需评估对现有CMDB调用的影响。

2. **`portStatus` 端口健康状态查询**：
   - **问题**：需查询 `system.proc_port` 的 `port_health` 指标，这是**新增的时序查询逻辑**。
   - **建议**：新增 `system.proc_port` 查询逻辑，与 `system.proc` 查询并行。
   - **风险**：低，但需确保查询性能。

3. **运行时数据查询性能**：
   - **问题**：每个进程需查询多个时序指标（`pid`、`cpuUsage`、`memRss`、`memUsage`、`uptime`、`user`），可能影响性能。
   - **建议**：考虑批量查询、缓存策略、降级方案（如字段留空或返回"--"）。
   - **风险**：中等，需性能测试。

## 四、架构符合度

| 方面 | 评估 | 说明 |
|------|------|------|
| **路由规划** | ✅ 符合 | 新接口统一挂在 `SceneViewViewSet` 下，与需求文档一致 |
| **数据流** | ✅ 符合 | CMDB + 时序数据源分离，符合当前架构 |
| **错误处理** | ✅ 符合 | 依赖Resource框架统一异常处理，新增时序查询需考虑降级策略 |
| **缓存策略** | ✅ 符合 | 面板配置可模块级缓存，运行时数据实时查询 |

## 五、风险与建议

| 风险点 | 等级 | 建议 |
|--------|------|------|
| `Process`类修改影响 | 中 | 先评估 `Process` 类被调用的范围，确保修改不影响其他功能 |
| 时序查询性能 | 中 | 实现时考虑批量查询、异步加载、前端分页 |
| 端口健康状态查询 | 低 | 确保 `system.proc_port` 数据源可用且查询逻辑正确 |
| 字段映射复杂性 | 低 | 前端需处理多个字段的组合和格式化 |

## 六、结论

**调研结果符合预期**，覆盖了UI设计稿中的所有字段需求，并提供了清晰的技术实现路径。重点关注3个技术实现点：

1. **`startCommand` 字段获取** - 需修改 `Process` 类或绕过封装
2. **`portStatus` 端口健康状态查询** - 新增时序查询逻辑
3. **运行时数据查询性能** - 需性能优化和降级策略

## 七、建议下一步

1. **先实现4个新接口**（面板配置），验证拆分可行性
2. **改造 `getHostProcessList` 接口**，补全CMDB侧字段
3. **新增时序查询逻辑**，获取运行时数据
4. **性能测试和降级方案验证**

---

## 附录：关键代码片段引用

### A. `get_auto_view_panels` 天然拆分点
```python
def get_auto_view_panels(view: SceneViewModel) -> tuple[list[dict], list[dict]]:
    panels = get_panels(view)
    if view.id == "process":
        extend_panels = PROCESS_EXTERNAL_PANELS.copy()
        ...
        panels = extend_panels + panels
    panels, order = sort_panels(panels, get_order_config(view))
    return panels, order
```

### B. `GetHostProcessListResource` 当前返回
```python
return [
    {"status": process["status"], "name": process["name"], "id": process["name"]}
    for process in processes[host.bk_host_id]
]
```

### C. `Process` 类字段限制
```python
# Process.__init__ 仅显式接收以下参数
bk_process_id, bk_process_name, bk_func_name,
service_instance_id, bk_host_id, bind_ip, port, protocol, process_template_id
```