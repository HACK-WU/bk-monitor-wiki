---
id: SR-04
feature: Wiki增量更新Skill
sub_requirement: 旧引用清理
priority: P1
status: 已确认
created: 2026-06-12
---

# SR-04: 旧引用清理

## 1. 职责

当源文件被删除（D）或重命名（R）时，清理 wiki 中的失效引用条目。

## 2. 核心接口

```python
def cleanup_dead_citations(
    wiki_content: str,
    dead_files: list[str],
    renamed_files: dict[str, str]
) -> str:
    """
    清理 wiki 内容中的失效引用。
    
    参数:
        wiki_content: wiki 文件完整内容
        dead_files: 被删除的源文件路径列表（D 类型）
        renamed_files: 重命名映射 {old_path: new_path}（R 类型）
    
    返回:
        清理后的 wiki 内容
    """
```

## 3. 清理规则

### 3.1 按变更类型

| 变更类型 | `<cite>` 处理 | 章节来源处理 | 图表来源处理 |
|---------|-------------|------------|------------|
| D（删除） | 移除该文件条目 | 移除该文件条目 | 移除该文件条目 |
| R（重命名） | 替换 old_path → new_path | 替换 old_path → new_path | 替换 old_path → new_path |
| M（修改） | 不处理 | 不处理 | 不处理 |

### 3.2 引用条目匹配正则

三种引用场景使用统一的条目匹配正则：

```python
# 匹配一条引用条目（含前面的 '- ' 和整行）
# 示例: "- [event.py](file://bkmonitor/alarm_backends/core/alert/event.py)"
# 示例: "- [event.py:14](file://bkmonitor/alarm_backends/core/alert/event.py#L14)"
ENTRY_RE = re.compile(r'^- \[([^\]]+)\]\(file://([^)]+)\)\s*$', re.MULTILINE)
```

## 4. 实现算法

```python
def cleanup_dead_citations(wiki_content, dead_files, renamed_files):
    result = wiki_content
    
    # 1. 处理删除的文件：移除整行
    for dead_path in dead_files:
        # 匹配包含该路径的引用条目（含行号部分）
        pattern = re.compile(
            r'^- \[[^\]]+\]\(file://' + re.escape(dead_path) + r'(?:#[^)]*)?\)\s*\n?',
            re.MULTILINE
        )
        result = pattern.sub('', result)
    
    # 2. 处理重命名的文件：替换路径
    for old_path, new_path in renamed_files.items():
        # 替换 file:// 后的路径部分，保留行号（如有）
        pattern = re.compile(
            r'(file://)' + re.escape(old_path) + r'(#L\d+(?:-L\d+)?)?',
        )
        result = pattern.sub(
            lambda m: f'{m.group(1)}{new_path}' + (m.group(2) or ''),
            result
        )
        # 同时更新显示名称（仅限引用条目内的方括号部分，避免全局替换误伤）
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        if old_name != new_name:
            # 只替换引用条目中的显示名称: - [old_name](...) 或 - [old_name:L...](...) 
            name_pattern = re.compile(
                r'(\[)' + re.escape(old_name) + r'((?::L\d+(?:-L\d+)?)?\])\(file://'
            )
            result = name_pattern.sub(
                lambda m: f'{m.group(1)}{new_name}{m.group(2)}(file://',
                result
            )
    
    # 3. 清理空引用块（如果所有条目都被删除）
    # 清理空的 cite 块
    result = re.sub(
        r'<cite>\s*\*\*本文引用的文件\*\*\s*</cite>\s*',
        '', result
    )
    # 清理空的章节来源/图表来源块
    result = re.sub(
        r'^章节来源\s*$',
        '', result, flags=re.MULTILINE
    )
    result = re.sub(
        r'^图表来源\s*$',
        '', result, flags=re.MULTILINE
    )
    
    return result
```

## 5. 清理示例

### 5.1 删除场景

**输入**（event.py 被删除）：
```markdown
<cite>
**本文引用的文件**
- [alert.py](file://bkmonitor/alarm_backends/core/alert/alert.py)
- [event.py](file://bkmonitor/alarm_backends/core/alert/event.py)
</cite>
```

**输出**：
```markdown
<cite>
**本文引用的文件**
- [alert.py](file://bkmonitor/alarm_backends/core/alert/alert.py)
</cite>
```

### 5.2 重命名场景

**输入**（adapter.py → alert_adapter.py）：
```markdown
章节来源
- [adapter.py:18-21](file://bkmonitor/alarm_backends/core/alert/adapter.py#L18-L21)
```

**输出**：
```markdown
章节来源
- [alert_adapter.py:18-21](file://bkmonitor/alarm_backends/core/alert/alert_adapter.py#L18-L21)
```

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 引用条目格式异常（非标准格式） | 跳过该条目，保留原样 |
| dead_files 中有路径但 wiki 中无对应引用 | 无影响（正则不匹配） |
| 清理后 cite 块为空 | 移除整个 cite 块 |
| 清理后章节来源/图表来源为空 | 移除标记行（保留给 SR-05 重新生成） |

## 7. 验收标准

1. D 类型文件引用从 cite / 章节来源 / 图表来源中完整移除
2. R 类型文件引用路径被正确替换（含行号保留）
3. 未受影响的 wiki 内容保持不变
4. 空引用块被清理
