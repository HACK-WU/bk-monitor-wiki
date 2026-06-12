---
id: SR-03
feature: Wiki增量更新Skill
sub_requirement: 增量更新 Skill
priority: P0
status: 已确认
created: 2026-06-12
---

# SR-03: 增量更新 Skill (SKILL.md)

## 1. 职责

编排增量更新全流程：变更检测 → AI 生成更新内容 → 旧引用清理 → 格式校验 → 写入 → 索引同步。支持 dry-run 预览模式。

## 2. Skill 定义结构

Skill 以 `SKILL.md` 文件形式存在，AI 读取指令后按流程执行。

```
skills/
└── wiki-incremental-update/
    └── SKILL.md
```

## 3. 流程编排

### 3.1 主流程

```
步骤 1: 环境准备
  ├── 读取 metadata.json 获取 old_commit
  ├── 确认 bk-monitor 仓库路径
  └── 确认 new_commit（用户提供 或 使用 HEAD）

步骤 2: 变更检测（调用 SR-02）
  ├── 执行 git diff + pathspec 排除
  ├── 三级匹配定位受影响 wiki
  └── 输出 ChangeReport（四类分类）

步骤 3: 展示分析结果
  ├── 显示受影响 wiki 列表 + 匹配级别标签
  ├── 显示新功能文件列表
  ├── 显示未覆盖变更列表
  └── 询问用户是否执行（dry-run 模式在此停止）

步骤 4: Wiki 更新（逐个处理）
  对每个受影响 wiki:
  ├── 4a. 读取当前 wiki 内容
  ├── 4b. git show 获取关联源文件新版本
  ├── 4c. AI 对比变更，生成更新后的 wiki 内容
  ├── 4d. 旧引用清理（调用 SR-04）
  ├── 4e. 格式校验（调用 SR-05）
  └── 4f. 写入文件

步骤 5: 新功能文件处理
  对每个新功能文件:
  ├── AI 判断是否需要新建 wiki 页面
  └── 如需要，生成新 wiki 页面

步骤 6: 索引同步（调用 SR-06）
  ├── 增量索引更新
  └── 更新 commit_id

步骤 7: 输出变更摘要
  ├── 更新统计（更新 wiki 数、新增 wiki 数、删除引用数）
  └── 记录本次更新对应的 commit 范围
```

### 3.2 dry-run 模式

dry-run 模式下，流程在**步骤 3** 后停止，不执行步骤 4-7。

输出内容：
- 受影响 wiki 列表（含匹配级别标签）
- 每个 wiki 关联的变更文件
- 预计的更新操作类型（内容更新 / 引用清理 / 引用更新）
- 新功能文件列表（AI 建议是否需要新建 wiki）

## 4. AI 更新策略

### 4.1 内容更新原则

| 原则 | 说明 |
|------|------|
| 保留手动编辑 | 只更新受变更影响的章节内容，保留其他章节不变 |
| 保持格式一致 | 更新后的内容遵循现有 wiki 格式（cite、章节来源、图表来源） |
| 标注变更范围 | 在 dry-run 输出中标注哪些章节会被更新 |
| 最小修改 | 优先修改现有段落，避免大范围重写 |

### 4.2 源文件读取

```python
def get_source_content(path: str, commit: str, repo_dir: str) -> str:
    """通过 git show 获取指定 commit 版本的源文件内容"""
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True, text=True, cwd=repo_dir
    )
    return result.stdout
```

### 4.3 AI Prompt 模板

对每个受影响的 wiki，AI 按以下步骤操作：

```
# Wiki 增量更新任务

## 背景
源文件 `{changed_file}` 发生了 {status} 变更（{old_commit} → {new_commit}）。
匹配级别: [{level}]（{exact/dirname/parent}）

## 输入
1. 当前 wiki 内容: `{wiki_path}`
2. 源文件旧版本内容: `git show {old_commit}:{changed_file}`
3. 源文件新版本内容: `git show {new_commit}:{changed_file}`
4. 源文件 diff: `git diff {old_commit}..{new_commit} -- {changed_file}`

## 任务
根据源文件变更，更新 wiki 中受影响的章节。要求：
1. **只更新受变更影响的章节**，其他章节保持原样
2. 更新 `<cite>` 列表（新增/移除/更新引用条目）
3. 更新相关章节的 `章节来源` / `图表来源`
4. 如果源文件被删除，移除所有相关引用
5. 如果源文件被重命名，更新路径引用

## 禁止事项
- 不要重写未受影响的章节内容
- 不要改变现有章节的结构和标题
- 不要删除人工添加的补充说明或注释
- 不要修改目录（除非新增了 ## 章节）
```

## 5. 错误处理

| 异常场景 | 处理方式 |
|---------|--------|
| 单个 wiki 更新失败 | 跳过该 wiki，记录到错误列表，继续处理其余 |
| git show 读取源文件失败 | 跳过该源文件，在 wiki 中标记引用失效 |
| 格式校验连续 3 轮不通过 | 使用最后一次修复结果，标记需要人工审核 |
| 索引更新失败 | 降级为全量重建（调用 build_index） |
| 用户取消操作 | 不写入任何文件，输出 "已取消" |
| wiki 文件被外部修改（与索引不一致） | 警告用户，建议先执行全量重建索引 |
| metadata.json 不存在或损坏 | 提示用户先执行 `build_index.py` 初始化 |
| 受影响 wiki 超过阈值（默认 50 个） | 提示用户确认是否继续，避免大规模误操作 |

## 6. 输出格式

### 6.1 更新完成后摘要

```
✅ Wiki 增量更新完成 (e353b1f → abc1234)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

更新 wiki: 5 个
新增 wiki: 1 个
删除引用: 3 条
更新引用: 7 条

| Wiki 页面 | 操作 | 匹配级别 |
|-----------|------|---------|
| 数据库设计/表结构.md | 内容更新 | [精确] |
| 数据链路/关系管理.md | 内容更新 | [dirname] |
| APM全栈监控/APM核心架构.md | 引用更新 | [父目录] |
| 新功能/新模块.md | 新建 | [新功能] |

⚠️ 需要人工审核:
  - 数据链路/关系管理.md (dirname 匹配，可能误报)
  - APM全栈监控/APM核心架构.md (父目录匹配，可能误报)
```

## 7. 与其他子需求的集成

| 步骤 | 调用子需求 | 传入数据 | 返回数据 |
|------|-----------|---------|---------|
| 步骤 2 | SR-02 | old_commit, new_commit, metadata | ChangeReport |
| 步骤 4d | SR-04 | wiki_content, dead_files, renamed_files | cleaned_content |
| 步骤 4e | SR-05 | updated_content | (fixed_content, violations) |
| 步骤 6 | SR-06 | metadata, affected_wikis, new_commit | updated_metadata |

## 8. 验收标准

1. SKILL.md 可被 AI 读取并按流程执行
2. dry-run 模式输出完整分析结果，不修改任何文件
3. 实际执行模式正确更新 wiki 内容
4. 错误处理：单个 wiki 失败不中断整体流程
5. 输出变更摘要包含所有操作记录
