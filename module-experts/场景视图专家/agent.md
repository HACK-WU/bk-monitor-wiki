# 场景视图专家

## 一句话职责
掌握蓝鲸监控「场景视图（scene_view）」后端：场景(scene)与视图(view)的定义、CRUD、面板(panel)配置聚合，以及内置场景处理器（host / kubernetes / uptime_check / apm / custom_metric / alert 等 10 种）与表格列格式化框架。

## 负责的模块
- 模块根：`bkmonitor/packages/monitor_web/scene_view/`
  - 对外通过 `SceneViewViewSet`（ResourceViewSet）暴露 76 条路由，处理场景/视图读写、面板数据、各类内置场景（主机/K8s/拨测/APM/自定义指标/告警）的详情与列表接口。
- 关联数据模型：`bkmonitor/packages/monitor_web/models/scene_view.py`（`SceneModel` / `SceneViewModel` / `SceneViewOrderModel`）。

## 何时找这个专家
- 要新增 / 修改某个场景（scene_id）的内置视图或面板配置
- 要新增 / 调整 `SceneViewViewSet` 的接口（Resource 路由）
- 要理解「DB 视图行 + 内置 JSON 配置」如何合并渲染出 panel
- 要扩展表格类接口（分页/排序/筛选/格式化，基于 `PageListResource` + `TableFormat`）
- 排查视图列表、面板数量计算、默认视图创建/删除同步相关问题
- 需要理解 `BuiltinProcessor` 抽象契约与按 scene_id 分发机制
- 要使用主机进程列表接口或理解其 4 路并发 TSDB 聚合模式

## 与相邻专家的边界
- **性能场景专家**（`monitor_web/performance`）：聚焦主机性能聚合 Resource，不含场景视图定义框架。
- **UnifyQuery 查询专家**：场景视图取数时会调用 UnifyQuery，取数细节归它。
- 本专家聚焦「视图/面板配置的组织与分发」，取数与告警查询细节转对应专家。

## 契约层就绪
C0 + C1 + C2 就绪

## 包含的资产
- **契约层**（根目录，黑盒使用文档）：
  - `C0-使用总览.md` — 能力清单 + 边界 + 已知问题与常见坑
  - `C1-能力契约.md` — 12 个公开类/方法契约 + 真实代码示例
  - `C2-使用流程.md` — 4 个业务目标调用路径 + 真实代码示例
- **实现层**（`implementation/`，白盒导航文档）：
  - `implementation/01-架构.md` — 模块结构、核心组件、架构图、依赖分析
  - `implementation/02-实现.md` — 核心流程、设计模式、关键类、热点路径、技术债
  - `implementation/03-数据流转.md` — 数据生命周期、状态变换、异步流
  - `implementation/04-模型.md` — 数据模型、DB schema、序列化契约
- **专用技能**：`skills/add-builtin-scene-view`（新增/修改内置场景视图配置）
- 未产出：`05-接口.md`（接口即 `views.py` 的 Resource 路由，已在 01/02/03 覆盖）；`06-测试.md`（模块内无独立单测目录）；`07-运维.md`（无独立配置/部署文件）

## 出处
- 生成日期：2026-07-27
- git commit：ca831622ca4f6dee5598449f78506d2f37bdafef
