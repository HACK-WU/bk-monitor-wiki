# issue 后台周期任务 · 代码 wiki

> 本文为完整讲解（Phase 0→7）的 Phase 2 产物。前序：`00-能力大纲.md`。

## 一、整体结构与文件位置

[专用] 全部逻辑集中在单文件 `bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py`（1531 行），调度注册在 `bkmonitor/config/role/worker.py` 的 `ACTION_TASK_CRONTAB`。

模块内部三段划分（与大纲一致）：

| 段落 | 行区间 | 关键符号 |
|---|---|---|
| 统计同步段 | L39-L229 | `sync_issue_alert_stats` / `_renew_legacy_migration_done_sentinel_if_needed` / `_process_single_issue` |
| 补偿与范围段 | L231-L886 | `_backfill_unlinked_alerts_for_strategy` / `_extract_origin_data_dimensions` / `_allowed_scope_keys` / `_build_impact_scope` / `_iter_issue_hits_with_total` / `_iter_alert_hit_batches` |
| LLM 段 | L867-L1531 | `_collect_example_groups` / `_apply_llm_title` / `generate_issue_llm_title` / `inspect_issue_llm_title_regeneration` / `regenerate_issue_llm_title` / `refresh_issue_llm_title_examples` |

## 二、术语表（首次出现先给"人话"）

| 术语 | 人话解释 | 出处 |
|---|---|---|
| **fingerprint（指纹）** | Issue 的身份 ID。由策略 ID + 一组"聚合维度"的取值拼成字符串后做 md5。**同一指纹 = 同一个具体问题**，这是聚合的判定依据 | `issue_processor.py::gen_issue_fingerprint` |
| **聚合维度（aggregate_dimensions）** | 策略配置的"按哪些维度聚"，如 `bk_target_ip`、`bcs_cluster_id` | Issue 上存快照 `aggregate_config.aggregate_dimensions` |
| **catch-all Issue** | 聚合维度配成空 `[]` 时退化出的"一策略一个 Issue"，任何告警都能命中它 | `_backfill_unlinked_alerts_for_strategy` docstring L234-L259 |
| **unlinked alert** | 没写 `issue_id` 字段的告警，即"没归属到任何 Issue 的告警" | L320-L324 的 `exclude("exists", field="issue_id")` |
| **legacy Issue** | 指纹改造前创建的旧 Issue，`fingerprint` 字段为空 | `documents/issue.py::migrate_legacy_active_issues` |
| **impact_scope（影响范围）** | Issue 上存的一份"这次问题影响了哪些资源"的快照，供前端展示 | `_build_impact_scope` L456 |
| **orphan Issue** | 存活超过 5 分钟却一条关联告警都没有的 Issue，属异常态 | L204 |
| **CAS 写入** | 写之前先比对"当前值是否等于我期望的旧值"，不等就不写。防止覆盖别人的修改 | `_apply_llm_title` L1062-L1065 |
| **few-shot** | 给 LLM 的提示词里塞几个"人类改名的真实例子"，让它照着风格生成 | `_apply_llm_title` L1036-L1037 |

## 三、任务一：`sync_issue_alert_stats` 逐层拆解

### 3.1 主循环（感知层）

[专用] 签名与执行节奏（`issue_tasks.py#L47-L111`）：

```python
@app.task(ignore_result=True, queue="celery_action_cron")
def sync_issue_alert_stats():
```

每 5 分钟一轮。主循环遍历 `_iter_issue_hits_with_total()` 产出的全部活跃 Issue，逐条调 `_process_single_issue`。

三个工程细节值得注意：

1. **单条失败不影响整批**：`try/except` 包住 `_process_single_issue`，失败只 `failed += 1` + `logger.exception`，继续下一条（L96-L103）。这是周期任务的标准姿态——一条脏数据不该拖垮整轮。
2. **进度日志按 100 条打点**：`PROGRESS_LOG_INTERVAL = 100`（L44），避免活跃 Issue 上万时日志淹没。
3. **`total` 从首批响应取，不发额外 count 请求**（L818-L844）：利用 ES 响应自带的 `hits.total.value`，省一次往返。

### 3.2 五项职责的入口顺序

```
sync_issue_alert_stats
  ├─ ① _renew_legacy_migration_done_sentinel_if_needed()   ← 先做，全局一次
  └─ for each 活跃 Issue: _process_single_issue()
        ├─ legacy 跳过（fingerprint 为空）
        ├─ ② _backfill_unlinked_alerts_for_strategy()      ← 按策略去重，非每 Issue 都跑
        ├─ ③ 统计 alert_count / last_alert_time            ← ES 聚合
        ├─ ④ _build_impact_scope()                          ← 扫该 Issue 全部告警
        ├─ ⑤ orphan 检测（alert_count == 0 且 age > 300s）
        └─ IssueDocument.bulk_create(UPDATE)
```

#### ① Legacy 哨兵续命（`#L114-L155`）

[专用] 这是一个容易看不懂的职责，需要先讲背景：

- 指纹改造把 Issue 模型从"一策略一活跃 Issue"升级为"按维度组合切分"。
- 改造前创建的活跃 Issue 没有 fingerprint，新代码无法可靠归属它们。
- 迁移由部署时的 `post_migrate` hook 触发 `migrate_legacy_active_issues()`，把旧 Issue 直接 RESOLVE 掉，**但它本身不写哨兵**（见下）。哨兵是全局 Redis key `issue.legacy_migration.done`，**TTL 30 天**（`core/cache/key.py#L1248-L1260`）。
- processor 看到哨兵就跳过 legacy fallback 查询（少一次全索引扫描）。

**这里有个反直觉的点：迁移函数不设置哨兵。**

设置动作只有一处 —— `_mark_legacy_migration_done()`（`documents/issue.py#L1116-L1135`），而它的唯一调用点就是这个周期任务（`issue_tasks.py#L146`）。`migrate_legacy_active_issues` 的 docstring 里三处明确写了「本函数不直接 set legacy 迁移完成哨兵」。

原因是 role 隔离：`post_migrate` hook 跑在 **web/saas role** 下，该 role 的 settings 不含 `REDIS_*_CONF`（只有 `config/role/worker.py` 定义）。而 `alarm_backends.core.cache.key` 在模块加载时 `import RedisProxy` 会解析 `settings.REDIS_CELERY_CONF`，在 web/saas role 下直接抛 `AttributeError`，导致 migrate 命令以非 0 退出。所以初始 set 只能由 worker role 的周期任务异步接管。

代价：哨兵未 set 期间 processor 多走 fallback 全索引查询，最大窗口 = 一个周期（默认 5min）。**只影响性能，不影响功能正确性**（fallback 路径本身是对的，只是慢）。

**为什么要续命**：哨兵 TTL 30 天。若 30 天内没有新部署触发 migrate，哨兵过期 → processor 退化到 fallback 全索引查询 → 性能退化。

续命逻辑是**双重确认**的保守设计：

1. Redis `exists` 查哨兵，存在就直接返回（正常路径，几乎不消耗）；
2. 不存在才去 ES 探查"当前是否真无 `fingerprint=null` 的活跃 Issue"；
3. 确认 `legacy_count == 0` 才重新 set 哨兵；仍有 legacy 则只 warning，交给下次部署的 migrate 处理。

[通用] 这里体现的模式是 **fail-safe + 事后确认**：Redis 故障或 ES 探查失败都只是 `return`（不续命），下个周期再试，绝不阻塞主流程。

#### ② 漏关联补偿：从 O(N×M) 到 O(N+M)（`#L234-L384`）

[通用] 这是本文件最值得学的一段优化。先讲问题：

> 术语回指：本节频繁使用 **fingerprint（Issue 身份 ID）**、**catch-all Issue（空维度退化出的兜底 Issue）**、**unlinked alert（没归属 Issue 的告警）**，定义见本文「二、术语表」。此处 backfill 的场景一句话概括：把主链路漏掉的、没归属任何 Issue 的告警补回去。

旧实现是"对每个活跃 Issue，单独扫一遍同策略的 unlinked alerts"。若某策略下有 N 个 Issue（高基数时 N 可能几百），就要扫 N 遍同样的告警，且同一条告警被反算指纹 N 次——**O(N×M)**。

新实现按策略批处理，一次扫完：

```
Step 0: 取 live issue_config（策略缓存），得到 live 聚合维度，作为"优先匹配组"
Step 1: 一次 scan 该策略全部活跃 Issue
        → 按 (聚合维度元组 → {fingerprint: (issue_id, create_time)}) 两级分组
        → 同时记录 earliest_create_time（最早 Issue 的创建时间）
Step 2: 一次 scan 该策略 unlinked alerts
        下界 = max(earliest_create_time, now - 7天)
        （7 天上限来自 _BACKFILL_ALERT_SCAN_MAX_LOOKBACK_SEC，L231）
Step 3: 内存中逐条反算指纹并分发命中
```

关键设计点有三个：

**分组为什么必要**：配置变更窗口期内，同一策略下的不同 Issue 可能带着**不同的 `aggregate_config` 快照**。按维度元组分组，才能让每条告警跟"用同样维度算出来的指纹"比对。

**匹配优先级为什么这样排**（L309-L313）：

```python
def _match_order_key(item):
    agg_tuple, _fp_map = item
    is_live = 0 if (live_agg_dims_tuple is not None and agg_tuple == live_agg_dims_tuple) else 1
    return (is_live, -len(agg_tuple))
```

即：**live 配置组优先，其余按维度个数降序**（维度多的优先）。

原因是 catch-all 组（空维度 `()`）**任何告警都能命中**。如果让它排第一，本该归到具体指纹 Issue 的告警会被错绑到 catch-all Issue。降序排列保证"具体的先匹配，兜底的后匹配"。

[专用] 代码注释里还特别提醒了一个陷阱：`live_agg_dims_tuple` 在 issue_config 缺失时必须保持 `None` 而不是 `()`，否则空元组会被当成"live = catch-all"，让 catch-all 组永远优先（L263-L272）。

**时间边界**（L352-L357）：命中后还要判断 `alert.begin_time >= issue.create_time`，否则跳过。语义是"告警必须晚于 Issue 出生才能归属"，避免 `first_alert_time` 与告警列表时间线断裂。注意这里用 `matched = True` + `break`——**视为已命中，不再回退到更通用的组**，防止错绑。

**失败处理**：`bulk_create` 失败直接 `return`（L370-L373），本周期放弃该策略；但 `backfilled_strategies` 的 `finally` 块已经把它加进 set，所以本周期不会重试，下周期再说。

#### ③④ 统计与影响范围

[专用] 统计走 ES 聚合，一次请求拿两个值（L180-L191）：

```python
alert_search.aggs.metric("alert_count", "value_count", field="id")
alert_search.aggs.metric("max_begin_time", "max", field="begin_time")
```

注意 `last_alert_time` 的**单位换算**：ES 日期聚合返回毫秒，IssueDocument 用秒，故 `int(raw_max / 1000)`。这条注释（L188-L189）是踩过坑的痕迹。

[专用] `_build_impact_scope`（L456-L767）是全文件最长的函数（约 310 行），职责是扫该 Issue 的全部关联告警，汇总出受影响资源。它按 target_type 分流：

| 场景 | 提取的资源维度 |
|---|---|
| HOST / SERVICE（CMDB） | `set` / `host` / `service_instances` |
| `K8S-*`（容器） | `cluster` / `node` / `service` / `pod` |
| `APM-SERVICE`（应用性能） | `apm_app` / `apm_service` |

三个工程细节：

1. **Set 展示名批量回填**（L620-L641）：`pending_set_names` 先把需要解析的 set 攒起来，循环结束后**按业务批量**调 `SetManager.mget`，避免逐条查 CMDB 造成 N+1。
2. **每个维度最多 50 条实例**：所有 `instance_list` 都截 `[:50]`，但 `count` 是真实总数——前端展示"共 N 个，列出前 50"。
3. **聚合维度收窄**（L763-L765）：

```python
allowed_keys = _allowed_scope_keys(aggregate_dimensions or [])
if allowed_keys is not None:
    result = {k: v for k, v in result.items() if k in allowed_keys}
```

`_allowed_scope_keys` 的返回值有三态语义（L410-L455），这是**容易看错的地方**：

| 返回值 | 含义 |
|---|---|
| `None` | 聚合维度为空 → **不收窄**，全量输出 |
| `set()` | 维度非空但无已知资源映射 → **收窄为空**，输出 `{}` |
| `{...}` | 只允许这些 key |

`None` 和 `set()` 语义相反，注释里专门强调了"两者语义不同"。

#### ⑤ orphan 检测

[专用] 逻辑很简单（L198-L211）：`alert_count == 0` 且 `now - create_time > 300s` 就打 `logger.error`。

为什么是 5 分钟阈值？因为 Issue 创建与告警写入 `issue_id` 之间存在时间差（告警先写 ES，关联字段后写），刚创建的 Issue 短暂无告警是正常的。5 分钟是"足够长到不正常"的经验值。

注意它**只打日志，不做任何修复动作**——是留给监控告警去发现的信号，不是自愈逻辑。

### 3.3 两个 scan 工具函数

[通用] `_iter_issue_hits_with_total`（L818-L844）与 `_iter_alert_hit_batches`（L847-L864）用的是同一套模式：**`search_after` 深分页**。

为什么不用 `from/size`？ES 的 `from` 深分页需要协调节点在堆上累积并排序 `from + size` 条结果，深度越大越慢、越吃内存，超过 `max_result_window`（默认 10000）直接报错。`search_after` 用上一页最后一条的排序值当游标，无此问题。

两个函数的差异只有一处：`_iter_issue_hits_with_total` 从首批响应的 `hits.total.value` 取总数并一路 yield 出去，省一次 count 请求；`_iter_alert_hit_batches` 按批 yield，让调用方批量处理。

## 四、任务二：`refresh_issue_llm_title_examples`

[专用] 签名与前置闸门（L1438-L1451）：

```python
@app.task(ignore_result=True, queue="celery_action_cron")
def refresh_issue_llm_title_examples():
    if not (getattr(settings, "ISSUE_LLM_TITLE_BIZ_WHITE_LIST", None) or []):
        return
```

**白名单为空直接 return**——这是一道重要的零副作用闸门：功能没开时，这个任务对 ES/Redis 完全无影响。

主体流程四步：

1. 扫近 30 天的 `NAME_CHANGE` 活动日志，过滤掉 `operator == "system"`（只要人类改名），按 `create_time` 降序取，同 Issue 只留最新一次。单轮扫描上限 2000 条（`max_scan`），防活动量异常时超时。
2. 反查这批 Issue 的现状，确认"改名没被改回"。
3. `_collect_example_groups` 筛选：当前名 == 最新改名值 → 过 `validate_title` 清洗（与 LLM 输出校验同一套禁项规则）→ 按 strategy / biz 两级去重聚合。
4. 写 Redis，TTL 24h，每级最多 `MAX_AUTO_EXAMPLES` 条。

[专用] 这里的失败模式设计得很干净：**任务挂掉 → 缓存 24h 自然过期 → 读路径自动退静态示例**。缓存是纯加速，不是数据源，所以任务失败无害。

## 五、异步任务：`generate_issue_llm_title`

[专用] 它不是周期任务，是 `IssueAggregationProcessor._maybe_dispatch_llm_title` 在**新建 Issue 后** `apply_async` 派发的一次性任务（`issue_processor.py#L164-L185`）。

派发有两级闸门：部署级 env `ENABLE_ISSUE_LLM_TITLE`（由 helm chart 按 llmWorker 容量注入）+ 运行时业务白名单。任一不过就不派发，避免队列积压。

[通用] 任务声明带**软硬双超时**（L1084）：

```python
@app.task(ignore_result=True, queue="celery_llm_task", soft_time_limit=60, time_limit=90)
```

docstring 解释了为什么必须有硬超时：取关联日志的下游实现里有 `except BaseException` 的重试逻辑，可能吞掉 soft_time_limit 信号导致软限失效——只能靠 time_limit 硬兜底。

核心逻辑抽在 `_apply_llm_title`（L899-L1082），与运维补偿路径 `regenerate_issue_llm_title` **共用同一函数**，保证两条路径取数/校验/写入口径完全一致。

`_apply_llm_title` 的流水线：

```
取 Alert → 取关联日志 → 判空 → 限流 → 取模板+示例 → 渲染 prompt
→ 调 LLM → validate_title → (可选)[回归]前缀 → shadow 模式判定
→ 取 Issue → CAS 比对 name → rename 写入
```

每个环节都有明确失败返回值（`alert_not_found` / `empty_log` / `ratelimited` / `timeout` / `llm_error` / `invalid_output` / `name_changed` / `ok` 等），全部进 `ISSUE_LLM_TITLE_TOTAL` 指标打点。

[专用] 三处细节体现了对"标题是体验增强"这一定位的贯彻：

1. **`enforce_unique=False`**（L1070-L1074）：同类错误天然生成相同标题，允许重名。若套用给用户改名用的唯一性约束，会被卡回默认名。
2. **rename 的 operator 恒为 `system`**（L1075）：真实运维账号只写进 `content` 供审计。因为"标题来源判别"依赖"最近 NAME_CHANGE.operator == system → 是 LLM 改的、可被覆盖"，若写真实账号，二次补偿会误判成用户手工改名而跳过。
3. **只对 `alert_not_found` 定向重试**（L1115-L1135）：延迟 1s、3s 各一次。因为新建 Issue 时告警刚写入 ES，可能因近实时刷新延迟查不到——这是**可恢复**的竞态。其他失败一律静默保留默认名。

## 六、设计模式与不变量汇总

| 模式 / 不变量 | 位置 | 说明 |
|---|---|---|
| 单条失败隔离 | L96-L103 | 周期任务逐条 try/except，不因一条脏数据中断整轮 |
| 按策略去重 | L73 + L168-L174 | `backfilled_strategies` set，含 `finally` 保证失败也不重试 |
| 指纹算法同源 | L330 / L387-L408 | backfill 复用 `gen_issue_fingerprint`，与主链路口径一致 |
| 具体优先于兜底 | L309-L313 | 匹配排序 live 优先 + 维度数降序，防止 catch-all 错绑 |
| 时间边界守恒 | L352-L357 | 告警须晚于 Issue 出生，命中即 break 不回退 |
| `search_after` 深分页 | L818-L864 | 规避 `from/size` 深分页性能塌陷 |
| 批量查 CMDB | L620-L641 | `pending_set_names` 攒批后 `mget`，避免 N+1 |
| CAS 写入 | L1062-L1065 | 防止覆盖并发改名 |
| 零副作用闸门 | L1447-L1451 | 白名单空则直接 return |
| 失败无害缓存 | L1500-L1531 | 缓存 24h TTL，过期自动退静态 |

## 七、依赖关系

**内部依赖**：`IssueDocument` / `AlertDocument` / `IssueActivityDocument`（ES 文档模型）、`IssueMergeRelation`（MySQL 模型）、`gen_issue_fingerprint`（聚合引擎）、`llm_title` 模块、`BusinessManager` / `SetManager`（CMDB 缓存）、`StrategyCacheManager`（策略缓存）。

**外部依赖**：Celery + redbeat（调度）、Elasticsearch、Redis、`api.aidev.chat_completion`（LLM 网关）。

**被谁依赖**：无直接调用方——周期任务由 beat 调度，是链路终点。间接影响：web 层 Issue 列表读取的 `alert_count` / `impact_scope` 字段由本任务维护。

## 八、解读评审记录

### 第 1 轮 · 教学法视角

| 维度 | 意见 |
|---|---|
| 结构是否递进 | 通过。术语表 → 主循环 → 五项职责 → 工具函数 → 另两个任务，符合认知阶梯 |
| 结论是否可溯源 | 通过。所有结论带 `file://` + 行号区间；常量行号经 grep 二次确认 |
| 有无编造 | 通过。O(N×M)→O(N+M) 来自代码 docstring 原文；7 天上限、5 分钟阈值均取自常量定义 |
| 通用/专用标注 | 通过。`search_after` 深分页、CAS、fail-safe 标为通用；指纹、catch-all、legacy 标为专用 |
| 章节来源跨度合规 | 通过。均为区间（如 L47-L111），无单点行号 |
| 图表选型 | 本阶段用代码块 ASCII 流程图，未用 SVG，合规 |

**P0 = 0。**

### 第 2 轮 · 新人视角

| 维度 | 意见 |
|---|---|
| 能否读懂 | 基本能。但**首次读时会在"fingerprint / catch-all / unlinked alert"处卡住**——这三个词在讲解正文里先于解释出现 |
| 卡住的具体位置 | 第三节 3.2 ② 直接使用了 catch-all 与 unlinked alert |
| 术语是否未铺垫 | ⚠️ **P1**：术语表虽已存在，但读者按线性顺序读到 3.2 时，术语表在第二节——需要往回翻。建议在 3.2 开头加一句回指 |

**修复**：已在 3.2 ② 开头补入"（术语见表二，此处 backfill 的场景是：把没归属 Issue 的告警补回去）"回指句。

| 能否说清系统位置 | 通过。第六、七节明确了"链路终点 + 被 web 层间接消费"的定位 |
|---|---|

**修复后 P0 = 0。**

## 章节来源

- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L39-L44`（常量定义）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L47-L111`（主任务与循环）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L114-L155`（哨兵续命）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L157-L229`（单 Issue 处理与 orphan 检测）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L231-L384`（backfill 与其 docstring）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L387-L455`（维度提取与收窄规则）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L456-L767`（impact_scope 构造）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L818-L864`（两个 scan 工具）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L899-L1082`（_apply_llm_title）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L1084-L1150`（generate_issue_llm_title 与重试）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L1322-L1393`（regenerate 补偿路径）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/tasks/issue_tasks.py#L1438-L1531`（refresh 周期任务）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/core/cache/key.py#L1248-L1260`（哨兵 TTL 30 天）
- `file:///root/bk-monitor/bkmonitor/alarm_backends/service/fta_action/issue_processor.py#L164-L185`（LLM 任务派发入口）
