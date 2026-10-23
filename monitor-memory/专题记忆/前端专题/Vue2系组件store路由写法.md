---
groupPath: 专题记忆/前端专题
relation: Vue2系组件store路由写法
exportedAt: "2026-10-19T08:03:15.095Z"
---
【专题记忆｜Vue2 系（monitor-pc / apm / fta-solutions）写法】
- 技术栈：Vue 2.x + TypeScript + TSX + vue-property-decorator + vue-tsx-support + Vue Router 3 + Vuex 3（vuex-module-decorators）+ bk-magic-vue
- 组件模板：新建优先 *.tsx + 同名 *.scss；@Component({ name }) 类组件；声明 IXxxProps / IXxxEvents 接口；@Prop / @Ref / @Watch / @Emit / @Provide / @InjectReactive；render() 手写 JSX，class='...'（不是 className）；复杂组件用 Mixins（如 authorityMixin）；历史 .vue 文件跟随其原有风格
- 状态管理：新模块用 vuex-module-decorators，多数 dynamic: true；monitor-pc 旧 JS 模块（require.context 自动注册，state + mutations + SET_XXX 字符串常量）与新 decorators 并存，改旧模块跟随旧风格；apm 全部 decorators；fta-solutions 静态 + dynamic 混用
- 路由：router/router.ts 聚合 + beforeEach（鉴权、SET_NAV_ID）；router/<domain>/index.ts 按域拆分；router/router-config.ts 是侧栏导航树配置（IRouteConfigItem：id/name/route/path/href/children），与 vue-router routes 是两回事；路由项用 components: { noCache: () => import(...) } 或 component 懒加载 + webpackChunkName；meta 常用 title、navId（必备）、authority.page、noNavBar、noCache、pageCls、route.parent；微前端下 path 统一拼 __BK_WEWEB_DATA__?.parentRoute 前缀
- UI：monitor-pc 在 common/import-magicbox-ui.ts 里 Vue.use(bkMagicVue, { zIndex: 3000 }) 全局注册；apm / fta 不重复引入，import 'monitor-pc/common/import-magicbox-ui' 复用；消息 this.$bkMessage({ theme, message })，弹窗 this.$bkInfo(...)
- 微前端入口：index.ts 区分独立运行 / 子应用；子应用分支挂 Vue.prototype.$bus / $api / $http / $authorityStore；monitor-pc/apm 用 __POWERED_BY_BK_WEWEB__ 判断，fta 用 __BK_WEWEB_APP_KEY__
- monitor-mobile 异类：Vue2 但用 SFC(.vue) + Vant 2，无 bk-magic-vue；Vuex 静态注册、无 authority 模块；路由全部内联在 router/router.ts，无 router-config.ts；无微前端；独立 i18n（zh-cn / en）；只依赖 monitor-common / monitor-static
- 文档源：bkmonitor-dev/references/vue2-packages.md sha256:2aaeb4a0（同步 2026-10-19）
- 检索触发词：Vue2, TSX, vue-property-decorator, Vuex, vuex-module-decorators, router-config, monitor-mobile, Vant