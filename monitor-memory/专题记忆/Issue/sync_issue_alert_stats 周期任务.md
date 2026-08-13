---
groupPath: 专题记忆/Issue
relation: sync_issue_alert_stats 周期任务
exportedAt: "2026-08-13T08:53:43.399Z"
---
sync_issue_alert_stats 是 Celery 周期任务入口，扫描全量活跃 Issue 同步统计与补偿漏关联告警。队列 celery_action_cron，ignore_result=True。包含告警统计同步、漏关联补偿、影响范围重算、orphan 检测、Legacy 续命五大职责。

## 关键符号
- 符号: `sync_issue_alert_stats()`
- 位置: `alarm_backends/service/fta_action/tasks/issue_tasks.py`
- 队列: `celery_action_cron`
- 异常: 单条 Issue 处理失败仅记日志并计数，不影响同批次其他 Issue

## 五大职责
1. 告警统计同步: 更新每条活跃 Issue 的 alert_count 和 last_alert_time
2. 漏关联补偿: 回填 AlertDocument.issue_id 未写入的告警（backfill 优化 O(N×M)→O(N+M)，策略级去重）
3. 影响范围重算: 基于关联告警重新汇总 impact_scope
4. orphan Issue 检测: 无关联告警的孤立 Issue（5 分钟后告警）
5. Legacy 哨兵续命: 防止 30 天 TTL 失效（fingerprint=null 的 Issue 被跳过）

## 影响范围维度
| 维度 | 数据来源 | ID 字段 |
| set | bk_topo_node | set_id |
| host | bk_host_id / ip | bk_host_id |
| service_instances | bk_service_instance_id | bk_service_instance_id |
| cluster/node/service/pod | bcs_cluster_id + target_type | — |
| apm_app/apm_service | app_name + service_name | — |

## backfill 优化
- 旧实现: O(N×M)，每条 Issue 扫一遍同策略 unlinked alerts
- 新实现: O(N+M)，一次 scan Issue + 一次 scan alerts + 内存分组匹配
- 每个策略在一个周期内只做一次批量 backfill

## 测试缺口
- 无直接单测，影响范围重算/孤立检测/backfill 路径未覆盖