---
groupPath: 专题记忆/Issue
relation: Issue 异常信息展示链路与 log_content 调用时机
exportedAt: "2026-09-11T03:05:22.752Z"
---
Issue 异常信息展示链路与 log_content 接口契约（2026-09-11 排查沉淀）

展示链路（前端）：Issue 列表行的异常信息展示为 log_content 优先、anomaly_message 兜底，具体兜底链为 row.log_content?.replace(DATETIME_PREFIX_REGEX, '') || row.anomaly_message || '--'，见 webpack/src/trace/pages/alarm-center/alarm-issues/issues-table/hooks/use-issues-columns-renderer.tsx 第 98/133/172 行；DATETIME_PREFIX_REGEX 用于清洗日志开头的形如 2026-08-07 17:12:00 的时间戳前缀，目前是该文件第 64 行的局部常量，未抽共享。

log_content 调用时机（前端零判断、全量拉）：触发点为 use-issues-table-enhancement.ts 的 watch(data)，列表数据一变化（首次加载/翻页/筛选）且 alarmType 为 ISSUES 且列表非空即并发 fetchLogContent，把当前页全部 issue_ids + bk_biz_ids 按每批 10 条、批间串行发出（services/issues-services.ts 的 getIssueLogContent）；前端不按告警类型或数据源做任何过滤，指标类 Issue 也在请求列表中。

是否真查日志的判定（后端逐 Issue 判定）：IssueLogContentResource @ packages/fta_web/issue/resources.py（约 1515 行起）对每个 Issue 取最新告警调 get_alert_relation_info（bkmonitor/utils/event_related_info.py），分两条路：
- 日志聚类路：get_log_clustering_info @ bkmonitor/utils/alert_drilling.py 扫描策略 labels，命中 LogClustering/NewClass/<索引集ID> 或 LogClustering/Count/<索引集ID> 前缀标签即认定为日志聚类 Issue，按聚类签名去对应 ES 索引集捞日志
- 非聚类路：查告警 query_config 的 (data_source_label, data_type_label) 是否在白名单内，共 5 组：(采集器, 日志)、(日志平台, 日志)、(日志平台, 时序)、(自定义, 事件)、(FTA, 事件)，命中才回查原始日志
- 两条路都不命中（如指标类）直接返回空串，不发起任何日志查询

接口契约：GET /fta/issue/issue/log_content/，入参 bk_biz_ids + issue_ids（数组），issue_ids 单批上限 10（serializer max_length=10），返回 {[issue_id]: {log_content: string}}；初始化给所有 issue_id 预置 {"log_content": ""}，失败静默返回不报错；指标类 Issue 与已删除成员（ES 查不到）均返回空串，由前端兜底接住（service 层已有 .catch(() => ({}))）。

已知不一致与对齐方案（2026-09-11，已同步前端）：合并明细抽屉 split-content.tsx 第 216 行直接渲染 issue.anomaly_message，未走 log_content 优先链，导致日志聚类类 Issue 在 Issue 列表与合并明细两处展示不一致（列表显示日志原文 ERROR biz/ds.go:325...，合并明细显示 anomaly_message 如 COUNT([采集项]...)）。对齐方案：打开合并明细抽屉时对成员 Issue 批量调用 log_content 接口，条目展示改为与列表完全一致的兜底链 log_content（清洗时间戳前缀后） || anomaly_message || '--'；实现要点：合并成员主键是 member_issue_id（非 issue.id）需做参数映射、成员数超 10 需按 10 条分批串行、建议 DATETIME_PREFIX_REGEX 抽共享常量、建议接口返回前先展示 anomaly_message 返回后覆盖；merge-content.tsx 第 183/231 行同类问题（直接展示 anomaly_message），可一并覆盖属可选范围。