# Issue 查询子专家

> 父专家：[Issue 专家](../agent.md)
> 覆盖范围：ES 查询构建、搜索结果处理、查询转换器
> 最后更新：2026-08-03
> **契约层**：已产出（C0-C4）
> **实现层**：已产出（01 / 02 / 03）

## 测试状态

- **测试位置**：`packages/fta_web/tests/issue/test_issue_trend_contract.py`（4 用例）、`packages/fta_web/tests/alert/test_issue_merge_expand.py`（10 用例）
- **测试可执行性**：✅ 大部分可跑（web 角色）；`test_issue_trend_contract.py` 1 条因前端文件缺失失败，详见 [父专家 06-测试.md](../../implementation/06-测试.md)
- **已知失败**：[父专家 test/known-failures.md](../../test/known-failures.md)

## 覆盖文件

| 文件 | 大小 | 职责 |
|------|------|------|
| `handlers/issue.py` | 56KB | `IssueQueryHandler` + `IssueQueryTransformer` |
| `resources.py` | 142KB | `SearchIssueResource` / `IssueTopNResource` / `IssueTrendResource` |
| `serializers.py` | 1.6KB | `IssueSearchSerializer` |

## IssueQueryHandler

继承 `BaseBizQueryHandler`，提供 Issue 列表的高级查询能力。

### 支持过滤条件

| 查询字段 | 类型 | 说明 |
|----------|------|------|
| `status` | keyword | 支持虚拟状态（MY_ASSIGNEE / NO_ASSIGNEE） |
| `priority` | keyword | P0/P1/P2 |
| `assignee` | keyword | 负责人 |
| `strategy_id` | keyword | 策略 ID |
| `strategy_name` | text(raw) | 策略名称 |
| `bk_biz_id` | keyword | 业务 ID |
| `labels` | keyword | 标签 |
| `fingerprint` | keyword | Issue 指纹 |
| `dimension_values.{key}` | keyword | 维度值精确过滤 |
| `impact_scope.{dimension}` | keyword | 影响范围维度过滤 |

### 时间范围语义

- `end_time` 约束 `create_time`（该时间前已创建）
- `start_time` 约束 `resolved_time`（在该时间之后才解决）
- 时间分片模式下，按 `resolved_time` 唯一归属分片，避免重复计数

### 排序

默认 `-first_alert_time, priority, status`

## IssueQueryTransformer

将前端查询参数转换为 ES DSL，负责字段映射：

| 前端字段 | ES 存储格式 |
|----------|-------------|
| `name` | `name.raw`（精确查询） |
| `strategy_name` | `strategy_name.raw`（精确查询） |
| `fingerprint` | `fingerprint`（本身是 keyword） |
| `impact_scope.{dim}` | `impact_scope.{dim}.instance_list.{id_field}`（exists 查询） |

## Issue TopN 查询

`IssueTopNResource` 支持按时间分片并行查询：
- 分片触发条件：时间跨度 > 7 天
- fields 去重：入口统一去重，防止分片合并时重复累加
- 业务权限：自动拆分 authorized / unauthorized bizs

## Issue 趋势查询

`IssueTrendResource` 按时间分片聚合 Issue 活跃/已解决趋势：
- 按 `status`（active/resolved）与 `priority` 做基数/计数聚合
- 内置 `_repair_missing_resolved_activity` 修复逻辑

## 新增搜索维度指南

1. 在 `IssueQueryTransformer.QUERY_FIELD_MAP` 中注册 `QueryField`
2. 确保 ES 索引中存在对应字段
3. 全文搜索（title/description）走 `query` 字段的 `query_string`

## 包含的资产

| 类型 | 文件 | 说明 |
|------|------|------|
| 契约层 | [C0-使用总览.md](C0-使用总览.md) | 能力清单、边界、已知问题、子专家导航 |
| 契约层 | [C1-能力契约.md](C1-能力契约.md) | `IssueQueryHandler` / `IssueQueryTransformer` / 三个 Resource 的公开契约与示例 |
| 契约层 | [C2-使用流程.md](C2-使用流程.md) | Issue 列表查询、TopN 聚合、趋势查询三条流程 |
| 契约层 | [C4-数据流向与消费.md](C4-数据流向与消费.md) | 查询结果与聚合统计的来源/去向/消费方/用途 |
| 实现层 | [implementation/01-实现.md](implementation/01-实现.md) | 现有实现要点速览 |
| 实现层 | [implementation/02-实现.md](implementation/02-实现.md) | 核心算法、查询转换模式、热点路径、关键类函数、技术债 |
| 实现层 | [implementation/03-数据流转.md](implementation/03-数据流转.md) | 查询请求生命周期、时间分片逻辑、结果合并与异常降级 |
