---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Pagination 分页
exportedAt: "2026-10-19T08:03:17.156Z"
---
【前端组件｜Pagination 分页】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Data/pagination.md
- 导入：import { Pagination } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：model-value / v-model: -（默认 当前页码）；count: 数据总数（默认 0）；limit: 每页显示条数(须存在于limit-list中)；limit-list: 每页显示条数可选项列表（默认 [10, 20, 50, 100]）；show-limit: 是否显示每页显示条数控件（默认 true）；type: 组件外观类型；align: 分页控件位置，优先级高于location（默认 left）；location: 每页显示条数控件位置（默认 right）
- 事件：change: 当前页码变化时的回调；limit-change: 当前分页尺寸变化时的回调
- 检索触发词：Pagination 分页, bkui-vue, 组件, pagination