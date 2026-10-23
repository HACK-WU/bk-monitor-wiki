---
groupPath: 专题记忆/前端专题
relation: bk-weweb微前端用法与陷阱
exportedAt: "2026-10-19T08:03:15.096Z"
---
【专题记忆｜bk-weweb 微前端框架用法与陷阱】
- 包：@blueking/bk-weweb；主应用入口 import 一次即自动注册自定义元素 bk-weweb 到 window.customElements；全局配置用默认导出 weWeb.start({ collectBaseSource, webComponentTag, fetchSource })
- 两种模式：mode='app'（默认，HTML 入口，解析并执行 script/style 渲染进容器）与 mode='js'（必须显式，JS 入口，执行 JS 并调用导出对象的 render(container, data)）；不写 mode 按微应用处理，微模块漏写 mode 会加载失败
- 两种用法：声明式 <bk-weweb id url>（连 DOM 自动加载，移出自动卸载）与 Hooks API loadApp / loadInstance / mount / unmount / activated / deactivated / unload / preLoadApp / preLoadInstance / preLoadSource；简单嵌入用标签，需要非标准时序、精确隔离、预加载、KeepAlive、容器复用或多框架编程式集成用 Hooks，推荐优先 Hooks
- 陷阱 1：微应用标签的 scopeJs 语义取反（不写开启沙箱，写 scopeJs 或 ="true" 关闭）；精确控制用 Hooks loadApp({ scopeJs: false })；微模块标签不取反
- 陷阱 2：微应用标签的 scopeCss 不能单独控制，由是否启用 Shadow DOM 决定（scopeCss = !setShadowDom）；要在不开 Shadow DOM 时关闭样式作用域用 Hooks
- 陷阱 3：默认值不同——微应用 scopeJs=true / scopeCss=true / scopeLocation=false / setShadowDom=false / keepAlive=false / showSourceCode=false；微模块 scopeJs=true / scopeCss=true / setShadowDom=false / keepAlive=false / showSourceCode=true
- 陷阱 4：<bk-weweb> 只监听 url 属性变化（observedAttributes），改其它属性连接后不生效
- 陷阱 5：mount / activated 是异步的（nextTask 微任务），不要假设同步完成，需要挂载后做事用回调参数
- 陷阱 6：必须先 await loadApp / loadInstance 再 mount，未加载就 mount 静默无效
- 陷阱 7：微模块必须导出含 render(container, data) 的对象；框架不会用 render 返回值做清理，清理方法需自行导出（如 destroy）并在卸载前调用
- 陷阱 8：Vite 子应用 dev 模式以 ESM 运行，必须在子应用 vite.config.ts 接入 @blueking/bk-weweb/vite/helper，且 appKey 与主应用加载的 id 一致
- 陷阱 9：子应用资源必须允许跨域（CORS），框架用 fetch 拉 HTML/JS，被拦截会静默白屏（内部失败兜底返回空字符串而非抛错）
- 通信：主到子用 data（标签是 JSON 字符串，Hooks 直接传对象），子应用读 window.__BK_WEWEB_DATA__；子到主 / 主到模块用微模块导出对象方法，通过 mount 回调第二参数获取；主到子全局通道是真实 window（子应用经 window.rawWindow），谨慎使用；子应用感知环境用 window.__POWERED_BY_BK_WEWEB__
- 三种卸载：unmount(id) 清空容器 + 失活沙箱 + 保留缓存；deactivated(id) 视 keepAlive 保留容器 + 失活沙箱 + 保留缓存；unload(url) 不清容器 + 不失效沙箱 + 删除缓存（传缓存键，微应用即 url）；强制热更新顺序 unmount → unload → loadApp → mount
- 文档源：bk-weweb/SKILL.md sha256:64321b36（同步 2026-10-19）
- 检索触发词：bk-weweb, 微前端, scopeJs, scopeCss, setShadowDom, loadApp, mount, KeepAlive, Vite 插件, CORS 白屏