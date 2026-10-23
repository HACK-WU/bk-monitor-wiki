---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Table 表格
exportedAt: "2026-10-19T08:03:17.156Z"
---
【前端组件｜Table 表格】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Data/table.md
- 导入：import { Table } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：data: 显示的数据；columns: 表格列的配置描述，具体项参考IColumn；stripe: 是否为斑马纹 Table（默认 false）；active-column: 当前选中列,当设置选中多列时（columnPick = multi），配置为数组[index1, index2；column-pick: 表格列选中方式,支持：（默认 禁用（disabled））；height: 设置表格高度,auto 根据行数自动填充高度, 100%，依赖初始化时父级容器高度（默认 auto）；min-height: 设置表格最小高度（默认 LINE_HEIGHT * 2）；max-height: 设置表格最大高度（默认 auto，依赖外层高度）
- 事件：row-click: 当某一行被点击时会触发该事件；row-dblclick: 当某一行被双击时会触发该事件；cell-click: 当表格单元格被点击时会触发该事件, cell 提供`getValue`方法，用于获取当前单元格内容；cell-dblclick: 当表格单元格被双击时会触发该事件, cell 提供`getValue`方法，用于获取当前单元格内容；row-expand: 当用户对某一行展开或者关闭的时候会触发该事件
- 插槽：#prepend: 插入至表格第一行之前的内容，会被固定在第一行；#expandRow: 展开收起一行；#expandCell: 自定义展开收起单元格；#expandContent: 自定义展开收起单元格内容（展开收起ICON内置）
- 方法：clearSelection: 用于多选表格，清空用户的选择；getSelection: 用于多选表格，获取用户的选择；toggleRowSelection: 用于多选表格，切换某一行的选中状态，如果使用了第二个参数，则是设置这一行选中与否（selected 为 tru；toggleAllSelection: 用于多选表格，切换所有行的选中状态
- 检索触发词：Table 表格, bkui-vue, 组件, table