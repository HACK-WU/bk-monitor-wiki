---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Form 表单
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Form 表单】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/form.md
- 使用：Vue2 全局注册，直接写 <bk-form>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：form-type: 表单类型, 水平布局（horizontal）和垂直布局（vertical）（默认 `horizontal`）；label-width: 表单项 label 宽度（默认 150）；model: 数据；rules: 表单项验证规则；ext-cls: 配置自定义样式类名，传入的类会被加在组件最外层的 DOM `.bk-form` 上；property: 必须结合 bk-form 的 model 属性来配置，用于从整个 model 获取值，通过此值再结合校验规则进；label: 表单项 label 显示的内容；label-width: 表单项 label 宽度, 如果没有设置则使用 bk-form 的 `label-width`（默认 `150`）
- 插槽：tip: 自定表单项提示内容
- 方法：validate: 对所有的表单项进行手动触发校验；clearError: 对所有的表单项的错误提示清除
- 检索触发词：Form 表单, bk-magic-vue, 组件, form