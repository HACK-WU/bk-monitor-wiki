---
groupPath: 关联关系/告警屏蔽
relation: shield_tasks-Shield模型-AlertDocument
exportedAt: "2026-09-15T01:48:14.173Z"
---
[强关联] 屏蔽结束关闭任务 与 Shield 模型 / AlertDocument
强度：必改——改 Shield 模型的 end_policy / is_enabled / is_deleted 语义或 close 屏蔽的时间字段（cycle_config / begin_time / end_time），关闭任务的判活逻辑必须连带改；改 AlertDocument.shield_end_close 字段或 alert.extra_info.shield_end_close_config 结构，扫描条件与归属解析必须连带改
原因：关闭任务按 shield_end_close 扫描 ES、从 extra_info.shield_end_close_config.shield_id 取归属、用 Shield.origin_objects 读 DB 实时判活，三处结构任一处变更都会断链

任务侧：
- check_shield_end_close_alert / shield_is_active / check_shield_end_close_finished @ alarm_backends/service/alert/manager/shield_tasks.py
- 任务注册 @ bkmonitor/config/role/worker.py（每分钟 cluster 任务）

模型侧：
- Shield（end_policy / cycle_config / begin_time / end_time / is_enabled / is_deleted）@ bkmonitor/models/base.py
- 迁移 @ bkmonitor/migrations/0205_shield_end_policy.py

文档侧：
- AlertDocument.shield_end_close（Boolean）@ bkmonitor/documents/alert.py
- alert.extra_info.shield_end_close_config（shield_id / window_begin / window_end）由接管侧写入 @ close.py

落盘侧：
- AlertDocument.bulk_create（UPSERT）+ AlertCache.update_alert_to_cache / save_alert_snapshot + AlertLog.bulk_create @ shield_tasks.py