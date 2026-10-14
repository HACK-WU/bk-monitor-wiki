---
groupPath: 通用记忆片段
relation: TopN 分片查询与基数聚合（bucket_count）机制
exportedAt: "2026-09-18T01:43:16.081Z"
---
告警/Issue 分析页的 TopN 采用「时间分片查询 + 基数聚合分离」双路径：主线程把整个时间范围切成多个分片用 bulk_request 并发查（每片只做 terms 汇总），另起一个线程 get_bucket_count 用完整时间区间单独跑一次 ES cardinality 求 bucket_count，最后合并。

- 位置: `bkmonitor/packages/fta_web/alert/resources.py`（AlertTopNResource.get_bucket_count）、`bkmonitor/packages/fta_web/issue/resources.py`（IssueTopNResource）、`bkmonitor/packages/fta_web/alert/handlers/base.py`（BaseQueryHandler.top_n）、`bkmonitor/packages/fta_web/issue/handlers/issue.py`
- 关键点: handler 的 need_bucket_count 必须显式透传给基类，否则基类默认 True → bucket_count_suffix=".bucket_count" → 分片查询也会挂 cardinality 子聚合，造成重复基数聚合（commit 7b4a8c54 修复的问题）
- 关键点: get_bucket_count 只读 aggs 不读 hits.total，故 ES 参数用 track_total_hits=False；而 top_n 主路径需要 doc_count，仍为 track_total_hits=True
- 关键点: top_n 的 terms 聚合空 key 桶一律跳过（不进入 buckets），仅在开启基数聚合时 bucket_count -= 1；未开基数聚合时分片结果 bucket_count 为 None，且不再混入空值桶（保证分片前后结果语义一致）