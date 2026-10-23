---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Input 输入框
exportedAt: "2026-10-19T08:03:17.155Z"
---
【前端组件｜Input 输入框】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Form/input.md
- 导入：import { Input } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：type: 输入框类型（默认 text）；placeholder: 空白提示（默认 Enter）；disabled: 是否不可用（默认 false）；readonly: 是否只读（默认 false）；prefix: 前缀字符，当配置prefix slot时失效（默认 false）；suffix: 后缀字符，当配置suffix slot时失效（默认 false）；clearable: 是否可清除。数字输入框时，此配置不生效；maxlength: 最大输入长度
- 事件：update:modelValue: 更新modelValue值；focus: 获取焦点时触发事件；blur: 失去焦点时触发事件；change: 值变更时触发事件；clear: 清空值时触发事件
- 插槽：prefix: 前置插槽；suffix: 后置插槽
- 方法：focus: 组件聚集；blur: 失去焦点；clear: 清空内容
- 检索触发词：Input 输入框, bkui-vue, 组件, input