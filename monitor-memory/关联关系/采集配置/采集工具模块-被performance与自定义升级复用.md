---
groupPath: 关联关系/采集配置
relation: 采集工具模块-被performance与自定义升级复用
exportedAt: "2026-10-13T10:18:01.997Z"
---
[强关联] 采集工具/类型文件 与 performance、custom-escalation 模块（反向被依赖）
强度：必改——改 variable-set.ts 的 localStorage key（collectVariablesConfig）或存取函数结构、log-handle.ts 的 hideOptions 类型、status-tab-list.tsx 的 IStatusData 类型，两个消费方必须连带改；改消费方，采集侧不用管
原因：采集旧可视化目录整体无入口引用，但其中三个工具/类型文件被跨模块复用——清理旧代码时不能整目录删除

采集（被依赖）端：
- variable-set.ts（getCollectVariable / setCollectVariable / delCollectScene / batchDelCollectRecord）@ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-view/
- log-handle.ts（hideOptions 类型）@ 同上
- status-tab-list.tsx（IStatusData）@ bkmonitor/webpack/src/monitor-pc/pages/collector-config/collector-view-detail/

消费端：
- performance 模块详情面板（dashboard-panels.vue / host-list.tsx）@ bkmonitor/webpack/src/monitor-pc/pages/performance/
- custom-escalation/event-view-setting.ts @ bkmonitor/webpack/src/monitor-pc/pages/custom-escalation/