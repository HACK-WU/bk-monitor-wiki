# BK-Monitor Wiki 知识库构建

> 将 `bk-monitor-wiki/wiki/` 快速导入 knowledge-indexer，构建语义搜索索引。
>
> 详细流程参考上游文档：[build-kb.md](https://github.com/HACK-WU/knowledge-indexer/blob/master/docs/build-kb.md)——本文档在其基础上补充本地环境检测与配置指引，避免重复描述通用步骤。

## 触发场景

- 首次为 bk-monitor-wiki 构建知识索引
- wiki 文档结构发生较大变化，需要重新全量导入
- 用户要求"构建 wiki 知识索引"、"导入 wiki 文档"

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| scope | `monitor` | 项目隔离标识 |
| sourceDir | `/root/bk-monitor/bk-monitor-wiki/wiki` | wiki 文档目录（绝对路径） |
| rootName | `BK-Monitor-Wiki` | 导入根节点名称 |

> ⚠️ **sourceDir 与 kbDir 注意**：ki 配置中 `kbDir` 指向 `/root/bk-monitor/bk-monitor-wiki`（索引数据根目录），`ai-results.json` 中的 `meta.sourceDir` 指向其下的 `wiki/` 子目录（文档源文件）。两者共享同一根目录，确保 Wiki 同步写回能正确落入 source 目录。

## Wiki 目录结构

```
wiki/
├── 项目概述/           # 项目整体介绍、设计理念、技术栈
├── 快速开始.md         # 快速入门指南
├── 核心模块架构/       # 核心模块设计文档
│   ├── 告警后端模块/
│   ├── APM监控模块/
│   └── 元数据管理模块/
├── API接口文档/         # REST API 接口说明
├── APM全栈监控/        # APM 应用性能监控
├── 告警系统设计/       # 告警规则、通知机制
├── 监控数据管理/       # 数据采集、存储和查询
├── 数据库设计/         # 数据库表结构和索引设计
├── 用户界面设计/       # 前端界面设计规范
├── 扩展开发指南/       # 扩展开发文档
├── 部署与运维/         # 部署流程和运维指南
├── 测试策略/           # 测试方法和最佳实践
├── 故障排查/           # 常见问题和解决方案
└── 安全考虑/           # 安全相关配置和注意事项
```

## 前置条件

### 第一步：环境自检（`mem doctor` + `ki`）

执行前**必须**完成以下两项检查：

#### 1.1 检查 mem

```bash
mem doctor
```

**✅ 通过标准**：输出中应看到：
- `✅ Config file` — 配置文件已找到
- `✅ Embedding API key present` — API Key 已配置
- `✅ Embedding API (...): OK` — 嵌入接口连通
- `✅ LanceDB read/write: OK` — 数据库可读写

**❌ 不通过时**，按以下步骤修复后再继续：

| 失败项 | 修复操作 |
|--------|----------|
| Config file 未找到 | 安装 mem 命令（见第二步） |
| Embedding API key 缺失 | 编辑 `~/.config/memory-mcp/config.yaml`，填入 `apiKey` |
| Embedding API 不通 | 检查网络与 `baseURL` 是否正确 |
| LanceDB 不可写 | 检查 `dbPath` 目录权限 |

#### 1.2 检查 ki

```bash
ki --version
```

**✅ 通过标准**：输出 ki 版本号（如 `ki v1.x.x`）。

**❌ 未安装时**，进入第二步安装 ki CLI 和配套 Skills。

### 第二步：安装缺失工具

#### 2.1 安装 ki CLI 与 Skills

若 `ki` 命令不存在，执行：

```bash
# 安装 ki CLI
curl -fsSL https://raw.githubusercontent.com/HACK-WU/knowledge-indexer/master/scripts/install-latest.sh | bash

# 安装配套 Skills 到项目目录
ki setup --skills -t ~/.codebuddy/skills -t ~/.agents/skills
```

> `ki setup --skills` 会将 `ki-foundation`、`codekb-skill`、`memory-skill` 等核心 Skill 安装到指定目录。

#### 2.2 安装与配置 mem

若 `mem doctor` 失败，按以下步骤安装配置：

**安装 mem 命令**：
```bash
curl -fsSL https://raw.githubusercontent.com/HACK-WU/memory-lancedb-mcp/master/scripts/install-latest.sh -o install-latest.sh
bash install-latest.sh
```

**配置嵌入 API**（已提供示例文件 `configs/mem/config.yaml`）：

编辑 `~/.config/memory-mcp/config.yaml`，核心配置：
```yaml
embedding:
  apiKey: ${SILICONFLOW_API_KEY}   # 替换为你的 API Key
  model: Qwen/Qwen3-Embedding-8B
  baseURL: https://api.siliconflow.cn/v1
  dimensions: 4096
```

> 📁 完整配置示例见：`bk-monitor-wiki/configs/mem /config.yaml`

**注册 `monitor` scope**：
```yaml
scopes:
  default: global
  definitions:
    monitor:
      description: BK-Monitor Wiki 文档知识库
      acl:
        - global
        - monitor
```

### 第三步：确认 ki 配置

本项目已提供 ki 配置文件 `configs/ki/config.json`：

```json
{
  "dataDir": "/root/.ki/kb",
  "backupDir": "$HOME/.ki-backup",
  "scopes": {
    "monitor": {
      "kbDir": "/root/bk-monitor/bk-monitor-wiki",
      "wikiSync": {
        "enabled": true,
        "sourceDir": "/root/bk-monitor/bk-monitor-wiki"
      }
    }
  }
}
```

> 📁 完整配置文件位于：`bk-monitor-wiki/configs/ki/config.json`
>
> ⚠️ `kbDir` 与 `wikiSync.sourceDir` 保持一致，确保知识索引数据与 Wiki 源文件共享同一根目录。

## 执行流程

通用流程详见 [build-kb.md](https://github.com/HACK-WU/knowledge-indexer/blob/master/docs/build-kb.md) 的 S-04 统一导入流程（2 步）。以下为本项目的具体参数。

### Step 1: 生成 ai-results.json

扫描 `wiki/` 目录，为每个 Markdown 文件生成结构化条目。

> ⚠️ **轻量读取**：优先使用文件路径、文件名、文档开头（前 10-20 行）生成摘要和关键词。**禁止逐文件全文读取**。

**输出文件**：`ai-results.json`（放在仓库根目录）

**格式示例**：
```json
{
  "meta": {
    "sourceDir": "/root/bk-monitor/bk-monitor-wiki/wiki",
    "rootName": "BK-Monitor-Wiki"
  },
  "entries": [
    {
      "path": "告警系统设计/告警引擎核心.md",
      "groupPath": "BK-Monitor-Wiki/告警系统设计",
      "relation": "告警引擎核心",
      "summary": "告警引擎核心模块，包含告警处理引擎、上下文管理、存储系统、缓存系统和控制流程管理。",
      "keywords": ["告警引擎", "处理引擎", "上下文管理", "存储系统"],
      "action": "add"
    }
  ]
}
```

> ⚠️ `sourceDir` 必须使用**绝对路径**，否则 `ki scan-kb import` 会报路径不存在错误。路径为 `/root/bk-monitor/bk-monitor-wiki/wiki`。

### Step 2: 执行导入

```bash
ki scan-kb import \
  --scope monitor \
  --results ai-results.json
```

> ⚠️ `ai-results.json` 也建议使用**绝对路径**，如 `/root/bk-monitor/ai-results.json`。

**内部流水线**（详见 build-kb.md）：
1. 格式校验：验证 ai-results.json 格式和字段完整性
2. 批量向量化：调用 mem store 批量向量化所有条目
3. Group 树创建：自动创建 Group 目录结构
4. Relations 缓存写入：写入 relations-cache.json
5. group-index.source 记录：记录导入元信息

## 验证步骤

导入完成后，执行以下验证：

### 1. Group 树结构
```bash
ki query-group --scope monitor --mode compact
```
预期：显示完整的 BK-Monitor-Wiki 目录结构

### 2. Relations 列表
```bash
ki query-group --scope monitor --groups "BK-Monitor-Wiki/告警系统设计"
```
预期：显示告警系统设计下的所有 Relation 和关键词

### 3. 语义检索测试
```bash
mem search "告警引擎" --scope monitor
```
预期：返回告警引擎相关的记忆条目

## 增量更新后的知识索引同步

> **⚠️ 禁止使用脚本更新 Wiki 内容。** Wiki 页面正文的更新/新建必须由 Agent 读取源文件后**手动分析和撰写**，不得使用脚本自动生成或替换。此处描述的 `ki scan-kb import` 仅用于**知识索引同步**（将已完成的 Wiki 页面向量化导入知识库），不参与 Wiki 页面内容的生成。

当 `wiki-incremental-update` Skill 新建或更新了 Wiki 页面后，需要同步到知识索引中，使新页面可被语义检索到。

### 增量导入新建页面

增量更新产生新 Wiki 页面后，为其生成 `ai-results.json` 并执行局部导入：

```bash
# 1. 为新页面生成 ai-results.json（仅含 action=add 的条目）
# 2. 执行导入
ki scan-kb import \
  --scope monitor \
  --results ai-results.json
```

> 无需全量重建，只需导入新建/变更的页面。

### 更新已有页面

如果增量更新只修改了已有 Wiki 页面（未新建），通常不需要重新导入知识索引。知识索引记录的是摘要和关键词，轻微内容变更不影响检索效果。但若页面主题发生较大变化，可重新导入该页面。

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Access denied to scope | scope 未注册 | 检查 `~/.config/memory-mcp/config.yaml` 中的 scopes 配置 |
| mem store 失败 | mem 命令未安装或配置错误 | 执行 `mem doctor` 检查配置 |
| 向量化超时 | 文档数量过多 | 分批处理，每次导入 20-30 个文档 |

## 相关链接

- [build-kb.md — knowledge-indexer 知识库构建文档](https://github.com/HACK-WU/knowledge-indexer/blob/master/docs/build-kb.md)
- [memory-lancedb-mcp](https://github.com/HACK-WU/memory-lancedb-mcp)
- 本仓库配置文件：
  - `bk-monitor-wiki/configs/ki/config.json` — ki 配置
  - `bk-monitor-wiki/configs/mem /config.yaml` — mem 配置（⚠️ 注意目录名尾部有空格）
