---
groupPath: 关联关系/采集配置
relation: 采集详情-datalink状态接口
exportedAt: "2026-10-13T10:18:01.997Z"
---
[强关联] 采集详情/执行详情 与 datalink 状态接口
强度：必改——改 datalink 模块 collecting_target_status / storage_status / alert_status / transfer_count_series 的字段或返回结构，采集详情组件必须连带改；改采集详情组件内部渲染，datalink 不用管
原因：详情页链路状态/存储状态/采集状态与执行详情的全部数据来自 datalink 模块，字段直连组件消费

接口端：
- collectingTargetStatus / storageStatus / alertStatus / transferCountSeries @ bkmonitor/webpack/src/monitor-api/modules/datalink.js

消费端：
- collector-detail.tsx / collector-status-details.tsx @ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-detail/
- components/link-status.tsx / components/storage-state.tsx / components/alert-topic.tsx @ 同上
- collector-operate-detail.tsx @ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-host-detail/