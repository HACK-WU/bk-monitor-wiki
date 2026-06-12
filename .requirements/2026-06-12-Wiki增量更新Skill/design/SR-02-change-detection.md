---
id: SR-02
feature: Wiki增量更新Skill
sub_requirement: 变更检测与匹配引擎
priority: P0
status: 已确认
created: 2026-06-12
---

# SR-02: 变更检测与匹配引擎

## 1. 职责

执行 `git diff --name-status`（含 pathspec 排除），通过三级匹配策略定位受影响的 wiki 页面，输出四类变更分类结果。

## 2. 核心接口

```python
from dataclasses import dataclass, field

@dataclass
class MatchResult:
    """单条匹配结果"""
    level: str              # exact / dirname / parent / none
    changed_file: str       # 变更文件路径
    wiki_paths: list[str]   # 命中的 wiki 路径列表

@dataclass
class ChangeReport:
    """变更检测报告"""
    exact_hits: list[MatchResult] = field(default_factory=list)
    dirname_hits: list[MatchResult] = field(default_factory=list)
    parent_hits: list[MatchResult] = field(default_factory=list)
    new_features: list[str] = field(default_factory=list)   # status=A 且无 wiki 引用
    unmatched: list[str] = field(default_factory=list)      # status=M/D 且无 wiki 引用
    excluded_count: int = 0  # 被排除的文件数

def detect_changes(
    old_commit: str,
    new_commit: str,
    metadata: dict,
    repo_dir: str = "."
) -> ChangeReport:
    """
    主入口：执行变更检测全流程。
    
    参数:
        old_commit: metadata.json 中记录的 commit_id
        new_commit: 用户指定的目标 commit
        metadata: metadata.json 解析后的 dict
        repo_dir: bk-monitor 仓库路径
    """

def build_pathspec_args(excluded_paths: list, noise_paths: list) -> list[str]:
    """将 metadata.json 过滤规则转换为 git pathspec ':!' 参数列表"""

def three_level_match(changed_file: str, source_to_wiki: dict) -> MatchResult:
    """三级匹配：精确 → dirname → 父目录回退"""
```

## 3. pathspec 排除实现

### 3.1 转换规则

| metadata.json 规则类型 | 示例值 | git pathspec 参数 | 转换逻辑 | 备注 |
|----------------------|--------|------------------|---------|------|
| `excluded_paths` 目录 | `bklog/` | `:!bklog/*` | 加 `/*` 后缀 | `*` 确保匹配目录内所有文件 |
| `noise_paths` 子路径 | `*/migrations/` | `:!*/migrations/*` | 保留通配符，加 `/*` | 末尾 `/` → `/*` |
| `noise_paths` 文件名 | `*/__init__.py` | `:!*/__init__.py` | 保留 `*/` 前缀 | 精确文件匹配 |
| `noise_paths` 后缀 | `*.pyc` | `:!*.pyc` | 直接透传 | 后缀通配 |
| `noise_paths` 路径前缀 | `^docs/` | `:!docs/*` | 去 `^`，加 `/*` | 等效于 excluded_paths |

> **边界说明**：实测确认 `:!dir/*` 在 `git diff --name-status` 中可正确排除目录下所有文件。
> `git diff --name-status` 输出仅含文件路径，无需处理目录本身的排除。

### 3.2 转换函数

```python
def build_pathspec_args(excluded_paths: list, noise_paths: list) -> list[str]:
    args = []
    
    # excluded_paths: 目录前缀 → :!<dir>/*
    for path in excluded_paths:
        args.append(f":!{path}*")
    
    # noise_paths: 按语法类型转换
    for pattern in noise_paths:
        if pattern.startswith("^"):
            # 路径前缀匹配: ^docs/ → :!docs/*
            args.append(f":!{pattern[1:]}*")
        elif pattern.startswith("*/"):
            if pattern.endswith("/"):
                # 子路径: */migrations/ → :!*/migrations/*
                args.append(f":!{pattern}*")
            else:
                # 文件名: */__init__.py → :!*/__init__.py
                args.append(f":!{pattern}")
        elif pattern.startswith("*."):
            # 后缀: *.pyc → :!*.pyc
            args.append(f":!{pattern}")
    
    return args
```

### 3.3 git diff 命令构造

```python
def run_git_diff(old_commit: str, new_commit: str, metadata: dict, repo_dir: str) -> list[tuple[str, str]]:
    """
    执行 git diff，返回 [(status, path), ...] 列表。
    status: A=added, M=modified, D=deleted, R=renamed
    """
    pathspec_args = build_pathspec_args(
        metadata.get("excluded_paths", []),
        metadata.get("noise_paths", [])
    )
    
    cmd = ["git", "--no-pager", "diff", "--name-status",
           f"{old_commit}..{new_commit}", "--"] + pathspec_args
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_dir)
    
    entries = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        if parts[0].startswith("R"):
            # R100\told_path\tnew_path
            entries.append(("R", parts[2], parts[1]))  # (status, new_path, old_path)
        else:
            entries.append((parts[0], parts[1]))       # (status, path)
    
    return entries
```

## 4. 三级匹配算法

```python
import os

def three_level_match(changed_path: str, source_to_wiki: dict) -> MatchResult:
    # Level 1: 精确匹配 O(1)
    if changed_path in source_to_wiki:
        return MatchResult("exact", changed_path, source_to_wiki[changed_path])
    
    changed_dir = os.path.dirname(changed_path)
    
    # Level 2: dirname 匹配 — 同目录
    dirname_wikis = set()
    for key, wikis in source_to_wiki.items():
        if os.path.dirname(key) == changed_dir and key != changed_path:
            dirname_wikis.update(wikis)
    
    if dirname_wikis:
        return MatchResult("dirname", changed_path, sorted(dirname_wikis))
    
    # Level 3: 父目录回退 — 前缀匹配
    parent_dir = os.path.dirname(changed_dir)
    if parent_dir:
        parent_wikis = set()
        for key, wikis in source_to_wiki.items():
            key_dir = os.path.dirname(key)
            if key_dir.startswith(parent_dir + "/"):
                parent_wikis.update(wikis)
        
        if parent_wikis:
            return MatchResult("parent", changed_path, sorted(parent_wikis))
    
    return MatchResult("none", changed_path, [])
```

## 5. 变更分类逻辑

```python
def classify_changes(git_entries: list, source_to_wiki: dict) -> ChangeReport:
    report = ChangeReport()
    
    for entry in git_entries:
        if len(entry) == 3:  # renamed
            status, new_path, old_path = entry
            # 对 old_path 做匹配（重命名影响旧路径的引用）
            result = three_level_match(old_path, source_to_wiki)
        else:
            status, path = entry
            result = three_level_match(path, source_to_wiki)
        
        if result.level == "exact":
            report.exact_hits.append(result)
        elif result.level == "dirname":
            report.dirname_hits.append(result)
        elif result.level == "parent":
            report.parent_hits.append(result)
        else:  # none
            if status == "A":
                report.new_features.append(path)
            else:
                report.unmatched.append(path)
    
    return report
```

## 6. 输出格式

### 6.1 结构化数据

```python
# ChangeReport 示例
ChangeReport(
    exact_hits=[
        MatchResult("exact", "bkmonitor/metadata/models/result_table.py",
                    ["数据库设计/表结构.md", "数据链路/数据模型.md", ...])
    ],
    dirname_hits=[
        MatchResult("dirname", "bkmonitor/metadata/models/data_link/relation.py",
                    ["数据链路/关系管理.md"])
    ],
    parent_hits=[
        MatchResult("parent", "bkmonitor/apm/models/shared_datasource.py",
                    ["APM全栈监控/APM核心架构.md"])
    ],
    new_features=["bkmonitor/new_module/models.py"],
    unmatched=["bkmonitor/metadata/utils.py"],
    excluded_count=27
)
```

### 6.2 用户可读输出

```
📋 变更检测分析 (e353b1f → abc1234)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

变更文件：41 个（排除 27 个）
受影响 wiki：26 个

| 级别 | Wiki 页面 | 变更文件 |
|------|-----------|---------|
| [精确] | 数据库设计/表结构.md | metadata/models/result_table.py |
| [精确] | 数据链路/数据模型.md | metadata/models/result_table.py |
| [dirname] | 数据链路/关系管理.md | metadata/models/data_link/relation.py |
| [父目录] | APM全栈监控/APM核心架构.md | apm/models/shared_datasource.py |

🆕 新功能文件（1 个）:
  - bkmonitor/new_module/models.py

⚠️ 未覆盖变更（9 个）:
  - bkmonitor/metadata/utils.py (M)
  - ...
```

## 7. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| old_commit 不存在 | 提示用户检查 commit hash |
| new_commit 不存在 | 提示用户检查 commit hash |
| git diff 执行失败 | 输出 stderr 错误信息 |
| metadata.json 中缺少 excluded_paths / noise_paths | 使用空列表默认值 |
| source_to_wiki 为空 | 提示需要先执行 build_index |

## 8. 验收标准

1. git diff 正确使用 pathspec 排除语法（实测已验证等价于 grep 后处理）
2. 三级匹配均有测试用例覆盖
3. 四类分类输出正确（精确命中 / 模糊命中 / 新功能 / 无命中）
4. 输出标注匹配级别标签：`[精确]` `[dirname]` `[父目录]` `[新功能]`
5. excluded_count 准确记录被排除的文件数
