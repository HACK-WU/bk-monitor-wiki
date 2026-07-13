# wiki-incremental · Wiki 增量更新工具库

> 维护 `bk-monitor-wiki/wiki/` 下 Markdown 文档与源代码仓库之间的双向引用索引，
> 根据 git commit 变更检测受影响的 Wiki 页面，支持增量更新。

## 架构概览

```
源文件变更 (git diff)
    │
    ▼
change_detection.py  ──▶  affected_wiki_paths (list)
    │                       feature_clusters (聚类新文件)
    │
    ├──▶ citation_cleanup.py  ──▶  清理旧引用 / 替换重命名
    ├──▶ format_validation.py ──▶  R1-R6 格式校验 + 机械修复
    └──▶ incremental_index.py ──▶  同步 metadata.json 索引
             │
             └── build_index()  ← index_builder.py (降级回退)
```

## 模块速览

| 模块 | 职责 | 关键导出 |
|------|------|----------|
| `index_builder.py` | 全量构建 `source_to_wiki` / `wiki_to_source` 索引 | `build_index()`, `parse_citations()`, `build_indexes()` |
| `change_detection.py` | git diff 变更检测 + 三级匹配 + 新文件聚类 | `detect_changes()`, `ChangeReport`, `FeatureCluster`, `MatchResult` |
| `citation_cleanup.py` | 清理 wiki 中已删除/重命名源文件的引用 | `cleanup_dead_citations()` |
| `format_validation.py` | R1-R5 格式校验 + 可机械修复的格式问题（R6 行号需人工补全） | `validate_and_fix()`, `Violation` |
| `incremental_index.py` | 增量更新受影响 wiki 的索引 | `incremental_index_update()`, `safe_index_update()`, `save_metadata()` |
| `json_utils.py` | 原子化 JSON 读写 | `load_json()`, `atomic_save_json()` |
|| `cli.py` | 命令行入口 | `build-index`, `detect`, `lookup` 子命令 |

## 快速开始

### 索引构建

```bash
cd /root/bk-monitor
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli build-index \
  --wiki-dir bk-monitor-wiki/wiki \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --repo-dir . \
  --repo-url git@github.com:TencentBlueKing/bk-monitor.git \
  --branch master \
  --output bk-monitor-wiki/wiki/metadata.json
```

- `--wiki-dir`：wiki Markdown 文件目录
- `--metadata`：已有 metadata.json（保留 excluded_paths/noise_paths 等配置）
- `--repo-dir`：源代码仓库根目录，用于自动获取 `HEAD` commit
- `--repo-url` / `--branch`：记录到 `metadata.source` 供追溯
- `--output`：输出路径（覆盖写入）

### 变更检测（dry-run）

```bash
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli detect \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --new-commit <new_commit> \
  --repo-dir .
```

输出示例：

```
Wiki incremental change analysis (e353b1f..3a3630a)

Changed files: 42 (excluded 18, total 60)
Affected wiki pages: 8

| 级别 | Wiki 页面 | 变更文件 |
|------|-----------|----------|
| [精确] | 告警系统设计/告警引擎核心.md | bkmonitor/alarm_backends/engine.py |
| [dirname] | API接口文档/数据查询.md | bkmonitor/query_api/views.py |
| [父目录] | 监控数据管理/数据模型.md | bkmonitor/data/backend.py |

新功能文件 (3):
- bkmonitor/new_module/views.py
- bkmonitor/new_module/serializers.py
- bkmonitor/new_module/urls.py

新功能文件簇 (1):
| 基础目录 | 文件数 | 可推断 | 文件列表 |
|----------|--------|--------|----------|
| bkmonitor/new_module | 3 | ✗ | views.py, serializers.py, urls.py |
```

- `新功能文件簇`：将新文件按公共父目录聚类，辅助 AI 判断是否构成独立新功能，决定新建 Wiki 还是扩展现有页面

匹配级别：
- `[精确]` — 源文件在索引中精确命中，优先更新
- `[dirname]` — 同目录模糊命中，须标注需审核
- `[父目录]` — 父目录回退命中，须标注需审核

### Wiki 反查（ranked lookup）

已知文件路径或 commit，反查受影响 Wiki 页面，按命中文件数降序排列。

```bash
# 指定文件路径
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli lookup \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --files bkmonitor/alarm_backends/engine.py bkmonitor/query_api/views.py

# 指定 commit（自动 diff 父提交）
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli lookup \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --new-commit 3a3630a \
  --repo-dir .

# 指定文件 + commit 合并查询（自动去重）
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli lookup \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --files bkmonitor/alarm_backends/engine.py \
  --new-commit 3a3630a \
  --old-commit e353b1f \
  --repo-dir .
```

输出示例：
```
指定文件: 2 个 + commit e353b1f..3a3630a: 42 个文件

共 8 篇 Wiki 页面受影响：

  [  5 文件]  告警系统设计/告警引擎核心.md
          ↳ bkmonitor/alarm_backends/engine.py, bkmonitor/alarm_backends/check.py ... +3

  [  3 文件]  API接口文档/告警管理API.md
          ↳ bkmonitor/api/alert.py, bkmonitor/api/alert/serializers.py, bkmonitor/api/alert/views.py

...

未匹配文件 (18):
  - bkmonitor/new_module/views.py
  ...
```

## Python API

### build_index

```python
from wiki_incremental import build_index

metadata = build_index(
    wiki_dir="wiki/",
    commit_id="e353b1fbc3fba22f7988f54aa43adff185d49706",
    base_metadata=existing_meta,              # 保留已有配置
    repo_url="git@github.com:TencentBlueKing/bk-monitor.git",
    branch="master",
)
# metadata["source_to_wiki"]  → {src_path: [wiki_path, ...]}
# metadata["wiki_to_source"]  → {wiki_path: [src_path, ...]}
# metadata["source"]          → {commit_id, repo_url, branch}
# metadata["stats"]           → {wiki_count, source_count, citation_count}
```

### detect_changes

```python
from wiki_incremental import detect_changes, format_report

report = detect_changes(
    old_commit="e353b1f",
    new_commit="3a3630a",
    metadata=metadata,
    repo_dir="/root/bk-monitor",
)
print(format_report(report))
print(report.affected_wikis)  # ["告警系统设计/告警引擎核心.md", ...]
print(report.feature_clusters) # [FeatureCluster(base_dir="bkmonitor/new_module", file_count=3, ...)]
```

### lookup_wikis

```python
from wiki_incremental import load_json, lookup_wikis, format_lookup

metadata = load_json("wiki/metadata.json")
source_to_wiki = metadata["source_to_wiki"]

# 按文件路径反查，返回 (ranked, unmatched)
ranked, unmatched = lookup_wikis(source_to_wiki, [
    "bkmonitor/alarm_backends/engine.py",
    "bkmonitor/query_api/views.py",
])
print(format_lookup(ranked, unmatched=unmatched))
# 共 8 篇 Wiki 页面受影响：
#
#   [  3 文件]  告警系统设计/告警引擎核心.md
#           ↳ bkmonitor/alarm_backends/engine.py, bkmonitor/alarm_backends/check.py ...
# ...
# 未匹配文件 (1):
#   - bkmonitor/query_api/views.py
```

### cleanup_dead_citations

```python
from wiki_incremental import cleanup_dead_citations

# 删除文件的引用
new_content = cleanup_dead_citations(
    wiki_content=old_content,
    dead_files=["bkmonitor/deleted_module/views.py"],
    renamed_files={},
)

# 重命名文件的引用
new_content = cleanup_dead_citations(
    wiki_content=old_content,
    dead_files=[],
    renamed_files={"bkmonitor/old/path.py": "bkmonitor/new/path.py"},
)
```

### validate_and_fix

```python
from wiki_incremental import validate_and_fix

content, violations = validate_and_fix(wiki_content)
# violations = [Violation(rule="R1", message="缺少 cite 标签", fixed=True), ...]
```

校验规则：

| 规则 | 内容 | 可机械修复 |
|------|------|-----------|
| R1 | `<cite>` 标签存在 | ✅ |
| R3 | 每个 `##` 章节有 `章节来源` | ✅ |
| R4 | Mermaid 图后有 `图表来源` / `图示来源` | ✅ |
| R5 | 引用路径使用 `file://` 前缀 | ✅ |
| R6 | 目录条目与 `##` 章节一致 | ✅ |

### incremental_index_update + save_metadata

```python
from wiki_incremental import incremental_index_update, safe_index_update, save_metadata

# 增量更新（只扫描 affected_wikis）
metadata = incremental_index_update(
    metadata=metadata,
    affected_wikis=["告警系统设计/告警引擎核心.md"],
    new_commit="3a3630a...",
    wiki_dir="wiki/",
)
save_metadata(metadata, "wiki/metadata.json")

# 安全更新（失败时自动降级为全量 build_index）
metadata = safe_index_update(metadata, affected_wikis, new_commit, wiki_dir)
```

## metadata.json 结构

```json
{
  "excluded_paths": ["bklog/", "bkmonitor/webpack/", "*/migrations/", "*/tests/", "*/__init__.py"],
  "noise_paths": ["*.pyc", "^docs/"],
  "source": {
    "commit_id": "e353b1fbc3fba22f7988f54aa43adff185d49706",
    "repo_url": "git@github.com:TencentBlueKing/bk-monitor.git",
    "branch": "master"
  },
  "source_to_wiki": {
    "bkmonitor/alarm_backends/engine.py": ["告警系统设计/告警引擎核心.md"]
  },
  "wiki_to_source": {
    "告警系统设计/告警引擎核心.md": ["bkmonitor/alarm_backends/engine.py"]
  },
  "stats": {
    "wiki_count": 132,
    "source_count": 1148,
    "citation_count": 1811
  },
  "wiki_path": "wiki/"
}
```

### 排除规则说明

| 字段 | 作用范围 | 语义 |
|------|----------|------|
| `excluded_paths` | build-index + detect | **完全排除**：不参与索引构建，也不参与变更检测 |
| `noise_paths` | detect only | **噪音过滤**：参与索引构建（wiki 可能引用），但 git diff 时不触发变更检测 |

路径格式支持三种：
- `*/migrations/` — 任意深度子目录匹配
- `*.pyc` — 扩展名匹配
- `^docs/` — 根目录前缀匹配
