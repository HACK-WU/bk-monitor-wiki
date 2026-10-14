---
groupPath: 关联关系/告警分派
relation: 告警分派列表页-query契约-告警组页与流转记录
exportedAt: "2026-10-14T03:13:17.205Z"
---
[强关联] 告警分派列表页 query 契约 与 告警组页 / 告警流转记录
强度：必改——改列表页 getRouteParams 读取的 query 参数名（groupName / group_id）或搜索语义时，两端入口必须连带改；改入口侧内部实现不影响本模块
原因：列表页以 query 参数作为跨模块直达契约——告警组页传 groupName、告警流转记录外链传 group_id，均作为搜索词预填（group_id 优先），并受 isSearch 双请求栅栏控制执行时机

告警分派端：
- getRouteParams / isSearch @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/alarm-dispatch.tsx

入口端：
- handleToAppDispatch（query.groupName，读 rules_count 决定是否可跳）@ bkmonitor/webpack/src/monitor-pc/pages/alarm-group/alarm-group-common/alarm-group.tsx
- 流转记录外链构造（#/alarm-dispatch?group_id=，由后端流转记录 router_info.router_name 驱动）@ bkmonitor/webpack/src/trace/pages/alarm-center/common-detail/components/alarm-view/alarm-records.tsx（fta-solutions 同源流转记录页）

证据：grep 实证两处入口代码