# 元数据种子数据与数据字典专家

> **专题**: 元数据管理专题
> **创建时间**: 2026-07-29
> **最后更新**: 2026-07-29
> **类型**: 专家（无子专家）

---

## 一、专家名片

| 属性 | 值 |
|------|-----|
| **名称** | 元数据种子数据与数据字典专家 |
| **职责** | 管理 bk-monitor 所有内置种子数据（JSON/YAML）的定义、加载机制，以及作为 UnifyQuery 查询链路的"数据字典"层——提供 table/field/unit/description 的映射来源 |
| **目录** | `.module-experts/元数据管理专题/元数据种子数据与数据字典专家/` |

## 二、覆盖文件清单

| 文件 | 大小 | 主要内容 |
|------|------|---------|
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_datasource.json` | 11KB | 内置数据源定义（bk_data_id, source_label, type_label, etl_config） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_resulttable.json` | 209KB | 内置结果表及字段定义（table_id, field_list 含 field_name/tag/unit/description） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_data.json` | 177KB | 旧版综合种子数据（result_table_list + datasource_list + cluster_list） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/description_unit.json` | 98KB | 指标描述与单位（result_table_id + item → conversion_unit, description, item_display） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_label.json` | 4KB | 标签分类体系（source_label, result_table_label, type_label 三级分类） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_storage.json` | 0.7KB | 存储路由配置（哪些表走 Kafka） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_cluster_info.json` | 0.7KB | 存储集群初始化配置（Kafka/InfluxDB/ES 地址） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/init_ts_or_event_group.json` | 2KB | 时序组和事件组初始化 |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/k8s_metrics/` | 25个YAML | K8s 各组件内置指标定义（apiserver, kubelet, etcd, container 等） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/k8s_events.json` | 6KB | K8s 内置事件定义（事件名 + 维度列表） |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/bkci_data.json` | 6KB | BKCI 数据指标定义 |
| `bk-monitor-base/src/bk_monitor_base/metadata/data/metadata_resulttablefield.txt` | 5KB | 表字段速查（table_id\|field\|unit\|description 制表符分隔） |
| `bk-monitor-base/src/bk_monitor_base/metadata/migrations/0002_initial_data.py` | 7KB | Django Migration 加载入口（bk-monitor-base 侧） |
| `bkmonitor/metadata/migrations/0002_create_initial_metadata.py` | 8KB | 旧版 Migration 加载入口（init_data.json） |
| `bkmonitor/metadata/migrations/0008_import_field_descriptions.py` | 8KB | description_unit 导入 Migration |
| `bk-monitor-base/src/bk_monitor_base/metadata/utils/k8s_metric.py` | 1.2KB | K8s 指标/事件运行时加载（bk-monitor-base 侧） |
| `bkmonitor/bkmonitor/utils/k8s_metric.py` | 1.9KB | K8s 指标/事件运行时加载（bkmonitor 侧） |

## 三、无子专家

本专家直接覆盖所有种子数据文件，不设子专家。

## 四、与其他专家的关系

### 4.1 上游依赖

| 上游专家 | 依赖内容 | 用途 |
|---------|---------|------|
| 元数据核心模型专家 | DataSource、ResultTable、ResultTableField、Label 等模型定义 | 种子数据加载时创建/更新这些模型的实例 |
| 存储与数据链路专家 | ClusterInfo、InfluxDBStorage、ESStorage、KafkaStorage | 种子数据中的集群配置和存储路由 |

### 4.2 下游消费者

| 下游模块 | 引用方式 | 影响 |
|---------|---------|------|
| `monitor_web/cc/resources/cmdb.py` | `load_data_source("bk_monitor", "time_series")` → `table="system.cpu_summary"` → `field="usage"` | 种子数据是 UnifyQuery 查询的"数据字典"层 |
| `metadata/resources/resources.py` | `get_built_in_k8s_metrics()` / `get_built_in_k8s_events()` | K8s 指标/事件查询接口 |
| `monitor_web/strategies/metric_list_cache.py` | `get_built_in_k8s_metrics()` | 策略指标列表缓存 |
| `metadata/management/commands/check_k8s_metrics.py` | `get_built_in_k8s_metrics()` | K8s 指标校验命令 |

## 五、使用指南

### 5.1 何时查阅本专家

- 需要了解内置数据源/结果表/字段的定义来源
- 需要了解种子数据的 JSON 结构和加载机制
- 需要了解 UnifyQuery 查询时 table/field/unit 的映射来源
- 需要新增/修改内置种子数据
- 需要了解 K8s 内置指标/事件的定义和加载方式
- 需要了解 description_unit 的格式和导入流程

### 5.2 文档导航

| 文档 | 类型 | 说明 |
|------|------|------|
| [C0-使用总览.md](C0-使用总览.md) | 契约层 | 黑盒使用文档：能力概览、典型场景、快速上手 |
| [C1-能力契约.md](C1-能力契约.md) | 契约层 | 种子数据文件结构契约、加载函数契约、UnifyQuery 对接契约 |
| [implementation/01-架构.md](implementation/01-架构.md) | 实现层 | 种子数据整体架构：三层映射、加载机制、Mermaid 架构图 |
| [implementation/02-实现.md](implementation/02-实现.md) | 实现层 | 各加载函数实现细节、格式转换、全局缓存机制 |
| [implementation/03-数据流转.md](implementation/03-数据流转.md) | 实现层 | 种子数据从 JSON → Model → DB → UnifyQuery 全链路 |
| [implementation/04-模型.md](implementation/04-模型.md) | 实现层 | 各 JSON 文件数据结构详解、tag 角色分类、label 体系 |
| [implementation/05-接口.md](implementation/05-接口.md) | 实现层 | 加载函数接口签名、K8s 指标/事件接口、调用关系 |

---

> **下一步**: 查阅 [C0-使用总览.md](C0-使用总览.md) 了解本专家覆盖的能力和典型使用场景。
