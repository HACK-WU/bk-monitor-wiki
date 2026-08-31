---
groupPath: 决策记录/告警查询
relation: 兼容处理-assign_tags回退OR展开防重入
exportedAt: "2026-08-31T03:18:06.719Z"
---
【决策记录｜告警查询 assign_tags 回退：event.ip 与 event.bk_cloud_id 自动 OR 展开嵌套查询】
- 分类：兼容处理
- 动机：一致性（传统主机告警与 K8s 告警的 IP 字段位置不同，用户用同一个字段搜索应都能命中）
- 决策：AlertQueryTransformer.ASSIGN_TAGS_FALLBACK_FIELDS 声明 event.ip 映射 ip、event.bk_cloud_id 映射 bk_cloud_id；_expand_assign_tags_fallback 把 event.ip:"x" 改写为 (event.ip:"x") OR nested(assign_tags, key="ip" AND value.raw:"x")
- 背景约束：传统主机告警的 event.ip 有值；K8s 告警只有 assign_tags 中的 ip 有值，两者并存，单一字段查询会漏掉其中一类
- 被否决方案：只查 event.ip 或只查 assign_tags，否决理由为会漏掉另一类告警（docstring：这样传统主机告警和 K8s 告警都能被搜到）
- 已知代价：改写后的查询是 nested 加 OR 组合，DSL 更复杂开销更高；必须靠 context 中的 assign_tags_expanded 标记防重入——generic_visit 到 clone_children 到 visit_iter 会递归遍历替换后节点的子节点，其中包含原始 SearchField("event.ip", ...)，不加防护会无限递归（docstring 原文）
- 重新评估触发条件：新增需要回退的字段（需同步 ASSIGN_TAGS_FALLBACK_FIELDS 与防重入逻辑）；或告警文档统一 IP 字段位置
- 关联代码：AlertQueryTransformer.ASSIGN_TAGS_FALLBACK_FIELDS、_expand_assign_tags_fallback、visit_search_field @ packages/fta_web/alert/handlers/alert.py；NESTED_KV_FIELDS @ handlers/base.py
- 证据来源：_expand_assign_tags_fallback docstring（含扩展示例、两类告警并存说明、无限递归警告）；NESTED_KV_FIELDS 注释（对标签进行特殊处理，(tags.a : b) 转 (tags.key : a AND tags.value : b)）
- 完整上下文：.module-experts/告警查询专家/C5-关键决策.md 决策 9