# BK-Monitor Wiki 增量更新

> 根据 `wiki/metadata.json` 中的源文件与 Wiki 映射关系，以及用户指定的 commit，分析并增量更新受影响的 Wiki 页面。

## 触发场景

- 用户要求根据某个 commit 更新 BK-Monitor Wiki
- 用户要求分析代码变更会影响哪些 Wiki 页面
- 用户要求维护 `wiki/metadata.json` 中的 source/wiki 双向索引

## 关键文件

| 文件 | 说明 |
|------|------|
| `wiki/metadata.json` | Wiki 元信息、排除规则、双向索引、**源代码仓库信息** (`source.repo_url`, `source.branch`, `source.commit_id`) |
| `scripts/wiki_incremental/index_builder.py` | 全量构建 `source_to_wiki` / `wiki_to_source`，记录源代码仓库 URL/分支/commit |
| `scripts/wiki_incremental/change_detection.py` | git diff 变更检测和三级匹配 |
| `scripts/wiki_incremental/pattern_inference.py` | 从 `source_to_wiki` 归纳路径模式，为新文件推断 Wiki 目录归属 |
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
  --repo-dir . \
  --repo-url git@github.com:TencentBlueKing/bk-monitor.git \
  --branch master \
  --output bk-monitor-wiki/wiki/metadata.json
```

`--metadata` 读取已有配置（excluded_paths/noise_paths 等），防止被 `setdefault` 默认值覆盖。

## 标准流程

### Step 1: 确认 commit 范围

- `old_commit` 默认读取 `bk-monitor-wiki/wiki/metadata.json` 的 `source.commit_id`
- `new_commit` 必须由用户指定（`--new-commit` 为必填参数）
- `source.repo_url` 和 `source.branch` 记录了源代码仓库的地址和分支，仅作追溯用途，不参与 diff 计算

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
- `可推断放置位置`：新功能文件中，通过路径模式推断出 Wiki 目录归属的（含置信度和关联页面）
- `需人工判断`：新功能文件中，路径模式未命中的，需人工决定 Wiki 归属
- `未覆盖变更`：已修改但无索引命中，仅在用户要求时处理

其中 `可推断放置位置` 表格各列含义：

| 列 | 说明 |
|----|------|
| 源文件 | 新增的源文件路径 |
| 建议 Wiki 目录 | 推断出的 Wiki 顶级目录 |
| 置信度 | 基于现有映射统计的匹配百分比（≥60% 才输出） |
| 策略 | `extend_existing`：同目录已有关联 Wiki，建议扩展；`new_page`：无关联页面，建议新建 |
| 关联页面 | 同路径前缀的已有 Wiki 页面（最多显示 2 个） |

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

### Step 4b: 新建 Wiki 页面（可推断放置）

对 dry-run 中 `[可推断放置位置]` 且 `strategy=new_page` 的文件：

1. **读取源代码**：读取新文件完整内容，理解功能定位。
2. **确定放置路径**：在建议的 Wiki 顶级目录下，根据功能模块选择或创建子目录。
   - 如果关联页面已覆盖同目录的其他文件，优先扩展关联页面。
   - 如果新文件构成独立功能模块，创建新的 Wiki 页面。
3. **按模板生成内容**：
   - 文件顶部：`# 标题` + `<cite>` 引用块（列出引用的源文件）
   - 目录：中文标题锚点，如 `[简介](#简介)`
   - 章节：简介 → 项目结构 → 核心组件 → 架构总览 → 组件详细分析 → 依赖关系分析 → 结论
   - 每个章节后附 `章节来源`（引用格式：`[名称](file://相对路径#Lx-Ly)`）
   - 如有架构图，使用 Mermaid 并附 `图示来源`
4. **标注审核状态**：新建页面在文件首行添加 `<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->`
5. **格式校验**：同 Step 5，使用 `validate_and_fix` 校验格式。
6. **索引同步**：同 Step 6，新建页面参与增量索引更新。

对 `strategy=extend_existing` 的文件：

- 优先在关联页面中补充新文件相关的章节和引用，不单独建页。

对 `需人工判断` 的文件：

- 仅在摘要中列出，不自动生成页面，由人工决定处理方式。

### Step 5: 格式校验

写入前对每个更新或新建的 wiki 执行格式校验：

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

- `source.commit_id = <new_commit>`（`repo_url` 和 `branch` 保持不变）
- `source_to_wiki`
- `wiki_to_source`
- `stats.source_count`
- `stats.wiki_count`
- `stats.citation_count`

如果增量索引失败，降级为全量 `build_index`。

## AI 更新原则

| 原则 | 要求 |
|------|------|
| 最小修改 | 只改受变更影响的章节和引用 |
| 保留人工内容 | 不删除人工补充说明、注释和未受影响章节 |
| 引用可追溯 | 新增或修改内容必须能对应到源文件引用 |
| 模糊命中保守 | `[dirname]` / `[父目录]` 命中优先标注审核，不做大范围推断 |
| 先预览后写入 | 默认 dry-run；用户确认后才实际改文件 |
| 新建标注审核 | AI 生成的新 Wiki 页面必须标注 `[待审核]`，人工确认后才算正式入库 |
| 高置信度优先 | 只对置信度 ≥60% 的推断结果生成页面，低置信度的仅列出不生成 |

## 完成摘要

实际更新后输出：

- commit 范围
- 更新 Wiki 数
- 新建 Wiki 数（含置信度和放置路径）
- 扩展已有页面数
- 需人工判断的新功能数
- 删除引用数
- 更新引用数
- 需要人工审核的 Wiki 列表（含新建页面）
- 是否已同步 `metadata.json`
