---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Pagination 分页
exportedAt: "2026-10-19T08:03:17.158Z"
---
【前端组件｜Pagination 分页】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/pagination.md
- 使用：Vue2 全局注册，直接写 <bk-pagination>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：count: 总数据量；current: 当前页码，正整数，支持`.sync`修饰符；limit: 每页显示条数(须存在于`limit-list`中) ，支持`.sync`修饰符；limit-list: 每页显示条数可选项列表（默认 [10, 20, 50, 100]）；show-limit: 是否显示每页显示条数控件（默认 true）；location: 每页显示条数控件位置（默认 right）；align: 分页控件位置，优先级高于location（默认 left）；type: 组件外观类型（默认 default）
- 事件：change: 当前页码变化时的回调；limit-change: 当前分页尺寸变化时的回调
- 检索触发词：Pagination 分页, bk-magic-vue, 组件, pagination