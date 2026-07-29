# 告警屏蔽专家

## 基本信息

| 属性 | 值 |
|------|-----|
| 专家名称 | 告警屏蔽专家 |
| 模块路径 | `bkmonitor/packages/monitor_web/shield` + `bkmonitor/alarm_backends/service/converge/shield` |
| 创建日期 | 2026-07-28 |
| 源文件数 | ~15 |
| 屏蔽类型 | scope / strategy / event / alert / dimension |

## 三层资产

### 契约层（黑盒使用）

| 文档 | 说明 | 何时阅读 |
|------|------|----------|
| [C0-使用总览](C0-使用总览.md) | 能力清单、使用边界、已知坑、快速导航 | 第一次使用本专家时 |
| [C1-能力契约](C1-能力契约.md) | 所有公开类/方法契约，含参数表、返回值、异常、代码示例 | 需要调用具体方法时 |
| [C2-使用流程](C2-使用流程.md) | 5 个核心业务目标的调用路径和流程图 | 理解端到端流程时 |

### 实现层（白盒导航）

| 文档 | 说明 | 何时阅读 |
|------|------|----------|
| [01-架构](implementation/01-架构.md) | 整体架构图、文件结构、分层说明 | 理解模块设计时 |
| [02-实现](implementation/02-实现.md) | CRUD、五种类型处理、匹配检测、通知、时间处理 | 深入实现细节时 |
| [03-数据流转](implementation/03-数据流转.md) | 6 条数据流的序列图和流程图 | 追踪数据流向时 |
| [04-模型](implementation/04-模型.md) | Shield 模型字段、dimension_config 结构、常量表 | 查看数据结构时 |
| [05-接口](implementation/05-接口.md) | API 端点表、Resource 清单、内部调用接口 | 对接接口时 |

### 源代码（最终确认）

| 文件 | 职责 |
|------|------|
| `monitor_web/shield/views.py` | ShieldViewSet，11 个端点路由 |
| `monitor_web/shield/resources/backend_resources.py` | 后端 CRUD（27KB，最核心） |
| `monitor_web/shield/resources/frontend_resources.py` | 前端展示增强（14KB） |
| `monitor_web/shield/resources/celery_resources.py` | Celery 定时任务资源 |
| `monitor_web/shield/serializers.py` | 5 种屏蔽类型序列化器 |
| `monitor_web/shield/utils.py` | ShieldDetectManager + DisplayManager |
| `alarm_backends/service/converge/shield/shield_obj.py` | ShieldObj 匹配核心（19KB） |
| `alarm_backends/service/converge/shield/shielder/saas_config.py` | 5 种 Shielder 实现（12KB） |
| `alarm_backends/service/converge/shield/manager.py` | ShieldManager 链式管理 |
| `alarm_backends/core/cache/shield.py` | Redis 缓存管理 |
| `alarm_backends/service/converge/shield/tasks.py` | 通知定时任务 |
| `alarm_backends/service/alert/manager/checker/shield.py` | 告警屏蔽状态检测 |
| `bkmonitor/utils/shield.py` | BaseShieldDisplayManager（14KB） |
| `bkmonitor/models/base.py` | Shield 模型定义 |
| `constants/shield.py` | 常量定义 |
