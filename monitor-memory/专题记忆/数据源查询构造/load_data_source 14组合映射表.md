---
groupPath: 专题记忆/数据源查询构造
relation: load_data_source 14组合映射表
exportedAt: "2026-08-13T12:00:36.682Z"
---
load_data_source 在 data_source/__init__.py 中维护内部字典，key 为 (data_source_label, data_type_label) 元组，value 为对应 DataSource 子类。模块加载时完成注册，共 14 个组合，覆盖 6 大数据来源和 4 种数据类型。

- 符号: `load_data_source`、`DataSourceLabel`、`DataTypeLabel`、`DataSource`、`BkMonitorTimeSeriesDataSource`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`、`bkmonitor/constants/data_source.py`

6 大数据来源:
- bk_monitor（监控采集）、custom（自定义）、bk_data（计算平台）、bk_log_search（日志平台）、bk_apm（APM）、bk_fta（第三方告警）、prometheus（Prometheus直查）

4 种数据类型:
- time_series（时序指标）、log（日志）、event（事件）、alert（告警）

14 个注册组合完整映射:
1. (bk_monitor, time_series) → BkMonitorTimeSeriesDataSource — 监控采集指标（最常用）— UNIFY硬编码
2. (bk_data, time_series) → BkdataTimeSeriesDataSource — 计算平台指标 — GRAY灰度
3. (custom, time_series) → CustomTimeSeriesDataSource — 自定义指标 — UNIFY硬编码
4. (bk_log_search, time_series) → LogSearchTimeSeriesDataSource — 日志平台指标 — GRAY灰度
5. (bk_log_search, log) → LogSearchLogDataSource — 日志关键字查询 — GRAY灰度
6. (bk_monitor, log) → BkMonitorLogDataSource — 日志关键字事件 — GRAY灰度
7. (bk_apm, log) → BkApmTraceDataSource — APM Trace查询 — GRAY灰度
8. (bk_apm, time_series) → BkApmTraceTimeSeriesDataSource — Trace明细指标 — NATIVE
9. (custom, event) → CustomEventDataSource — 自定义事件 — GRAY灰度
10. (bk_monitor, event) → BkMonitorEventDataSource — 系统事件 — NATIVE
11. (bk_fta, event) → BkFtaEventDataSource — 第三方告警事件 — NATIVE
12. (bk_fta, alert) → BkFtaAlertDataSource — 关联告警 — NATIVE
13. (bk_monitor, alert) → BkMonitorAlertDataSource — 关联策略告警 — NATIVE
14. (prometheus, time_series) → PrometheusTimeSeriesDataSource — Prometheus直查 — NATIVE

返回值是类本身（非实例），调用方需再实例化: data_source = data_source_class(bk_biz_id, interval, metrics, table, group_by)