---
groupPath: 决策记录/性能场景
relation: 性能取舍-列表类大响应启用gzip
exportedAt: "2026-08-31T02:23:39.118Z"
---
【决策记录｜性能场景 列表类大响应接口启用 gzip 压缩】
- 分类：性能取舍
- 动机：优化（主机列表与指标响应体大，尤其跳过 target 下推后响应仍可能很大）
- 决策：HostListViewSet、SearchHostInfoViewSet、SearchHostMetricViewSet 三个列表类接口的 ResourceRoute 均设置 content_encoding 为 gzip；详情页、拓扑节点、拓扑进程三类小响应接口不设置
- 背景约束：列表接口单业务可返回上千主机乘多字段；gzip 对 JSON 重复结构压缩率高
- 被否决方案：无（未找到相关记录）
- 已知代价：服务端压缩开销（CPU）换取传输体积；调试时需解压才能看明文响应
- 重新评估触发条件：响应体小于阈值（gzip 收益不抵压缩开销）；或出现压缩相关的兼容性问题
- 关联代码：HostListViewSet、SearchHostInfoViewSet、SearchHostMetricViewSet @ monitor_web/performance/views.py
- 证据来源：代码实现（ResourceRoute 的 content_encoding 等于 gzip）；commit 4faf55fb50（body：大响应启用 gzip，Verification 中列有对比 gzip wire size）
- 完整上下文：.module-experts/性能场景专家/C5-关键决策.md 决策 6