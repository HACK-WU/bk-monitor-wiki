# 插件管理专家

**一句话职责**：BK-Monitor 前端「指标插件管理」功能域专家——monitor-pc 指标插件的全生命周期前端实现：列表（tab 分类/搜索/排序/删除/导入导出/官方标记）、三步新建/编辑/升级向导（定义插件 → 插件调试 → 完成发布）、插件详情、指标&维度设置。

**负责的模块**：
- `bkmonitor/webpack/src/monitor-pc/pages/plugin-manager/`（41 个源文件）
- 关联契约面：路由 `bkmonitor/webpack/src/monitor-pc/router/integrated/plugin-manager.ts`（6 条）；请求层 `monitor-api/modules/model.js`（collector_plugin 系列）+ `modules/plugin.js` + `commons.js`/`strategies.js`；Vuex `store/modules/plugin-manager.js`

**何时找这个专家**：
- 修改/排查插件列表、三步向导（定义/调试/发布）、插件详情、指标维度编辑器（三条实现路径）
- 理解插件生效链路（两阶段提交 `saveMetric/pluginRegister`（token）→ `releaseCollectorPlugin`；异步注册轮询；调试轮询）
- 排查导入冲突（`conflict_ids` 五级）、公共插件双重权限、draft 草稿态分流
- 改动 `collector_plugin` / `saveMetric` / `pluginRegister` / `release` 等接口的前端消费方
- 新增插件类型 / 新增指标维度入口 / 调整权限点

**契约层就绪**：C0 + C1 + C2 + C4 + C5 就绪

**所属专题**：前端专题（[T0-专题总览](../T0-专题总览.md)）

**子专家**：无

**包含的资产**：
- 契约层（根目录）：`C0-使用总览.md`、`C1-能力契约.md`、`C2-使用流程.md`、`C4-数据流向与消费.md`、`C5-关键决策.md`
- 实现层（`implementation/`）：`01-架构.md`、`02-实现.md`、`03-数据流转.md`、`04-模型.md`、`05-接口.md`、`06-测试.md`

**测试状态**：❌ 该模块无测试——`bkmonitor/webpack/tests/` 无 plugin-manager 专测（7 个含 "plugin" 字样的测试文件已逐一核实均属其它模块），未产出 `test/known-failures.md`；e2e 无入库用例（详见 `implementation/06-测试.md`）

**关联专家**：
- 采集专家（下游消费方）——采集配置复用本模块 `MANAGE_AUTH`（`PLUGIN_MANAGE_AUTH`）、`pluginUpgradeInfo`、插件详情/新建跳转；反向强关联见 ki `关联关系/采集配置`

**出处行**：生成日期 2026-10-13，git commit：ff89f63ff4（资产基线）
