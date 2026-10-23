---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Dialog 对话框
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Dialog 对话框】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/dialog.md
- 使用：Vue2 全局注册，直接写 <bk-dialog>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：value: 是否显示弹框，支持 `v-model` 双向绑定（默认 false）；title: 弹框的标题，不设置 `title` 和 `slot header` 可配置出无 `header` 的弹框；render-directive: 弹框的渲染方式（默认 `show`）；ok-text: 确定按钮的文字；cancel-text: 取消按钮的文字；theme: 颜色 按钮类型（默认 `primary`）；position: 设置层的位置，接收 `top`, `left` 两个属性。；width: 弹框的宽度，支持数字和百分比（默认 400）
- 事件：confirm: 点击确定按钮触发的事件；cancel: 点击取消按钮触发的事件，主动调用关闭才会触发，通过改变双向绑定的值关闭弹框时不会触发；value-change: 弹框显示状态变化的回调函数；after-leave: 弹框消失的动画结束后触发的回调函数
- 插槽：匿名插槽: 没有名字的插槽，会被渲染到dialog的主体上；header: title部分的插槽，dialog头部区域；footer: 确认和取消按钮部分的插槽，dialog底部区域；tools: 工具栏插槽，顶部区域
- 检索触发词：Dialog 对话框, bk-magic-vue, 组件, dialog