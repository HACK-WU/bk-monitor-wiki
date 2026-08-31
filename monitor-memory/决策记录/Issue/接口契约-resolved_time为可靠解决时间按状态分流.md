---
groupPath: 决策记录/Issue
relation: 接口契约-resolved_time为可靠解决时间按状态分流
exportedAt: "2026-08-31T03:10:49.492Z"
---
【决策记录｜Issue 以 resolved_time 为可靠解决时间，并按状态分流时间过滤】
- 分类：接口契约
- 动机：避坑（resolved_time 残留会导致 is_resolved 误判；统一用 create_time 过滤会导致已解决 Issue 归属错分片）
- 决策：四项约定：reopen、restore、合并成员回到活跃时用 skip_empty=False 显式清空 resolved_time（避免残留值导致 is_resolved 误判）；合并成员转到 RESOLVED 时同步写入 resolved_time；查询时间过滤按状态分流（活跃不受时间约束、RESOLVED 按 resolved_time、ARCHIVED 按 update_time，非分片分支保留 create_time 小于等于 end_time 上界）；is_resolved 改为基于 status 等于 RESOLVED 并排除 ARCHIVED
- 背景约束：Issue 的解决时间与归档时间是两个不同语义，统一按一个字段过滤会让已解决 Issue 在错误的时间分片中失踪
- 被否决方案：统一按 create_time 或 update_time 过滤，否决理由为已解决 Issue 的归属与 resolved_time 不一致会漏数据
- 已知代价：时间过滤规则分三支，新增状态或改状态语义时需同步调整分流逻辑
- 重新评估触发条件：状态机新增终态；或时间分片策略调整
- 关联代码：状态流转方法 resolve、reopen、restore @ bkmonitor/documents/issue.py；时间过滤分流 @ packages/fta_web/issue/handlers/issue.py
- 证据来源：commit ee169861d1（body 四条改动，含显式清空 resolved_time 避免 is_resolved 误判、按状态分流、is_resolved 排除 ARCHIVED）；C0 已知问题 5
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 12