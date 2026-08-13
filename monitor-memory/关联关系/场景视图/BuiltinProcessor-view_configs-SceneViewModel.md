---
groupPath: 关联关系/场景视图
relation: BuiltinProcessor-view_configs-SceneViewModel
exportedAt: "2026-08-13T11:54:27.102Z"
---
[强关联] BuiltinProcessor 处理器 与 view_configs/*.json 骨架/SceneViewModel 模型
强度：必改——改 view_configs/*.json 文件名或内容时，对应 Processor 的 filenames 列表与 get_view_config 必须跟着改；改 SceneViewModel 字段定义，序列化器和 Processor 都要适配
原因：NormalProcessorMixin.create_default_views 以 filenames 声明的 JSON 骨架为准做 DB 双向同步（补建+删除），JSON 文件名与内容变更直接级联影响 DB 视图行；get_view_config 读 JSON + _translate_config 递归国际化后输出

源端（处理器+同步逻辑）:
- `NormalProcessorMixin.create_default_views` @ `bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`（bulk_create 补建 + delete 删除多余）
- `NormalProcessorMixin.load_builtin_views` @ `bkmonitor/packages/monitor_web/scene_view/builtin/__init__.py`（读 JSON + _translate_config 递归国际化）
- 10 种 Processor 子类（host/kubernetes/uptime_check/apm/alert/custom_metric/custom_event/observation_scene/collect/custom_metric_v2）

目标端（JSON 骨架+模型）:
- `view_configs/*.json` @ `bkmonitor/packages/monitor_web/scene_view/builtin/view_configs/`（47 个内置视图骨架）
- `SceneViewModel` @ `bkmonitor/packages/monitor_web/models/scene_view.py`（bk_biz_id/scene_id/id/type/mode/variables/panels/order/options JSON 字段）
- 风险：JSON 骨架临时缺失会触发 existed_view_ids - builtin_view_ids 的差集删除，物理删除 DB 视图行