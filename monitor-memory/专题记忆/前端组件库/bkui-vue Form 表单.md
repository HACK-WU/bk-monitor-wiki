---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Form 表单
exportedAt: "2026-10-19T08:03:17.156Z"
---
【前端组件｜Form 表单】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Form/form.md
- 导入：import { Form } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：form-type: 表单模式；label-width: 表单域标签的宽度；label-position: 表单域标签的位置；model: 表单数据；rules: 表单验证规则；item-type: 表单项布局模式；label: 标签；label-width: 表单域标签的宽度
- 事件：submit: 表单提交；validate: Form Item 校验结束后触发
- 插槽：label: 自定义表单项 label；error: 自定义表单项验证错误信息
- 方法：validate: 触发表单校验；getValidateResult: 只获取表单校验结果，不会标记错误表单项；clearValidate: 触发表单校验
- 检索触发词：Form 表单, bkui-vue, 组件, form