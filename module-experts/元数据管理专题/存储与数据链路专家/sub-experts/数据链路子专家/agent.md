# 数据链路子专家

> **父专家**: 存储与数据链路专家
> **专题**: 元数据管理专题
> **创建时间**: 2026-07-28

---

## 一、子专家名片

| 属性 | 值 |
|------|-----|
| 名称 | 数据链路子专家 |
| 职责 | 管理监控数据链路的编排、配置、下发与元数据同步，覆盖 metadata 模型定义层 |
| 目录 | `sub-experts/数据链路子专家/` |

## 二、覆盖文件清单

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `models/data_link/data_link.py` | 56 KB | DataLink 主模型、策略枚举、链路申请/删除/元数据同步 |
| `models/data_link/data_link_configs.py` | 42 KB | DataLinkResourceConfigBase 基类、DataIdConfig、ResultTableConfig、VMStorageBindingConfig、ESStorageBindingConfig、DorisStorageBindingConfig、DataBusConfig、ConditionalSinkConfig、ClusterConfig |
| `models/data_link/relation.py` | 18 KB | BKBase V4 组件关联关系重建 |
| `models/data_link/service.py` | 8 KB | apply_data_id_v2、get_data_id_v2、组件状态/配置查询 |
| `models/data_link/utils.py` | 10 KB | 命名规则、模板渲染、字段组装 |
| `models/data_link/constants.py` | 3.5 KB | DataLinkKind、DataLinkResourceStatus、命名空间常量 |
| `models/data_link/__init__.py` | 542 B | 对外导出 |

## 三、范围边界

- **本子专家覆盖**：`metadata/models/data_link/` 的模型定义层
- **不覆盖**：APM 层的数据链路操作服务（`apm/views.py`、`apm/models/config.py`、`apm/core/discover/precalculation/storage.py`）
- **不覆盖**：存储引擎模型（归存储引擎子专家）

## 四、关键概念

- **DataLink**：链路编排器，按策略组装 BKBase 组件
- **DataLinkResourceConfigBase**：组件配置基类，提供 compose_config/delete_config/component_status/component_config
- **DataLinkKind**：BKBase 组件类型枚举
- **DataLinkResourceStatus**：资源状态枚举（Initializing → Creating → Pending → OK）
- **namespace**：按数据域隔离（bkmonitor/bklog/bkapm）
