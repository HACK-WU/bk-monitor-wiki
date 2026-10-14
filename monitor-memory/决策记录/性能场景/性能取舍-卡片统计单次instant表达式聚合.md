---
groupPath: 决策记录/性能场景
relation: 性能取舍-卡片统计单次instant表达式聚合
exportedAt: "2026-09-22T08:22:27.542Z"
---
【决策记录】
- 分类：性能取舍
- 动机：优化
- 决策：build_host_stats_query 构造两个数据源（a 按 bk_host_id 白名单、b 按 bk_target_ip 与 bk_target_cloud_id targets），拼成一个多数据源表达式，一次 instant 查询（180 秒窗口）同时算出 value、id_count、ip_count、duplicates；不按主机展开查询分支，不做 per-host 查询；三张卡各自独立失败与重试
- 背景约束：卡片在页级阶段就要展示，不能等全量；页级卡片必须与列表共用时间锚点、设备过滤与 180 秒窗口
- 被否决方案：无
- 重新评估触发条件：单业务身份数使表达式或白名单体积成为瓶颈；或需要新增卡片类别
- 关联代码：build_host_stats_query @ bkmonitor/packages/monitor_web/performance/host_metric_stats.py:17；query_host_metric_stats @ host_metric_stats.py:67
- 证据来源：代码注释（host_metric_stats.py:18：白名单只随身份数增长，表达式不为每台主机展开一个查询分支）；PR 描述（每张卡使用一次 instant UQ 查询，沿用现有阈值、舍入和设备过滤）