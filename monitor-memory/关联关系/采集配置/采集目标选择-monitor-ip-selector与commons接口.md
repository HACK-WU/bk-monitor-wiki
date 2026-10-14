---
groupPath: 关联关系/采集配置
relation: 采集目标选择-monitor-ip-selector与commons接口
exportedAt: "2026-10-13T10:18:01.997Z"
---
[强关联] 采集目标选择流程 与 monitor-ip-selector 共享组件/commons 节点接口
强度：必改——改 monitor-ip-selector 的 props/events 契约或 commons 节点接口（get_nodes_by_template、host_agent_status）返回结构，新建/增删目标流程的目标选择必须连带改；改采集侧内部逻辑，组件与 commons 不用管
原因：两条流程（新建 Step2、增删目标 Step1）共用 monitor-ip-selector（拓扑/动态分组/服务模板等 panel），回填与转换依赖 commons 节点接口返回结构（config-select 的 transformMonitorToValueExpand 处理 DYNAMIC_GROUP 的接口差异）

共享组件/接口端：
- monitor-ip-selector @ bkmonitor/webpack/src/monitor-pc/components/monitor-ip-selector/
- getNodesByTemplate / hostAgentStatus @ bkmonitor/webpack/src/monitor-api/modules/commons.js

采集端：
- config-select.vue（handleConfig / getParams）@ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-add/config-select/
- bk-host.vue（transformValueToMonitorExpand / transformMonitorToValueExpand）@ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-target-add-del/bk-host/