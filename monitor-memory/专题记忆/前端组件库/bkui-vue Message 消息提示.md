---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Message 消息提示
exportedAt: "2026-10-19T08:03:17.156Z"
---
【前端组件｜Message 消息提示】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Feedback/message.md
- 导入：import { Message } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：theme: 组件主题色（默认 primary）；message: 组件显示的文字内容，如果需要高阶用法，请查看IMessage说明；delay: 组件延时关闭时间，值为 0 时需要手动关闭（默认 常规模式3000，高阶模式8000）；dismissable: 是否显示右侧关闭 icon（默认 true）；offsetY: 组件出现时距离视口顶部的偏移量（默认 30）；spacing: 多个组件之间的垂直距离（默认 10）；extCls: 配置自定义样式类名，传入的类会被加在组件最外层的 DOM .bk-message 上；onClose: 关闭组件时的回调函数, 参数为组件实例
- 插槽：#action: 操作项插槽，可以覆盖默认操作项列表，完全自定义，如果启用此插槽，IMessageActions 相关配置将不再；#title: 操作项描述，默认格式 【错误码】错误概述 + 操作建议（面向用户）（默认 `【message.code】${mes）
- 检索触发词：Message 消息提示, bkui-vue, 组件, message