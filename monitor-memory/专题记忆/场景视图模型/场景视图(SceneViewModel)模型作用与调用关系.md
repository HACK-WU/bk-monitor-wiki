---
groupPath: 专题记忆/场景视图模型
relation: 场景视图(SceneViewModel)模型作用与调用关系
keywords: [SceneViewModel, SceneModel, SceneViewOrderModel, BuiltinProcessor, get_view_config, scene_view, overview, detail, panels, variables, UpdateSceneViewResource, create_or_update_view, BulkUpdateSceneViewOrderAndNameResource, GetSceneViewListResource, get_panel_count, get_view_list, GetSceneResource, BUILTIN_SCENES, view_configs, _read_builtin_view_config, load_builtin_views]
exportedAt: "2026-07-10T08:49:30.002Z"
---
## SceneViewModel 模型作用

- 路径：`bkmonitor/packages/monitor_web/models/scene_view.py` (line 36)
- 是监控平台「场景视图（监控大盘）」的持久化配置单元，对应数据库表
- 唯一约束 `unique_together = (bk_biz_id, scene_id, type, id)`

### 字段含义
- `scene_id`：场景分类，如 host / kubernetes / uptime_check
- `type`：overview（概览）/ detail（详情）两层
- `id`：视图ID，如 host / process / cluster
- `variables`：前端模板变量（$bk_host_id、$bcs_cluster_id 等），详情页定位目标对象
- `mode`：auto（平铺分组）/ custom（自定义）
- `order`：平铺模式下面板分组与排序配置
- `panels`：Grafana 风格图表配置（targets / query_configs，决定查哪张表、哪个指标）
- `list`：overview 类型的列表页配置
- `options`：其他开关（show_panel_count、selector_panel 等）

## 与其它模型的关系

```
SceneModel（场景，如"主机监控"）
   └── SceneViewModel（场景下的视图，如 host 概览页 / host 详情页 / process 详情页）
         └── SceneViewOrderModel（该场景某类型下所有视图的排序列表）
```
- SceneModel：管"有哪些场景"
- SceneViewModel：管"每个场景里具体有哪几张页、每页怎么画"
- SceneViewOrderModel：管"这些页怎么排顺序"

## 调用关系（谁用它）

### 1. 内置场景默认视图由 Processor 灌入此表
- 路径：`bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`
- `BUILTIN_SCENES` 注册内置场景；各 `BuiltinProcessor` 读取内置 JSON 配置，`bulk_create` 成 SceneViewModel（首次访问惰性创建，`create_default_views`）
- `get_view_config(view)` 通过 processor 把 SceneViewModel 对象转成前端渲染的 panels（注入查询参数、维度 where 条件）
- 示例 processor：`builtin/kubernetes.py` 的 `KubernetesBuiltinProcessor`

### 2. scene_view 系列 Resource 提供 CRUD/查询
- 路径：`bkmonitor/packages/monitor_web/scene_view/resources/view.py`
- `GetSceneViewListResource`：列出场景下的视图（`SceneViewModel.objects.filter`），按 `SceneViewOrderModel.config` 排序
- `GetSceneViewResource`：取单个视图完整配置
- `UpdateSceneViewResource` / `DeleteSceneViewResource` / `BulkUpdateSceneViewOrderAndNameResource`：用户前端增删改视图，直接读写此表
- `GetSceneViewDimensionsResource` / `GetSceneViewDimensionValueResource`：解析视图 panels 的 query_configs 取出 result_table_id / metrics，再查 `MetricListCache` 得可用维度和维度候选值

### 3. 模型自带 update_order 方法
- 路径：`scene_view.py` (line 70)
- 用 `atomic` + `select_for_update`，把当前视图插到 `SceneViewOrderModel.config` 指定位置，实现拖拽排序

### 4. UpdateSceneViewResource 更新/落库逻辑（补充）
- 路径：`bkmonitor/packages/monitor_web/scene_view/resources/view.py` (line 357-408)
- 名义"更新场景视图配置"，实际既能更新也能创建（因 `id` 可选）
- 两段式执行：
  1. 排序表更新(view.py:386-395)：仅当请求带非空 `view_order` 时，`SceneViewOrderModel.objects.get_or_create` 后整体覆盖 `config` 为视图ID顺序数组（全量覆盖，非 `update_order` 的增量挪位）
  2. 确定视图ID(view.py:397)：有 `id` 则更新已有视图，无则生成 `custom_{SceneViewModel.objects.count()}` 走新建
  3. 落库 SceneViewModel(view.py:400)：调用 `create_or_update_view`(builtin/__init__.py:291) 按 `scene_id` 路由到对应 BuiltinProcessor
- 各 processor 落库差异（host 与 alert/apm 同模式，未展开 host.py）：
  - alert / apm：`get()` 已存在视图，仅回写 `order` 字段后 save 返回 view
  - kubernetes：同上，但写 `order` 前剥掉重复前缀 `bk_monitor.time_series.k8s.{id}.`
  - collect：有则更新 name/variables/options/order，无则 `create`
  - custom_metric_v2：`update_or_create` 写 name/mode/options
  - uptime_check：直接 `return None`（不落库）
- 注意点：
  - 排序写入两套路径并存：`UpdateSceneViewResource`(全量数组覆盖) vs `SceneViewModel.update_order()`(scene_view.py:70 单视图增量挪位)，不可混用
  - 多数 processor 只回写 `order`，即便前端传 panels/variables/options 也不处理
  - 接口支持无 id 新建，但 host/alert/apm/kubernetes 用 `.objects.get`，视图不存在会抛 DoesNotExist；真正能新建的仅 collect / custom_metric_v2

### 5. GetSceneViewListResource 查询/排序/字段映射（补充）
- 路径：`bkmonitor/packages/monitor_web/scene_view/resources/view.py` (line 114-199)
- 作用：列出某业务 + 场景 + 类型(overview/detail)下的所有视图元信息，按 `SceneViewOrderModel` 排序返回，不渲染图表
- 执行流程(get_view_list, line 114-187)：
  1. 查库：`SceneViewModel.objects.filter(bk_biz_id, scene_id, type)` (line 119)
  2. 惰性补齐内置视图：`create_default_views(...)` (line 122) 首次访问灌入，再重查 (line 125)
  3. 组装列表：非 kubernetes 优先用 `list_processors_view`(processor 自定义列表)否则 DB views，逐视图 `get_view_config(only_simple_info=True)`，跳过 `hidden` (line 135-141)；kubernetes 单独分支只取 mode，不计算 panel_count，show_panel_count 硬编码 False (line 152-170)
  4. 排序：查 `SceneViewOrderModel.config`，按视图ID顺序排 result(不在顺序里的排最后)；processor 自定义排序走 `sort_view_list` (line 172-185)
- perform_request (line 189)：scene_id != kubernetes 且不传 type 时，自动拼接 overview + detail 两列表返回；传 type 只返回该类型
- 返回字段映射：
  - id：`view.id`
  - name：`_(view.name)` 国际化
  - show_panel_count：`view_config.options.show_panel_count`(默认 False)
  - mode：`view_config.mode`(默认 "")
  - type：请求参数 scene_type (overview/detail)
  - panel_count：`get_panel_count(view_config)` 递归统计 panels，排除 row 容器和 tag-chart (line 100-112)
- 视图类型两层含义：① `type` 维度 overview/detail 两层；② 同类型下按 id 区分(host/process/cluster 等)

### 6. GetSceneResource 作用 + SceneModel 写入点（补充）
- GetSceneResource 路径：`bkmonitor/packages/monitor_web/scene_view/resources/view.py` (line 62-80)
- 作用：返回场景分类列表，结果 = 内置场景(BUILTIN_SCENES 常量, builtin=True) + 用户自定义场景(SceneModel 表, builtin=False) 拼接；前端据此渲染左侧场景导航
- 内置场景不入表，直接来自 `builtin/__init__.py` 的 `BUILTIN_SCENES` 字典；用户场景来自 SceneModel 查询
- SceneModel 模型定义：`monitor_web/models/scene_view.py` (line 19)，字段 unique_id/bk_biz_id/id/name/data_range/view_order，唯一约束 (bk_biz_id, id)
- SceneModel 写入点（全仓库搜索结论）：代码中**无常规业务创建接口**，仅有：
  1. data_migrate 导入工具：`data_migrate/data_import.py` 删除后由 `data_migrate/fetcher/query.py` 从导出文件写入；`constants.py` 列入迁出模型
  2. DeleteSceneViewResource 删视图时更新 `scene.view_order` 后 save (view.py:438-440)——更新已有记录，非新建
  3. migrations/0054_auto_20210928_1124.py 建表
- 结论：用户自定义场景的 SceneModel 记录在代码内无创建入口，主要靠数据迁移导入；内置场景完全不进 SceneModel
- 注：场景的 type(overview/detail) 是场景之下的视图分层，与 GetSceneResource 的场景是上下级关系

### 7. 内置 JSON 配置存储位置与加载机制（补充）
- **存储位置（代码包内置，部署即随包发布）**：
  - 绝对路径：`/root/bk-monitor/bkmonitor/packages/monitor_web/scene_view/builtin/view_configs/`（仓库根下）
  - 相对路径：`bkmonitor/packages/monitor_web/scene_view/builtin/view_configs/`
  - 共 44 个 json 文件，跟随代码仓库提交与版本发布；不进数据库、不随业务运行态变化（内置视图的"源数据"）
- **运行时库表镜像**：首次访问某场景时，`create_default_views` 把这些 JSON `bulk_create` 进 `SceneViewModel` 表；真正被接口读取的是库表记录，而非这个目录文件（JSON 是源、库表是运行时副本）
- 加载机制：`BuiltinProcessor._read_builtin_view_config` (builtin/__init__.py:61) 读取 `{view_config_path}/{filename}.json`；`view_config_path` = builtin 目录下的 view_configs 子目录
- 各 `BuiltinProcessor` 通过 `filenames` 类属性声明加载哪些 JSON；`NormalProcessorMixin.load_builtin_views` (builtin/__init__.py:172) 遍历 filenames 读入 `cls.builtin_views`
- 文件命名约定：`{scene_id}-{view_id}.json`（如 kubernetes-cluster.json、apm_service-service-default-overview.json）；也有无前缀的（host.json、process.json、uptime_check_task_detail.json），由各 processor 的 filenames 直接指定
- 这些 JSON 是 SceneViewModel 的默认 `panels`/`variables`/`order`/`options` 配置源；首次访问场景时由 `create_default_views` 惰性 `bulk_create` 进表；`create_default_order` 同理基于内置视图生成默认排序
- `create_default_views` 用 `v.split("-", 1)[-1]` 取 view_id 匹配场景
- 现有文件按场景分组：host(host.json/process.json)、kubernetes(9 个 kubernetes-*.json)、uptime_check(uptime_check_task_detail.json)、alert(alert-log.json)、apm(30+ 个 apm_*)

## 一句话
SceneViewModel = 一个业务 + 场景 + 概览/详情 + 视图ID 对应的可持久化监控大盘配置。内置场景由 Processor 用默认 JSON 初始化，用户自定义视图也存这里，前端通过 scene_view 接口读它渲染 Grafana 风格图表。