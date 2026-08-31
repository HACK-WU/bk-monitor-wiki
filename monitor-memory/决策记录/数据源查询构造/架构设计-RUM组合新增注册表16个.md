---
groupPath: 决策记录/数据源查询构造
relation: 架构设计-RUM组合新增注册表16个
exportedAt: "2026-08-31T02:15:35.032Z"
---
【决策记录｜数据源查询构造 注册表演进：RUM 两个组合新增，当前实际 16 个组合（专家资产原记 14 已过期）】
- 分类：架构设计
- 动机：可维护性（RUM 复用 APM Trace 的检索链路，不重复实现）
- 决策：2026-08 新增两个注册组合，均继承 BkApmTraceDataSource 复用其检索能力：BK_RUM 加 LOG 映射到 BkRumDataSource、BK_RUM 加 TIME_SERIES 映射到 BkRumTimeSeriesDataSource。load_data_source 当前注册 16 个类共 16 个组合，而本专家资产的 C0 速查矩阵与 C1 映射表仍记 14 个未含 RUM 两项，已过期
- 背景约束：RUM（前端性能与用户体验监控）的数据形态与 APM Trace 一致，复用父类可少写一套检索实现
- 被否决方案：为 RUM 独立实现数据源类，无相关记录；从继承结构看复用 APM Trace 是明确的复用意图
- 已知代价：专家资产 C0、C1 与实现层的组合数与路径矩阵已过期，使用时须以 load_data_source 源码为准
- 重新评估触发条件：新增数据源类型时必须同步更新 load_data_source 列表与专家资产的映射表
- 关联代码：BkRumDataSource 与 BkRumTimeSeriesDataSource @ data_source/data_source/__init__.py；GrayUnifyQueryDataSources 含 BK_RUM 加 LOG @ constants/data_source.py
- 证据来源：代码实现（类定义与 load_data_source 注册列表）；commit 2067bb6ca8（RUM 基础检索模块开发）、f8d1c56245、b093b8e7d7、6c28913271
- 完整上下文：.module-experts/数据源查询构造专家/C5-关键决策.md 决策 7