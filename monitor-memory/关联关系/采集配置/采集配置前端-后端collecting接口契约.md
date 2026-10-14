---
groupPath: 关联关系/采集配置
relation: 采集配置前端-后端collecting接口契约
exportedAt: "2026-10-13T10:18:01.997Z"
---
[强关联] 采集配置前端（monitor-pc）与 后端 collecting 接口契约
强度：必改——改后端 rest/v2/collecting_config/* 的字段名/返回结构/语义（config_list 字段、type_list 结构、is_task_ready 就绪语义、refresh_status 刷新行为），前端 TableStore 字段映射与相关页面必须连带改；改前端页面内部实现，后端不用管
原因：前端 33 个接口调用与列表行模型（snake_case→camelCase）全部依赖后端契约；已有两个真实事故佐证：跨业务详情报 CollectConfigNotExist（3311003，列表口径与详情校验不一致）、改名跨业务静默假成功（filter 0 行不报错）

后端端：
- collecting_config 系列（config_list/save/toggle/upgrade/rollback/is_task_ready/status 等）@ bkmonitor/packages/monitor_web/collecting/（列表口径 = 本业务 ∪ 全局插件配置；详情/写接口严格按 (id, biz_id)）

前端端：
- TableStore（字段映射唯一入口）@ bkmonitor/webpack/src/monitor-pc/pages/collector-config/store.ts
- 33 个接口定义 @ bkmonitor/webpack/src/monitor-api/modules/collecting.js
- 页面调用点 @ bkmonitor/webpack/src/monitor-pc/pages/collector-config/（collector-config.vue / collector-detail / config-delivery 等）