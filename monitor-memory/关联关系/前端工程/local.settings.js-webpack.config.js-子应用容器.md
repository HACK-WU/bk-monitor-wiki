---
groupPath: 关联关系/前端工程
relation: local.settings.js-webpack.config.js-子应用容器
exportedAt: "2026-10-19T06:55:58.501Z"
---
[强关联] local.settings.js 与 webpack.config.js 与 子应用容器（dev 端口契约）
强度：必改——改端口分配、代理字段名或 CORS 白名单任一处，另外两处必须连带核对；只改内部实现（不动配置字段与端口语义）不用管
原因：本地 dev 的 7001 / 7002 不是口头约定，而是三处硬编码共同锁定：portfinder 从 7001 起抢占、monitor-pc 内 13 处子应用容器硬编码 <devHost>:7002、dev server 的 Access-Control-Allow-Origin 写死 7001

配置端：
- devProxyUrl / host / port / proxy / logProxy / tenantProxy / defaultBizId @ bkmonitor/webpack/local.settings.js（已 gitignore，凭据不入库不入对话）
- webpack.config.js 对导出对象整体 Object.assign 覆盖默认值，新增字段必须两边同步

构建配置端：
- portfinder 从 devConfig.port（默认 7001）起找空端口，上限 8888 @ bkmonitor/webpack/webpack.config.js
- CORS Access-Control-Allow-Origin 写死 http://<host>:7001 @ webpack.config.js
- OPTIONS 预检本地应答（后端 Allow-Headers 不含 traceparent）@ webpack.config.js

子应用容器端：
- apm 容器 @ src/monitor-pc/pages/apm/apm.tsx
- trace 容器 10 处 @ src/monitor-pc/pages/{host,trace-retrieval,alarm-center,alarm-shield,incident,rum,rum-explore,new-report,profiling,rotation}
- fta 容器 2 处 @ src/monitor-pc/pages/fta/fta.tsx 与 utils/index.ts
- 子应用开发态 publicPath 指向自身 dev server（如 src/apm/public-path.ts）

升级约束：新增可独立调试的子应用时，必须同时改容器 host、CORS 白名单与页面映射文档 bkmonitor/webpack/wikis/local-dev.md，否则出现白屏或跨端口请求被拒