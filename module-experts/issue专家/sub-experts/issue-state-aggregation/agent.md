# Issue 状态聚合子专家

> 父专家：[Issue 专家](../agent.md)
> 覆盖范围：状态机、聚合引擎、周期任务、LLM 标题生成
> 最后更新：2026-08-03

## 测试状态

- **测试位置**：`alarm_backends/tests/service/fta_action/test_issue_fingerprint.py`（64 用例）、`test_issue_merge.py`（72 用例）、`test_issue_llm_title.py`、`test_regenerate_issue_llm_title_command.py`
- **测试可执行性**：✅ 可跑——指纹/LLM 标题用 worker 角色；**合并/拆分需 api 角色**（worker/web 角色下会"假失败"），详见 [父专家 06-测试.md](../../implementation/06-测试.md)
- **已知失败**：[父专家 test/known-failures.md](../../test/known-failures.md)

## 覆盖文件

| 文件 | 路径 | 职责 |
|------|------|------|
| Issue 数据模型 | `bkmonitor/documents/issue.py` | ES 文档模型 + 状态机方法 |
| Issue 常量 | `constants/issue.py` | 状态、优先级、活动类型枚举 |
| 聚合处理器 | `alarm_backends/service/fta_action/issue_processor.py` | 告警 → Issue 聚合入口 |
| 周期任务 | `alarm_backends/service/fta_action/tasks/issue_tasks.py` | 后台统计同步、漏关联补偿 |
| Issue 合并 | `bkmonitor/issue_merge.py` | Issue 合并/展开逻辑 |
| LLM 标题 | `alarm_backends/service/fta_action/llm_title.py` | LLM 标题生成 |

## 状态机

```
pending_review → unresolved (assign 首次指派)
pending_review → resolved (resolve 直接解决)
pending_review → archived (archive 直接归档)
unresolved → resolved (resolve)
unresolved → archived (archive)
resolved → unresolved (reopen)
archived → pending_review/unresolved (restore 恢复归档)
```

### 自动流转

- `add_comment`：若当前为 `pending_review`，自动流转到 `unresolved`
- `update_priority`：若当前为 `pending_review`，自动流转到 `unresolved`

### 状态定义

| 状态 | 值 | 是否活跃 |
|------|-----|----------|
| 待审核 | `pending_review` | 是 |
| 未解决 | `unresolved` | 是 |
| 已解决 | `resolved` | 否 |
| 归档 | `archived` | 否 |

### 活动类型

| 类型 | 触发操作 |
|------|----------|
| `create` | Issue 创建 |
| `status_change` | 状态流转 |
| `assignee_change` | 指派/改派 |
| `priority_change` | 改优先级 |
| `name_change` | 重命名 |
| `comment` | 添加跟进 |
| `comment_edit` | 编辑评论 |
| `create_tapd` | 创建并关联 TAPD 单 |
| `tapd_link` | 关联已有 TAPD 单 |

## 聚合引擎（IssueAggregationProcessor）

### 核心流程

1. 配置校验：`issue_config.is_enabled` + `alert_levels` 匹配 + `conditions` 过滤
2. 指纹计算：`gen_issue_fingerprint(strategy_id, agg_dims, data_dims)` → `count_md5`
3. 活跃 Issue 查找：Redis 缓存 → ES 标准查找 → Legacy 兜底（三级）
4. 不存在则创建（分布式锁保护）
5. 告警关联：`AlertDocument.issue_id` UPSERT

### 指纹计算规则

```
payload = ["strategy:{id}"]
for key in sorted(aggregate_dimensions):
    value = data_dimensions.get(key)
    if value is None: return None  # 维度缺失，跳过
    payload.append(f"{key}={value}")
return count_md5(payload)
```

### 并发控制

- 锁粒度：按 fingerprint
- 获取方式：`SET NX EX` 一次性尝试
- 释放安全：Lua 脚本 Token 锁，只释放自己持有的锁

### 高基数防护

- 单策略活跃 Issue 数超过阈值时：仅 metric + warning，不阻塞新建
- ES count 结果缓存到 Redis，5 分钟 TTL（±20% jitter）

## 周期任务

### sync_issue_alert_stats（主任务）

对全量活跃 Issue 执行：
1. 告警统计同步：更新 `alert_count` 和 `last_alert_time`
2. 漏关联补偿：回填 `AlertDocument.issue_id` 未写入的告警
3. 影响范围重算：基于关联告警重新汇总 `impact_scope`
4. orphan Issue 检测：无关联告警的孤立 Issue（5 分钟后告警）
5. Legacy 哨兵续命：防止 30 天 TTL 失效

### backfill 优化

旧实现 O(N×M)（每条 Issue 扫一遍同策略 unlinked alerts）→ 新实现 O(N+M)（一次 scan Issue + 一次 scan alerts + 内存分组匹配）

### 影响范围维度

| 维度 | 数据来源 | ID 字段 |
|------|----------|---------|
| set | `bk_topo_node` | `set_id` |
| host | `bk_host_id` / `ip` | `bk_host_id` |
| service_instances | `bk_service_instance_id` | `bk_service_instance_id` |
| cluster/node/service/pod | `bcs_cluster_id` + target_type | — |
| apm_app/apm_service | `app_name` + `service_name` | — |

## LLM 标题生成

- 新建 Issue 后异步派发到 `celery_llm_task` 独立队列
- 两级闸门：部署级 env `ENABLE_ISSUE_LLM_TITLE` + 运行时业务白名单
- CAS 保护：写入前检查当前 name 是否仍为默认名
- 失败静默：任何失败保留默认名，不重试不入队
- few-shot 示例：`refresh_issue_llm_title_examples` 周期预计算缓存

## 持久化策略

- 写入顺序：先 ES 后 Redis（ES 为唯一持久化存储）
- ES 写入失败重试 1 次，仍失败抛异常
- Redis 操作 fail-silent（只 log，不阻塞）
- 活跃 Issue 写入缓存，非活跃 Issue 删除缓存
