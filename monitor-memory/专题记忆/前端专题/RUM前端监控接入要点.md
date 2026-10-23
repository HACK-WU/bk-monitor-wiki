---
groupPath: 专题记忆/前端专题
relation: RUM前端监控接入要点
exportedAt: "2026-10-19T08:03:15.097Z"
---
【专题记忆｜RUM 前端监控（@blueking/open-telemetry）接入要点】
- 定位：浏览器上报 SDK，基于 OpenTelemetry Web SDK，把页面访问、接口请求、静态资源、JS 错误、Web Vitals、白屏、设备、会话、用户动作统一转成 RUM Span，通过唯一 OTLP HTTP Trace 通道上报 collector；不创建 Metric / Log Provider
- 心智模型：单一 Trace 信号（计数 / 直方图 / 分位数 / 错误分组 / 跨事件聚合由服务端完成）；内置采集统一放 tracking（View、请求、资源、错误、Web Vitals、Action 等），Fetch/XHR 由 SDK 自有请求生命周期 patch，统一创建 browser.resource CLIENT Span；扩展放 extensions.plugins 与 extensions.instrumentations，使用 SDK 私有 provider 并遵循 Consent 生命周期
- 会话级确定性采样：session.sampleRate（0-1，默认 1）不是单 Span 级，由 application.name + session.id 的稳定 hash 决定，同一 Session 所有 Span 决定一致；未命中时数据不导出，reportAction / reportCustomEvent 会被静默丢弃；调试时临时设 sampleRate: 1 和 debug: true
- 运行时上下文：user.id（业务方提供，SDK 原样透传、不 hash 不脱敏）、session.id（生成 / 轮换）、view.*（View 管理器维护）、活动窗口内 action.id；运行中 setUser() 更新用户，手动 View 用 startView() 划界、setViewName() 改名
- 归一字段：span_type（session/view/resource/vital/error/long_task/action/websocket/custom）、outcome.type（success/warning/error/timeout/abort）、可选 outcome.reason；子类由 resource.type、vital.metric、error.source 等领域字段表达
- 最小接入：new BkOpenTelemetry({ application: { name, environment, version }, transport: { endpoint, token }, context: { user: { id } } })；endpoint 是上报根地址，可以含网关前缀但不要包含最终 /v1/rum（SDK 去尾斜杠后自动追加）；token 作为 Authorization: Bearer <token>；默认 autoStart: true 异步启动，要确保首个手动事件不丢则 autoStart: false + await start()
- 默认开启：Session、View；内置采集 request、action、resource、error、webVitals、blankScreen、device；View Loading Time 默认开启；默认关闭按需打开 longTask、cspViolation、websocket；关闭默认能力显式设 false
- 易错点：单实例（fetch/xhr/action/websocket patch 全局 API，同页只初始化一个，微前端只在主应用初始化一次）；use() / useInstrumentation() 必须在 start() 之前（要注册插件就 autoStart: false 再手动 start）；采样影响手动上报；手动事件不排队（异步 autoStart 未建立 View 时立即调用可能被过滤）；隐私要业务显式配置（URL、属性通过 privacy / request.beforeSend 处理，SDK 不采集 HTTP Body，user.id 需 hash 要在传入前处理，tracking.beforeSend 新写入字段不会再次经过 redactAttributes）；Consent 未授权用 privacy.trackingConsent: 'not-granted'，授权后 setTrackingConsent('granted')，撤销会停止采集并解除 patch；低基数路由用 tracking.view.getUrlTemplate 与 tracking.request.getUrlTemplate，默认已折叠数字 ID / UUID / 长十六进制段；手动 View 必须先 await start() 建立 Session 再 startView()；Action 默认 nameCollection: 'explicit' 只读 data-bk-action-name，设 text 才读可访问名称和 DOM 文本
- 文档源：bk-rum-otele/SKILL.md sha256:f3eb5cb8；references/ 下 22 个主题文档（同步 2026-10-19）
- 检索触发词：RUM, open-telemetry, BkOpenTelemetry, OTLP, 采样, 白屏, Web Vitals, 隐私脱敏, Consent