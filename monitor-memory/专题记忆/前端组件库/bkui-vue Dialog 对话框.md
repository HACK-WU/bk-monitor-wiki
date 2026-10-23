---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Dialog 对话框
exportedAt: "2026-10-19T08:03:17.156Z"
---
【前端组件｜Dialog 对话框】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Feedback/dialog.md
- 导入：import { Dialog } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：is-show: 是否显示弹框（默认 false）；title: 弹框的标题；width: 自定义对话框宽度（默认 480）；close-icon: 是否显示右上角的关闭 icon（默认 true）；esc-close: 是否允许 esc 按键关闭弹框（默认 true）；show-mask: 是否允许出现遮罩（默认 true）；quick-close: 是否允许点击遮罩关闭弹框（默认 true）；transfer: 控制弹框是否出现在 body 内（默认 true）
- 事件：update:isShow: 更新关闭状态；closed: 点击 取消，右上角的关闭 icon 或 按 esc 触发；hidden: 弹框关闭；shown: 弹框弹出
- 插槽：header: 头部插槽（显式传空内容时不渲染头部区域）；default: 内容插槽；footer: 底部插槽；tools: 工具栏插槽，顶部区域
- 检索触发词：Dialog 对话框, bkui-vue, 组件, dialog