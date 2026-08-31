---
groupPath: 决策记录/告警查询
relation: 安全合规-业务可见性fail-close与terms省略
exportedAt: "2026-08-31T03:17:23.270Z"
---
【决策记录｜告警查询 业务可见性过滤改 fail-close，全部业务查询在全量授权时可省略业务 terms（告警查询侧视角）】
- 分类：安全合规
- 动机：避坑（过滤子句为空时业务过滤整体消失导致越权可见）、优化（十万级 terms 撑爆查询 DSL）
- 决策：add_biz_condition 四种情形收口：已构造业务子句取并集；指定了业务范围但无任何业务子句追加 match_none 失败关闭；未指定业务范围保持各 Handler 既有语义；单租户加明确 -1 加 IAM 全量授权时可省略业务 terms（需同时满足五条件：单租户、请求含 -1、OP.ANY 或 skip_check、授权业务非空、无真实未授权业务）
- 背景约束：生产取证中授权业务列表可达 11.5 万个，展开后单次查询 DSL 约 1.15 MB，是 fta/alert/alert/top_n 超时的放大因素之一
- 被否决方案：见 issue 专家 C5 决策 10（同一 commit 的完整否决理由清单：fail-open 状态、以及通过缓存覆盖推断全量权限方案）
- 已知代价（告警查询侧特有）：add_biz_condition 是告警、故障、处理记录、Issue 共用的业务可见性入口，改它等于改四个域的可见性语义，回归面大；多租户模式、显式业务 ID 列表、无请求上下文、IAM 非全量策略四种情况仍保留 terms，TopN 超时在多租户下未完全解决；本模块内 get_bucket_count 仍使用 track_total_hits=True，基数聚合走的是另一条路径
- 重新评估触发条件：历史索引补齐 bk_tenant_id 后可评估多租户下的省略优化；或 TopN 超时仍有复发
- 关联代码：add_biz_condition @ packages/fta_web/alert/handlers/action.py；parse_biz_item 与 get_biz_filter_ids @ handlers/base.py；get_bucket_count @ resources.py
- 证据来源：commit bdc35a27d2（body 五段，含 11.5 万与 1.15 MB 实测数据）；commit 71b100a2dd、96c8639cb0、f199ce93f3；交叉引用 .module-experts/issue专家/C5-关键决策.md 决策 10
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 2