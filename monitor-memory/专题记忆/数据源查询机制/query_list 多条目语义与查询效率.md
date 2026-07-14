---
groupPath: 专题记忆/数据源查询机制
relation: query_list 多条目语义与查询效率
keywords: [合并后单跑, 引擎内部并行, 故障隔离, 响应体积, 关联计算]
exportedAt: "2026-07-14T04:50:48.402Z"
---
## query_list 多条目：语义与查询效率

### 1. 类型与数量
`query_list` 是切片类型 `QueryList []*Query`（`pkg/unify-query/query/structured/query_ts.go:48`），支持多条，每条用 `reference_name`（a/b/c…）区分。

### 2. 多条目必须靠 metric_merge 合成一条 PromQL
多条项并非「各查各的打包返回」，而是必须经 `metric_merge` 组合成**单条** PromQL 才能执行；`metric_merge` 为空直接报错（`query_ts.go:360-361` `if q.MetricMerge == ""`）。因此 query_list 多条目是为「关联计算」（如 `a / b`）设计的，不是批量独立查询机制。

### 3. 执行模型（合并后单跑）
主路径 `queryTsWithPromEngine` → `queryTsToInstanceAndStmt` 把所有项经 `queryTs.ToPromExpr` 合成**一条 stmt**，再 `instance.DirectQueryRange(ctx, stmt, ...)` **只执行一次**（`service/http/query.go:883` 与 `:934`）。

### 4. 引擎内部并行 fan-out
Prometheus 引擎对合成后的子查询用 goroutine / `ants` 池并发执行，并发度受 `QueryMaxRouting` 限制。整体延迟≈**最慢子查询**，而非各条之和。

### 5. 多条≠零代价
每个 query_list 项经 `ToQueryMetric` 会因路由/时间分片 `GetStorageIDRangesWithDirectionalOverlap` 展开成多个存储子查询，相同 storage 才合并（`query_ts.go:866-1014`）。N 条 ≈ 后端实际调用数累加，线性增加 series 扫描量、返回数据量、内存（全部 series 合进一个 `PromData.Fill`）。

### 6. 共享信封的代价
- 超时预算：全部项共享 `SingleflightTimeout=1m` 与 `SlowQueryThreshold=3s`（`service/http/settings.go`、`hook.go`）。
- 故障域：任一子查询慢/失败 → 整请求失败。
- 响应体积：所有 series 聚合进单一 `PromData`，内存/包体更大。

### 7. 硬上限与特例
- 单请求 `query_list` 上限 `DefaultQueryListLimit=20`（配置 `http.default_query_list_limit`，`query.go:796-799`，超限报错）。
- 反例：`/ts/cluster_metrics` 的 `ToQueryClusterMetric` 强制 `len(QueryList)==1`（`query_ts.go:263-264`）。

### 8. 实践建议
- **互不相关、无需跨指标运算的数据** → 拆成多次请求（或客户端并发查询），获得独立超时预算、故障隔离、更小响应体积；注意自限流/连接池。
- **需关联计算或严格同时间轴对齐** → 用 `query_list` 多条目 + `metric_merge`（设计正途，比 N 次往返再客户端对齐更省更准）。
- 单请求内 query_list 到 10 量级即需关注响应体积与慢查询阈值。