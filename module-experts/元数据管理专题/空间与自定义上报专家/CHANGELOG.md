# CHANGELOG

> **专家**: 空间与自定义上报专家
> **专题**: 元数据管理专题
> **路径**: `.module-experts/元数据管理专题/空间与自定义上报专家/`

---

## [2026-07-28] 初始创建

### 专家层（8 份文档）
- `agent.md` — 专家名片：职责、覆盖文件、子专家列表、依赖关系、使用指南
- `C0-使用总览.md` — 能力清单、边界、已知坑、子专家导航
- `C1-能力契约.md` — Space/CustomReport/RecordRule API 契约（含代码示例）
- `implementation/01-架构.md` — 模块分层架构图、文件职责、依赖关系、术语表
- `implementation/02-实现.md` — 核心实现：Space 路由推送、CustomReport 全链路、RecordRule 匹配
- `implementation/03-数据流转.md` — 空间路由推送、自定义上报创建、记录规则数据流
- `implementation/04-模型.md` — Space 模型族（6个）+ CustomReport 模型族（4个）+ RecordRule 模型族（2个）
- `implementation/05-接口.md` — 50+ 方法签名

### 子专家：空间管理子专家（8 份文档）
- `sub-experts/空间管理子专家/agent.md` — 专家名片
- `sub-experts/空间管理子专家/C0-使用总览.md` — 空间类型管理、生命周期、路由推送、查询、数据源授权
- `sub-experts/空间管理子专家/C1-能力契约.md` — Space/Manager/SpaceTableIDRedis/工具函数 API 契约
- `sub-experts/空间管理子专家/implementation/01-架构.md` — 模块分层架构图、文件职责、依赖关系
- `sub-experts/空间管理子专家/implementation/02-实现.md` — Redis 路由推送机制、空间 CRUD、批量创建、数据源授权
- `sub-experts/空间管理子专家/implementation/03-数据流转.md` — 路由推送、空间创建、空间合并数据流
- `sub-experts/空间管理子专家/implementation/04-模型.md` — 6 个 Space 模型字段定义 + 枚举常量
- `sub-experts/空间管理子专家/implementation/05-接口.md` — 40+ 方法签名

### 子专家：自定义上报子专家（8 份文档）
- `sub-experts/自定义上报子专家/agent.md` — 专家名片
- `sub-experts/自定义上报子专家/C0-使用总览.md` — 时序/事件/日志上报、记录规则能力清单
- `sub-experts/自定义上报子专家/C1-能力契约.md` — CustomGroupBase/TimeSeriesGroup/EventGroup/LogGroup/RecordRule API 契约
- `sub-experts/自定义上报子专家/implementation/01-架构.md` — 模块分层架构图、文件职责、依赖关系
- `sub-experts/自定义上报子专家/implementation/02-实现.md` — 自定义上报全链路、时序指标同步双通道、事件维度自动发现、日志 Token 管理
- `sub-experts/自定义上报子专家/implementation/03-数据流转.md` — 四种上报类型 + 记录规则数据流
- `sub-experts/自定义上报子专家/implementation/04-模型.md` — CustomReport 模型族（4个）+ RecordRule 模型族（2个）
- `sub-experts/自定义上报子专家/implementation/05-接口.md` — 50+ 方法签名

### 覆盖源码文件
- `space/`: `space.py`, `constants.py`, `managers.py`, `utils.py`, `space_table_id_redis.py`, `serializers.py`
- `custom_report/`: `base.py`, `time_series.py`, `event.py`, `log.py`, `common.py`
- `record_rule/`: `models.py`, `tasks.py`, `utils.py`, `serializers.py`

### 统计
- 总文档数: 24 份
- 专家层: 8 份
- 子专家层: 16 份（2 子专家 × 8 份）
- 总大小: ~200 KB
