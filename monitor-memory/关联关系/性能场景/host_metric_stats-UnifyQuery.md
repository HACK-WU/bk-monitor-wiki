---
groupPath: 关联关系/性能场景
relation: host_metric_stats-UnifyQuery
exportedAt: "2026-09-22T08:22:27.541Z"
---
[强关联] performance.host_metric_stats 与 bkmonitor.data_source.UnifyQuery
强度：必改——改统计表达式依赖的 UQ 行为（instant 语义、多数据源表达式解析、is_partial 判定、返回记录结构）会让卡片统计的数值与完整性判断失真；改统计表达式结构，测试需同步更新

原因：统计是多数据源表达式必走 UQ 的单次 instant 查询，表达式用 or 拼接四个 label_replace 子表达式，一次取回 value、id_count、ip_count、duplicates

统计端：
- build_host_stats_query（a 按 bk_host_id、b 按 bk_target_ip 与 bk_target_cloud_id 组表达式、阈值 79.995）@ bkmonitor/packages/monitor_web/performance/host_metric_stats.py:17
- query_host_metric_stats（180 秒窗口、is_partial、非有限值、字段集合校验、身份歧义）@ host_metric_stats.py:67

UQ 端：
- UnifyQuery.query_data（instant 语义、query_output_config）@ bkmonitor/bkmonitor/data_source/unify_query/query.py
- 统一查询后端接口契约（success、is_partial、series 结构）