---
groupPath: 专题记忆/前端组件库
relation: tdesign-ui 组件库使用总则
exportedAt: "2026-10-19T08:03:17.155Z"
---
【前端组件库｜@blueking/tdesign-ui（Vue3）】
- 定位：蓝鲸基于 tdesign-vue-next 的二次封装，核心增量是表格；文档在 .codebuddy/skills/blueking-tdesign-ui/references/
- 导出：PrimaryTable（= Table 别名）、EnhancedTable（树形/可编辑）、TableColumn（声明式列）、BaseTable（直接透传 tdesign）、Button 系列；Pagination 源码存在但当前未导出
- 核心要点：蓝鲸增量只在 PrimaryTable / EnhancedTable 上生效，BaseTable 不含增强；列设置用 bkUiSettings（不是原生 columnController），配套事件 @bk-ui-settings-change；声明式列用 <TableColumn>，与 columns 数组二选一（同时存在时 columns 优先）；列 filter.type = single | multiple 启用蓝鲸筛选浮层
- 类型：PrimaryTableProps / EnhancedTableProps / TableProps = CommonTableProps & 原生 Props
- 安装：peerDependency vue ^3；样式随入口自动引入（src/vue3.ts 内 import theme）
- 本项目用法：src/trace 表格优先 PrimaryTable；虚拟滚动只在 host 指标表格与 failure 告警详情两处硬开，不要无脑开启
- 检索触发词：tdesign-ui, PrimaryTable, EnhancedTable, TableColumn, bkUiSettings, 蓝鲸表格