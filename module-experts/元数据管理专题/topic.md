# 元数据管理专题

> **专题标识**: `元数据管理专题`
> **创建时间**: 2026-07-28
> **模块路径**: `bk-monitor-base/src/bk_monitor_base/metadata/`
> **专题路径**: `.module-experts/元数据管理专题/`

---

## 专题范围

本专题覆盖 bk-monitor 监控平台的**元数据管理模块**（metadata），是监控系统的核心基础设施，负责数据源管理、结果表管理、存储引擎配置、空间隔离、自定义上报、数据链路编排、任务调度与运维、API 接口等全链路元数据治理。

## 专家列表

| # | 专家名 | 覆盖范围 | 子专家数 | 批次 |
|---|--------|---------|---------|------|
| 1 | 元数据核心模型 | data_source, result_table, common, entity_relation | 2 | Batch 1 |
| 2 | 存储与数据链路 | storage, data_link, es_snapshot, influxdb_cluster, vm/ | 2 | Batch 1 |
| 3 | 空间与自定义上报 | space/, custom_report/, record_rule/ | 2 | Batch 1 |
| 4 | 任务调度与运维 | task/, management/commands/, dataflow/, health_check | 0 | Batch 2 |
| 5 | API与工具库 | resources/, utils/, service/, bcs/ | 2 | Batch 2 |
| 6 | 元数据种子数据与数据字典 | data/ 种子数据文件 + 加载机制 | 0 | Batch 4 |

## 创建信息

- **创建方式**: expert-team skill 专题机制（三级结构：专题 → 专家 → 子专家）
- **分批策略**: 5 批执行（Batch 0 架构先行 → Batch 1 三专家并行 → Batch 2 两专家并行 → Batch 3 汇总 → Batch 4 种子数据专家）
- **预计总产出**: ~118 份文档
- **详细计划**: 见 [PLAN.md](PLAN.md)

## 参考文档

- [元数据管理模块 Wiki](/root/bk-monitor/bk-monitor-wiki/wiki/核心模块架构/元数据管理模块/元数据管理模块.md)
- [元数据模型设计 Wiki](/root/bk-monitor/bk-monitor-wiki/wiki/核心模块架构/元数据管理模块/元数据模型设计/元数据模型设计.md)
- [元数据服务层 Wiki](/root/bk-monitor/bk-monitor-wiki/wiki/核心模块架构/元数据管理模块/元数据服务层/元数据服务层.md)
- [元数据任务调度 Wiki](/root/bk-monitor/bk-monitor-wiki/wiki/核心模块架构/元数据管理模块/元数据任务调度.md)
- [元数据资源接口 Wiki](/root/bk-monitor/bk-monitor-wiki/wiki/核心模块架构/元数据管理模块/元数据资源接口.md)
