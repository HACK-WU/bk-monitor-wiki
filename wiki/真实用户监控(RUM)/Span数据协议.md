# RUM Span 数据协议

<cite>
**本文引用的文件**
- [packages/rum_web/docs/spec/span/span.md](file://bkmonitor/packages/rum_web/docs/spec/span/span.md)
- [constants/rum.py](file://bkmonitor/constants/rum.py)
- [rum/models/datasource.py](file://bkmonitor/rum/models/datasource.py)
</cite>

## 目录
1. [简介](#简介)
2. [公共字段](#公共字段)
3. [Span 类型（span_type）](#span-类型span_type)
4. [关键 Attributes](#关键-attributes)
5. [Resource 与 Status](#resource-与-status)
6. [完整规范](#完整规范)
7. [性能考虑](#性能考虑)
8. [故障排查指南](#故障排查指南)

## 简介
RUM 采集数据以 OpenTelemetry Span 形式上报，由 `resource.telemetry.sdk.language = webjs`、`resource.rum.provider = blueking` 标识为蓝鲸前端 Web JS SDK 数据。完整字段定义见源码规范文件 `packages/rum_web/docs/spec/span/span.md`，本文为速览。

章节来源
- [packages/rum_web/docs/spec/span/span.md:1-26](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L1-L26)
- [constants/rum.py:117-125](file://bkmonitor/constants/rum.py#L117-L125)

## 公共字段
顶层核心字段：`app_name`、`bk_biz_id`、`trace_id` / `span_id` / `parent_span_id`、`span_name`、`kind`（Span 类型，0-5）、`start_time` / `end_time` / `elapsed_time`（微秒）、`time`（ES 写入标记）、`status`（`code` + `message`）、`attributes`（属性集）、`resource`（资源信息）、`events`（事件，error 时存在）、`links`。

章节来源
- [packages/rum_web/docs/spec/span/span.md:7-25](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L7-L25)

## Span 类型（span_type）
共九种，决定专属字段：

| span_type | 含义 | 常见 span_subtype |
|-----------|------|-------------------|
| `document` | 文档加载 | navigate / document_fetch |
| `route` | 路由切换 | pushState / replaceState / popstate / hashchange |
| `resource` | 静态资源 | script / link / img / css / fetch / xhr / iframe … |
| `http` | HTTP / API | fetch / xhr / beacon / sendbeacon |
| `longtask` | 长任务 | script / layout / paint / unknown |
| `action` | 用户交互 | click / input / keydown / scroll / submit / custom |
| `vital` | Web 指标 | lcp / fcp / cls / inp / fid / ttfb |
| `error` | 错误 | js / promise / resource_load / blank_screen / csp / network / cors / console / custom |
| `custom` | 自定义 | websocket / 自定义 |

章节来源
- [packages/rum_web/docs/spec/span/span.md:36-138](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L36-L138)

## 关键 Attributes
- **Web Vitals（vital.metric）**：`lcp` / `fcp` / `cls` / `inp` / `ttfb`，评级 `good` / `needs-improvement` / `poor`。LCP 额外含 `lcp.target`（DOM 选择器）、`lcp.url`（资源 URL）、`lcp.time_to_first_byte` 等，用于定位首屏瓶颈。
- **错误（error）**：`error.handled`、`error.source`（window.error / resource / unhandledrejection）、`exception.fingerprint` / `message` / `stacktrace` / `type`，白屏（blank_screen）含 `score` / `detected` / `dom_node_count`，CSP 含 `blocked_uri` / `violated_directive`。
- **页面/路由**：`rum.page.host` / `rum.page.path`、`view.id` / `view.url` / `view.loading_type`（`initial_load` / `route_change`）、`trace_scene`（`page_load` / `route_change` / `user_action` / `startup`）。
- **设备/网络**：`device.mobile` / `device.platform` / `device_type`、`network.effective_type` / `network.rtt` / `network.downlink`、`browser.screen/viewport`。

章节来源
- [packages/rum_web/docs/spec/span/span.md:33-116](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L33-L116)
- [packages/rum_web/docs/spec/span/span.md:193-338](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L193-L338)

## Resource 与 Status
- **Resource**：`resource.service.name`（同应用名）、`resource.service.version`、`resource.deployment.environment.name`、`resource.rum.provider = blueking`、`resource.telemetry.sdk.language = webjs`。
- **Status**：`status.code`（0 未设置 / 1 正常 / 2 异常），`status.message` 仅在异常时存在。

章节来源
- [packages/rum_web/docs/spec/span/span.md:117-133](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L117-L133)

## 完整规范
字段级逐项定义（含各 span_type 专属字段、device/network/session/user_agent/view 分组、websocket 插件等）请直接查阅源码规范：

- [packages/rum_web/docs/spec/span/span.md](file://bkmonitor/packages/rum_web/docs/spec/span/span.md)

存储侧对应字段映射见 `RUM_FIELD_LIST` 与 `RUM_RESULT_TABLE_OPTION`（查询时间字段 `end_time`）。

章节来源
- [constants/rum.py:49-191](file://bkmonitor/constants/rum.py#L49-L191)
- [rum/models/datasource.py:316-363](file://bkmonitor/rum/models/datasource.py#L316-L363)

## 性能考虑

- **采集端计算与限流**：Apdex 计算（`apdex_calculator/rum_apdex_common`）与 QPS 限流（`rate_limiter/token_bucket`）在 bk_collector 端完成，后端不接触上报流量，避免接入压力上扬。
- **采样控制**：`sampler:percentage` 与 Web Vitals 采样可下调前端上报量，高流量应用建议开启以控制 ES 写入与成本。
- **字段膨胀**：`attributes`/`resource` 为动态 object 字段，长期运行需关注 mapping 膨胀；异常事件（`events`）仅在 error 时出现，天然削峰。

章节来源
- [rum/core/application_config.py:96-188](file://bkmonitor/rum/core/application_config.py#L96-L188)
- [constants/rum.py:49-191](file://bkmonitor/constants/rum.py#L49-L191)

## 故障排查指南

- **数据未上报**：确认前端 SDK 设置 `resource.telemetry.sdk.language=webjs`、`resource.rum.provider=blueking` 以被正确识别为蓝鲸 RUM 数据；检查接入 Token 鉴权。
- **字段缺失 / 查不到**：以 `packages/rum_web/docs/spec/span/span.md` 完整规范为准，确认 `RUM_FIELD_LIST` 字段映射与 `RUM_RESULT_TABLE_OPTION` 时间字段 `end_time`；ES 动态 mapping 下新字段可能延迟索引。
- **Apdex 不产出**：确认 `apdex:apdex_view_load` / `apdex:apdex_api_request` 配置与 T 值；`predicate_value=documentLoad` 需前端确有 documentLoad span。

章节来源
- [packages/rum_web/docs/spec/span/span.md:1-338](file://bkmonitor/packages/rum_web/docs/spec/span/span.md#L1-L338)
- [rum/core/application_config.py:96-188](file://bkmonitor/rum/core/application_config.py#L96-L188)
