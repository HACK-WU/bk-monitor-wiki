---
groupPath: 专题记忆/前端专题
relation: 本地开发环境与dev-server双进程
exportedAt: "2026-10-19T08:03:15.094Z"
---
【专题记忆｜前端本地开发环境与 dev server 双进程】
- 基础要求：Node >= 20.17.0（团队实测 v22，.nvmrc 指定 22），pnpm 10.x（preinstall 强制 only-allow pnpm，旧文档的 pnpm@8 已过时）；cd bkmonitor/webpack 后 nvm use 再 pnpm i（等价 make deps）
- 双进程铁律：pnpm dev 等价 pnpm pc:dev，只启动主应用 monitor-pc；APM / Trace 系 / FTA 页面由主应用通过微前端嵌入，必须另开终端启动对应子应用
- 端口与顺序：主应用 7001、子应用 7002；webpack.config.js 用 portfinder 从 devConfig.port（默认 7001）起抢占，上限 8888；monitor-pc 内 13 处子应用容器硬编码请求 <devHost>:7002，CORS Access-Control-Allow-Origin 写死 7001；必须先启主应用再启子应用；一次只能挂一个子应用（7002 唯一），换目标先停旧的
- 页面映射：/apm → make dev-apm；/fta → make dev-fta；主机监控（新版）/ 调用链检索 / 告警中心 / 告警屏蔽 / 故障详情 / RUM / RUM 探索 / 报表 / Profiling / 轮值 → make dev-vue3；mobile / external 为独立入口
- 命令：pnpm dev / pc:dev / make dev-pc；pnpm trace:dev / apm:dev / fta:dev；pnpm mobile:dev / external:dev；pnpm i = make deps
- 其它不变式：开发态 axios baseURL 为空走同源代理；子应用 publicPath 指向自身 dev server；nodemon 监听 local.settings.js / webpack.config.js / pnpm-lock.yaml 自动重启；OPTIONS 预检由 dev server 本地应答（后端 Allow-Headers 不含 traceparent）
- 高频排查：子应用页空白或一直 loading → 7002 未启动；容器里加载到别的应用 → 启动顺序反了；端口不在 7001/7002 → lsof -i:7001 -i:7002 清占用后按序重启；接口 404 或返回 HTML → devProxyUrl 错或 proxy.context 缺前缀；主应用打不开 → hosts 未配
- 文档源：bkmonitor-dev-server/SKILL.md sha256:f55a24be；references/troubleshooting.md sha256:292269fa；bkmonitor/webpack/wikis/local-dev.md（同步 2026-10-19）
- 检索触发词：pnpm dev, 本地开发, 7001, 7002, 子应用空白, dev server, 启动顺序, hosts