---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Select 下拉选框
exportedAt: "2026-10-19T08:03:17.156Z"
---
【前端组件｜Select 下拉选框】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Form/select.md
- 导入：import { Select } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：model-value / v-model: 绑定值；multiple: 是否多选（默认 false）；disabled: 是否禁用（默认 false）；size: 输入框尺寸（默认 default）；clearable: 是否可以清空选项（默认 true）；loading: 是否正在加载中（默认 false）；filterable: 是否可搜索（默认 false）；remoteMethod: 远程搜索方法
- 事件：update:modelValue: v-model事件；change: 选中值发生变化时触发；toggle: 下拉框出现/隐藏时触发；clear: 清空选项；scroll-end: 列表滚动到底部时触发
- 插槽：prefix: 前置插槽；suffix: 后置插槽；trigger: 选项插槽；extension: 下拉选项拓展插槽
- 方法：hidePopover: 隐藏Popover弹窗；showPopover: 显示Popover弹窗；setSelected: 手动设置选择的值（需要配置idKey和displayKey）
- 检索触发词：Select 下拉选框, bkui-vue, 组件, select