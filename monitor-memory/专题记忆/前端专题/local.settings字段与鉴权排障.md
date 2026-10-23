---
groupPath: 专题记忆/前端专题
relation: local.settings字段与鉴权排障
exportedAt: "2026-10-19T08:03:15.095Z"
---
【专题记忆｜local.settings.js 字段与鉴权排障】
- 文件：bkmonitor/webpack/local.settings.js，已 gitignore；禁止提交、禁止整文件读入对话、禁止手改
- 字段：devProxyUrl（代理的后端环境地址，默认 appdev 环境）、host（dev server 监听域名，需 hosts 指向 127.0.0.1）、port（起始端口，一般不要设，端口由启动顺序决定）、proxy（监控平台代理，context 命中前缀转发）、logProxy（日志平台代理）、tenantProxy（租户平台代理）、defaultBizId（未带 bizId 时的默认业务 ID，默认 2）
- 最小骨架：const context = ['/apm','/rest','/fta','/weixin','/version_log','/calendars','/alert','/query-api']；changeOrigin=true；secure=false；devProxyUrl='<环境地址>'；host='appdev.<环境域>'；proxy.headers 里 host / referer 由 devProxyUrl 推导，X-CSRFToken 与 Cookie 留空由脚本或用户填写；defaultBizId 从 Cookie 的 bk_biz_id 提取或默认 2
- 生成与检查：node .codebuddy/skills/bkmonitor-dev-server/scripts/setup-config.js --url "<环境地址>" 生成骨架；无参运行输出 CONFIG_VALID 或 CONFIG_INVALID:CONFIG_NOT_FOUND / URL_NOT_CONFIGURED / COOKIE_NOT_CONFIGURED / TOKEN_NOT_CONFIGURED；--force true 会清空已填凭据
- 鉴权刷新：接口 401 / 403、bk_token 过期时跑 sync-local-auth.js；默认优先剪贴板（可 --clipboard），否则打开临时浏览器读登录态（--browser），写入后若 nodemon 在跑会自动重启；--dry-run 只检查不写；脚本不接受凭据参数
- 排障：401/403 → 刷新鉴权；502/504 → 检查 devProxyUrl 可达性与协议（缺 http:// 或末尾多斜杠会错）；404 或返回 HTML → context 缺前缀；打不开 → hosts 未配；编译报错 → 语法 / 类型 / 导入；CORS → 确认 changeOrigin=true 与 host header；请求 canceled → 组件卸载取消 / needCancel / 超时
- 凭据规则：Cookie、X-CSRFToken、bk_token 不进对话、不进命令行、不进 shell history；用户贴了明确拒用；日志只打印掩码值
- 文档源：bkmonitor-dev-server/SKILL.md sha256:f55a24be；references/local-auth.md；references/troubleshooting.md sha256:292269fa（同步 2026-10-19）
- 检索触发词：local.settings.js, devProxyUrl, Cookie, X-CSRFToken, 401, 403, hosts, 鉴权刷新, proxy.context