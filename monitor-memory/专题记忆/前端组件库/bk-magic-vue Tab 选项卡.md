---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Tab 选项卡
exportedAt: "2026-10-19T08:03:17.158Z"
---
【前端组件｜Tab 选项卡】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/tab.md
- 使用：Vue2 全局注册，直接写 <bk-tab>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：active: 当前显示的选项卡名称，支持`sync`修饰符；type: 选项卡样式（默认 `border-card`）；tab-position: 选项卡位置（默认 `top`）；closable: 是否可关闭选项卡（默认 `false`）；addable: 是否可新增选项卡（默认 `false`）；sortable: 标签是否可拖拽排序（默认 `false`）；sort-type: 标签拖拽排序的方式（默认 `replace`）；label-height: 选项卡label的高度（默认 50）
- 事件：tab-change: 选项卡切换时调用；close-panel: 关闭选项卡时调用；add-panel: 新增选项卡时调用；sort-change: 标签拖动交互位置后调用；on-drag-tab: 标签拖动时调用
- 插槽：setting: 插入至选项卡右上角的扩展内容；add: 自定义新增按钮；extension: 自定义扩展内容（紧接选项卡之后，新增按钮之前）；label: 替换默认显示的选项卡文案的内容，当内容需要动态改变时，请选择使用`render-label`配置
- 检索触发词：Tab 选项卡, bk-magic-vue, 组件, tab