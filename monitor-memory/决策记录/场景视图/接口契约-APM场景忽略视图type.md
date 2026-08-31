---
groupPath: 决策记录/场景视图
relation: 接口契约-APM场景忽略视图type
exportedAt: "2026-08-31T01:50:02.299Z"
---
【决策记录｜场景视图中 APM 场景不区分视图 type（overview/detail）】
- 分类：接口契约
- 动机：一致性（APM 视图集合按应用、服务、组件维度组织，无 overview/detail 分层）
- 决策：validate_scene_type 对 apm_application、apm_service、kubernetes、alert 场景把 type 强制置空；ApmBuiltinProcessor.get_view_config 不读 view.type，改由 params 中的 app_name 与 service_name 判断视图形态
- 背景约束：这些场景的 view_id 自带层级语义（如 apm_service-service-default-overview），无需再用 type 字段区分
- 被否决方案：无（未找到相关记录）
- 已知代价：调用方传入 type 会被静默忽略
- 重新评估触发条件：APM、K8s、alert 场景引入 overview/detail 分层视图
- 关联代码：validate_scene_type @ scene_view/resources/view.py；ApmBuiltinProcessor.get_view_config @ scene_view/builtin/apm.py
- 证据来源：代码注释（apm.py get_view_config docstring：APM 下不需要区分视图的 type 类型 overview/detail）
- 完整上下文：.module-experts/场景视图专家/C5-关键决策.md 决策 9