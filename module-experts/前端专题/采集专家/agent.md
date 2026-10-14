# 采集专家

**一句话职责**：BK-Monitor 前端「数据采集配置」功能域专家——monitor-pc 采集配置的全生命周期前端实现：列表（统计/搜索/轮询）、四步新建/编辑/克隆向导、采集详情（独立页 + 列表侧滑）、增删目标、启停/升级/回滚、可视化视图、执行详情、删除（含级联删策略）。

**负责的模块**：
- `bkmonitor/webpack/src/monitor-pc/pages/collector-config/`（约 106 个文件）——采集配置功能域页面与组件
- 关联契约面：路由 `bkmonitor/webpack/src/monitor-pc/router/integrated/collector-config.ts`（9 条路由）；请求层 `bkmonitor/webpack/src/monitor-api/modules/collecting.js`（33 个方法）

**何时找这个专家**：
- 修改/排查采集配置列表、新建向导、详情、增删目标、启停/升级、可视化、执行详情页面
- 理解采集页面的数据流（列表 5s 轮询、下发等待、`is_task_ready` 就绪门闩、竞态防护）
- 排查跨业务采集配置的可见性与只读行为（#12736 语义）
- 改动 `rest/v2/collecting_config/*` 接口的前端消费方（影响面反查）
- 新增采集类型 / 新增流程步骤 / 新增采集相关权限点

**契约层就绪**：C0 + C1 + C2 + C4 + C5 就绪

**所属专题**：前端专题（[T0-专题总览](../T0-专题总览.md)）

**子专家**：无

**包含的资产**：
- 契约层（根目录）：`C0-使用总览.md`、`C1-能力契约.md`、`C2-使用流程.md`、`C4-数据流向与消费.md`、`C5-关键决策.md`
- 实现层（`implementation/`）：`01-架构.md`、`02-实现.md`、`03-数据流转.md`、`04-模型.md`、`05-接口.md`、`06-测试.md`
- 测试状态：`test/known-failures.md`

**测试状态**：⚠️ 部分可跑——`bkmonitor/webpack/tests/` 采集专测 3 文件 28 用例（node:test 直跑源码）；`collector-detail-back`（5）与 `collector-detail-isolation`（12）实测全绿；`collector-cross-business`（11）受根 `node_modules` 的 vue-router 链接漂移影响全数失败（强制解析 3.6.5 后 11/11 通过，属环境问题）。详见 `implementation/06-测试.md` 与 `test/known-failures.md`

**关联专家**：插件管理专家（已创建）——采集配置依赖插件选择与 `checkPluginVersion` 版本校验，插件本体管理（CRUD/调试/发布/指标维度）由该专家承接

**出处行**：生成日期 2026-10-13，git commit：ff89f63ff4（资产基线）
