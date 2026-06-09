# BK-Monitor Wiki 知识库构建

> 为 BK-Monitor Wiki 文档仓库构建知识索引，支持语义搜索和 AI 助手集成。

## 触发场景

- 首次为 bk-monitor-wiki 构建知识索引
- wiki 文档结构发生较大变化，需要重新全量导入
- 用户要求"构建 wiki 知识索引"、"导入 wiki 文档"

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| scope | `monitor` | 项目隔离标识 |
| sourceDir | `wiki/` | wiki 文档目录（相对仓库根目录） |
| rootName | `BK-Monitor-Wiki` | 导入根节点名称 |

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

1. **安装 mem 命令**：知识索引的所有向量化操作都依赖 mem 命令
   ```bash
   curl -fsSL https://raw.githubusercontent.com/HACK-WU/memory-lancedb-mcp/master/scripts/install-latest.sh -o install-latest.sh
   bash install-latest.sh
   ```

2. **配置嵌入 API**：确保 `~/.config/memory-mcp/config.yaml` 中已配置嵌入 API 密钥
   ```yaml
   embedding:
     apiKey: ${SILICONFLOW_API_KEY}
     model: Qwen/Qwen3-Embedding-8B
     baseURL: https://api.siliconflow.cn/v1
     dimensions: 4096
   ```

3. **注册 scope**：在 `~/.config/memory-mcp/config.yaml` 中注册 `monitor` scope
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

4. **验证配置**：
   ```bash
   mem doctor
   ```

## 执行流程

基于 [knowledge-indexer 统一导入流程](https://github.com/HACK-WU/knowledge-indexer/blob/master/skills/knowledge-index-build/SKILL.md)，2 步完成构建。

### Step 1: 生成 ai-results.json

扫描 `wiki/` 目录，为每个 Markdown 文件生成结构化条目。

**输出文件**：`ai-results.json`

**格式示例**：
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

### Step 2: 执行导入

```bash
ki scan-kb import \
  --scope monitor \
  --results ai-results.json
```

**内部流水线**：
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

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Access denied to scope | scope 未注册 | 检查 `~/.config/memory-mcp/config.yaml` 中的 scopes 配置 |
| mem store 失败 | mem 命令未安装或配置错误 | 执行 `mem doctor` 检查配置 |
| 向量化超时 | 文档数量过多 | 分批处理，每次导入 20-30 个文档 |

## 相关链接

- [knowledge-indexer 统一导入流程](https://github.com/HACK-WU/knowledge-indexer/blob/master/skills/knowledge-index-build/SKILL.md)
- [memory-lancedb-mcp](https://github.com/HACK-WU/memory-lancedb-mcp)
