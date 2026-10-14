---
groupPath: 关联关系/告警分派
relation: TAG_FIELD_BATCH_SIZE-AlertTopNResource上限同步
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] 前端标签值批量取数分片 与 后端 AlertTopN 嵌套字段上限
强度：必改——改后端 AlertTopNResource.MAX_NESTED_TOP_N_FIELDS 时，前端 TAG_FIELD_BATCH_SIZE（当前 20）必须同步；反之亦然
原因：条件编辑器按 20 个字段分片批量调 alertTopN 取标签维度值候选，源码注释明写需与后端上限保持同步；不同步会导致批量取数被拒或截断（条件值候选项缺失）

两端：
- TAG_FIELD_BATCH_SIZE / chunkFields @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/typing/condition.ts
- AlertTopNResource.MAX_NESTED_TOP_N_FIELDS @ 后端 fta alert（AlertTopNResource）

证据：代码注释原文「需与后端 AlertTopNResource.MAX_NESTED_TOP_N_FIELDS 保持同步」