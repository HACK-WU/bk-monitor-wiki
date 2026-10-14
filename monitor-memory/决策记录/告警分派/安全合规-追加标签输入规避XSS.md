---
groupPath: 决策记录/告警分派
relation: 安全合规-追加标签输入规避XSS
exportedAt: "2026-10-14T03:12:07.453Z"
---
【决策记录｜追加标签输入规避 XSS】
- 分类：安全合规
- 动机：避坑：追加标签的 key/value 为用户输入自由文本，曾作为 tooltip 选择器参与渲染，存在 XSS 注入风险
- 决策：追加标签输入框的 tooltip-key 固定为不可能字符串 __null__，使真实标签值不进入 tooltip 选择器
- 背景约束：标签值自由输入且会进入 tooltip 渲染路径（列表页「修改告警内容」列与批量编辑）
- 被否决方案：无（注释只说明改法）
- 重新评估触发条件：底层 tooltip 组件修复 key 注入问题（届时方可移除该防御常量）
- 关联代码：alarm-dispatch-config.tsx 与 components/alarm-batch-edit.tsx 中的 tooltip-key='__null__' @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/
- 证据来源：代码注释原文「这里有xss注入问题 改成一个不可能字符串字段」
- 完整上下文：.module-experts/前端专题/告警分派专家/C5-关键决策.md 决策 6