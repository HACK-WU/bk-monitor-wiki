---
groupPath: 专题记忆/数据源查询构造
relation: 路径决策机制 use_unify_query
exportedAt: "2026-08-13T12:00:36.682Z"
---
use_unify_query 是路径决策的核心方法，根据数据源 id=(data_source_label, data_type_label) 判断走统一查询后端还是原生查询路径。三种路径决策类型：UNIFY硬编码、GRAY灰度、NATIVE原生。

- 符号: `use_unify_query`、`UnifyQueryDataSources`、`GrayUnifyQueryDataSources`、`switch_unify_query`、`_query_data_using_datasource`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`、`bkmonitor/bkmonitor/data_source/unify_query/query.py`

UnifyQueryDataSources（硬编码，恒走 unify-query）:
- (BK_MONITOR_COLLECTOR, TIME_SERIES) — 监控采集指标，最常用
- (CUSTOM, TIME_SERIES) — 自定义指标
- use_unify_query() 对这两个组合始终返回 True，不会进入原生查询分支

GrayUnifyQueryDataSources（6个灰度组合，条件判定）:
- (bk_data, time_series): 按 BKDATA_USE_UNIFY_QUERY_GRAY_BIZ_LIST 灰度业务列表判定
- (bk_log_search, time_series/log): 按 DB 白名单判定
- (bk_monitor, log): 按白名单判定
- (custom, event): 按白名单判定
- (bk_apm, log): 按黑名单 + query_string 特征判定
- 各数据源类实现各自的 switch_unify_query(bk_biz_id) 方法，通过 DB/Redis 白名单或黑名单决定

NATIVE 原生路径（永不走 unify-query）:
- 不在以上两个列表的组合，use_unify_query() 直接返回 False
- 通过 _query_data_using_datasource → DataQueryHandler 路由到存储后端
- FTA 事件/告警 → 直连 ES
- 系统事件/告警 → 直连 ES
- APM 时序指标 → metadata/ES
- Prometheus → PromQL 直查

特殊灰度条件（仅 BkdataTimeSeriesDataSource）:
- 接入数据平台(IS_ACCESS_BK_DATA) + cmdb-level 查询 + 表在 BKDATA_CMDB_LEVEL_TABLES 白名单 → 走原生路径

决策流程:
use_unify_query() → 取 data_source.id → 不在两列表返回 False(NATIVE) → 在 GrayUnifyQueryDataSources 调 switch_unify_query(GRAY) → 在 UnifyQueryDataSources 返回 True(UNIFY)