---
groupPath: 专题记忆/前端组件库
relation: PrimaryTable
exportedAt: "2026-10-19T08:03:17.158Z"
---
【前端组件｜PrimaryTable】
- 本质：封装 tdesign PrimaryTable，蓝鲸增强的核心载体
- 关键能力：bkUiSettings 列设置（传入即在最右追加齿轮列）、@bk-ui-settings-change 事件、#bkUiAppearanceSettings 插槽、needCustomScroll 自定义滚动条、列 filter.type = single | multiple 自定义筛选浮层
- ref 方法：见 references/table-bk-enhancements.md「ref 暴露的方法」
- 内置列 key（不参与列设置）：见文档「内置列 key」节
- 常见误区：把 bkUiSettings 写成原生 columnController；在 BaseTable 上找蓝鲸增强；同时使用 TableColumn 与 columns 数组（columns 优先）
- 文档源：.codebuddy/skills/blueking-tdesign-ui/references/table-bk-enhancements.md
- 检索触发词：PrimaryTable, tdesign-ui, 蓝鲸表格