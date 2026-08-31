---
groupPath: 决策记录/性能场景
relation: 接口契约-缺失值三分语义None与空列表
exportedAt: "2026-08-31T02:23:39.117Z"
---
【决策记录｜性能场景 缺失值三分语义：None 表示未成功完成、空列表表示成功且无数据、未知值排序置后】
- 分类：接口契约
- 动机：避坑（把查询失败与确实没有数据混为一谈，会让前端把失败渲染成 0 或空，掩盖故障）
- 决策：_empty_host_metric 作为每个主机的默认模板，进程 component 与告警 alarm_count 默认值为 None，其余指标为 None，状态为 AGENT_STATUS.UNKNOWN；语义约定为 None 表示该分区未成功完成，成功查询且确实无数据时由分区写入空列表；缺失值在前端保持未知展示、排序时置后、筛选时只判断已知值
- 背景约束：4 路并行聚合中任一路可能单独失败，调用方需要能区分没查到与查失败
- 被否决方案：失败与空数据统一用空列表表达，否决理由为无法区分失败与真实空数据（commit body 明确进程与告警硬失败使用 null，成功无数据使用空列表）
- 已知代价：消费方必须处理三种取值（None、空列表、有值），直接把 component 当列表遍历会报错
- 重新评估触发条件：前端统一要求失败也返回空数组；或缺失值语义导致前端展示异常反馈累计大于等于 2 次
- 关联代码：SearchHostMetricResource._empty_host_metric、get_process_status、get_alarm_count @ monitor_web/performance/resources.py
- 证据来源：代码注释（_empty_host_metric：None 表示对应分区未成功完成，成功查询且确实无数据时由分区写入空列表）；commit 4faf55fb50（body：UQ partial 或单指标异常时保留已返回数据，缺失值保持未知，排序置后，筛选仅判断已知值，进程与告警硬失败使用 null，成功无数据使用空列表）
- 完整上下文：.module-experts/性能场景专家/C5-关键决策.md 决策 2