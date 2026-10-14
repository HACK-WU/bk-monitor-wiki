---
groupPath: 关联关系/告警分派
relation: 告警分派-共享组件-strategy-config与导出工具
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] 告警分派 与 strategy-config 共享组件 / custom-escalation / view-detail 工具
强度：建议改——改共享组件或工具函数的对外契约时，告警分派（及各自其它消费方）需连带回归；改告警分派内部实现，共享资产不用管
原因：告警分派复用 strategy-config 的告警组选择 / 错误提示 / 横滚容器，custom-escalation 的 CSV 解析，view-detail 的 CSV 下载；均为跨模块共享资产（多消费方）

告警分派端（消费）：
- alarm-batch-edit.tsx（AlarmGroup / VerifyItem）、common-condition-new.tsx（HorizontalScrollContainer）、alarm-dispatch-config.tsx（csvToArr / downCsvFile）@ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/

共享资产端：
- strategy-config/strategy-config-set-new/components/{alarm-group,verify-item,horizontal-scroll-container}.tsx
- custom-escalation/utils.ts（csvToArr）/ view-detail/utils.ts（downCsvFile）

证据：grep 实证 import 链