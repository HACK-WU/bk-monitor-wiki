# 前端专题

**一句话职责**：BK-Monitor Web 前端工程（`bkmonitor/webpack`）——6 个可独立构建/启动的应用（monitor-pc 主应用 / trace / apm / fta / monitor-mobile / external）与共享包（monitor-api / monitor-common / monitor-ui / monitor-static）的功能域知识与契约聚合。

**专题范围**：`bkmonitor/webpack/`（`src/` 下 6 应用 + 共享包，约 4600 个源文件）。

**何时找这个专题**：
- 需要了解前端工程整体结构（应用划分 / 微前端 / 共享包 / 构建与本地开发）
- 接手或修改 monitor-pc 某功能域页面（先经专题定位对应专家，再进专家契约层）
- 排查前端页面问题（本地 dev 启动、路由注册、接口调用、权限、跨业务行为）
- 新增前端专家前确认既有划分与边界

**专家清单**：
- **采集专家**：数据采集配置功能域（`pages/collector-config`）——列表 / 四步新建向导 / 详情 / 增删目标 / 启停升级 / 可视化 / 执行详情，9 条路由全生命周期
- **插件管理专家**：指标插件管理功能域（`pages/plugin-manager`）——列表 / 三步新建调试发布向导 / 详情 / 指标维度设置（三条编辑器路径）/ 导入导出；与采集专家互为上下游（采集配置依赖插件选择与版本校验）
- **告警分派专家**：告警分派功能域（`pages/alarm-dispatch`）——规则组列表 / 分派规则配置（条件编辑器 / 分派动作 / 统一设置）/ 效果调试三态（全局调试 / 调试并删除 / 调试并生效）/ CSV 导入导出；与告警组（`pages/alarm-group`）互为上下游（分派目标是告警组）

**专题就绪**：`T0` 就绪（T0-专题总览.md；T1 暂无）

**包含的资产**：T0-专题总览.md + 3 个已建专家（采集专家：agent.md + C0/C1/C2/C4/C5 + implementation/ + test/；插件管理专家：agent.md + C0/C1/C2/C4/C5 + implementation/；告警分派专家：agent.md + C0/C1/C2/C4/C5 + implementation/）

**出处行**：生成日期 2026-10-13（告警分派专家 2026-10-14 增补），git commit：ff89f63ff4（前端工程资产基线）
