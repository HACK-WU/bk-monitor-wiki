# 告警分派专家

**一句话职责**：BK-Monitor 前端「告警分派」功能域专家——monitor-pc 告警自动分派的配置与管理前端实现：规则组列表（搜索/新建/行内编辑/调试并删除）、分派规则配置（匹配条件编辑器 / 分派动作 / 通知升级 / ITSM 流程套餐 / 等级与标签 / 统一设置 / 查找替换 / 批量编辑 / CSV 导入导出）、效果调试三态（全局调试 / 调试并删除 / 调试并生效）。

**负责的模块**：
- `bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/`（16 个 ts/tsx 源文件，9390 行）
- 关联契约面：路由 `router/manager/alarm-dispath.ts`（2 条，注意文件名拼写）；菜单 `router/router-config.ts`；请求层 `monitor-api/modules/model.js`（assign 系列）+ `modules/assign.js`；权限 `authority-map.ts`
- 跨应用复用：`fta-solutions/pages/alarm-dispatch/*`（独立壳 + 同构路由，复用本模块页面组件与 authority-map）

**何时找这个专家**：
- 修改/排查告警分派列表页（规则组搜索/懒渲染/优先级算法/内置组保护）与配置页（变更追踪/批量操作/统一设置/导入导出）
- 理解「分派规则为什么这样生效」——调试并生效的整组提交链路、`matchDebug` 与 `batchUpdate` 的一致性约定
- 排查条件编辑器问题（字段/值选项装载 `allKVOptions` 12 路、策略维度联动、通知人员远程搜索、只读模式）
- 改动 `fta/assign/*` 接口消费方 / 提交体结构（`RuleData.getSubmitParams`）/ `settings.public_conditions` 语义
- 从告警组页、告警流转记录跳转规则组的入口问题（`query.groupName` / `query.group_id` 契约）
- 删除链路、离开拦截（`isRuleChange`）与内置组（`edit_allowed`）行为排查

**契约层就绪**：C0 + C1 + C2 + C4 + C5 就绪

**所属专题**：前端专题（[T0-专题总览](../T0-专题总览.md)）

**子专家**：无

**包含的资产**：
- 契约层（根目录）：`C0-使用总览.md`、`C1-能力契约.md`、`C2-使用流程.md`、`C4-数据流向与消费.md`、`C5-关键决策.md`
- 实现层（`implementation/`）：`01-架构.md`、`02-实现.md`、`03-数据流转.md`、`04-模型.md`、`05-接口.md`、`06-测试.md`

**测试状态**：❌ 该模块无测试——`bkmonitor/webpack/tests/` 22 个测试文件中 0 个覆盖本模块（10 组直接关键词全 0 命中，宽口径命中逐一核验后均属其它模块），e2e 无入库用例；按 skill 规则不产出 `test/known-failures.md`（详见 `implementation/06-测试.md`）

**关联模块**：
- `pages/alarm-group`（告警组）——分派目标实体；复用 `AlarmGroupDetail` 详情抽屉与权限常量；告警组页「相关分派规则」反向跳入本模块
- `fta-solutions`（FTA 应用）——双壳复用本模块页面组件，改动需双端回归
- 告警中心（trace / fta 流转记录）——`?group_id=` 直接入口；调试命中告警的跳转出口

**出处行**：生成日期 2026-10-14，git commit：ff89f63ff4（资产基线）
