---
groupPath: 待生效变更/告警屏蔽
relation: 告警屏蔽专题记忆补end_policy与静默关闭机制
exportedAt: "2026-09-10T08:27:26.839Z"
---
【待生效变更｜告警屏蔽专题记忆补end_policy与静默关闭机制】
- 触发来源：PR#12433（feat: 支持屏蔽结束后静默关闭告警，TAPD 1010158081137962111 选项二实现）
- 资产类型：ki 记忆
- 影响资产：专题记忆/告警屏蔽 下的 架构总览、五种屏蔽类型对比与选择、屏蔽匹配引擎双维度校验、屏蔽缓存同步机制 共 4 条 Relation
- 变更类型：修改
- 当前内容：按“五种屏蔽类别（业务/主机/IP/维度/PromQL）+ 匹配引擎双维度（时间范围×维度条件）+ 缓存同步（Web写Redis/引擎读）+ 通知幂等”描述，无屏蔽结束策略概念
- 合并后应为：
  - 五种屏蔽类型对比与选择：新增正交维度 end_policy（notify_once 默认=屏蔽结束对未恢复告警补发一次通知，保持现行为；close=屏蔽期间产生的告警被接管，期间不通知、不执行处理套餐，结束时静默关闭），end_policy 与屏蔽类别正交组合，仅新建屏蔽页可选，快捷屏蔽两入口不传走默认 notify_once
  - 屏蔽匹配引擎双维度校验：新增“告警维度接管判定”——CloseShieldMatcher（converge/shield/close.py）对 end_policy=close 且告警 begin_time（秒级）落在屏蔽窗口内时 take_over：写 alert.shield_end_close=true + shield_end_close_config（window_end 快照仅溯源）；首接粘滞（已接管不重选）；is_match 对 close 屏蔽从“当前时间匹配”改为“告警 begin_time 落窗匹配”，时间解析走 _BusinessCalendar 业务时区
  - 屏蔽缓存同步机制：新增关闭周期任务 alarm_backends/service/alert/manager/shield_tasks.py（分钟级，按 biz 分组复读缓存校验归属、读 DB end_time 判到期、scan 查 ABNORMAL+shield_end_close 批量关闭，先持久化再更缓存，BulkIndexError 部分回滚剔除失败 ID）
  - 架构总览：新增 7 个隔离点（通知信号/分派/状态检查/composite/动作创建/周期检查/扫描过滤）切断托管告警全部副作用；发布顺序依赖 DB迁移→ES mapping 加 shield_end_close→消费者分流→关闭任务部署→前端放开选项二
- 状态：待生效
- 登记时间：2026-09-10