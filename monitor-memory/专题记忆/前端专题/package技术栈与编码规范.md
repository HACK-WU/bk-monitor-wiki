---
groupPath: 专题记忆/前端专题
relation: package技术栈与编码规范
exportedAt: "2026-10-19T08:03:15.095Z"
---
【专题记忆｜前端 package 技术栈与编码规范】
- 第一步永远是定位 package：目标文件属于哪个 src/* 子包，决定用 Vue2 还是 Vue3、用哪套 store / UI / 组件写法，禁止混用
- 包速查：monitor-pc = Vue2，TSX class 为主（250 个 .vue / 589 个 .tsx），Vuex + vuex-module-decorators，bk-magic-vue，微前端主壳兼子应用；apm = Vue2，100% TSX class；fta-solutions = Vue2，TSX class；monitor-mobile = Vue2 SFC(.vue)，Vant 2，无微前端；trace = Vue3，100% TSX defineComponent + setup + render，Pinia，bkui-vue + @blueking/tdesign-ui；monitor-api = 无框架 request() 工厂；monitor-common = 纯工具；monitor-ui = 以 Vue2 为主；monitor-static = 图标 / SVG
- external 不是独立 package：是 monitor-pc 用 APP=external 构建的变体（条件编译只留 dashboard），改 external 即改 src/monitor-pc，不要找 / 新建 src/external
- 全局硬规则：不混用 Vue2/Vue3 语法（defineComponent / Pinia / useI18n 只属于 trace；@Component / Vuex / this.$t 属于 Vue2 包）；不引入 qiankun（微前端是 @blueking/bk-weweb）；不写 debugger；不加 licensed 头；可见文案走 i18n 不硬编码中文（调试占位除外）
- 命名与格式：文件名 kebab-case、组件 PascalCase、SCSS 类名 kebab-case、样式文件与组件同名；缩进 2 空格、行宽 120、单引号、必加分号、LF；import 排序由 eslint-plugin-perfectionist 自动处理，不手排
- 路径别名：包内 @ / @router / @store / @page / @static；跨包 @api → src/monitor-api、@common → src/monitor-common（仅 webpack 别名，tsconfig 无），更稳妥用 workspace 包名 monitor-api / monitor-common / monitor-ui / monitor-static
- 工具链：biome 负责格式化 + 基础 lint（noDebugger 为 error，organizeImports 关闭）；eslint 补 perfectionist 排序与 Vue 规则；stylelint 管样式（recess-order、禁 vendor prefix、优先主题变量）；pre-commit 跑 lint-staged
- 提交规范：commit-msg 钩子（webpack/verify-commit.js）校验 subject 1-50 字符；新格式 <type>(<scope>): <subject>，type 属于 feat / fix / docs / style / refactor / perf / test / chore；旧格式 feature / bugfix / minor / optimization / sprintfix / merge 仍兼容；Merge branch 放行；分支命名 {type}/{category}/#{TAPD_ID}，基线 upstream/master
- 路由组件一律懒加载：() => import(/* webpackChunkName: "X" */ '...')
- 文档源：bkmonitor-dev/SKILL.md sha256:550c2f49；references/conventions-and-workflow.md sha256:a3bc68c5；bkmonitor/webpack/AGENTS.md（同步 2026-10-19）
- 检索触发词：Vue2, Vue3, trace, monitor-pc, 技术栈, 命名规范, import 排序, commit message, 分支命名, external, 路径别名