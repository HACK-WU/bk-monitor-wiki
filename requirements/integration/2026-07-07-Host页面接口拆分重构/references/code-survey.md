# 代码调研：Host 页面接口拆分重构

> 调研来源：项目记忆索引 ✓ | 知识库记忆索引 ✓ | 代码搜索 ✓ | 语义检索 ✗
> 调研范围：代码路径、架构模式、类似功能、数据存储、API 约定、错误处理

---

## 1. 代码路径

**核心文件清单**

| 文件路径 | 说明 |
|---------|------|
| `bkmonitor/packages/monitor_web/scene_view/resources/view.py` | `GetSceneViewResource` 实现，Host 场景视图总入口 |
| `bkmonitor/packages/monitor_web/scene_view/resources/host.py` | `GetHostProcessListResource` 实现，进程列表仅返回 3 字段 |
| `bkmonitor/packages/monitor_web/scene_view/builtin/host.py` | `HostBuiltinProcessor` 及 `get_auto_view_panels`、`get_panels`、`get_order_config` |
| `bkmonitor/packages/monitor_web/scene_view/builtin/utils.py` | `sort_panels` 排序分组工具函数 |
| `bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py` | `get_view_config` 分发器，按 `scene_id` 路由到 `BuiltinProcessor` |
| `bkmonitor/packages/monitor_web/scene_view/views.py` | `SceneViewViewSet` 路由注册，含 `get_scene_view`、`get_host_process_list` 等 |
| `bkmonitor/packages/monitor_web/cc/resources/cmdb.py` | `get_process_info` 实现，封装 CMDB 进程查询 |
| `bkmonitor/api/cmdb/define.py` | `Process` 类定义，限制字段透传（无 `_extra_attr` 兜底） |
| `bkmonitor/metadata/models/constants.py` | `system.proc` / `system.proc_port` 维度和指标定义 |
| `bkmonitor/packages/monitor_web/performance/views.py` | `PerformanceViewSet` 参考，含 `search_host_info`、`search_host_metric`、`get_topo_tree` |
| `bkmonitor/packages/monitor_web/performance/resources.py` | 上述接口的 Resource 类实现 |

**来源**：代码搜索 + 知识库记忆索引

---

## 2. 架构模式

**Host 场景视图生成链路**

```
GET /scene_view/get_scene_view/
  ↓
SceneViewViewSet.get_scene_view
  ↓
GetSceneViewResource.perform_request(params)
  ├─ 1. create_default_views(...)    # 自动创建默认视图
  ├─ 2. SceneViewModel.objects.filter(...)  # 查询视图配置
  └─ 3. get_view_config(view, params)
        ↓
        builtin/__init__.py: get_view_config
          ↓ 匹配 HostBuiltinProcessor
          host.py: HostBuiltinProcessor.get_view_config
            ├─ load_builtin_views()          # 读取 host.json / process.json
            ├─ get_auto_view_panels(view)      # 生成 panels + order
            │   ├─ get_panels(view)            # 查 MetricListCache 构建指标面板
            │   ├─ get_order_config(view)      # 取默认/自定义分组排序
            │   └─ sort_panels(...)            # 按 order 分组排序
            └─ 合并为 view_config 返回
```

**关键发现**：`get_auto_view_panels(view)` 已天然按 `view.id`（`"host"` / `"process"`）区分，返回 `(panels, order)` 元组。4 个新接口可直接复用该函数，分别取 `panels` 或 `order`。

**来源**：代码搜索

---

## 3. 类似功能

**已有接口可直接保持兼容**：
- `search_host_info` — `SearchHostInfoResource`（`POST` / `performance/search_host_info/`）
- `search_host_metric` — `SearchHostMetricResource`（`POST` / `performance/search_host_metric/`）
- `get_topo_tree` — `GetTopoTreeResource`（`GET` / `performance/topo_tree/`）

以上 3 个接口不在本次拆分范围，直接保留原路由和参数。

**可参考的模式**：
- `PerformanceViewSet` 使用 `ResourceRoute` 批量注册 Resource → ViewSet 映射，新接口可沿用同一模式在 `SceneViewViewSet` 中追加路由。

**来源**：项目记忆索引 + 代码搜索

---

## 4. 数据存储

### 4.1 CMDB 进程配置数据

**数据源**：`api.cmdb.get_process` → `Process` 对象

**字段限制**：`Process.__init__` 仅显式接收以下参数，无 `_extra_attr` 兜底：
```python
bk_process_id, bk_process_name, bk_func_name,
service_instance_id, bk_host_id, bind_ip, port, protocol, process_template_id
```
原始 CMDB JSON 中的 `start_cmd`、`bk_start_param_regex`、`create_time`、`last_time` 等字段在构造对象后被丢弃。

**可直接补全的字段**：`bind_ip`（已有但未返回）、`port`、`protocol`、`bk_process_name`（映射为 `display_name`）。

### 4.2 运行时性能数据

**数据源**：`system.proc`（时序维度 + 指标）

| 期望字段 | 对应维度/指标 |
|---------|-------------|
| `running_status` | 维度 `state`（R/S/D/Z 等） |
| `pid` | 维度 `pid` |
| `param_regex` | 维度 `param_regex` |
| `cpu_usage` | 指标 `cpu_usage_pct` |
| `mem_usage` | 指标 `mem_usage_pct` |

**查询方式**：需通过时序查询接口（如 `grafana.graphUnifyQuery` 或 `resource.grafana.unify_query`）按 `bk_host_id` + `display_name` 维度筛选最新数据点。

### 4.3 缺失字段

| 字段 | 状态 | 建议 |
|-----|------|------|
| `start_cmdline`（`startCommand`） | CMDB 原始 JSON 有 `start_cmd`，但 `Process` 丢弃 | 需改 `Process.__init__` 增加 `_extra_attr` 或绕过封装 |
| `created_at` | CMDB 原始 JSON 有 `create_time`，但 `Process` 丢弃 | 同上 |

**来源**：代码搜索 + 知识库记忆索引

---

## 5. API 约定

**框架**：Django + BlueKing Resource 框架。

**Resource 类规范**：
- 继承 `Resource` 基类（`bkmonitor/packages/monitor_web/commons/bk_monitor/resource/base.py`）。
- 必须实现 `perform_request(self, params)` 方法。
- 入参校验通过类属性 `RequestSerializer` 实现（Django REST Framework Serializers）。
- 返回标准 dict，由框架统一包装为 JSON 响应。

**路由注册规范**：
```python
class SceneViewViewSet(ResourceViewSet):
    resource_routes = [
        ResourceRoute("GET", resource.scene_view.get_scene_view, endpoint="get_scene_view"),
        ResourceRoute("GET", resource.scene_view.get_host_process_list, endpoint="get_host_process_list"),
        # ...
    ]
```
- `endpoint` 对应 URL path 最后一段。
- 新接口若为 `GET` 且参数简单，可沿用 `"GET"`；若参数复杂建议用 `"POST"`。

**错误响应**：Resource 框架自动捕获异常并包装为统一错误格式，无需手动处理 HTTP status。

**来源**：项目记忆索引（Resource 框架使用小技巧、APIResource 扩展模式）+ 代码搜索

---

## 6. 错误处理

**当前 `GetHostProcessListResource` 的错误模式**：
- 依赖 `resource.cc.get_process_info`，若 CMDB 查询失败会抛出 `ApiResultError`。
- 无显式重试逻辑，由调用方（Resource 框架中间件）统一处理。
- 新增实时查询 `system.proc` 后，需考虑时序数据源查询失败时的降级策略（如字段留空 / 返回 `"--"`）。

**来源**：代码搜索

---

## 7. 补充：关键代码片段

### 7.1 `get_process_info` 当前裁剪逻辑（cmdb.py L177-184）
```python
pp_instance = {
    "bk_host_id": pp.bk_host_id,
    "name": pp.bk_process_name,
    "protocol": pp.protocol,
    "ports": ports,
    "status": status,
}
```

### 7.2 `GetHostProcessListResource` 当前返回（host.py L488-491）
```python
return [
    {"status": process["status"], "name": process["name"], "id": process["name"]}
    for process in processes[host.bk_host_id]
]
```

### 7.3 `HostBuiltinProcessor.get_view_config`（builtin/host.py L337-347）
```python
class HostBuiltinProcessor(BuiltinProcessor):
    @classmethod
    def get_view_config(cls, view: SceneViewModel, *args, **kwargs) -> dict:
        cls.load_builtin_views()
        if view.id not in ["host", "process"]:
            raise TypeError(f"host scene don't have view({view.id})")
        view_config = json.loads(json.dumps(cls.builtin_views[view.id]))
        view_config["panels"], view_config["order"] = get_auto_view_panels(view)
        return view_config
```

### 7.4 `get_auto_view_panels` 天然拆分点（builtin/host.py L275-287）
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

**来源**：代码搜索

---

## 8. 边界注意

1. **`portStatus` 非现有 `status`**：后端 `get_process_info` 已返回进程运行状态 `status`（ON/OFF/UNKNOWN），但前端 Wiki 中的 `portStatus`（0=Normal, 1=Abnormal）是**端口健康状态**，需额外查询 `system.proc_port` 的 `port_health` 指标。两者语义不同。
2. **`startCommand` 需改 CMDB `Process` 类**：原始 CMDB JSON 包含 `start_cmd`，但 `Process.__init__` 无 `_extra_attr` 兜底，构造对象后丢弃。需调整 `Process` 类或绕过封装才能获取。

---

## 调研结论

1. **4 个新接口实现成本低**：`get_auto_view_panels` 已按 `host` / `process` 区分并返回 `(panels, order)`，只需封装 4 个新 Resource 类分别取对应字段。
2. **进程列表字段补全路径清晰**：
   - **CMDB 侧直接补全（无需额外查询）**：`bindIp`→`pp.bind_ip`、`protocol`→`pp.protocol`、`port`→`ports[0]`、`startCommand`→`pp.start_cmd`（需改 `Process` 类保留 `_extra_attr` 或绕过封装）。
   - **`system.proc` 实时查询（新增时序查询逻辑）**：`pid`、`cpuUsage`、`memRss`、`memUsage`、`uptime`、`user`。按 `bk_host_id` + `display_name` 维度查最新时序数据点。
   - **`system.proc_port` 查询（新增）**：`portStatus`（端口健康状态，0/1），区别于当前进程运行状态 `status`（ON/OFF）。
   - **`hostIp` 与 `id`**：`hostIp` 直接取主机 IP；`id` 延续当前做法（进程名），前端自行拼接为 `name@hostIp`。
3. **建议路由归属**：新接口统一挂在 `SceneViewViewSet` 下，保持与 `get_scene_view`、`get_host_process_list` 同模块。
