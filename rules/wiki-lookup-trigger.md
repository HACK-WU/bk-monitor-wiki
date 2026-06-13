---
description: 当 AI 需要修改代码、review commit、排查问题或探索不熟悉的文件时，先通过 wiki-lookup skill 反查相关 Wiki 文档了解设计上下文。
alwaysApply: false
enabled: true
updatedAt: 2026-06-13T16:35:00.000Z
provider:
---

# Wiki 反查触发规则

> 代码修改、审查、排错前，先反查相关 Wiki 了解设计上下文。

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
