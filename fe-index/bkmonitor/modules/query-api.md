# QueryApiConfig（`query-api`）

> **职责**：数据查询代理：bkmonitor data query proxy（统一查询转发）

> **职责**：数据查询代理：bkmonitor data query proxy（统一查询转发）

- **位置**：`query_api/` · 归属文件 **13** 个 · 约 **1138** 行
- **定义**：`query_api/exceptions.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **0** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkmonitor`、`core.drf_resource`、`kernel_api`、`metadata`
- **被依赖**（动它会影响）：`alarm_backends`、`core.drf_resource`、`kernel_api`

## 数据表（2）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `metadata_clusterinfo` ⚠︎默认命名 | ClusterInfo | 1 | import（metadata） | `query_api/drivers/influxdb/__init__.py:40` |
| `metadata_resulttable` ⚠︎默认命名 | ResultTable | 2 | import（metadata） | `query_api/drivers/proxy.py:17` |

## 归属文件（13）

- `query_api/exceptions.py`
- `query_api/__init__.py`
- `query_api/resources.py`
- `query_api/apps.py`
- `query_api/drivers/__init__.py`
- `query_api/drivers/proxy.py`
- `query_api/drivers/client_pool.py`
- `query_api/drivers/influxdb/__init__.py`
- `query_api/drivers/influxdb/client.py`
- `query_api/sql_parse/__init__.py`
- `query_api/sql_parse/statement.py`
- `query_api/tests/conftest.py`
- `query_api/tests/__init__.py`
