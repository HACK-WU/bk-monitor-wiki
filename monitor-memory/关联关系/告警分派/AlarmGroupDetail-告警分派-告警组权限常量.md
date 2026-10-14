---
groupPath: 关联关系/告警分派
relation: AlarmGroupDetail-告警分派-告警组权限常量
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] AlarmGroupDetail 组件与告警组权限常量 与 告警分派
强度：必改——改 AlarmGroupDetail 的 props（id / v-model / customEdit / onEditGroup）或行为语义时，告警分派两页的告警组详情弹窗必须连带改；改告警分派内部实现，alarm-group 不用管
原因：告警分派复用 alarm-group 的详情抽屉（列表页 customEdit + 接管 editGroup 跳转、配置页 customEdit=false 由弹窗内部跳转），并别名复用其 MANAGE_AUTH 权限常量

alarm-group 端（源）：
- AlarmGroupDetail @ bkmonitor/webpack/src/monitor-pc/pages/alarm-group/alarm-group-detail/alarm-group-detail.tsx
- MANAGE_AUTH（manage_notify_team_v2）@ bkmonitor/webpack/src/monitor-pc/pages/alarm-group/authority-map.ts

告警分派端（消费）：
- alarm-dispatch.tsx（handleSelcetAlarmGroup / handleEditGroup）与 alarm-dispatch-config.tsx（handleSelcetAlarmGroup）@ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/
- authority-map.ts（ALARM_GROUP_MANAGE_AUTH = MANAGE）@ 同上

证据：grep 实证（告警分派 authority-map 直接 import 告警组 MANAGE_AUTH；两页 import AlarmGroupDetail）