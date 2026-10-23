# profile（`profile`）

> **职责**：Profiling 子模块（apm_web 内）：Profile 采集、解析与查询

> **职责**：Profiling 子模块（apm_web 内）：Profile 采集、解析与查询

- **位置**：`packages/apm_web/profile/` · 归属文件 **29** 个 · 约 **4686** 行
- **定义**：`packages/apm_web/profile/models.py:1`（django）
- **挂载前缀**：`/profile_api` · 视图/接口入口 **13** 个
- **置信度**：🟡（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`apm_web`、`bkmonitor`、`core.drf_resource`
- **被依赖**（动它会影响）：无

## 数据表（4）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `apm_web_application` ⚠︎默认命名 | Application | 2 | import（apm_web） | `packages/apm_web/profile/views.py:29` |
| `apm_web_profileuploadrecord` ⚠︎默认命名 | ProfileUploadRecord | 3 | import（apm_web） | `packages/apm_web/profile/views.py:29` |
| `bkmonitor_querytemplate` ⚠︎默认命名 | QueryTemplate | 1 | import（bkmonitor） | `packages/apm_web/profile/resources.py:23` |
| `metadata_label` ⚠︎默认命名 | Label | 3 | import（metadata） | `packages/apm_web/profile/doris/converter.py:15` |

## 归属文件（29）

- `packages/apm_web/profile/models.py`
- `packages/apm_web/profile/views.py`
- `packages/apm_web/profile/file_handler.py`
- `packages/apm_web/profile/collector.py`
- `packages/apm_web/profile/__init__.py`
- `packages/apm_web/profile/serializers.py`
- `packages/apm_web/profile/patch.py`
- `packages/apm_web/profile/urls.py`
- `packages/apm_web/profile/profileconverter.py`
- `packages/apm_web/profile/constants.py`
- `packages/apm_web/profile/resources.py`
- `packages/apm_web/profile/diagrams/ebpf_converter.py`
- `packages/apm_web/profile/diagrams/callgraph.py`
- `packages/apm_web/profile/diagrams/grafana_flame.py`
- `packages/apm_web/profile/diagrams/dotgraph.py`
- `packages/apm_web/profile/diagrams/__init__.py`
- `packages/apm_web/profile/diagrams/tendency.py`
- `packages/apm_web/profile/diagrams/diff.py`
- `packages/apm_web/profile/diagrams/flamegraph.py`
- `packages/apm_web/profile/diagrams/tree_converter.py`
- `packages/apm_web/profile/diagrams/table.py`
- `packages/apm_web/profile/diagrams/base.py`
- `packages/apm_web/profile/doris/converter.py`
- `packages/apm_web/profile/doris/__init__.py`
- `packages/apm_web/profile/doris/querier.py`
- `packages/apm_web/profile/perf/converter.py`
- `packages/apm_web/profile/perf/__init__.py`
- `packages/apm_web/profile/pprof/converter.py`
- `packages/apm_web/profile/pprof/__init__.py`
