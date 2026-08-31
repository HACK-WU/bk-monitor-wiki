# 告警查询专家

## 一句话职责
负责「告警查询」业务域：以 `SearchAlertResource`（`alert/search`）为核心，覆盖告警列表、趋势、TopN、导出、关联事件等所有基于 ES 文档 `AlertDocument` 的只读查询能力。

## 负责的模块
- 模块根：`bkmonitor/packages/fta_web/alert/`
- 一句话职责：告警域后端，提供告警 / 事件 / 处理记录 / 反馈的查询与处理接口；本专家聚焦其中的**查询（读）路径**。

## 何时找这个专家
- 排查告警列表 / 趋势 / TopN 查不出数据、数量对不上、查询超时
- 新增 / 修改告警查询条件、排序、聚合维度
- 理解 `query_string` / `conditions` 的解析与 ES DSL 生成
- 业务鉴权（`bk_biz_ids=-1` 全业务展开、负责人可见性）
- 合并告警（Issue Merge）在查询中的 `issue_id` 展开逻辑

## 契约层就绪
`C0-使用总览` + `C1-能力契约` + `C2-使用流程` + `C5-关键决策` 就绪（C5 于 2026-08-31 补建，12 条，全部有证据；暂无 C3）。
> 与 Issue 专家共用 `add_biz_condition` / `AlertQueryHandler` 等能力：跨模块权限语义见 `.module-experts/issue专家/C5-关键决策.md` 决策 10（两处互相引用）。

## 子专家清单
无（单一业务域，未拆分）。

## 包含的资产
- 契约层（根目录，黑盒使用，无需读实现即可使用）：`C0-使用总览.md`、`C1-能力契约.md`、`C2-使用流程.md`、`C5-关键决策.md`（12 条：业务名称检索 1000 上限 / 业务可见性 fail-close / `-1` 哨兵展开 / 查询异常 fail-open / partial 完整性标识 / track_total_hits=10000 / 大小写不敏感不改 mapping / issue_id 合并展开 / assign_tags 回退 / 展示值双向翻译 / CMDB 请求合并 / 可组合管线与字段白名单）
- 实现层（白盒导航，深入模块前先看地图）：`implementation/01-架构.md`、`02-实现.md`、`03-数据流转.md`、`05-接口.md`、`06-测试.md`
- 专用技能：`skills/query-alert/`（查询告警标准步骤与排查）

## 出处
- 重建日期：2026-07-27
- 实现层基于 git commit：310f13e（源码快照；章节来源行号见各实现层文档）
