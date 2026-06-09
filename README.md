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
├── rules/                   # 规则文件
│   ├── django-url-view-resolver.md   # Django URL 解析规则
│   ├── gitnexus-mcp-usage-guide.md  # GitNexus MCP 使用指南
│   └── resource-locator.md          # Resource/API 代码定位规则
├── scripts/                 # 工具脚本
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

## 规则文件

### resource-locator.md
Resource/API 代码定位规则，用于从 `resource.xxx.yyy` 格式的路径定位到对应的 Python 类源码。

### django-url-view-resolver.md
Django URL → View / Resource 解析脚本的使用说明。

### gitnexus-mcp-usage-guide.md
GitNexus MCP 工具的使用指南。

## 知识库索引

使用 [memory-lancedb-mcp](https://github.com/HACK-WU/memory-lancedb-mcp) 构建 wiki 文档的知识库索引，支持语义搜索和智能检索。

### 功能说明

- 将 wiki 文档内容向量化存储到 LanceDB
- 支持语义搜索，根据自然语言查询找到相关文档
- 可与 AI 助手集成，提供上下文感知的文档检索

### 配置指南

详细配置步骤请参考：[首次使用配置 SKILL](https://github.com/HACK-WU/memory-lancedb-mcp/blob/master/skills/setup-first-use/SKILL.md)

### 快速开始

```bash
# 安装 mem 命令
curl -fsSL https://raw.githubusercontent.com/HACK-WU/memory-lancedb-mcp/master/scripts/install-latest.sh -o install-latest.sh
bash install-latest.sh

# 初始化配置
mem config init

# 验证配置
mem doctor
```

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