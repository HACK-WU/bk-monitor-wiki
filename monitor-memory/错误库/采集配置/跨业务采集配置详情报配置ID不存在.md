---
groupPath: 错误库/采集配置
relation: 跨业务采集配置详情报配置ID不存在
exportedAt: "2026-10-12T10:11:13.329Z"
---
【错误库｜跨业务采集配置详情报配置ID不存在】
- 报错原文片段：CollectConfigNotExist，code 3311003，message「采集配置ID不存在：1538」；接口 GET rest/v2/collecting_config/frontend_config_detail/?id=1538&bk_biz_id=2；HTTP 200 + result false（error_details.code=3311003、type=CollectConfigNotExist、popupMessage=warning）
- 现象：业务 2 列表能看到归属业务 75 的采集配置（实测 id=1538，space_name=光谱(业务)，Script 采集，plugin_id=guangpu_airflow_mainprocess），点名称进详情报「采集配置ID不存在」；同一行「升级」标签可点，但升级页数据加载失败、底部按钮不出现；同页编辑/更新目标/更多按钮因有跨业务守卫而不显示
- 根因：列表与详情的业务可见性口径不一致。列表 = 本业务 ∪ 全局插件(bk_biz_id=0)配置：monitor_web/collecting/resources/backend.py:334 过滤 Q(plugin_id__in=plugin_ids) OR Q(bk_biz_id__in=user_biz_ids)，其中 plugin_ids 只由全局插件 ∩ 当前业务空间平台数据源算出，plugin_id 支按插件放行全部归属业务的配置，既不校验配置归属业务、也不校验用户对配置所属业务的权限；详情与写接口 = 严格 get(id=..., bk_biz_id=当前业务)（backend.py:478-483），跨业务必然 3311003。前端守卫只覆盖列表操作列 3 个入口（collector-config.vue:250/276/287），名称点击跳详情（182）与升级标签（185-192）无守卫；独立详情页 6 个写入口 0 个有跨业务守卫（侧栏有）。升级页首个请求 CollectRunningStatusResource 严格按 (id, bk_biz_id) 查且未捕获异常（collecting/resources/status.py:38-56），失败后按钮 v-show=tables 不出现
- 解法（修复方向，未实施）：语义二选一——A 收窄列表口径为 Q(bk_biz_id=当前) OR Q(bk_biz_id=0)（联动 exists_by_biz，backend.py:241-259）；B 详情放开跨业务读取并按配置真实归属业务做权限校验（连带 frontend_target_info、storage_status、alert_status 等读接口）。止血项：升级标签与名称点击补 v-if="scope.row.bizId === bizId"（collector-config.vue:185-192、182）；列表「所属」列默认展示（534）
- 验证方式：python manage.py shell 查 CollectConfigMeta.objects.filter(id=1538).values('id','bk_biz_id','plugin_id') 确认真实归属；用仅授权业务 2 的账号搜 1538 复现「列表可见、详情报错」；修复后断言列表可见条目均能打开详情、且跨业务写入口不可用
- 关联方案：无。完整分析报告 .pm/collecting-config-cross-biz-20261012.md（含方案对比、影响面、待确认清单）