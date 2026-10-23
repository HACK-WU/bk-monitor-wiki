---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Table 表格
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Table 表格】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/table.md
- 使用：Vue2 全局注册，直接写 <bk-table>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：data: 显示的数据；height: Table 的高度，默认为自动高度。如果 height 为 Number 类型，单位 px；如果 height；max-height: Table 的最大高度；stripe: 是否为斑马纹 Table（默认 false）；border: 是否带有边框（默认 false）；dark-header: 是否是深色表头模式（默认 false）；custom-header-color: 自定义表头颜色，设置了此选项后，dark-header将会失效（默认 ''）；custom-header-color-hover: 自定义表头Hover的颜色，设置了此选项后，dark-header将会失效（默认 ''）
- 事件：select: 当用户手动勾选数据行的 Checkbox 时触发的事件；select-all: 当用户手动勾选全选 Checkbox 时触发的事件；selection-change: 当选择项发生变化时会触发该事件；cell-mouse-enter: 当单元格 hover 进入时会触发该事件；cell-mouse-leave: 当单元格 hover 退出时会触发该事件
- 插槽：prepend: 插入至表格第一行之前的内容；append: 插入至表格最后一行之后的内容，如果需要对表格的内容进行无限滚动操作，可能需要用到这个 slot。若表格有合计行
- 方法：clearSelection: 用于多选表格，清空用户的选择；toggleRowSelection: 用于多选表格，切换某一行的选中状态，如果使用了第二个参数，则是设置这一行选中与否（selected 为 tru；toggleAllSelection: 用于多选表格，切换所有行的选中状态；toggleRowExpansion: 用于可展开表格，切换某一行的展开状态，如果使用了第二个参数，则是设置这一行展开与否（expanded 为 tr
- 检索触发词：Table 表格, bk-magic-vue, 组件, table