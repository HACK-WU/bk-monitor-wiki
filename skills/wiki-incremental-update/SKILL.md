# BK-Monitor Wiki 增量更新

> 根据 `wiki/metadata.json` 中的源文件与 Wiki 映射关系，以及用户指定的 commit，分析并增量更新受影响的 Wiki 页面。

## 触发场景

- 用户要求根据某个 commit 更新 BK-Monitor Wiki
- 用户要求分析代码变更会影响哪些 Wiki 页面
- 用户要求维护 `wiki/metadata.json` 中的 source/wiki 双向索引

## 关键文件

| 文件 | 说明 |
|------|------|
| `wiki/metadata.json` | Wiki 元信息、排除规则、双向索引 |
| `scripts/wiki_incremental/index_builder.py` | 全量构建 `source_to_wiki` / `wiki_to_source` |
| `scripts/wiki_incremental/change_detection.py` | git diff 变更检测和三级匹配 |
| `scripts/wiki_incremental/citation_cleanup.py` | 删除/重命名文件的旧引用清理 |
| `scripts/wiki_incremental/format_validation.py` | Wiki 格式校验和机械修复 |
| `scripts/wiki_incremental/incremental_index.py` | 受影响 Wiki 的增量索引同步 |

## 前置检查

1. 确认当前工作目录是仓库根目录。
2. 确认 `bk-monitor-wiki/wiki/metadata.json` 存在。
3. 如果 `metadata.json` 不含 `source_to_wiki` 或 `wiki_to_source`，先构建索引：

```bash
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli build-index \
  --wiki-dir bk-monitor-wiki/wiki \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --output bk-monitor-wiki/wiki/metadata.json
```

## 标准流程

### Step 1: 确认 commit 范围

- `old_commit` 默认读取 `bk-monitor-wiki/wiki/metadata.json` 的 `source.commit_id`
- `new_commit` 使用用户指定值；如果用户没有指定，使用当前 `HEAD`

### Step 2: Dry-run 变更检测

```bash
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli detect \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --new-commit <new_commit> \
  --repo-dir .
```

输出需要重点检查：

- `[精确]`：源文件在索引中精确命中，可直接作为更新候选
- `[dirname]`：同目录模糊命中，必须在摘要里标注需要审核
- `[父目录]`：父目录回退命中，必须在摘要里标注需要审核
- `新功能文件`：新增且未被现有 Wiki 引用，AI 判断是否需要新建页面
- `未覆盖变更`：无索引命中，仅在用户要求时处理

dry-run 阶段不得写入任何 Wiki 或 metadata 文件。

### Step 3: 用户确认

除非用户已经明确要求直接执行，否则在展示 dry-run 结果后询问是否继续实际更新。

如果受影响 Wiki 超过 50 个，必须提醒风险并等待确认。

### Step 4: 更新受影响 Wiki

对每个受影响 Wiki：

1. 读取当前 Wiki 内容，保留手动编辑内容。
2. 读取相关源文件的旧版本、新版本和 diff。
3. 只更新受变更影响的章节，避免重写整篇文档。
4. 如果源文件删除，调用 `citation_cleanup.cleanup_dead_citations(content, dead_files=[path], renamed_files={})` 清理失效引用。
5. 如果源文件重命名，调用 `citation_cleanup.cleanup_dead_citations(content, dead_files=[], renamed_files={old: new})` 替换路径。
6. 保持现有 Wiki 风格：
   - 文件顶部标题后保留 `<cite>`
   - 目录使用中文标题锚点，如 `[简介](#简介)`
   - 来源标题使用现有纯文本风格：`章节来源`、`图表来源`、`图示来源`
   - 引用格式为 `[名称](file://相对路径#Lx-Ly)`

### Step 5: 格式校验

写入前对每个更新的 wiki 执行格式校验：

```python
from wiki_incremental.format_validation import validate_and_fix

content, violations = validate_and_fix(updated_content)
# violations 中包含所有 R1-R6 违规及修复状态
```

校验规则：

- `<cite>` 块存在
- 引用路径使用 `file://相对路径`
- 目录条目和 `##` 章节一致
- Mermaid 图后保留来源段落
- 更新章节保留或补充 `章节来源`

机械修复只能改格式，不得凭空改正文含义。

### Step 6: 索引同步

更新完成后，只扫描受影响 Wiki 并更新 metadata：

```python
from wiki_incremental.incremental_index import incremental_index_update, save_metadata
```

更新内容：

- `source.commit_id = <new_commit>`
- `source_to_wiki`
- `wiki_to_source`
- `stats.source_count`
- `stats.wiki_count`

如果增量索引失败，降级为全量 `build_index`。

## AI 更新原则

| 原则 | 要求 |
|------|------|
| 最小修改 | 只改受变更影响的章节和引用 |
| 保留人工内容 | 不删除人工补充说明、注释和未受影响章节 |
| 引用可追溯 | 新增或修改内容必须能对应到源文件引用 |
| 模糊命中保守 | `[dirname]` / `[父目录]` 命中优先标注审核，不做大范围推断 |
| 先预览后写入 | 默认 dry-run；用户确认后才实际改文件 |

## 完成摘要

实际更新后输出：

- commit 范围
- 更新 Wiki 数
- 新增 Wiki 数
- 删除引用数
- 更新引用数
- 需要人工审核的 Wiki 列表
- 是否已同步 `metadata.json`
