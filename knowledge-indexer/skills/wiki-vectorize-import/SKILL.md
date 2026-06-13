# BK-Monitor Wiki 向量化导入

> 基于 memory-lancedb-mcp 的首次配置流程，对 `bk-monitor-wiki/wiki/` 下的 Markdown 文档进行向量化导入，构建语义搜索能力。

## 触发场景

- 用户要求"对 wiki 进行向量化"、"wiki 语义搜索"、"wiki 向量导入"
- 用户首次配置 memory-lancedb-mcp 后需要导入 wiki 文档
- wiki 文档数量大幅变化，需要重新全量导入
- 用户说"把 wiki 文档导入到记忆服务"

## 前置要求：首次配置 memory-lancedb-mcp

> **重要**：在进行 wiki 向量化导入之前，必须先完成 memory-lancedb-mcp 的安装和配置。

请先参照 [memory-lancedb-mcp 首次使用配置 SKILL](https://github.com/HACK-WU/memory-lancedb-mcp/blob/master/skills/setup-first-use/SKILL.md) 完成以下步骤：

1. **安装 mem 命令**
2. **初始化配置文件** `~/.config/memory-mcp/config.yaml`
3. **配置嵌入 API**（推荐 SiliconFlow + Qwen/Qwen3-Embedding-8B）
4. **注册 `monitor` scope**
5. **执行 `mem doctor` 通过所有健康检查**

### scope 配置要点

在 `~/.config/memory-mcp/config.yaml` 中注册 `monitor` scope：

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

### 嵌入配置要点

```yaml
embedding:
  apiKey: ${SILICONFLOW_API_KEY}
  model: Qwen/Qwen3-Embedding-8B
  baseURL: https://api.siliconflow.cn/v1
  dimensions: 4096
```

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| scope | `monitor` | 项目隔离标识 |
| sourceDir | `wiki/` | wiki 文档目录（相对 `bk-monitor-wiki/` 或仓库根目录） |
| rootName | `BK-Monitor-Wiki` | 导入根节点名称 |

## Wiki 目录结构

```
bk-monitor-wiki/wiki/
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

## 执行流程

```
确认 mem 已安装 && mem doctor 全部通过
│
▼
[Step 1] 扫描 wiki 目录，生成 ai-results.json
│
▼
[Step 2] 执行向量化导入
│  ├── 格式校验
│  ├── 批量向量化
│  ├── Group 树创建
│  ├── Relations 缓存写入
│  └── group-index.source 记录
│
▼
[Step 3] 验证导入结果
│
▼
完成
```

---

### Step 1: 生成 ai-results.json

扫描 `wiki/` 目录下的所有 `.md` 文件，为每个文件生成结构化条目。

**输出文件**：`ai-results.json`

**条目格式**：

```json
{
  "meta": {
    "sourceDir": "wiki",
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

**字段说明**：

| 字段 | 说明 |
|------|------|
| `meta.sourceDir` | wiki 文档目录路径 |
| `meta.rootName` | 导入知识库的根节点名称 |
| `entries[].path` | wiki 文档相对 sourceDir 的路径 |
| `entries[].groupPath` | 所属 Group 完整路径，基于目录结构生成 |
| `entries[].relation` | 文档标题/名称，作为记忆的 relation 标识 |
| `entries[].summary` | 文档摘要，50-150 字，概括文档内容 |
| `entries[].keywords` | 关键词列表，3-8 个，用于辅助检索 |
| `entries[].action` | `"add"`（新增）/ `"update"`（更新）/ `"delete"`（删除） |

**生成注意事项**：

1. 排除 `metadata.json` 等非 wiki 内容的配置文件
2. `groupPath` 按目录层级生成：`{rootName}/{子目录}/{子目录}`
3. 根目录下的文件（如 `快速开始.md`），`groupPath` 直接为 `BK-Monitor-Wiki`
4. `summary` 需读取文档前 200 行生成，抓住文档主旨
5. `keywords` 从文档标题、章节标题、关键术语中提取

---

### Step 2: 执行向量化导入

```bash
ki scan-kb import \
  --scope monitor \
  --results ai-results.json
```

**内部流水线**（由 ki 命令自动完成）：

1. **格式校验**：验证 `ai-results.json` 格式和字段完整性
2. **批量向量化**：调用 `mem store` 批量向量化所有条目
3. **Group 树创建**：自动创建 Group 目录结构
4. **Relations 缓存写入**：写入 `relations-cache.json`
5. **group-index.source 记录**：记录导入元信息

**分批导入（文档数量 > 30 时推荐）**：

```bash
# 将 ai-results.json 拆分为多个批次文件，每个 20-30 条
ki scan-kb import --scope monitor --results ai-results-batch-1.json
ki scan-kb import --scope monitor --results ai-results-batch-2.json
# ...
```

---

### Step 3: 验证导入结果

#### 3.1 Group 树结构

```bash
ki query-group --scope monitor --mode compact
```

预期输出：完整的 BK-Monitor-Wiki 目录结构，所有子目录正确显示。

#### 3.2 单目录内容验证

```bash
ki query-group --scope monitor --groups "BK-Monitor-Wiki/告警系统设计"
```

预期：显示告警系统设计下的所有 Relation 和关键词。

#### 3.3 语义检索测试

```bash
mem search "告警引擎的处理流程" --scope monitor
```

预期：返回告警引擎相关的记忆条目，相关性从高到低排列。

#### 3.4 统计信息

```bash
mem stats --scope monitor
```

预期：显示的条目数应与 `ai-results.json` 中 entries 数量一致。

---

## AI 操作原则

| 原则 | 要求 |
|------|------|
| 先配置后导入 | 必须确认 mem 已安装、`doctor` 全部通过，才能开始导入 |
| summary 质量 | 每个 summary 需真实阅读文档内容总结，不得捏造 |
| 关键词准确 | keywords 从文档中提取实际出现的术语 |
| 分批处理 | 文档数量 > 30 时分批导入，避免向量化超时 |
| 验证闭环 | 每个步骤完成后验证结果，确认成功再继续 |

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `mem: command not found` | mem 未安装 | 参照 [setup-first-use](https://github.com/HACK-WU/memory-lancedb-mcp/blob/master/skills/setup-first-use/SKILL.md) 安装 |
| `Access denied to scope: monitor` | scope 未注册 | 在 `config.yaml` 中注册 monitor scope |
| `mem store` 失败 | API Key 无效或网络不通 | 执行 `mem doctor` 排查 |
| 向量化超时 | 文档数量过多 | 拆分为每批 20-30 条，分批 `ki scan-kb import` |
| 搜索结果不相关 | summary 质量差 | 重新生成 `ai-results.json`，改进 summary 和 keywords |
| LanceDB 锁文件冲突 | 上次导入异常退出 | 删除 `~/.local/share/memory-mcp/lancedb/*.lock` |

## 完成摘要

导入完成后输出：

- 导入的文档总数
- Group 目录数量
- 使用的 Scope（`monitor`）
- 嵌入模型和维度
- 语义检索测试结果（至少 3 条验证）
- 是否需要补充或修正的文档列表

## 相关链接

- [memory-lancedb-mcp 首次使用配置 SKILL](https://github.com/HACK-WU/memory-lancedb-mcp/blob/master/skills/setup-first-use/SKILL.md)
- [memory-lancedb-mcp](https://github.com/HACK-WU/memory-lancedb-mcp)
- [knowledge-indexer 统一导入流程](https://github.com/HACK-WU/knowledge-indexer/blob/master/skills/knowledge-index-build/SKILL.md)
