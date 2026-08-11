`_query_data_using_datasource` 分支链路总结，分析当查询不走统一查询模块（unify-query HTTP 接口）时，由 UnifyQuery 直接把查询下推到各数据源原生 query_data，再由数据源自身构造原生存储查询（DataQueryHandler）的完整链路。

- 符号: `UnifyQuery._query_data_using_datasource`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- 分支判定：`UnifyQuery.use_unify_query()` → `False`
- 调用方：`UnifyQuery._query_data_internal()` 的 `else` 分支
- 本文档聚焦 `_query_unify_query` 之外的另一条路径

## 1. 分支定位与触发条件

- 符号: `UnifyQuery._query_data_internal` / `UnifyQuery.use_unify_query`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- `use_unify_query()` 返回 `False` 的全部情形：

| # | 条件 | 代码位置 | 说明 |
|---|------|----------|------|
| 1 | `data_sources[0].id` **不在** `UnifyQueryDataSources + GrayUnifyQueryDataSources` | query.py | **恒走本分支** |
| 2 | 灰度数据源 `switch_unify_query(bk_biz_id)` 返回 `False` | query.py | 仅 `GrayUnifyQueryDataSources` 命中 |
| 3 | 接入数据平台（`IS_ACCESS_BK_DATA`）+ cmdb-level 查询 + 表在 `BKDATA_CMDB_LEVEL_TABLES` 白名单 | query.py | 仅 `BkdataTimeSeriesDataSource` 命中 |

> 其余情形（多指标、有表达式、有 functions、命中 `AggMethods/CpAggMethods`、无 table 或负 biz_id）一律走 unify-query 分支。

### 1.1 恒走本分支的数据源（id 不在两个列表）

数据源 id = `(data_source_label, data_type_label)`。

- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py` / `bkmonitor/bkmonitor/data_source/constants/data_source.py`

| 数据源类 | id | 备注 |
|----------|-----|------|
| `PrometheusTimeSeriesDataSource` | `("prometheus", "time_series")` | data_source/__init__.py |
| `BkApmTraceTimeSeriesDataSource` | `(BK_APM, TIME_SERIES)` | data_source/__init__.py |
| `BkMonitorEventDataSource` | `(BK_MONITOR_COLLECTOR, EVENT)` | data_source/__init__.py |
| `BkFtaEventDataSource` | `(BK_FTA, EVENT)` | data_source/__init__.py |
| `BkFtaAlertDataSource` | `(BK_FTA, ALERT)` | data_source/__init__.py |
| `BkMonitorAlertDataSource` | `(BK_MONITOR_COLLECTOR, ALERT)` | data_source/__init__.py |

### 1.2 条件走本分支的数据源（灰度关闭时）

均属于 `GrayUnifyQueryDataSources`，仅当 `switch_unify_query(bk_biz_id) == False` 时落入本分支：

| 数据源类 | id | 灰度判定 |
|----------|-----|----------|
| `BkdataTimeSeriesDataSource` | `(BK_DATA, TIME_SERIES)` | `BkdataTimeSeriesDataSource.switch_unify_query`，web 角色恒 True；多指标/有 functions 走 unify；按 `BKDATA_USE_UNIFY_QUERY_GRAY_BIZ_LIST` 灰度 |
| `BkMonitorLogDataSource` | `(BK_MONITOR_COLLECTOR, LOG)` | 继承 `BaseBkMonitorLogDataSource.switch_unify_query`，按业务白名单/聚类表/全量灰度判定 |
| `BkApmTraceDataSource` | `(BK_APM, LOG)` | 同上（继承日志基类） |
| `LogSearchTimeSeriesDataSource` | `(BK_LOG_SEARCH, TIME_SERIES)` | 同上 |
| `LogSearchLogDataSource` | `(BK_LOG_SEARCH, LOG)` | 同上 |
| `CustomEventDataSource` | `(CUSTOM, EVENT)` | 继承 `BkMonitorLogDataSource`，内置事件表（`system_event`/`k8s_event`/`cicd_event`）强制 unify |

> 注意：灰度数据源的 `query_data` **不会**再内部回路由 unify-query——`switch_unify_query` 仅在 `UnifyQuery` 编排层决定走哪条分支；一旦落入本分支，数据源 `query_data` 直接构造原生查询。

## 2. 最终参数组装（`_query_data_using_datasource`）

### 2.1 入参来源

`_query_data_using_datasource` 的参数由 `_query_data_internal` 透传：

```python
data, series_stat = self._query_data_using_datasource(
    start_time=start_time,      # 已 process_time_range，缺省回退近 1h
    end_time=end_time,
    limit=limit,                # 默认 settings.SQL_MAX_LIMIT
    slimit=slimit,              # 默认 settings.SQL_MAX_LIMIT
    offset=offset,
    with_series_stat=with_series_stat,
    **kwargs,                   # 透传 instant / time_alignment 等
)
```

### 2.2 逐数据源循环

```python
for datasource in self.data_sources:
    if with_series_stat and hasattr(datasource, "query_data_with_stat"):
        data, stat = datasource.query_data_with_stat(
            start_time=start_time, end_time=end_time,
            limit=limit, slimit=slimit, offset=offset, **kwargs)
        all_series_stat.update(stat)
    else:
        data = datasource.query_data(
            start_time=start_time, end_time=end_time,
            limit=limit, slimit=slimit, offset=offset, **kwargs)
    if len(self.data_sources) == 1:
        # 单数据源：把 metrics[0] 字段值映射为统一结果字段 _result_
        metric_field = datasource.metrics[0].get("alias") or datasource.metrics[0]["field"]
        record["_result_"] = record[metric_field]
    all_data.extend(data)
return all_data, all_series_stat
```

关键点：
- **`with_series_stat` 仅在数据源具备 `query_data_with_stat` 时生效**（如 `PrometheusTimeSeriesDataSource`、`TimeSeriesDataSource` 子类），否则退化为 `query_data`，`all_series_stat` 为空。
- **单数据源**时，将 `metrics[0]` 的字段（优先 `alias`）复制到统一字段 `_result_`，与 unify-query 分支的 `process_unify_query_data` 输出结构对齐。
- 返回 `(all_data, all_series_stat)` 二元组；多数据源时相同 key 的 stat 会被后者覆盖。

### 2.3 后置处理（`process_data_by_datasource`）

- 符号: `UnifyQuery.process_data_by_datasource`
- 位置: `bkmonitor/bkmonitor/data_source/unify_query/query.py`
- 仅当首个数据源 id 为 `(CUSTOM, EVENT)` 或 `(BK_MONITOR_COLLECTOR, LOG)` 时，记录会再经 `first_ds.process_unify_query_data(records)` 做统一结果格式归一化；其余数据源原样返回。

## 3. 最终请求的目标对象（各数据源 `query_data`）

`_query_data_using_datasource` 的**目标对象**是各 `TimeSeriesDataSource` 子类的 `query_data` / `query_data_with_stat` 方法。它们最终都收敛到 `_get_queryset` → `DataQueryHandler`，即原生存储查询构造器。

### 3.1 基类 `TimeSeriesDataSource.query_data`

- 符号: `TimeSeriesDataSource.query_data`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

通用时序路径，组装参数后调用 `_get_queryset`：

```python
filter_dict = self.filter_dict.copy()       # 含系统磁盘/网络维度过滤（见 process_data_sources）
if start_time: start_time += self.time_offset   # 时区偏移
if end_time:   end_time   += self.time_offset
q = self._get_queryset(
    bk_tenant_id=self.bk_tenant_id, metrics=self.metrics, table=self.table,
    index_set_id=self.index_set_id, query_string=self.query_string,
    agg_condition=self.where, group_by=self.group_by, interval=self.interval,
    where=filter_dict, time_field=self.time_field, order_by=self.order_by,
    limit=limit, slimit=slimit, start_time=start_time, end_time=end_time)
records = q.raw_data
records = self._format_time_series_records(records)   # 时间字段统一为 _time_
return self._filter_by_advance_method(records)        # 高级条件后置过滤
```

### 3.2 `PrometheusTimeSeriesDataSource.query_data`

- 符号: `PrometheusTimeSeriesDataSource.query_data`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

不走 `_get_queryset`，而是执行 PromQL：

```python
data, end_time_ms = self._execute_promql(start_time, end_time)
return UnifyQuery.process_unify_query_data({}, data, end_time=end_time_ms)
```

> 注意：虽然执行 PromQL 不经 unify-query HTTP，但结果仍复用 `UnifyQuery.process_unify_query_data` 做格式归一。**目标对象是 Prometheus 查询引擎**，非 unify-query 服务。

### 3.3 `BkApmTraceTimeSeriesDataSource` / `BkApmTraceDataSource.query_data`

- 符号: `BkApmTraceTimeSeriesDataSource.query_data` / `BkApmTraceDataSource.query_data`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

```python
if limit is not None: limit = min(limit, 10000)        # 上限 10000
start_time, end_time = self._process_time_range(start_time, end_time)  # 非默认时间字段时转毫秒
return super().query_data(start_time, end_time, limit, search_after_key, *args, **kwargs)
```

`_process_time_range`：当 `time_field != "time"` 时把起止时间 ×1000 转毫秒（APM trace 用微/毫秒级时间字段）。

### 3.4 `BkFtaEventDataSource` / `BkMonitorAlertDataSource.query_data`

- 符号: `BkFtaEventDataSource.query_data` / `BkMonitorAlertDataSource.query_data`
- 位置: `bkmonitor/bkmonitor/data_source/data_source/__init__.py`

事件/告警类走专用 `_get_queryset`，**table 被替换为时间区间字符串**：

```python
if start_time: start_time += self.time_offset
if end_time:   end_time   += self.time_offset
q = self._get_queryset(
    bk_tenant_id=self.bk_tenant_id,
    table=f"{start_time}|{end_time}",     # 事件表以时间区间作为路由键
    metrics=self.metrics, agg_condition=self.where, interval=self.interval,
    group_by=self.group_by, where=self.filter_dict, time_field=self.time_field,
    start_time=start_time, end_time=end_time)
records = q.raw_data
records = self._filter_by_advance_method(records)
records = self._format_time_series_records(records)
return records[:limit]
```

`BkFtaAlertDataSource` / `BkMonitorAlertDataSource` 仅覆盖 `data_source_label/data_type_label`，复用上述实现。

### 3.5 灰度关闭时的日志/计算平台数据源

- **`BkMonitorLogDataSource.query_data`**：按 `topo_nodes` 逐拓扑节点调 `_get_queryset`（bklog DSL），再做 `distinct` 计算与维度前缀清理。
- **`BkdataTimeSeriesDataSource`**（灰度关闭 + cmdb-level）：`_get_queryset` 将 `_cmdb_level` 表替换为 bk_data 结果表，转调 `BkdataTimeSeriesDataSource._get_queryset` 走 **bk_sql** 查询；指标字段加反引号转义。

## 4. 最终后端目标：从 `DataQueryHandler` 到真实存储

所有 `_get_queryset` 最终构造 `DataQueryHandler(cls.data_source_label, cls.data_type_label)`，按 `(data_source_label, data_type_label)` 路由到对应存储后端的查询执行器，链式拼装后执行：

```python
q = DataQueryHandler(cls.data_source_label, cls.data_type_label)
if where: q = q.where(dict_to_q(where))
if time_filter: q = q.where(**time_filter)
return (q.select(*select).bk_tenant_id(bk_tenant_id).metrics(metrics).table(table)
         .agg_condition(agg_condition).group_by(*group_by)
         .dsl_index_set_id(index_set_id).dsl_raw_query_string(query_string, nested_paths=nested_paths)
         .use_full_index_names(use_full_index_names).order_by(*order_by)
         .distinct(distinct).limit(limit).slimit(slimit).offset(offset).time_field(time_field))
```

`q.raw_data` / `q.original_data` 即原生存储返回。但 `DataQueryHandler` **不是最终落点**——它只是按 id 选择 handler 子类，真正执行在 `DataQuery` 基类的 `raw_data`/`original_data` → `compiler.execute_sql()` → `connection.execute(...)`。

### 4.1 handler 路由

下表**仅列出能够实际进入本分支**的 id（即在 `UnifyQueryDataSources` 列表之外，或属于 `GrayUnifyQueryDataSources` 且灰度关闭，或 `BK_DATA` cmdb-level 路由）。

> ⚠️ 重要：`(BK_MONITOR_COLLECTOR, TIME_SERIES)` 与 `(CUSTOM, TIME_SERIES)` **不在本表**——二者在 `UnifyQueryDataSources` 列表内，`use_unify_query` 对其恒返回 `True`，**永远走 unify-query 分支**，不会进入 `_query_data_using_datasource`。`(BK_DATA, LOG)` 虽在 `DATA_SOURCE` 字典中，但无对应 DataSource 类，亦不进入本分支。

| 数据源 id | 进入本分支条件 | handler 子类 | backend | `query_func`（最终调用） |
|-----------|----------------|--------------|---------|--------------------------|
| `(BK_APM, TIME_SERIES)` | 恒走（不在两列表） | `ESDataQuery` | `elastic_search` | `api.metadata.get_es_data` |
| `(BK_MONITOR_COLLECTOR, LOG)` | 灰度关闭 | `ESDataQuery` | `elastic_search` | `api.metadata.get_es_data` |
| `(CUSTOM, EVENT)` | 灰度关闭 | `ESDataQuery` | `elastic_search` | `api.metadata.get_es_data` |
| `(BK_APM, LOG)` | 灰度关闭 | `ESDataQuery` | `elastic_search` | `api.metadata.get_es_data` |
| `(BK_LOG_SEARCH, LOG)` | 灰度关闭 | `LogSearchDataQuery` | `log_search` | `api.log_search.es_query_search` |
| `(BK_LOG_SEARCH, TIME_SERIES)` | 灰度关闭 | `DataQuery` | `log_search` | `api.log_search.es_query_search` |
| `(BK_DATA, TIME_SERIES)` | 灰度关闭 + cmdb-level | `DataQuery` | `time_series` | `api.bkdata.query_data` |
| `(BK_FTA, EVENT)` | 恒走（不在两列表） | `DataQuery` | `fta_event` | **`None`** → 直连 ES（`EventDocument`） |
| `(BK_FTA, ALERT)` | 恒走（不在两列表） | `DataQuery` | `fta_event` | **`None`** → 直连 ES（`EventDocument`） |
| `(BK_MONITOR_COLLECTOR, EVENT)` | 恒走（不在两列表） | `DataQuery` | `fta_event` | **`None`** → 直连 ES（`EventDocument`） |
| `(BK_MONITOR_COLLECTOR, ALERT)` | 恒走（不在两列表） | `DataQuery` | `fta_event` | **`None`** → 直连 ES（`EventDocument`） |

> 另：`(prometheus, time_series)`（`PrometheusTimeSeriesDataSource`）恒走本分支，但**不经 `_get_queryset`/`DataQueryHandler`**，而是执行 PromQL（§3.2）。
>
> 映射源：`models/sql/query.py` 的 `DATA_SOURCE` 字典（`query` 字段即 `query_func`，`backends` 字段即 backend 模块）；handler 类名来自 `handler/__init__.py` 的 `DataQueryHandler.__new__` 路由。

### 4.2 最终落点结论：外部 API 还是 ES 还是数据库？

**结论：本分支绝大多数走"外部 API 接口"调用兄弟微服务；只有 FTA 事件/告警走"直连 ES"；没有直接连关系型数据库。**

| 类别 | 数据源（本分支可达） | 最终落点 | 底层存储 |
|------|----------------------|----------|----------|
| **外部 API**（metadata 服务） | `BK_APM/*`、监控采集 LOG、自定义 EVENT（均为灰度关闭或恒走） | `api.metadata.get_es_data` | metadata 服务再查 **ES** |
| **外部 API**（日志检索服务） | `BK_LOG_SEARCH/*`（LOG / TIME_SERIES，灰度关闭） | `api.log_search.es_query_search` | 日志检索服务再查 **ES** |
| **外部 API**（计算平台） | `BK_DATA/TIME_SERIES`（灰度关闭 + cmdb-level） | `api.bkdata.query_data` | 计算平台再执行 **BKSQL / bk-sql** |
| **直连 ES**（不经过 api.*） | `BK_FTA/EVENT`、`BK_FTA/ALERT`、`BK_MONITOR_COLLECTOR/EVENT`、`BK_MONITOR_COLLECTOR/ALERT` | `EventDocument.search(...).update_from_dict(params).execute()`（backends/fta_event/connection.py） | **ES**（通过 ES Python 客户端，非 HTTP 网关） |

> 注：`BK_MONITOR_COLLECTOR/TIME_SERIES` 与 `CUSTOM/TIME_SERIES` 虽在 `DATA_SOURCE` 字典中映射为 `api.metadata.get_ts_data`，但二者恒走 unify-query 分支（见 §4.1 警告），**不计入本分支落点**。

要点：
- **外部 API 路径**：`connection.execute` 把编译好的查询体作为参数传给 `api.<service>.<method>`（core.drf_resource 内部服务网关，本质是 HTTP/RPC 调兄弟服务）。例如 ES backend 的 `execute` 调 `self.query_func(table_id=rt_id, query_body=params, ...)`，`query_func = api.metadata.get_es_data`。
- **直连 ES 路径**：`fta_event` backend 的 `query_func` 为 `None`，`execute` 直接 `EventDocument.search(all_indices=True).update_from_dict(params).execute()` 命中 ES（带 `es_query` span）。
- **数据库**：本分支**没有**直接 JDBC/ORM 查业务库；time_series 的 `BKSQL` 是发给 metadata 服务的 SQL 字符串（由 metadata 转发到 TSDB/bk-sql），并非 SaaS 直连 DB。

### 4.3 各 backend 的 `execute` 形态

- **elastic_search**：`execute(rt_id, params)` → `query_func(table_id=rt_id, query_body=params, use_full_index_names=..., bk_tenant_id=...)`，span=`es_query`。
- **time_series**：`execute(sql, params)` → 拼出 **BKSQL 字符串**，`query_func(sql=sql_str, prefer_storage="", bk_tenant_id=...)`，span=`bksql`。
- **log_search**：同上 ES 形态，调 `api.log_search.es_query_search`。
- **fta_event**：`execute(rt_id, params)` → `EventDocument.search(all_indices=True).update_from_dict(params).execute().to_dict()`，**无 api.* 调用**。

## 5. 最终参数示例

### 5.1 ES 路径示例（`BkMonitorLogDataSource`，id=`BK_MONITOR_COLLECTOR/LOG`）

`_get_queryset` 入参（来自 `BkMonitorLogDataSource.query_data`）：

```python
self._get_queryset(
    bk_tenant_id="tencent",
    metrics=[{"field": "count", "method": "COUNT", "alias": "count"}],
    table="2_bkmonitor_time_series_100010_0",   # 结果表
    agg_condition=[{"key": "level", "method": "eq", "value": "error"}],
    group_by=["bk_target_ip"],
    interval=60,
    where={"bk_target_ip__eq": "10.0.0.1"},     # filter_dict
    time_field="time",
    order_by=["-time"],
    limit=10, slimit=None,
    start_time=1710000000000, end_time=1710003600000,
    query_string="*", index_set_id=None,
    nested_paths={}, use_full_index_names=False,
)
```

经 ES `SQLCompiler.as_sql` 编译后，`connection.execute(table_id, dsl)` 实际下发的 **ES DSL**（`api.metadata.get_es_data(table_id=..., query_body=dsl)`）：

```json
{
  "bk_tenant_id": "tencent",
  "_source": ["bk_target_ip"],
  "query": {
    "bool": {
      "filter": [
        {"term": {"bk_target_ip": "10.0.0.1"}},
        {"range": {"time": {"gte": 1710000000000, "lt": 1710003600000}}},
        {"term": {"level": "error"}}
      ]
    }
  },
  "aggregations": {
    "_group_": {
      "composite": {
        "size": 10,
        "sources": [{"bk_target_ip": {"terms": {"field": "bk_target_ip"}}}]
      },
      "aggregations": {
        "time": {
          "date_histogram": {"field": "time", "fixed_interval": "60s"},
          "aggregations": {"count": {"value_count": {"field": "count"}}}
        }
      }
    }
  },
  "sort": [{"time": "desc"}],
  "size": 0
}
```

> 说明：`where`（`filter_dict`）→ `query.bool.filter`；`agg_condition` → 追加到 filter；`metrics[].method` → `METRIC_AGG_TRANSLATE`（count→value_count）；`interval` → `date_histogram.fixed_interval`；`group_by` → composite aggregation `sources`。

### 5.2 BKSQL 路径示例（`BkdataTimeSeriesDataSource`，id=`BK_DATA/TIME_SERIES`，cmdb-level 路由）

> 该数据源在 `use_unify_query` 中因 cmdb-level 表命中白名单而返回 `False`，进入本分支；其 `_get_queryset` 将 `_cmdb_level` 表替换为 bk_data 结果表，转走 **bk_sql** 查询。

`_get_queryset` 入参（来自 `BkdataTimeSeriesDataSource.query_data` 继承的基类 `TimeSeriesDataSource.query_data`；`BkdataTimeSeriesDataSource` 覆写 `_get_queryset`）：

```python
self._get_queryset(
    bk_tenant_id="tencent",
    metrics=[{"field": "cpu_usage", "method": "AVG", "alias": "cpu_usage"}],
    table="2_system_cpu_detail",          # 原始 _cmdb_level 表，已由覆写替换为 bk_data 结果表
    agg_condition=[{"key": "bk_target_ip", "method": "eq", "value": "10.0.0.1"}],
    group_by=["bk_target_ip"],
    interval=60,
    where={},
    time_field="dtEventTimeStamp",        # BkdataTimeSeriesDataSource.DEFAULT_TIME_FIELD
    order_by=["-dtEventTimeStamp"],
    limit=100, slimit=None,
    start_time=1710000000000, end_time=1710003600000,
)
```

经 `BkdataTimeSeriesDataSource._get_queryset` 给指标字段加反引号、time_series `SQLCompiler` 编译后，`connection.execute(sql, params)` 拼出 **BKSQL 字符串** 并调 `api.bkdata.query_data(sql=..., bk_tenant_id="tencent")`：

```sql
SELECT AVG(`cpu_usage`) as `cpu_usage`, `bk_target_ip`
FROM `2_system_cpu_detail`
WHERE `bk_target_ip` = '10.0.0.1'
  AND `dtEventTimeStamp` >= 1710000000000 AND `dtEventTimeStamp` < 1710003600000
GROUP BY `bk_target_ip`, time(60s)
ORDER BY `dtEventTimeStamp` DESC
LIMIT 100
```

> 说明：time_series backend 的 `execute` 把参数转义后 `%` 拼进 SQL 模板，span=`bksql`；最终由计算平台执行 BKSQL。指标字段在 `BkdataTimeSeriesDataSource._get_queryset` 中加反引号转义；cmdb-level 表替换逻辑见覆写方法。
>
> ⚠️ 注意：监控采集时序 `BkMonitorTimeSeriesDataSource`（`BK_MONITOR_COLLECTOR/TIME_SERIES`）与 `CUSTOM/TIME_SERIES` **不在此示例范围内**——它们恒走 unify-query 分支（见 §4.1），不会进入 `_query_data_using_datasource`，其 `DataQueryHandler` 虽映射 `api.metadata.get_ts_data` 但本分支不会触发。

### 5.3 FTA 直连 ES 路径示例（`BkFtaAlertDataSource`，id=`BK_FTA/ALERT`）

`_get_queryset` 入参（来自 `BkFtaEventDataSource.query_data`，`table` 被替换为时间区间键）：

```python
self._get_queryset(
    bk_tenant_id="tencent",
    table="1710000000000|1710003600000",     # 事件表以时间区间路由
    metrics=[{"field": "_index", "method": "COUNT", "alias": "a"}],
    agg_condition=[{"key": "alert_status", "method": "eq", "value": "ACITVE"}],
    interval=60, group_by=[],
    where={"bk_biz_id__eq": 2},
    time_field="time",
    start_time=1710000000000, end_time=1710003600000,
)
```

编译为 ES DSL 后，`fta_event` backend 的 `execute` **不经 api.***，直接：

```python
EventDocument.search(all_indices=True).update_from_dict(es_dsl).execute().to_dict()
```

即直接命中 **ES**（告警/事件索引），返回 `hits.total` + `hits.hits`。

## 6. 与 `_query_unify_query` 分支对照

| 维度 | `_query_unify_query`（unify 分支） | `_query_data_using_datasource`（本分支） |
|------|-----------------------------------|------------------------------------------|
| 触发条件 | `use_unify_query() == True` | `use_unify_query() == False` |
| 目标对象 | `api.unify_query.query_data` 等 HTTP 接口 | 各 `DataSource.query_data` → `DataQueryHandler` |
| 参数形态 | `get_unify_query_params` 拼 `query_list`/`step`/`order_by` 等 | 直接透传 `start_time/end_time/limit/slimit/offset/**kwargs` |
| 聚合处理 | 在 `to_unify_query_config` 中映射 function/time_aggregation | 在数据源原生查询中按 `metrics[].method` 处理 |
| 结果归一 | `process_unify_query_data` | 单数据源时手动映射 `_result_`；`process_data_by_datasource` 仅对部分日志/事件类再归一 |
| series_stat | `_query_unify_query` 计算后由 `_query_data_internal` 透出 | 仅 `with_series_stat` 且数据源有 `query_data_with_stat` 时计算 |

## 7. 关键源码定位速查

| 内容 | 位置 |
|------|------|
| 分支判定 `use_unify_query` | `bkmonitor/bkmonitor/data_source/unify_query/query.py` |
| 本分支入口 `_query_data_using_datasource` | `bkmonitor/bkmonitor/data_source/unify_query/query.py` |
| 调用方 `_query_data_internal` else 分支 | `bkmonitor/bkmonitor/data_source/unify_query/query.py` |
| 数据源 id 列表 `UnifyQueryDataSources` / `GrayUnifyQueryDataSources` | `bkmonitor/bkmonitor/data_source/constants/data_source.py` |
| 基类时序查询 `TimeSeriesDataSource.query_data` | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| Prometheus 查询 | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| APM trace 查询 | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| 事件/告警查询 | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| 日志数据源查询（灰度关闭） | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| 计算平台 cmdb-level 路由 | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| 原生查询构造 `DataQueryHandler` | `bkmonitor/bkmonitor/data_source/data_source/__init__.py` |
| 结果后置 `process_data_by_datasource` | `bkmonitor/bkmonitor/data_source/unify_query/query.py` |
