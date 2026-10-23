---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue 组件库使用总则
exportedAt: "2026-10-19T08:03:17.155Z"
---
【前端组件库｜bk-magic-vue（Vue2）】
- 定位：基于蓝鲸 MagicBox + Vue2 的组件库，标签前缀 bk-*；权威文档按组件拆分在 .codebuddy/skills/bk-magicbox-vue-components/references/<组件>.md
- 注册：monitor-pc 在 common/import-magicbox-ui.ts 里 Vue.use(bkMagicVue, { zIndex: 3000 }) 全局注册；apm / fta-solutions 不重复引入，import 'monitor-pc/common/import-magicbox-ui' 复用
- 调用：消息提示 this.$bkMessage({ theme, message })，弹窗 this.$bkInfo(...)；组件直接用 <bk-button> / <bk-table> / <bk-dialog>
- 使用纪律：props / events / slots / methods 以 references 文档为准，文档没有的属性就是不存在
- 组件索引分类：基础（Color/Font/Icon/Button/Link/Transition）、布局（Grid/ResizeLayout）、导航（Navigation/Tab/Steps/Breadcrumb）、数据（Table/Tree/Pagination/Tag）、表单（Form/Input/Select/Cascader/Upload/DatePicker）、反馈（Dialog/Message/Notify/Popover/Sideslider）
- 本项目用法：monitor-pc / apm / fta-solutions（Vue2）使用；monitor-mobile 不用 bk-magic-vue，改用 Vant 2
- 检索触发词：bk-magic-vue, magicbox, Vue2 组件, bk-select, bk-table, $bkMessage