---
feature: BK_DATA 数据源 collect_interval 动态最小值
status: 已确认
created: 2026-06-08
---

# 需求摘要：BK_DATA 数据源 collect_interval 动态最小值

## 核心诉求
告警策略汇聚周期的最小值需要基于数据源的实际计算/采集频率动态限制。对于 BK_DATA 数据源，该频率来自 BKBase 结果表的 `count_freq` 与 `count_freq_unit`。

## 需求形态
真实需求。无需新增字段或接口，复用现有 `collect_interval` 字段，补齐 BK_DATA 数据源的值设置逻辑即可。

## 核心场景
- **场景 1**：运维人员在 BK Monitor 告警策略页面选择 BK_DATA 数据源，前端根据 `collect_interval` 自动限制汇聚周期最小值，避免配置过短周期导致数据无效。

## 根本性分析结论
- **核心问题**：`BkdataMetricCacheManager.get_metrics_by_table` 未设置 `collect_interval`，导致 BK_DATA 指标使用默认值 `1`，前端最小限制失效。
- **方案评估**：情况 A（方案对症）。`collect_interval` 本身就是设计用来表示采集/计算周期的，其他数据源已正确使用，只需补齐 BK_DATA 的映射。
- **建议**：短期实现即可，无需长期替代方案。

## 需求清单

| 优先级 | 需求 ID | 需求描述 | 验收标准 |
|--------|---------|----------|----------|
| P0 | REQ-01 | `BkdataMetricCacheManager.get_metrics_by_table` 的 `base_dict` 中设置 `collect_interval`，值为 `count_freq` 按 `count_freq_unit` 换算后的秒数 | `MetricListCache` 中 BK_DATA 指标的 `collect_interval` 等于换算后的秒数 |
| P1 | REQ-02 | `count_freq` 为 `None` 或 `0` 时，使用默认值 `1` | 无效 `count_freq` 不导致异常，降级为 `1` |

## 关键假设

| 假设 | 验证状态 |
|------|----------|
| 前端已基于 `collect_interval` 限制 `agg_interval` 最小值 | 待验证（由前端确认） |
| `count_freq` 与 `count_freq_unit` 在 BKBase API 中总是同时返回 | 已验证（API 实测 + Mock 数据） |

## 非功能性约束
- 指标缓存定期同步，换算逻辑在缓存更新时执行，不影响查询性能
- `collect_interval` 单位保持为秒，与其他数据源语义一致

## 潜在风险
- `count_freq_unit` 返回值为空或非预期字符串时需有降级处理
- `month` 单位换算建议统一按 30 天（2592000 秒）
- `count_freq` 为 `0` 在部分结果表中可能出现（如截图所示），需正确处理

## 相关代码位置
- `bkmonitor/packages/monitor_web/strategies/metric_list_cache.py` — `BkdataMetricCacheManager.get_metrics_by_table`
- `bkmonitor/bkmonitor/models/metric_list_cache.py` — `collect_interval` 模型定义
