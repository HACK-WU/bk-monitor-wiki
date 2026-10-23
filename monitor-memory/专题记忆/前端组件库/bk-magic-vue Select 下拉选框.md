---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Select 下拉选框
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Select 下拉选框】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/select.md
- 使用：Vue2 全局注册，直接写 <bk-select>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：value: 当前被选中的值，支持 `v-model`；multiple: 是否多选（默认 false）；display-tag: 是否将选择的结果以标签的形式显示，仅当开启`multiple`时生效（默认 false）；auto-height: 下拉框高度是否自动撑开，当开启`display-tag`时生效（默认 true）；is-tag-width-limit: 是否对标签进行宽度限制，超出显示`...`（默认 true）；collapse-tag: 当以标签形式显示选择结果时，是否合并溢出的结果以数字显示（默认 true）；show-select-all: 是否显示全选选项，仅当开启`multiple`时生效（默认 false）；scroll-height: 下拉列表滚动高度（默认 216）
- 事件：selected: 选择列表时调用，多选时，回调参数均为数组；toggle: 切换下拉折叠状态时调用；change: 选项发生变化时调用；clear: 清空已选项时调用；tab-remove: 删除tab时触发
- 插槽：extension: 固定在下拉列表最后的内容；trigger: 可用于自定义选框的触发者,作用域插槽参数为该组件的props中的属性；search: 可用于自定义搜索区域,作用域插槽参数为该组件的props中的属性
- 检索触发词：Select 下拉选框, bk-magic-vue, 组件, select