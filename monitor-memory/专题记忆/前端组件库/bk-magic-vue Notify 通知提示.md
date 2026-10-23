---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Notify 通知提示
exportedAt: "2026-10-19T08:03:17.158Z"
---
【前端组件｜Notify 通知提示】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/notify.md
- 使用：Vue2 全局注册，直接写 <bk-notify>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：theme: 组件主题色（默认 primary）；icon: 组件左侧图标（默认 info）；title: 组件的标题；message: 组件显示的文字内容，支持字符串或用 `this.$createElement` 生成的 DOM 片段；position: 组件出现的方向（默认 top-center）；delay: 组件延时关闭时间，值为 0 时需要手动关闭（默认 5000）；dismissable: 是否显示右侧关闭 icon（默认 true）；limit: 组件个数限制，默认不限制个数，设置为 0 时，清除所有实例
- 方法：close: 关闭当前的组件
- 检索触发词：Notify 通知提示, bk-magic-vue, 组件, notify