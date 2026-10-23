---
groupPath: 专题记忆/前端专题
relation: traceVue3写法与公共包API
exportedAt: "2026-10-19T08:03:15.095Z"
---
【专题记忆｜trace（Vue3）写法与公共包 API】
- 适用范围：仅 src/trace；100% TSX，无 .vue SFC、无 <script setup>；defineComponent + setup + render；Vue Router 4 + createWebHashHistory；Pinia；bkui-vue 2.x + @blueking/tdesign-ui
- 组件：props 对象声明，复杂 props 抽 XXX_PROPS + PropType；emits 用对象形式（带校验）；setup 返回值在 render 里通过 this.xxx 访问；响应式默认 shallowRef（eslint 规则 monitor-vue3/no-ref），需要深响应用 ref as deepRef 或 deepRef
- 状态：Option Store（app / authority 等基础 store）与 Setup Store 并存；新代码用 Setup Store，可直接用 shallowRef 控制粒度；组件里 useXxxStore() 后自动 unwrap 可直接赋值
- 路由：router/router.ts 聚合 + router/modules/*.ts；router/router-config.ts 只是顶栏导航元数据；trace 路由基本不写 meta，权限/导航通过 store + router-config + provider；微前端下同样拼 parentRoute
- UI：按需 import { Dialog, Sideslider, Select, Message, Exception, Pagination } from 'bkui-vue'；表格优先 import { PrimaryTable } from '@blueking/tdesign-ui'；CSS 在 index.ts 全局引入 tdesign 样式；根组件用 ConfigProvider 注入 locale；指令 bkTooltips / clickoutside 在 directive/index.ts 注册；不要 Vue.use
- i18n：createI18n({ legacy: true, messages: mergeI18nJson() })，语言包来自 monitor-pc；组件内 useI18n().t；非 setup 用 window.i18n.t
- API：优先按模块具名 import（import { traceDetail } from 'monitor-api/modules/apm_trace'）；兼容层 $api 仅用于按字符串动态调度；trace 无 $http
- 公共包：monitor-api 的 base.ts 是 request(method, url) 工厂，modules/*.js 一行一个接口，api.ts 用 require.context 自动聚合，新增模块文件无需注册；request 第二参数默认 needBiz=true、needMessage=true、needCancel=false、isAsync=false、needRes=false、needTraceId=true、reject403=false；GET 总是自动注入 bk_biz_id 且内部强制 needMessage=false；needCancel 用 method_url 作 key
- monitor-common / monitor-ui / monitor-static：优先复用 mergeSpaceList / setGlobalBizId / getBizRouteHref / downloadFile / formatPercent / getCookie / deepClone / getUrlParam / DOCS_LINK_MAP 等；monitor-ui 以 Vue2 为主，trace 只复用无 Vue 实例绑定的纯 TS（chart-plugins/typings、monitor-echarts/valueFormats、constants）
- 权限：Vue2 用 authorityMixinCreate(map) + this.authority.VIEW_AUTH，路由 meta.authority 守卫校验；Vue3 用 useAuthorityStore + getAuthorityMap
- 文档源：bkmonitor-dev/references/vue3-trace.md sha256:9f8d71e2；references/shared-and-api.md sha256:8fffc787（同步 2026-10-19）
- 检索触发词：trace, Vue3, Pinia, shallowRef, PrimaryTable, monitor-api, request 配置, monitor-common, authority