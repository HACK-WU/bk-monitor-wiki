---
groupPath: 决策记录/告警分派
relation: 架构设计-条件编辑器半受控与随机key重建
exportedAt: "2026-10-14T03:12:07.453Z"
---
【决策记录｜条件编辑器半受控与随机 key 重建】
- 分类：架构设计
- 动机：优化（条件编辑含多段 tag 与多层弹层，全受控逐键上报会让父表格深层监听与 diff 在高频输入下抖动）
- 决策：[推测] 现行 CommonCondition 不在 value 变化时同步内部状态（无 value watch）；外部数据刷新统一用更换组件 key 强制重建（conditionsRenderKey / conditionsKey / conditionsSelectorKey）
- 背景约束：条件值改动必须回写宿主行数据参与差异对比与提交
- 被否决方案：旧版实现对 value 做受控同步（@Watch('value')，对照实现；无明确否决记录）
- 重新评估触发条件：出现「外部数据刷新后组件状态陈旧」的反馈累计大于等于 2 次
- 关联代码：CommonCondition @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/components/common-condition-new.tsx（对照旧版 common-condition.tsx 的 @Watch('value')）
- 证据来源：无直接证据，基于「新版删除 value watch + 全部刷新点均使用随机 key」的结构推断
- 完整上下文：.module-experts/前端专题/告警分派专家/C5-关键决策.md 决策 8