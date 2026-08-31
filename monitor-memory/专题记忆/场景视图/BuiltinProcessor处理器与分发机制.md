---
groupPath: 专题记忆/场景视图
relation: BuiltinProcessor处理器与分发机制
exportedAt: "2026-08-31T01:55:17.334Z"
---
BuiltinProcessor 是场景视图模块的内置场景处理器抽象基类，采用模板方法+注册表分发模式，按 scene_id 路由到 10 种子处理器。NormalProcessorMixin 提供从 JSON 文件加载内置视图并做差异同步的默认实现。

- 符号: `BuiltinProcessor`、`NormalProcessorMixin`、`get_builtin_processors`、`get_view_config`、`create_default_views`、`is_builtin_scene`
- 位置: bkmonitor/packages/monitor_web/scene_view/builtin/

抽象契约（4 个 abstractmethod）:
- create_default_views: 补齐默认视图（JSON 骨架↔DB 同步）
- create_or_update_view: 创建或更新单个视图
- get_view_config: 生成视图配置（panels/order/variables/options）
- is_builtin_scene: 判断是否属于该处理器

可选钩子方法:
- handle_view_config: 视图配置后处理
- is_custom_view_list: 是否使用自定义列表逻辑
- is_custom_sort: 是否使用自定义排序

NormalProcessorMixin.create_default_views 同步逻辑（默认实现，仅 alert 场景走此 Mixin）:
- 加载: load_builtin_views 读 view_configs/{filename}.json + _translate_config 递归国际化
- 补建: builtin_view_ids - existed_view_ids → bulk_create
- 删除: existed_view_ids - builtin_view_ids → delete（⚠️ 高风险：JSON 骨架临时缺失会物理删除 DB 视图行）
- 排序: create_default_order 补齐默认排序

分发函数:
- get_view_config(view, params): 遍历 get_builtin_processors()，命中 is_builtin_scene(view.scene_id) 的第一个 Processor，调用其 get_view_config（先 convert_custom_params 转参）

同步策略因 Processor 而异（2026-08-31 核对修正，此前误将差集删除视为统一机制）:
- 双向差集（新增+删除，有物理删除风险）: NormalProcessorMixin（alert 场景）、HostBuiltinProcessor（仅 view_type=detail 才执行，overview 直接 return）、KubernetesBuiltinProcessor、ApmBuiltinProcessor（删除只按 bk_biz_id+scene_id 过滤，未按 type 收敛，删除面更宽）
- 仅首次补齐、已有视图即跳过（从不删除）: CollectBuiltinProcessor 及子类 custom_event/custom_metric/observation_scene、UptimeCheckBuiltinProcessor
- 完全不建默认视图: CustomMetricV2BuiltinProcessor（默认视图为自由视图，方法直接 return）
- 判据: 改 collect/uptime_check 的 JSON 骨架不会触发删除；改 alert/host(detail)/kubernetes/apm 的 JSON 骨架才会
- 详见 .module-experts/场景视图专家/C5-关键决策.md 决策 1