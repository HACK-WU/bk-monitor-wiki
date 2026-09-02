---
groupPath: 决策记录/Issue
relation: 接口契约-via_issue_id仅溯源不加索引
exportedAt: "2026-09-01T07:21:15.265Z"
---
【决策记录｜Issue 关系表 via_issue_id 字段：纯溯源标签，不得假设它仍是本组成员，且不加索引】
- 分类：接口契约
- 动机：可维护性（字段只服务溯源展示，若加索引或当关联键用会引入错误的语义假设）
- 决策：IssueMergeRelation 新增 varchar(64) 可空字段 via_issue_id（上一跳主 Issue ID），记录该成员是「随着某个已成组的主一起被并入」（扁平化 reparent）；直接合并进来的成员为 None
- 背景约束：该值可能指向一个**已不在本组**的 Issue（如上一跳主随后被拆分），因此它只是历史路径标签，**不是关系成员资格断言**；同时**不加索引**——无按它过滤的查询路径
- 被否决方案：无
- 已知代价与边界：前端与运维侧若误把它当「该 Issue 仍属本组」的依据会渲染错误；故 ListMergeSourcesResource 与 bkm_cli detail 输出该字段时，注释均明确警示「不得据此假设它仍是本组成员」
- 重新评估触发条件：出现需要按 via_issue_id 过滤或回溯整条改挂链路的查询需求（届时须同时补索引并重新界定语义）
- 关联代码：via_issue_id 字段定义 @ bkmonitor/bkmonitor/models/issue.py；迁移 0203_add_via_issue_id_to_issue_merge_relation.py；输出字段 @ bkmonitor/packages/fta_web/issue/resources.py（ListMergeSourcesResource）
- 证据来源：代码注释（models/issue.py L77-82 明写「该值可能指向一个已不在本组的 Issue，仅作溯源展示，不得假设它仍是本组成员。不加索引：无按它过滤的查询路径」；resources.py 输出处注释「纯溯源标签，可能指向已不在本组的 Issue，前端不得据此假设它仍是本组成员」）；commit 438a146（PR#12234）