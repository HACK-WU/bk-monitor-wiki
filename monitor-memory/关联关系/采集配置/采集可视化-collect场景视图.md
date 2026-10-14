---
groupPath: 关联关系/采集配置
relation: 采集可视化-collect场景视图
exportedAt: "2026-10-13T10:18:01.998Z"
---
[强关联] 采集可视化页 与 场景视图 collect 场景
强度：必改——改 sceneId 命名约定（collect_<id>）或场景视图 collect_* 场景的视图配置契约，采集可视化页必须连带改；改采集可视化页的容器使用，场景视图侧需核对（后端 CollectBuiltinProcessor 按 collect_* 场景精确计数）
原因：可视化页以 sceneId=collect_<id> 打开场景视图框架（monitor-k8s CommonPage），后端场景视图侧有 CollectBuiltinProcessor 专门处理 collect_* 与 plugin_* 场景的视图配置；两端通过 scene_id 命名与视图配置契约耦合

场景视图端：
- CollectBuiltinProcessor（get_view_config / get_simple_panel_count，collect_* 场景）@ bkmonitor/packages/monitor_web/scene_view/builtin/collect.py（详见 .module-experts/场景视图专家/）

采集端：
- collector-view.tsx（sceneId / viewOptions）@ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-view-detail/