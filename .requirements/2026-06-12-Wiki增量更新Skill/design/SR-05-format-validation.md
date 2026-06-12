---
id: SR-05
feature: Wiki增量更新Skill
sub_requirement: 格式校验与修复
priority: P1
status: 已确认
created: 2026-06-12
---

# SR-05: 格式校验与修复

## 1. 职责

对更新后的 wiki 内容执行 R1-R6 格式规则校验链，不合规项自动修复，确保输出 wiki 格式一致。

## 2. 核心接口

```python
from dataclasses import dataclass

@dataclass
class Violation:
    """一条违规记录"""
    rule: str       # R1-R6
    message: str    # 违规描述
    fixed: bool     # 是否已修复

def validate_and_fix(wiki_content: str) -> tuple[str, list[Violation]]:
    """
    R1-R6 校验链，不通过则自动修复。
    
    参数:
        wiki_content: 更新后的 wiki 内容
    
    返回:
        (修复后内容, 违规记录列表)
    
    最多执行 3 轮校验-修复循环，防止死循环。
    """
```

## 3. 校验规则清单

> **注意**：实测发现现有 wiki 使用纯文本 `章节来源`（非 `**章节来源**`），校验和修复均以纯文本为准。

| 规则 | 校验方法 | 修复策略 |
|------|---------|---------|
| R1 | 文件开头是否有 `<cite>...</cite>` 块 | 生成空 cite 骨架，等待 AI 补充引用 |
| R2 | cite 中路径是否为相对路径、不含 `file://` 以外的前缀 | 去除 `file://` 前缀（如误写为绝对路径） |
| R3 | 每个 `##` 章节后是否有 `章节来源` 段落 | 在章节末尾插入 `章节来源` 骨架 |
| R4 | 每个 ` ```mermaid ` 代码块后是否有 `图表来源` 段落 | 在代码块后插入 `图表来源` 骨架 |
| R5 | 引用格式是否为 `[名称](file://相对路径)` | 修正格式错误（如缺少 file://） |
| R6 | 目录链接是否与实际 `##` 标题对应 | 根据实际标题重新生成目录 |

## 4. 校验链执行流程

```python
MAX_FIX_ROUNDS = 3

def validate_and_fix(wiki_content):
    violations = []
    content = wiki_content
    
    for round_num in range(MAX_FIX_ROUNDS):
        round_violations = []
        
        # R1: cite 标签存在
        if not has_cite_block(content):
            round_violations.append(Violation("R1", "缺少 cite 标签", True))
            content = fix_r1_add_cite(content)
        
        # R2: cite 路径格式
        bad_paths = find_bad_cite_paths(content)
        if bad_paths:
            round_violations.append(Violation("R2", f"cite 路径格式错误: {bad_paths}", True))
            content = fix_r2_paths(content, bad_paths)
        
        # R3: 章节来源
        missing_sections = find_missing_section_sources(content)
        if missing_sections:
            round_violations.append(Violation("R3", f"缺少章节来源: {missing_sections}", True))
            content = fix_r3_section_sources(content, missing_sections)
        
        # R4: 图表来源
        missing_charts = find_missing_chart_sources(content)
        if missing_charts:
            round_violations.append(Violation("R4", f"缺少图表来源: {missing_charts}", True))
            content = fix_r4_chart_sources(content, missing_charts)
        
        # R5: 引用格式
        bad_refs = find_bad_references(content)
        if bad_refs:
            round_violations.append(Violation("R5", f"引用格式错误: {bad_refs}", True))
            content = fix_r5_references(content, bad_refs)
        
        # R6: 目录对应
        if not is_toc_consistent(content):
            round_violations.append(Violation("R6", "目录与章节不对应", True))
            content = fix_r6_regenerate_toc(content)
        
        violations.extend(round_violations)
        
        # 如果本轮没有违规，校验通过
        if not round_violations:
            break
    
    return content, violations
```

## 5. 各规则检测与修复实现

### 5.1 R1: cite 标签

```python
def has_cite_block(content: str) -> bool:
    return bool(re.search(r'<cite>.*?</cite>', content, re.DOTALL))

def fix_r1_add_cite(content: str) -> str:
    """在标题后插入 cite 骨架"""
    cite_skeleton = "\n<cite>\n**本文引用的文件**\n</cite>\n"
    # 在第一个 ## 之前插入
    return re.sub(r'(\n## )', cite_skeleton + r'\1', content, count=1)
```

### 5.2 R2: cite 路径格式

```python
def find_bad_cite_paths(content: str) -> list[tuple[str, str]]:
    """找出 cite 中路径格式错误的条目，返回 [(显示名, 错误路径), ...]"""
    cite_block = re.search(r'<cite>.*?</cite>', content, re.DOTALL)
    if not cite_block:
        return []
    
    bad = []
    for match in re.finditer(r'- \[([^\]]+)\]\(([^)]+)\)', cite_block.group()):
        path = match.group(2)
        # 正确格式: file://相对路径
        if path.startswith("/") or "://" in path and not path.startswith("file://"):
            bad.append((match.group(1), path))
    return bad

def fix_r2_paths(content: str, bad_paths: list[tuple[str, str]]) -> str:
    """修正 cite 路径格式"""
    for display_name, bad_path in bad_paths:
        if bad_path.startswith("file://"):
            # 已经是 file:// 前缀，跳过
            continue
        elif bad_path.startswith("/"):
            # 绝对路径 → 去除前导 /，加 file://
            fixed = f"file://{bad_path.lstrip('/')}"
        elif "://" in bad_path:
            # 其他协议前缀（如 http://）→ 替换为 file://
            fixed = re.sub(r'^[a-z]+://', 'file://', bad_path)
        else:
            # 无前缀的相对路径，已经是正确格式
            continue
        content = content.replace(f'({bad_path})', f'({fixed})')
    return content
```

### 5.3 R3: 章节来源

```python
def find_missing_section_sources(content: str) -> list[str]:
    """找出缺少章节来源的 ## 章节"""
    sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
    missing = []
    
    for section in sections:
        if section in ("目录",):  # 跳过目录章节
            continue
        # 检查该章节后是否有 "章节来源"
        pattern = re.compile(
            rf'^## {re.escape(section)}\b.*?(?=^## |\Z)',
            re.MULTILINE | re.DOTALL
        )
        section_content = pattern.search(content)
        if section_content and "章节来源" not in section_content.group():
            missing.append(section)
    
    return missing
```

### 5.4 R4: 图表来源

```python
def find_missing_chart_sources(content: str) -> list[int]:
    """找出缺少图表来源的 mermaid 代码块，返回代码块结束行号列表"""
    missing = []
    for match in re.finditer(r'```mermaid\n.*?```', content, re.DOTALL):
        end_pos = match.end()
        # 检查代码块后是否有 "图表来源"
        following = content[end_pos:end_pos+200]  # 检查后续 200 字符
        if not re.match(r'\s*\n*\*{0,2}图表来源\*{0,2}\s*$', following, re.MULTILINE):
            missing.append(content[:end_pos].count('\n'))
    return missing

def fix_r4_chart_sources(content: str, missing_lines: list[int]) -> str:
    """在缺少图表来源的 mermaid 代码块后插入图表来源骨架"""
    for match in re.finditer(r'```mermaid\n.*?```', content, re.DOTALL):
        end_pos = match.end()
        following = content[end_pos:end_pos+200]
        if not re.match(r'\s*\n*\*{0,2}图表来源\*{0,2}\s*$', following, re.MULTILINE):
            insert = "\n\n图表来源\n"
            content = content[:end_pos] + insert + content[end_pos:]
    return content
```

### 5.5 R5: 引用格式

```python
def find_bad_references(content: str) -> list[tuple[str, str]]:
    """找出格式错误的引用条目，返回 [(显示名, 错误路径), ...]"""
    bad = []
    # 查找缺少 file:// 前缀的引用
    for match in re.finditer(r'- \[([^\]]+)\]\(([^)]+)\)', content):
        path = match.group(2)
        # 跳过正确的引用和目录锚点引用
        if path.startswith("file://") or path.startswith("#"):
            continue
        # 看起来像文件路径但缺少 file://
        if '/' in path and not path.startswith('http'):
            bad.append((match.group(1), path))
    return bad

def fix_r5_references(content: str, bad_refs: list[tuple[str, str]]) -> str:
    """修正引用格式，补充 file:// 前缀"""
    for display_name, bad_path in bad_refs:
        fixed = f"file://{bad_path}"
        content = content.replace(f'({bad_path})', f'({fixed})')
    return content
```

### 5.6 R6: 目录对应

> **实测发现**：现有 wiki 目录锚点直接使用中文标题文本（如 `[简介](#简介)`），而非 GitHub 式 slug。
> 305 条跨文件引用全部使用行号锚点（`#L1-L29`），0 条使用章节名锚点。
> 因此 R6 **不重新生成锚点**，而是检测目录条目与实际 `##` 标题的一致性。

```python
def is_toc_consistent(content: str) -> bool:
    """检查目录中的每个条目是否对应实际存在的 ## 标题"""
    # 提取所有 ## 标题
    headings = set(re.findall(r'^## (.+)$', content, re.MULTILINE))
    
    # 提取目录中的条目: [标题](#锚点)
    toc_section = re.search(r'^## 目录\n((?:.*\n)*?)(?=^## )', content, re.MULTILINE)
    if not toc_section:
        return True  # 无目录则跳过
    
    toc_entries = re.findall(r'\[([^\]]+)\]\(#[^)]+\)', toc_section.group(1))
    
    # 每个目录条目都应有对应的 ## 标题
    for entry_title in toc_entries:
        if entry_title not in headings:
            return False
    
    # 每个非目录 ## 标题都应在目录中出现
    for heading in headings:
        if heading == "目录":
            continue
        if heading not in toc_entries:
            return False
    
    return True

def fix_r6_regenerate_toc(content: str) -> str:
    """根据实际 ## 标题重建目录，保留现有锚点格式"""
    sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
    
    # 从现有目录中提取 标题→锚点 映射（保留原锚点不变）
    existing_anchors: dict[str, str] = {}
    toc_section = re.search(r'^## 目录\n((?:.*\n)*?)(?=^## )', content, re.MULTILINE)
    if toc_section:
        for match in re.finditer(r'\[([^\]]+)\]\((#[^)]+)\)', toc_section.group(1)):
            existing_anchors[match.group(1)] = match.group(2)
    
    # 生成目录条目
    toc_entries = []
    for section in sections:
        if section == "目录":
            continue
        # 优先使用已有锚点；新标题使用标题文本本身（中文 markdown 惯例）
        anchor = existing_anchors.get(section, f"#{section}")
        toc_entries.append(f"{len(toc_entries)+1}. [{section}]({anchor})")
    
    toc_block = "## 目录\n" + "\n".join(toc_entries) + "\n"
    
    # 替换现有目录
    if toc_section:
        content = re.sub(
            r'^## 目录\n(?:.*\n)*?(?=^## )',
            toc_block + "\n",
            content,
            flags=re.MULTILINE
        )
    else:
        # 无目录章节时，在第一个 ## 前插入
        content = re.sub(r'(?=^## )', toc_block + "\n", content, count=1, flags=re.MULTILINE)
    
    return content
```

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 修复后仍有违规（3 轮未收敛） | 返回最后一轮修复结果，标记需人工审核 |
| cite 块格式严重损坏 | 移除并重新生成空骨架 |
| 目录锚点生成异常 | 跳过该条目（实际使用中文文本锚点，无需 slug 生成） |

## 7. 验收标准

1. R1-R6 全部覆盖
2. 不合规项自动修复后重新校验通过（3 轮内收敛）
3. 修复仅调整格式标记，不改动 wiki 实质内容
4. 输出违规记录（含规则编号、描述、是否修复）
