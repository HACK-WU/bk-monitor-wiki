---
groupPath: 数据流/告警屏蔽
relation: Shield模型
exportedAt: "2026-09-15T01:51:10.486Z"
---
【数据流｜Shield 模型（表 alarm_shield）】
- 实体类型：表（MySQL alarm_shield）
- 结构：bk_biz_id / category / scope_type / dimension_config(JSON) / cycle_config(JSON) / end_policy / begin_time / end_time / failure_time / is_enabled / is_quick / is_deleted / content / label（字段细节见 04-模型.md）
- 生产方：AddShieldResource / EditShieldResource / DisableShieldResource / BulkAddAlertShieldResource @ packages/monitor_web/shield/resources/backend_resources.py；UpdateFailureShieldContentResource 补写 content @ shield/resources/celery_resources.py
- 主要消费方：ShieldCacheManager.refresh（全量读入 Redis）@ alarm_backends/core/cache/shield.py；check_and_send_shield_notice（筛选待通知屏蔽）@ converge/shield/tasks.py；shield_is_active（关闭任务直读判活，用 Shield.origin_objects 含软删除记录）@ alert/manager/shield_tasks.py
- 业务用途：屏蔽配置的唯一持久化载体，Web 管理面写、告警引擎面读
- 详细流向：见 .module-experts/告警屏蔽专家/implementation/03-数据流转.md