# BK-Monitor Wiki 知识索引数据恢复

> 参照 [knowledge-indexer 数据恢复指南](https://github.com/HACK-WU/knowledge-indexer/blob/master/docs/restore-data.md)，从 WAL 自动备份恢复 `monitor` scope 的 Group 索引和 Relations 缓存数据。

## 触发场景

- 用户要求"恢复 wiki 数据"、"从备份恢复"、"还原知识索引"
- `group-index.json` 或 `relations-cache.json` 文件损坏（JSON 解析异常）
- 需要重置 `monitor` scope 的数据
- 首次在新环境部署，需要从备份中恢复已有的索引结构
- 导入过程中数据损坏，需要回滚

## 关键目录与文件

> **重要**：备份文件与 ki 运行时数据位于 **两个独立目录**，不要混淆。

### 备份目录（静态，在 wiki 仓库内）

| 路径 | 说明 |
|------|------|
| `bk-monitor-wiki/knowledge-indexer/backup/` | WAL 备份存放目录 |
| `backup/group-index.{timestamp}.bak.json` | Group 索引备份 |
| `backup/relations-cache.{timestamp}.bak.json` | Relations 缓存备份（含文本、路径、关键词） |
| `knowledge-indexer/scripts/restore_vectors.py` | 向量恢复脚本（从 relations-cache + wiki 提取摘要） |

### 运行时目录（动态，在 knowledge-indexer 项目内）

ki 命令的运行时数据存储在 **knowledge-indexer 项目的 `kb/` 目录**下，非 wiki 仓库内。先确认其位置：

```bash
# ki 全局安装，数据目录在 knowledge-indexer 项目根目录下
ls /path/to/knowledge-indexer/kb/monitor/
```

| 文件 | 说明 |
|------|------|
| `kb/monitor/group-index.json` | 当前 Group 索引（运行时） |
| `kb/monitor/relations-cache.json` | 当前 Relations 缓存（运行时） |

### 完整架构

```
bk-monitor-wiki/knowledge-indexer/      # wiki 仓库内（备份、skills、脚本）
├── backup/
│   ├── group-index.{timestamp}.bak.json
│   └── relations-cache.{timestamp}.bak.json
├── scripts/
│   └── restore_vectors.py
└── skills/
    ├── data-restore/SKILL.md
    └── wiki-vectorize-import/SKILL.md

/path/to/knowledge-indexer/kb/monitor/  # ki 项目内（运行时数据）
├── group-index.json                    # 当前活跃索引
└── relations-cache.json                # 当前活跃缓存
```

## 备份机制

knowledge-indexer 基于 **WAL（预写日志）** 机制，每次写入前自动创建备份。备份文件命名格式：`{文件名}.{ISO8601时间戳}.bak.json`

> **注意**：备份恢复只能恢复 **Group 索引和 Relations 缓存文件**。**LanceDB 向量数据库**中的记忆数据不在备份范围内，恢复后需单独使用 `ki scan-kb import` 重新导入向量数据。

---

## 恢复决策树

```
数据异常
├─ group-index.json / relations-cache.json 丢失或损坏？
│   └─ 从 backup/ 找最新备份 → 覆盖到 kb/monitor/（场景 A）
├─ 整个 kb/monitor/ 不可用？
│   └─ 删除 kb/monitor/ → 运行 ki 触发初始化 → 恢复备份 → 重导向量（场景 B）
├─ 向量数据（mem search）丢失？
│   └─ 重新执行 ki scan-kb import（场景 C）
└─ 索引正常但内容不对？
    └─ 检查备份时间戳，选择更早的版本恢复
```

---

## 执行流程

```
确认数据异常类型 + 定位 ki 运行时目录
│
├─ 场景 A：索引文件损坏 ──▶ 从 backup/ 覆盖到 kb/monitor/
│
├─ 场景 B：整个 scope 损坏 ──▶ 删除 kb/monitor/ → 初始化 → 恢复
│
└─ 场景 C：向量数据丢失 ──▶ 重新 ki scan-kb import
```

---

### 场景 A：从备份恢复（最常用）

当 `group-index.json` 或 `relations-cache.json` 损坏或丢失时执行。

#### Step A0: 定位 ki 运行时目录

```bash
# ki 数据在 knowledge-indexer 项目根目录的 kb/ 下
# 如果不知道项目路径，全局搜索：
find ~ -maxdepth 5 -path "*/kb/monitor/group-index.json" 2>/dev/null
```

#### Step A1: 查看可用备份

```bash
ls -la bk-monitor-wiki/knowledge-indexer/backup/
```

**当前可用备份**（2026-06-10 快照）：

| 文件 | 大小 | 备份时间 |
|------|------|----------|
| `group-index.2026-06-10T08-42-08-000Z.bak.json` | 1.1K | 2026-06-10 08:42:08 UTC |
| `relations-cache.2026-06-10T08-42-08-000Z.bak.json` | 50K | 2026-06-10 08:42:08 UTC |

#### Step A2: 备份当前运行文件（防止误操作）

```bash
KB_MONITOR="/path/to/knowledge-indexer/kb/monitor"
cp "$KB_MONITOR/group-index.json" "$KB_MONITOR/group-index.json.before-restore"
cp "$KB_MONITOR/relations-cache.json" "$KB_MONITOR/relations-cache.json.before-restore"
```

#### Step A3: 从备份恢复

```bash
BACKUP_DIR="bk-monitor-wiki/knowledge-indexer/backup"
KB_MONITOR="/path/to/knowledge-indexer/kb/monitor"

# 恢复两个文件（必须使用同一时间戳的备份）
cp "$BACKUP_DIR/group-index.{最新时间戳}.bak.json" "$KB_MONITOR/group-index.json"
cp "$BACKUP_DIR/relations-cache.{最新时间戳}.bak.json" "$KB_MONITOR/relations-cache.json"
```

> **重要**：`group-index` 与 `relations-cache` 必须使用**同一时间戳**的备份，否则数据可能不一致。

#### Step A4: 验证恢复结果

```bash
# 查看整体 Group 树和统计信息
ki query-group --scope monitor

# 验证特定 Group 的内容
ki query-group --scope monitor --groups "BK-Monitor-Wiki/告警系统设计"
```

**验证通过标准**：
- 总索引数不再为 1（表明数据已恢复）
- Group 树包含所有子目录（项目概述、告警系统设计、核心模块架构等）
- 特定 Group 下有关联的 Relations 和关键词

---

### 场景 B：从模板重新初始化（整个 scope 损坏）

当整个 `monitor` scope 数据不可用时执行。

#### Step B1: 备份当前残留数据（可选）

```bash
KB_MONITOR="/path/to/knowledge-indexer/kb/monitor"
if [ -d "$KB_MONITOR" ]; then
  cp -r "$KB_MONITOR" "$KB_MONITOR.bak.$(date +%Y%m%d%H%M%S)"
fi
```

#### Step B2: 删除受损目录

```bash
rm -rf "$KB_MONITOR"
```

#### Step B3: 触发自动初始化

直接运行 `ki query-group --scope monitor`，ki 会自动初始化空的 `kb/monitor/` 目录：

```bash
ki query-group --scope monitor
```

#### Step B4: 从备份恢复 + 重新导入

```bash
# 按场景 A 的步骤恢复备份文件
BACKUP_DIR="bk-monitor-wiki/knowledge-indexer/backup"
cp "$BACKUP_DIR/group-index.{最新时间戳}.bak.json" "$KB_MONITOR/group-index.json"
cp "$BACKUP_DIR/relations-cache.{最新时间戳}.bak.json" "$KB_MONITOR/relations-cache.json"

# 重导向量数据
ki scan-kb import --scope monitor --results ai-results.json
```

> 如果没有 `ai-results.json`，需要参照 [wiki-vectorize-import 流程](../wiki-vectorize-import/SKILL.md) 重新生成。

---

### 场景 C：向量数据丢失（mem search 无结果）

当 LanceDB 中的向量记忆数据丢失，但 `group-index.json` 和 `relations-cache.json` 正常时。

可选两种方式恢复向量数据：

#### 方式 1：从 relations-cache 提取摘要 + mem bulk-store（推荐，无需 ai-results.json）

利用 `restore_vectors.py` 脚本：解析 `relations-cache` → 读取 wiki 文件的 `## 简介` 段落 → 生成 `memories.json` → 批量导入。

**Step C1**: 生成 `memories.json`

```bash
cd /path/to/bk-monitor
python3 bk-monitor-wiki/knowledge-indexer/scripts/restore_vectors.py \
  --cache bk-monitor-wiki/knowledge-indexer/backup/relations-cache.{最新时间戳}.bak.json \
  --wiki-dir bk-monitor-wiki/wiki \
  --output bk-monitor-wiki/knowledge-indexer/memories.json \
  --scope monitor \
  --category fact
```

**输出格式**（每个条目 = 摘要 + 路径）：

```json
{
  "text": "{## 简介段落内容}\n\n[来源: {sourcePath}]",
  "category": "fact",
  "importance": 0.7,
  "tags": "关键词1,关键词2",
  "scope": "monitor"
}
```

**Step C2**: dry-run 验证

```bash
mem bulk-store -f bk-monitor-wiki/knowledge-indexer/memories.json --scope monitor --dry-run
```

**Step C3**: 执行导入（127 条约 2 分钟）

```bash
mem bulk-store -f bk-monitor-wiki/knowledge-indexer/memories.json --scope monitor -c fact
```

**Step C4**: 验证

```bash
mem stats --scope monitor      # 检查条数
mem search "告警引擎" --scope monitor  # 语义检索测试
```

#### 方式 2：ki scan-kb import（需要 ai-results.json）

```bash
ki scan-kb import --scope monitor --results ai-results.json
```

> 如果没有 `ai-results.json`，需要参照 [wiki-vectorize-import 流程](../wiki-vectorize-import/SKILL.md) 重新生成。**推荐方式 1**，因为它直接复用已有的 relations-cache 备份，无需重新扫描和生成条目。

---

## AI 操作原则

| 原则 | 要求 |
|------|------|
| 先定位后操作 | 先确认 ki 运行时数据目录（`kb/monitor/`），再执行恢复 |
| 备份先行 | 恢复前先备份当前状态（`.before-restore`），即便文件已损坏 |
| 时间戳一致 | `group-index` 和 `relations-cache` 必须使用同一时间戳的备份 |
| 双向记录 | 恢复后更新 `group-index.json` 中的 `source.dir` 为本地路径（如需） |
| 验证闭环 | 恢复后必须执行 `ki query-group --scope monitor` 验证数据完整性 |
| 向量需重导 | 备份恢复只恢复索引文件，向量数据需独立执行 `ki scan-kb import` |

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 找不到 `kb/monitor/` | ki 运行时数据不在预期位置 | `find ~ -maxdepth 5 -path "*/kb/monitor/group-index.json"` 全局搜索 |
| 恢复后 `mem search` 无结果 | 向量数据不在备份中 | 执行 `ki scan-kb import --scope monitor --results ai-results.json` |
| `ki query-group` 报 `--mode compact` 无效 | 该版本不支持此 mode | 去掉 `--mode` 参数，直接用 `ki query-group --scope monitor` |
| 恢复的 index 和 relations 不匹配 | 选用了不同时间戳的备份 | 确保两个文件使用同一时间戳 |
| 备份中 `source.dir` 是服务器路径 | 备份在服务器创建 | 恢复索引文件本身即可，`source.dir` 仅作追溯用途 |
| 无法找到 `ai-results.json` | 文件丢失或未生成 | 参照 [wiki-vectorize-import](../wiki-vectorize-import/SKILL.md) 重新生成 |
| 备份文件被覆盖 | 导入操作触发了新的 WAL 备份 | 从 git 历史恢复 `backup/` 目录 |

## 完成摘要

恢复完成后输出：

- 恢复场景（A / B / C）
- ki 运行时数据目录位置
- 使用的备份时间戳
- `ki query-group --scope monitor` 结果（总索引数、热区/常温/冷区分布）
- Group 树完整性验证（是否包含所有子目录）
- 是否已重新导入向量数据
- 残留数据的处理情况

## 相关链接

- [knowledge-indexer 数据恢复指南](https://github.com/HACK-WU/knowledge-indexer/blob/master/docs/restore-data.md)
- [memory-lancedb-mcp 首次使用配置](https://github.com/HACK-WU/memory-lancedb-mcp/blob/master/skills/setup-first-use/SKILL.md)
- [wiki-vectorize-import SKILL](../wiki-vectorize-import/SKILL.md)
