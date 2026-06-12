---
id: SR-01
feature: Wiki增量更新Skill
sub_requirement: 索引构建工具
priority: P0
status: 已确认
created: 2026-06-12
---

# SR-01: 索引构建工具 (build_index.py)

## 1. 职责

全量扫描 wiki 目录下所有 `.md` 文件，解析 `<cite>`、章节来源、图表来源三种引用标记，构建 source_to_wiki / wiki_to_source 双向索引，写入 metadata.json。

## 2. 核心接口

```python
from dataclasses import dataclass

@dataclass
class Citation:
    """一条引用关系"""
    wiki_path: str          # wiki 相对路径
    source_path: str        # 源文件相对路径（去除 file:// 和行号）
    type: str               # cite / section_source / chart_source
    section_name: str = ""  # 归属章节（仅 section_source/chart_source 有值，cite 为文档级引用始终为空）

def build_index(wiki_dir: str, commit_id: str) -> dict:
    """
    主入口：全量扫描 wiki 目录，返回完整的 metadata dict。
    
    参数:
        wiki_dir: wiki 目录绝对路径
        commit_id: 当前 bk-monitor 仓库 commit hash
    
    返回:
        完整 metadata dict，包含 source_to_wiki 和 wiki_to_source
    """

def parse_citations(wiki_path: str, wiki_content: str) -> list[Citation]:
    """
    解析单个 wiki 文件中的所有引用关系。
    
    参数:
        wiki_path: wiki 文件相对路径（如 "告警系统设计/告警引擎核心/告警引擎核心.md"）
        wiki_content: wiki 文件完整内容
    
    返回:
        该文件中所有 Citation 列表
    """

def build_indexes(citations: list[Citation]) -> tuple[dict, dict]:
    """
    从引用列表构建双向索引。
    
    返回:
        (source_to_wiki, wiki_to_source) 两个 dict
    """
```

## 3. 引用解析规则

### 3.1 `<cite>` 标签解析

> **引用层级**：`<cite>` 中的引用是**文档级引用**（`section_name=""`），表示整篇 wiki 引用的源文件。
> `章节来源`/`图表来源` 中的引用是**章节级引用**（`section_name` 有值），表示特定章节引用的源文件。
> 索引构建时两者均纳入双向索引，但 Citation.type 和 section_name 保留区分信息。

**匹配模式**：`<cite>` 和 `</cite>` 之间的所有 `- [名称](file://路径)` 条目。

```
<cite>
**本文引用的文件**
- [apps.py](file://bkmonitor/alarm_backends/apps.py)
- [event.py](file://bkmonitor/alarm_backends/core/alert/event.py)
</cite>
```

**正则**：
```python
CITE_BLOCK_RE = re.compile(r'<cite>.*?</cite>', re.DOTALL)
CITE_ENTRY_RE = re.compile(r'- \[([^\]]+)\]\(file://([^)]+)\)')
```

**路径清洗**：
- 提取 `file://` 后的路径
- 去除 `#L1-L71` 等行号部分：`path.split('#')[0]`
- 所有路径为相对路径，不含 `file://` 前缀

### 3.2 章节来源解析

**实测发现**：现有 wiki 使用纯文本 `章节来源`（非 `**章节来源**`），共 11 处。需求文档模板中的 `**章节来源**` 与实际不符。

**实际格式**：
```markdown
## 项目结构
[内容]

章节来源
- [apps.py:16-22](file://bkmonitor/alarm_backends/apps.py#L16-L22)
- [constants.py:11-81](file://bkmonitor/alarm_backends/constants.py#L11-L81)
```

**正则**（兼容纯文本和加粗两种格式）：
```python
SECTION_SOURCE_HEADER_RE = re.compile(r'^\*{0,2}章节来源\*{0,2}\s*$', re.MULTILINE)
SECTION_SOURCE_ENTRY_RE = re.compile(r'- \[([^\]]+)\]\(file://([^)]+)\)')
```

**章节归属**：向上查找最近的 `##` 标题作为 section_name。

### 3.3 图表来源解析

**格式**（与章节来源同理）：
```markdown
```mermaid
graph TB
...
```

图表来源
- [apps.py:16-22](file://bkmonitor/alarm_backends/apps.py#L16-L22)
```

**正则**：
```python
CHART_SOURCE_HEADER_RE = re.compile(r'^\*{0,2}图表来源\*{0,2}\s*$', re.MULTILINE)
```

**图表归属**：向上查找最近的 ````mermaid` 代码块。

## 4. 索引构建算法

```python
def build_indexes(citations: list[Citation]) -> tuple[dict, dict]:
    source_to_wiki = {}   # {source_path: [wiki_path, ...]}
    wiki_to_source = {}   # {wiki_path: [source_path, ...]}
    
    for c in citations:
        # source_to_wiki
        if c.source_path not in source_to_wiki:
            source_to_wiki[c.source_path] = set()
        source_to_wiki[c.source_path].add(c.wiki_path)
        
        # wiki_to_source
        if c.wiki_path not in wiki_to_source:
            wiki_to_source[c.wiki_path] = set()
        wiki_to_source[c.wiki_path].add(c.source_path)
    
    # set → sorted list（确保确定性输出）
    return (
        {k: sorted(v) for k, v in source_to_wiki.items()},
        {k: sorted(v) for k, v in wiki_to_source.items()}
    )
```

## 5. metadata.json 输出结构

```json
{
  "wiki_path": "bk-monitor-wiki/wiki",
  "source": {
    "repo": "bk-monitor",
    "branch": "master",
    "commit_id": "<new_commit>"
  },
  "excluded_paths": ["bklog/", "bkmonitor/webpack/"],
  "noise_paths": [
    "*/migrations/",
    "*/tests/",
    "*/__init__.py",
    "*.pyc",
    "^docs/"
  ],
  "stats": {
    "wiki_count": 132,
    "source_count": 1481,
    "citation_count": 2626
  },
  "wiki_catalogs": [...],
  "source_to_wiki": {...},
  "wiki_to_source": {...}
}
```

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| wiki 文件解析失败（编码错误等） | 跳过该文件，输出警告到 stderr |
| `file://` 路径为空或格式异常 | 跳过该条目，记录到 warnings 列表 |
| wiki 目录不存在 | 抛出 FileNotFoundError |
| 重复引用（同一 source 在同一 wiki 中出现多次） | 去重（使用 set） |

## 7. 验收标准

1. `build_index.py` 可独立执行：`python build_index.py --wiki-dir <path> --commit <hash>`
2. 1481 个源文件全部索引（source_to_wiki keys 数量）
3. 双向索引数据完整（source_to_wiki + wiki_to_source 交叉验证）
4. orjson 序列化输出 ~392KB JSON
5. 执行耗时 < 5 秒

## 8. 格式规范修正记录

> **实测发现**：现有 wiki 中 `章节来源` 和 `图表来源` 均为纯文本格式，不使用 `**` 加粗。需求文档 §7.1 模板中的 `**章节来源**` 和 `**图表来源**` 与实际不符。
> 
> **设计决策**：解析时兼容两种格式（`^\*{0,2}章节来源\*{0,2}$`），生成新内容时统一使用纯文本格式（与现有 wiki 保持一致）。
