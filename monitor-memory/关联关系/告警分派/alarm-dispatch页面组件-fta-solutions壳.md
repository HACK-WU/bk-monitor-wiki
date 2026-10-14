---
groupPath: 关联关系/告警分派
relation: alarm-dispatch页面组件-fta-solutions壳
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] alarm-dispatch 页面组件 与 fta-solutions 复用壳
强度：必改——改 monitor-pc 页面组件（AlarmDispatch / AlarmDispatchConfig）的对外契约（组件导出、渲染行为、authority-map 常量）时，fta-solutions 的壳与路由必须连带回归；改 fta-solutions 壳内部实现（mixin 来源差异等），monitor-pc 不用管
原因：fta-solutions 以「壳 + 同构路由」直接 import monitor-pc 的页面组件与 authority-map 复用（各自 authorityMixinCreate，mixin 来源分别为 monitor-pc/mixins/authorityMixin 与 monitor-ui/mixins/authorityMixin）

monitor-pc 端：
- AlarmDispatch / AlarmDispatchConfig / AlarmDispatchPage / AlarmDispatchConfigPage @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/
- authority-map.ts（MANAGE_ACTION_CONFIG / ALARM_GROUP_MANAGE_AUTH）@ 同上

fta-solutions 端：
- FtaAlarmDispatch / FtaAlarmDispatchConfig @ bkmonitor/webpack/src/fta-solutions/pages/alarm-dispatch/
- 同构路由 @ bkmonitor/webpack/src/fta-solutions/router/manage/alarm-dispatch/alarm-dispath.ts

证据：全仓 grep 引用链（fta-solutions 壳 import monitor-pc 组件与 authority-map）；GitNexus 索引未覆盖本前端模块，关联以 grep 实证