# BK-Monitor Wiki

BK-Monitor 项目的文档仓库，包含项目架构设计、API 文档、部署指南等技术文档。

## 目录结构

```
bk-monitor-wiki/
├── wiki/                    # 主文档目录
│   ├── 项目概述/           # 项目整体介绍
│   ├── 快速开始.md         # 快速入门指南
│   ├── 核心模块架构/       # 核心模块设计文档
│   ├── API接口文档/         # API 接口说明
│   ├── APM全栈监控/        # APM 相关文档
│   ├── 告警系统设计/       # 告警系统设计文档
│   ├── 监控数据管理/       # 数据管理相关
│   ├── 数据库设计/         # 数据库设计文档
│   ├── 用户界面设计/       # UI 设计文档
│   ├── 扩展开发指南/       # 扩展开发文档
│   ├── 部署与运维/         # 部署运维指南
│   ├── 测试策略/           # 测试相关文档
│   ├── 故障排查/           # 故障排查指南
│   └── 安全考虑/           # 安全相关文档
├── skills/                  # 技能文件
│   ├── wiki-incremental-update/  # Wiki 增量更新技能
│   └── wiki-knowledge-build/     # Wiki 知识库构建技能
├── rules/                   # 规则文件
├── scripts/                 # 工具脚本
│   ├── wiki_incremental/          # Wiki 增量更新工具库
│   ├── django-url-view-resolver.py  # Django URL 解析脚本
│   └── hello.py                      # Django 环境初始化
├── requirements/            # 需求文档
└── mcp.json                 # MCP 配置
```

## 文档分类

### 核心文档
- **项目概述** - 项目整体架构和设计理念
- **快速开始** - 快速入门和基本使用
- **核心模块架构** - 核心模块的设计和实现

### 开发文档
- **API接口文档** - REST API 接口说明
- **扩展开发指南** - 如何扩展和定制功能
- **测试策略** - 测试方法和最佳实践

### 运维文档
- **部署与运维** - 部署流程和运维指南
- **故障排查** - 常见问题和解决方案
- **安全考虑** - 安全相关配置和注意事项

### 专题文档
- **APM全栈监控** - 应用性能监控
- **告警系统设计** - 告警规则和通知机制
- **监控数据管理** - 数据采集、存储和查询
- **数据库设计** - 数据库表结构和索引设计
- **用户界面设计** - 前端界面设计规范

## 工具脚本

### Wiki 增量更新工具

维护源文件与 Wiki 文档之间的双向引用索引，根据 git commit 变更检测受影响的 Wiki 页面，支持增量更新。

```bash
# 全量构建索引
cd /root/bk-monitor
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli build-index \
  --wiki-dir bk-monitor-wiki/wiki \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --repo-dir . \
  --repo-url git@github.com:TencentBlueKing/bk-monitor.git \
  --branch master \
  --output bk-monitor-wiki/wiki/metadata.json

# 检测变更影响范围（dry-run）
PYTHONPATH=bk-monitor-wiki/scripts python3 -m wiki_incremental.cli detect \
  --metadata bk-monitor-wiki/wiki/metadata.json \
  --new-commit <commit_hash> \
  --repo-dir .
```

详细用法：[scripts/wiki_incremental/README.md](scripts/wiki_incremental/README.md)

### Django URL 解析脚本

用于从 HTTP 接口 URL 反推出最终处理代码（视图函数、视图类、Resource 类）。

**使用方法：**
```bash
cd /root/bk-monitor/bk-monitor-wiki
python scripts/django-url-view-resolver.py "<URL>" "<METHOD>"
```

**示例：**
```bash
python scripts/django-url-view-resolver.py "/rest/v2/data_explorer/get_graph_query_config/" "POST"
```

## 技能文件

### wiki-incremental-update

根据代码变更增量更新受影响的 Wiki 页面。完整流程：commit 范围确认 → 变更检测 → 更新 Wiki → 格式校验 → 索引同步。

详见：[skills/wiki-incremental-update/SKILL.md](skills/wiki-incremental-update/SKILL.md)

### wiki-knowledge-build

将 wiki 文档向量化导入知识库，支持语义搜索和 AI 助手集成。

详见：[skills/wiki-knowledge-build/SKILL.md](skills/wiki-knowledge-build/SKILL.md)

## 规则文件（旧）

规则已迁移到 IDE 规则系统，此处仅保留历史参考。

## 知识库索引

通过 [memory-lancedb-mcp](https://github.com/HACK-WU/memory-lancedb-mcp) 和 [knowledge-indexer](https://github.com/HACK-WU/knowledge-indexer) 构建 wiki 文档的向量知识索引，支持语义搜索和 AI 助手集成。

详见技能文件中的 [wiki-knowledge-build](skills/wiki-knowledge-build/SKILL.md) 和 [wiki-incremental-update](skills/wiki-incremental-update/SKILL.md)。

## 相关项目

- [bk-monitor](../) - 主项目仓库
- [bk-monitor-base](../bk-monitor-base/) - 基础组件库
- [bkmonitor](../bkmonitor/) - 监控平台核心代码
- [memory-lancedb-mcp](https://github.com/HACK-WU/memory-lancedb-mcp) - 知识库索引工具

## 贡献指南

1. 文档使用 Markdown 格式编写
2. 按照目录结构放置文档
3. 保持文档与代码同步更新
4. 使用中文编写文档，技术术语可保留英文

## 许可证

本项目采用 [LICENSE](../LICENSE.txt) 许可证。