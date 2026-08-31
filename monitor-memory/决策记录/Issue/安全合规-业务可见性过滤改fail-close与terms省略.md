---
groupPath: 决策记录/Issue
relation: 安全合规-业务可见性过滤改fail-close与terms省略
exportedAt: "2026-08-31T03:10:17.255Z"
---
【决策记录｜Issue 与告警链路 业务可见性过滤改 fail-close，全部业务查询在全量授权时可省略业务 terms】
- 分类：安全合规
- 动机：避坑（过滤子句为空时业务过滤整体消失导致越权可见）、优化（十万级 terms 撑爆查询 DSL）
- 决策：add_biz_condition 显式收口四种情形：已构造业务子句取并集；指定了业务范围但无任何业务子句追加 match_none 失败关闭；未指定业务范围保持各 Handler 既有语义；单租户加明确选择全部业务加 IAM 授予全量权限时可省略无区分度的业务 terms。省略需同时满足五条件：单租户模式、请求明确包含 -1、IAM 返回 OP.ANY 或启用 skip_check、授权业务非空、不存在真实未授权业务。同时把 -1 从 unauthorized_bizs 归一化移除（它是全部业务标记而非真实业务 ID）
- 背景约束：生产取证中授权业务列表可达 11.5 万个，展开后单次查询 DSL 约 1.15 MB，是 TopN 接口超时的放大因素之一；告警检索链路不能统一依赖 bk_tenant_id（历史索引存在完全没有该字段的数据）
- 被否决方案：维持构造不出子句就原样返回（fail-open），否决理由为分片资源透传 authorized_bizs 与 unauthorized_bizs 时 kwargs 通道允许出现空空组合，业务过滤会整体消失；通过缓存中的当前空间集合恰好被授权集合覆盖推断全量权限，否决理由为避免缓存时序、新增业务或遗留索引文档使查询范围被错误放宽
- 已知代价：多租户模式、显式业务 ID 列表、无请求上下文、IAM 非全量策略四种情况仍保留业务 terms；fail-close 分支会收紧原本依赖空子句放行的调用方
- 重新评估触发条件：历史索引补齐 bk_tenant_id 后可评估多租户下的省略优化
- 关联代码：add_biz_condition @ packages/fta_web/alert/handlers/action.py（告警、故障、处理记录、Issue 共用的业务可见性入口）；get_biz_filter_ids；Permission.filter_space_list_by_action_with_scope
- 证据来源：commit bdc35a27d2（body 的问题、改动、租户隔离边界、验证、影响范围五段，含两条否决理由与 11.5 万与 1.15 MB 实测数据）；commit 71b100a2dd（get_biz_filter_ids 收口 -1 哨兵）；commit 96c8639cb0 与 f199ce93f3（ES terms 65536 限制导致权限过滤失效的前置修复）
- 完整上下文：.module-experts/issue专家/C5-关键决策.md 决策 10