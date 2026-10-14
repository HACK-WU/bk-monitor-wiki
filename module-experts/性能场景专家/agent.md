# 性能场景专家

## 一句话职责
负责蓝鲸监控「主机性能 / 拓扑 / 进程状态」场景的后端聚合层，对外提供主机列表、主机详情、拓扑节点详情、拓扑进程、主机基础信息、主机指标 6 类接口的数据聚合能力；2026-09 起主机列表新增「CMDB 侧过滤分页 + 按页加载」与「页级性能卡片统计」两种形态（页级先出屏、全量后台接替）。

## 负责的模块
- 模块根：`bkmonitor/packages/monitor_web/performance`
- 以 Django DRF Resource 形式并行聚合 CMDB、Agent 状态、TSDB 性能指标、告警计数等多源数据；**自身无持久化**（`models.py` 已迁空）。

## 何时找这个专家
- 需要新增/修改主机性能列表、主机详情、拓扑节点、进程状态、主机指标等接口返回字段时
- 排查「主机列表/指标数据缺失、某字段为 None、聚合慢」等问题时
- 理解前端主机场景页、拓扑树的数据来源与聚合链路时
- 评估在 `HostPerformanceResource`（HOST 缓存）新增实时字段的缓存影响时
- 需要理解 `ThreadPool` 4 路并行聚合模式并复用到其他聚合接口时
- 需要排查「主机列表首屏慢 / 全量数据未就绪 / 翻页卡顿 / 卡片统计显示未知」时（页级加载态与前端 Worker 接替链路）
- 需要改动分享链接下的主机列表范围校验（`HostApiAuthChecker`）或新增列表类分享接口时

## 与相邻专家的边界
- **场景视图专家**（`monitor_web.scene_view`）：聚焦场景/视图/面板配置的组织与分发，性能模块为其提供主机聚合数据。
- **CMDB 资源专家**（`monitor_web.cc`）：`resource.cc.*` 的底层实现，性能模块是其消费方。
- **外部 API 集成专题 / CMDB 与容器资源专家**（`api/cmdb`）：本模块页级加载依赖的 `GetHostPage` / `GetHostIdentities` / `GetTopoTreeResource(raw)` / `GetProcess(bk_host_ids)`，以及 `TopoTree.module_links_from_raw` 均落在 `api/cmdb/*`，产权属该专题；本专家记录「性能模块如何消费这些能力 + 页级接口契约」。
- **前端主机列表数据层**（`webpack/src/trace/pages/host`）：页级/全量/卡片三条链的编排与 Worker 三级缓存在前端，不在本专家范围；本专家只固定它们的后端契约与约束。
- 本专家聚焦「主机性能/拓扑/进程的聚合逻辑」，CMDB/TSDB 查询细节转对应专家。

## 契约层就绪
C0 + C1 + C2 + C5 就绪（C5 于 2026-08-31 补建 11 条；2026-09-22 增量补建 7 条，共 18 条）

## 包含的资产
- **契约层**（根目录，黑盒使用文档）：
  - `C0-使用总览.md` — 10 项能力清单 + 9 项边界 + 16 个已知坑
  - `C1-能力契约.md` — 8 个 Resource 类契约 + 页级/统计新增契约 + 真实代码示例
  - `C2-使用流程.md` — 6 个业务目标调用路径 + 真实代码示例
  - `C5-关键决策.md` — 18 条关键决策（原 11 条 + 2026-09-22 新增 7 条：页级先出屏与全量后台接替 / 页模式响应结构兼容 / 统计单次 instant 聚合与 79.995 阈值 / 统计身份歧义返回未知 / 分享列表接口一页校验与后代节点放行 / 请求代次拒绝迟到响应 / 进程查询先筛原始服务实例）
- **实现层**（`implementation/`，白盒导航文档）：
  - `implementation/01-架构.md` — 模块结构、核心组件表、架构图、依赖分析
  - `implementation/02-实现.md` — 核心流程图、设计模式、关键类函数表、热点路径、技术债
  - `implementation/03-数据流转.md` — 数据生命周期图（含页级/全量/统计三链）、状态变换节点
  - `implementation/04-模型.md` — 无 DB 模型，描述运行时 `host_dict` 内存结构
- **专用技能**：`skills/add-host-performance-field/`（新增主机性能聚合字段的标准步骤）
- 未产出：`05-接口.md`（接口即 `views.py` 的 7 个 ViewSet 路由，已在 01/02/C1 覆盖）；`06-测试.md`（模块内无独立单测，本次新增用例位于 `bkmonitor/packages/monitor_web/tests/performance/` 与 `bkmonitor/tests/api/cmdb/`）；`07-运维.md`（无独立配置/部署文件）

## 出处
- 生成日期：2026-07-27
- git commit：916585dbb98e40c68dfa62a54713a0096c156ccf
- **增量更新：2026-09-22（PR #12574「新版主机列表按页加载与全量接替」，PR head commit `33b11cbe9e`）**
  - ⚠️ 该 PR 合入 `master` 的提交为 `fc1695a`（2026-09-21），**本机 checkout 尚未包含**（本地 HEAD `d350091733`），需 `git pull` 或 `git fetch upstream refs/pull/12574/head` 后才能对照源码。
  - 本次更新文件：`agent.md`、`C0`、`C1`、`C2`、`C5`、`implementation/01`、`implementation/02`、`implementation/03`、`.module-experts/INDEX.md`。
