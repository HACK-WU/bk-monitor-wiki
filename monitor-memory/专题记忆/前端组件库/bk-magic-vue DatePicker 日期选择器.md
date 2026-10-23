---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue DatePicker 日期选择器
exportedAt: "2026-10-19T08:03:17.158Z"
---
【前端组件｜DatePicker 日期选择器】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/date-picker.md
- 使用：Vue2 全局注册，直接写 <bk-datepicker>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：type: 类型（默认 date）；value: 日历组件的值，可以是 Date 或字符串或数组，只有在 daterange 和 datetimerange 类；editable: 设置文本框是否可编辑（默认 true）；format: 格式（默认 date: yyyy-MM-dd <br）；readonly: 是否只读（默认 false）；disabled: 是否禁用（默认 false）；clearable: 是否可清空（默认 true）；open: 控制日历面板的显示与隐藏（默认 false）
- 事件：change: 日期改变事件，参数为当前选择的日期以及当前日历组件的类型；clear: 日历面板点击清空事件，无参数；open-change: 日历面板弹出或收起事件，参数为日历面板展开收起的状态；pick-success: 日历面板选择日期后，点击确定选择成功的事件，无参数；shortcut-change: 快捷项改变事件
- 插槽：trigger: 可用该插槽配合`open`属性，自定义日期选择器的展示；footer: 可用该插槽，自定义日期选择器 footer 的展示；header: 可用该插槽，自定义日期选择器 header 的展示；shortcuts: datetimerange、daterange类型可用该插槽，自定义时间范围选择器快捷选项区域的展示
- 检索触发词：DatePicker 日期选择器, bk-magic-vue, 组件, date-picker