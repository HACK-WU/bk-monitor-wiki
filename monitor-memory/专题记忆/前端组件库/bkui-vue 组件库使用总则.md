---
groupPath: 专题记忆/前端组件库
relation: bkui-vue 组件库使用总则
exportedAt: "2026-10-19T08:03:17.155Z"
---
【前端组件库｜bkui-vue（Vue3）】
- 定位：蓝鲸 BlueKing Vue3 基础组件库，标签前缀 bk-*；权威文档按组件拆分在 .codebuddy/skills/bkui-vue-components/references/<分类>/<组件>.md
- 导入：按需 import { Button, Input, Select, Dialog, Message } from 'bkui-vue'；不要像 Vue2 那样全局 Vue.use
- 样式：随组件按需加载；根组件用 ConfigProvider 注入 locale；指令 bkTooltips / clickoutside 在 directive/index.ts 注册
- 使用纪律：props / events / slots / methods 必须查对应 reference，文档中没有的属性就是不存在，禁止凭记忆臆造
- 组件索引分类：Base（Button/Icon）、Layout（Grid/ResizeLayout）、Nav（Tab/Menu/Steps/DatePicker/TimePicker 等）、Data（Table/Tree/Pagination/Tag 等）、Form（Form/Input/Select/Cascader/Upload 等）、Feedback（Dialog/Message/Notify/Popover/Sideslider 等）
- 本项目用法：仅 src/trace（Vue3）使用；表格优先 @blueking/tdesign-ui 的 PrimaryTable，弹窗/侧栏/表单/消息用 bkui-vue
- 检索触发词：bkui-vue, 蓝鲸组件, Vue3 组件, bk-button, bk-table, 按需引入