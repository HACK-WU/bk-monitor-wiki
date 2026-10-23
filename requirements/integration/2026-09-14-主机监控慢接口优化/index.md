# 主机监控慢接口优化 文件索引

> 自动生成，请勿手动编辑

## 目录结构

```
2026-09-14-主机监控慢接口优化/
├── requirement.md          # 需求分析报告（REQ-20260914-001）
└── perf/
    ├── performance-analysis.md   # 性能分析报告（5 个慢接口 + 双样本 Trace）
    └── frontend-research.md      # 前端实现与调用流程调研
```

## 文档清单

| 文件 | 类型 | 说明 |
|------|------|------|
| requirement.md | requirement | 需求文档（状态：草案，分页查询已拍板为主方案，REQ-02~09 待确认优先级） |
| perf/performance-analysis.md | performance-analysis | 性能分析报告 v3（覆盖 5 个慢接口；主接口 38357 台 26.37s vs 4551 台 3.73s 双样本差分，主瓶颈=指标路 UQ 全业务查询占 67.1%；A 路径上限约 14.2s，B 路径 3.1~5.4s 待产品评估；其余 4 接口含 topo_tree 13MB / 策略告警串行等） |
| perf/frontend-research.md | research | 前端实现与调用流程调研（2026-09-20）：Worker 三层架构、`loadData` 全链路、5 接口触发点对照；修正性能报告 2 处判断（非内存分页、首屏为 29.6s 非 max），下调 B 路径前端改造成本 |
