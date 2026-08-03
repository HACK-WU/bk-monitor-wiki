# CHANGELOG

> **专家**: 元数据种子数据与数据字典专家
> **专题**: 元数据管理专题

---

## [2026-07-29] 初始创建

### 新增
- 创建专家目录 `.module-experts/元数据管理专题/元数据种子数据与数据字典专家/`
- 创建 `agent.md` — 专家名片，含覆盖文件清单、无子专家声明、与其他专家关系、使用指南
- 创建 `C0-使用总览.md` — 契约层黑盒使用文档：能力清单（数据源注册/结果表注册/字段定义/指标描述与单位/K8s指标事件/标签分类/存储路由/时序组事件组/BKCI数据）、能力边界、已知问题与常见坑
- 创建 `C1-能力契约.md` — 契约层 API 契约：11 个种子数据文件的结构契约（JSON schema 级描述）、8 个加载函数的契约、UnifyQuery 对接契约、依赖关系
- 创建 `implementation/01-架构.md` — 实现层架构：种子数据目录结构、三层映射架构、加载机制架构（Migration vs 运行时）、UnifyQuery 对接架构、2 个 Mermaid 架构图
- 创建 `implementation/02-实现.md` — 实现层实现细节：5 个加载函数实现、result_table_id 格式转换、K8s 全局缓存机制、关键代码路径
- 创建 `implementation/03-数据流转.md` — 实现层数据流转：JSON→Model→DB→UnifyQuery 全链路、2 个 Mermaid 序列图
- 创建 `implementation/04-模型.md` — 实现层数据模型：12 种种子数据文件的数据结构详解、tag 角色分类、label 三级分类体系、K8s YAML 结构
- 创建 `implementation/05-接口.md` — 实现层接口：7 个 Migration 加载函数接口、2 个 K8s 加载函数接口、3 个调用方关系
- 创建 `CHANGELOG.md` — 本文件

### 覆盖范围
- 种子数据文件：`init_datasource.json`, `init_resulttable.json`, `init_data.json`, `description_unit.json`, `init_label.json`, `init_storage.json`, `init_cluster_info.json`, `init_ts_or_event_group.json`, `k8s_metrics/*.yaml` (25个), `k8s_events.json`, `bkci_data.json`, `metadata_resulttablefield.txt`
- 加载机制：`0002_initial_data.py`, `0002_create_initial_metadata.py`, `0008_import_field_descriptions.py`, `k8s_metric.py` (2份)
- 消费方：`resources/resources.py`, `cmdb.py`, `metric_list_cache.py`, `check_k8s_metrics.py`
