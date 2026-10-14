---
groupPath: 决策记录/插件管理
relation: 兼容处理-指标diff类型提交降级double
exportedAt: "2026-10-13T12:07:37.824Z"
---
【决策记录｜[推测] 指标 diff 类型提交降级 double】
- 分类：兼容处理
- 动机：兼容（后端指标类型体系不含独立 diff 存储类型）
- 决策：[推测] 前端展示 diff 类型；提交前转 {type: 'double', is_diff_metric: true}，详情回显时反向转换为 diff；diff 仅对 Script/JMX/Exporter/Pushgateway 开放（getMetricTypeList 白名单）
- 背景约束：metric_json 直接落后端无中间转换层；类型列表按插件类型差异化控制
- 被否决方案：无（未找到记录）
- 重新评估触发条件：后端支持 diff 类型原生存储后可取消双向转换
- 关联代码：getMetricTypeList @ bkmonitor/webpack/src/monitor-pc/pages/plugin-manager/components/indicator-dimension/utils.ts；handleTableDataChange @ components/metric-dimension-dialog.tsx
- 证据来源：无直接证据，基于提交前转换 + 回显反向转换 + typeList 白名单的结构推断