---
groupPath: 决策记录/Issue
relation: 接口契约-指纹每个元素带prefix防维度错位
exportedAt: "2026-09-01T07:21:50.229Z"
---
【决策记录｜Issue 指纹每个元素带 prefix（strategy: / key=value），防维度错位】
- 分类：接口契约
- 动机：避坑（不同维度组合算出同一指纹 → 不相关告警被错误聚合到同一 Issue）
- 决策：gen_issue_fingerprint 构造 payload 时每个元素都带语义前缀——策略段为 strategy:{strategy_id}，维度段为 {key}={value}；维度按 key 排序后参与计算（顺序无关）
- 背景约束：底层 count_md5 内部使用 list_sort=True，若只传裸值，{a:X, b:Y} 与 {a:Y, b:X} 排序后结果相同，会产生维度错位的误聚合
- 被否决方案：
  - 直接把维度值按序拼接后 md5：否决理由 —— 裸值在 list_sort=True 下丢失 key 与 value 的绑定关系（Wiki 明确列出该反例）
- 已知代价与边界：指纹串比裸值拼接更长；prefix 格式一旦确定即成为事实契约，改动会导致存量 Issue 无法按新指纹命中，需配套迁移
- 重新评估触发条件：聚合维度模型变更（须同时评估存量 fingerprint 的迁移方案）
- 关联代码：gen_issue_fingerprint @ bkmonitor/alarm_backends/service/fta_action/issue_processor.py
- 证据来源：Wiki《Issue 聚合引擎》「指纹计算 → 关键设计决策」表（「每个元素带 prefix，防止 count_md5 内部 list_sort=True 导致维度错位（如 {a:X,b:Y} 与 {a:Y,b:X} 排序后相同）」）