---
groupPath: 专题记忆/场景视图
relation: BuiltinProcessor处理器与分发机制
exportedAt: "2026-08-13T11:53:38.885Z"
---
BuiltinProcessor 是场景视图模块的内置场景处理器抽象基类，采用模板方法+注册表分发模式，按 scene_id 路由到 10 种子处理器。NormalProcessorMixin 提供从 JSON 文件加载内置视图并做差异同步的默认实现。

- 符号: `BuiltinProcessor`、`NormalProcessorMixin`、`get_builtin_processors`、`get_view_config`、`create_default_views`、`is_builtin_scene`
- 位置: `bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`

抽象契约（4 个 abstractmethod）:
- create_default_views: 补齐默认视图（JSON 骨架↔DB 双向同步）
- create_or_update_view: 创建或更新单个视图
- get_view_config: 生成视图配置（panels/order/variables/options）
- is_builtin_scene: 判断是否属于该处理器

可选钩子方法:
- handle_view_config: 视图配置后处理
- is_custom_view_list: 是否使用自定义列表逻辑
- is_custom_sort: 是否使用自定义排序

NormalProcessorMixin.create_default_views 双向同步逻辑:
- 加载: load_builtin_views 读 view_configs/{filename}.json + _translate_config 递归国际化
- 补建: builtin_view_ids - existed_view_ids → bulk_create
- 删除: existed_view_ids - builtin_view_ids → delete（⚠️ 高风险：JSON 骨架临时缺失会物理删除 DB 视图行）
- 排序: create_default_order 补齐默认排序

分发函数:
- get_view_config(view, params): 遍历 get_builtin_processors()，命中 is_builtin_scene(view.scene_id) 的第一个 Processor，调用其 get_view_config（先 convert_custom_params 转参）
- create_default_views(scene_id, bk_biz_id, scene_type): 遍历 Processor 列表，命中者执行 create_default_views
- 未命中则 raise TypeError('not scene processor')

10 种内置场景处理器:
- host（主机）、kubernetes（K8s）、uptime_check（拨测）、apm（APM）、alert（告警）、custom_metric（自定义指标）、custom_event（自定义事件）、observation_scene（观测场景）、collect（采集）、custom_metric_v2（自定义指标v2）