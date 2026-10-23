---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Input 输入框
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Input 输入框】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/input.md
- 使用：Vue2 全局注册，直接写 <bk-input>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：type: 输入框类型（默认 `text`）；input-style: 样式（默认 {}）；placeholder: 空白提示；disabled: 是否禁用（默认 false）；readonly: 是否只读（默认 false）；clearable: 是否可清除。**数字输入框时，此配置不生效**（默认 false）；maxlength: 最大输入长度；minlength: 最小输入长度
- 事件：change: 文本框内容变化时调用；input: 文本框输入时调用；focus: 文本框获取焦点时调用；blur: 文本框失去焦点时调用；keypress: 文本框输入按下键盘时调用
- 检索触发词：Input 输入框, bk-magic-vue, 组件, input