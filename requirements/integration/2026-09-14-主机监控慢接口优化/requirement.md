---
id: REQ-20260914-001
feature: 新版主机监控慢接口优化
status: 草案
created: 2026-09-14
updated: 2026-09-14
version: 1
tags: [integration, perf, host, search_host_metric, 分页查询]
depends_on: []
author: AI
document_type: requirement
---

# 需求报告：新版主机监控慢接口优化

- **需求 ID**：REQ-20260914-001
- **状态**：草案（分页查询已拍板为主方案，其余项待确认优先级）
- **分类**：integration / 性能优化
- **依据**：2026-09-11 接口性能截图 + Trace 实证 + 2026-09-14 代码调研（行号均经代码核对）

## 1. 背景与问题

新版主机监控页面在业务主机规模大（截图业务 DFM 主机数 38478）时，页面加载与刷新显著缓慢。DevTools 实测（2026-09-11 截图）：

| 接口 | 后端视图（Resource） | 耗时 | 体积 | 主要成因（代码定位） |
|------|------|------|------|------|
| `search_host_metric` | `SearchHostMetricResource`（`performance/resources.py:400`） | 21.80s | 861KB | 见第 2 节专项分析（核心问题） |
| `get_topo_tree` | `GetTopoTree`（`commons/cc/resources/frontend_resources.py:24`，底层 `CCTopoTreeResource`，API 缓存每分钟刷新） | 9.31s | 12.9MB | 全业务拓扑树每次全量返回，树中聚合字段（监控覆盖/告警数等）非首屏必需，但每次全量随行 |
| `get_strategy_and_event_count` | `GetStrategyAndEventCountResource`（`scene_view/resources/view.py:695`） | 8.43s | 0.2KB | 串行执行两个重查询：① `get_strategy_list_v2` 策略计数（DB 聚合）② `search_alert` 告警计数（ES 查近1h未屏蔽异常 total） |
| `search_host_info` | `SearchHostInfoResource`（`performance/resources.py:312`） | 7.76s | 645KB | CMDB 全量主机 + 全量 topo_tree（已并行）后逐台组装 module 拓扑链接信息 |
| `get_host_or_topo_node_detail` | `GetHostOrTopoNodeDetailResource`（`scene_view/resources/host.py:102`） | 2.90s | 0.6KB | 节点详情：CMDB 拓扑树 + 主机列表 + 策略计数 + 告警计数多段串行 |
| `fetch_febot_info` | （本仓库无对应实现） | 3.95s | 1.0KB | 站点级外部服务，非本需求范围，建议转运维确认 |
| `managinfo/` | — | 70ms | 0.6KB | 正常 |

**总结**：页面总耗时被 `search_host_metric`（`SearchHostMetricResource`，21.8s）主导；`get_topo_tree`（`GetTopoTree`，12.9MB）是传输与前端解析的次要负担。

## 2. search_host_metric 专项分析（核心问题）

### 2.1 架构现状

`SearchHostMetricResource`（`packages/monitor_web/performance/resources.py:400`）一次返回 4 类数据，ThreadPool 4 路并发（Agent 状态/性能指标/进程/告警计数），总耗时=最慢一路：

1. **指标路**（最大头）：6 个指标各发一次 UQ 查询并发打向 UQ 服务。Trace 实测最慢一条 18.49s，VM 底层实查仅 0.66~3.73s——瓶颈在 UQ 服务端排队与响应组装（排队放大 2~5 倍），不在存储。
2. **进程路**：`get_host_process_list` 内部 GetHostByTopoNode(5.93s) → GetProcess(1.88s) → UQ proc_exists(3.32s) 三段全串行约 11.1s（Trace 实证）。
3. **告警计数路**：`get_host_alarm_count`（`packages/monitor_web/cc/resources/cmdb.py:869`，模块级函数，供 `SearchHostMetricResource` 调用）对业务全量 7 天 ABNORMAL 告警 ES `scan()` 逐条拉取 + Python 逐条按 IP 匹配计数，业务告警多时几千到几万行逐条反序列化。
4. **Agent 状态路**：`get_agent_status`（`cc/resources/cmdb.py:66`，模块级函数）单条 UQ instant 查询（便宜），无数据主机再补 NodeMan 查询（尾部 3 批各 1.3~1.6s）。

### 2.2 根因链

- 前端分页是**内存分页**：`search_host_info` 全量拉基础数据，worker 内存排序/过滤后 slice 当页显示；**指标查询却不按页**——普通场景不传 `bk_host_ids`（`use-host-list.ts` 的 `getMetricQueryParams` 仅分享场景传），后端 `_resolve_hosts` 退化为「CMDB 拉业务全量主机」。
- 后端 4 路查询全部承载全业务规模：UQ target 全量、ES terms IP 列表全量、CMDB 拓扑拉取全量。
- 次级问题：UQ 服务端排队放大、两条链存在未覆盖 gap（疑似大响应读取/解析开销）。

## 3. 需求拆分清单

| REQ | 描述 | 后端视图（Resource） | 类型 | 预估收益 | 状态 |
|-----|------|------|------|----------|------|
| REQ-01 | 主机列表指标查询按页查询 | `SearchHostMetricResource`（现有视图，零契约变更） | 前端为主 | 21.8s → 2~4s | 已拍板主方案 |
| REQ-02 | Agent 状态拆独立轻量接口 | `GetHostAgentStatusResource`（新建） | 后端新增+前端配合 | 保住状态过滤/统计能力 | 方案内，待细节确认 |
| REQ-03 | get_topo_tree 裁剪+缓存 | `GetTopoTree`（`frontend_resources.py:24`） | 后端 | 9.3s/12.9MB → 秒级/MB 级 | 待确认 |
| REQ-04 | get_strategy_and_event_count 两段并行+缓存 | `GetStrategyAndEventCountResource`（`view.py:695`） | 后端 | 8.4s → 3s 内 | 待确认 |
| REQ-05 | search_host_info 拓扑预览拆分 | `SearchHostInfoResource`（`performance/resources.py:312`） | 前后端 | 7.8s → 3s 内 | 待确认 |
| REQ-06 | get_host_or_topo_node_detail 并行化 | `GetHostOrTopoNodeDetailResource`（`scene_view/resources/host.py:102`） | 后端 | 2.9s → ~1.5s | 待确认 |
| REQ-07 | 指标路 UQ 查询合并（同表 6→2~3 条） | `SearchHostMetricResource`（指标路内部优化） | 后端 | 指标路 15~18s → 5~8s | 待确认 |
| REQ-08 | 进程路三段并行化 | `SearchHostMetricResource`（进程路内部优化） | 后端 | ≈11.1s → ~6s | 待确认 |
| ~~REQ-09~~ | ~~UQ 服务端扩容/排队观测~~ | —（UQ 独立服务，非本仓库视图） | ~~运维+后端~~ | ❌ **2026-09-20 确认不可行**：UQ 为上游服务，服务端 worker 数固定、扩容不可获得。**替代手段：客户端并发度收敛（A1′）+ 分页缩小查询规模（REQ-01）** | 关闭 |

## 4. REQ-01 主方案设计：主机列表按页查询指标

### 4.1 方案

前端把 `getMetricQueryParams` 的 `bk_host_ids` 从「分享场景才传」改为「始终传当页主机 ID 列表」：

```text
现状：search_host_info 全量 → worker 内存分页 → search_host_metric（全业务主机）
改为：search_host_info 全量 → worker 内存分页 → search_host_metric（bk_host_ids=当页50台）
```

后端 `SearchHostMetricResource._resolve_hosts` 已支持 `bk_host_ids` 路径（`get_host_by_id` + `push_host_target=True` 下推），分享场景已在线上稳定使用，后端无需大改。

### 4.2 三个产品语义变更（需确认）

1. **指标排序仅当页有效**：排序在前端 worker 内存做，全量排序需全量指标；分页后仅当页有值。可接受，或排序时退回全量慢查（低频操作）。
2. **Agent 状态过滤/分类统计失真**：`status` 字段来自 metric 接口，按状态筛选和顶部统计（如「告警中的主机 72」）依赖全量数据 → 由 REQ-02 兜住。
3. **刷新变当页语义**：定时/手动刷新只刷当页；对「3 分钟快照」数据反而更合理；可加页级 LRU 缓存。

### 4.3 交互细节建议

- 翻页时取消在途请求（现有 metricRequestGeneration 机制可直接复用）
- 页级 loading 态 + 刷新按钮语义明确为「刷新本页」
- 分享/拓扑节点分享场景保持现有 `bk_host_ids` 语义不变
- pageSize 可配置，契约上限建议 200

### 4.4 兼容性设计

- 后端零契约变更（`bk_host_ids` 已在 RequestSerializer，required=False）
- 老前端不传 `bk_host_ids` 时行为完全不变（全量慢查兜底）
- 分享安全契约（`test_share_security.py`）已覆盖 bk_host_ids 场景，测试资产就绪

## 5. REQ-02 设计：Agent 状态独立轻量接口

Agent 状态查询本身便宜（单条 UQ instant 查询，Trace 实测非大头），独立成接口后可**全量查**（保持业务全量语义），保住状态过滤和分类统计能力：

- 新增 `GetHostAgentStatusResource`：入参 bk_biz_id（+可选拓扑范围），后端全量 UQ instant 查询，返回 `{bk_host_id: status}` 映射
- metric 接口的 agent_status 分区保留，前端不再依赖它做过滤/统计
- 成本：1 个新 Resource + 1 条路由 + 前端 1 次并行请求，预估 1 天

## 6. 后端配套深水区（REQ-07/08/09）

- 指标路 6 条 UQ 合并为 2~3 条（同表合并：cpu_summary/mem/io/disk 各自归并）
- 进程路三段并行化（topo/process/proc_exists 互不依赖部分并发）
- UQ 服务端 worker 扩容 + 排队时长观测（Trace 证实并发排队放大 2~5 倍，是分页方案多用户场景的前置保障）
- 告警计数路 ES 聚合改造（composite agg 替代 scan+Python 计数）：分页后全量触发概率大降，优先级降低
- 全链路短 TTL 缓存（30~60s）作为低成本兜底

## 7. 验证标准

| 验证项 | 指标 |
|--------|------|
| 首屏耗时 | search_host_metric 当页查询 P95 < 4s（当前 21.8s） |
| 状态统计准确性 | 顶部「告警中的主机」等分类统计与全量口径一致（REQ-02 保证） |
| 兼容性 | 老前端不传 bk_host_ids 行为不变；分享契约测试全绿 |
| 排序语义 | 指标排序当页有效（或明确「排序退回全量慢查」交互） |
| 其余接口 | topo_tree ≤ 3s 且 ≤ 2MB；strategy_and_event_count ≤ 3s；host_info ≤ 3s |

## 8. 风险与注意事项

1. **UQ 不可扩容（2026-09-20 确认，硬约束）**：UQ 为上游独立服务，服务端 worker 数固定。**此约束下分页方案（REQ-01）不再是"依赖扩容"，反而成为缓解排队的唯一有效手段**——排队 ∝ 并发数 × 单查询工作量，分页把扫描范围从 38357 台缩到 50 台（工作量降约 767×），服务端容量不变也能同步降低队列等待。多用户并发场景的实际收益须通过 ≥10 并发压测验证（不扩容前提下的验证目标：P95 ≤6s）。
2. **UQ 分支失败不回退原生查询**（ki 决策记忆）：分页后 bk_host_ids 下推 UQ target 数量减少，partial 语义保持现状（fail_on_incomplete=False 保留已返回数据），前端兜底显示未知。
3. **排序语义需产品确认**：分页后全量排序能力受损，需明确交互文案或「排序时全量慢查」兜底。
4. **38478 台是极限场景**：分页后每页查询规模稳定，极限规模只影响全量路（host_info/topo_tree），需同步做 REQ-03/05。
5. **fetch_febot_info（3.95s）**：本仓库无此接口实现，属站点级公共组件，转交运维确认，不在本需求范围。

## 9. 实施计划

| 阶段 | 内容 | 预估 |
|------|------|------|
| 阶段一 | REQ-01 分页查询 + REQ-02 Agent 状态拆分 | 前端 2 天 + 后端 1 天 |
| 风险确认 | 4.2 节三点产品语义确认 | 0.5 天 |
| 阶段二 | REQ-03/04/05/06 慢接口治理 | 后端 2~3 天 |
| 阶段三 | REQ-07/08/09 后端深水区优化 | 后端 3~5 天 |

## 10. 实施记录

- **2026-09-14**：需求报告初版落盘（基于 2026-09-11 截图与 Trace + 2026-09-14 代码调研），状态=草案，待用户对 REQ-01 细节与 REQ-02~09 优先级拍板。
