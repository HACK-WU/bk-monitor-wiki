---
description: 当 AI 需要修改代码、review commit、排查问题或探索不熟悉的文件时，先通过 wiki-lookup skill 反查相关 Wiki 文档了解设计上下文。注意：wiki-lookup 回答设计意图/架构（查 Wiki），codekb-skill 回答函数签名/调用关系（查代码知识库），两者不可混淆。
alwaysApply: false
enabled: true
updatedAt: 2026-06-13T16:50:00.000Z
provider:
---

# Wiki 反查触发规则

> 代码修改、审查、排错前，先反查相关 Wiki 了解设计上下文。

## ⚠️ 与 codekb-skill 严格区分

| | wiki-lookup（本规则） | codekb-skill |
|--|----------------------|-------------|
| **回答什么** | 这段代码的**设计意图**是什么？整体架构是怎样的？ | 这个**函数/类/API 怎么用**？签名是什么？谁调用了它？ |
| **数据来源** | Wiki 文档（人工编写的设计文档、架构说明） | 代码知识库（从代码中提取的结构化知识） |
| **典型问题** | "Issue 功能的整体设计是怎样的？"<br>"告警引擎的架构决策是什么？" | "`IssueManager.create_issue()` 的参数和返回值？"<br>"哪些模块调用了 `AlarmChecker`？" |
| **使用命令** | `lookup --files` / `lookup --new-commit` | `ki query-group` / `ki get-module-info` |
| **输出** | 按命中数排序的 Wiki 文档列表 | 函数签名、调用关系、模块依赖图 |

> **简单判断**：你需要的是**设计文档**还是**代码细节**？设计文档 → wiki-lookup，代码细节 → codekb-skill。
> 两者不互斥，可以先查 Wiki 了解设计全貌，再查 codekb 了解代码级细节。

## 触发条件

以下任一场景，**必须先执行 `lookup` 命令反查 Wiki**，再开始工作：

| 场景 | 用户典型表达 | 执行 |
|------|-------------|------|
| **修改代码** | "修改 XX 文件"、"重构 XX 模块"、"给 XX 加个功能" | 用 `--files` 传入待修改文件，阅读排名前 3 的 Wiki |
| **Code Review** | "review 这个 commit"、"审查 XX 提交" | 用 `--new-commit` 传入 commit hash，按命中数顺序阅读 Wiki |
| **排查 Bug** | "XX 文件有问题"、"为什么 XX 报错" | 用 `--files` 传入问题文件，了解模块架构和依赖 |
| **探索代码** | "XX 模块是干什么的"、"帮我理解 XX" | 用 `--files` 传入文件，从引用它的 Wiki 了解用途 |
| **影响评估** | "改这个会影响什么"、"这个提交涉及哪些模块" | 用合并模式 `--files` + `--new-commit` 看完整覆盖 |

## 执行

```
Skill(skill="wiki-lookup")  →  按 skill 中的命令速查执行 lookup  →  按行动策略阅读 Wiki
```

## 例外

| 情况 | 处理 |
|------|------|
| `metadata.json` 不含 `source_to_wiki` | 先执行 `build-index` 构建索引 |
| `lookup` 返回空 | 该文件无关联 Wiki，跳过反查，直接工作 |
| 用户明确说"不用查 Wiki" | 跳过 |
| 纯格式/注释修改 | 跳过（如"改个注释"、"格式化代码"） |
