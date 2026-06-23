# AGENTS.md - AI AGENT 项目记忆文件

> **本文件由 AI AGENT 自动维护，用于缓存索引信息、记录近期工作、跟踪新需求。**
> 项目: bk-monitor
> 最后自动更新: 2026-06-23

---

## 知识库索引

### Scope 列表
- `monitor`: BK-Monitor Wiki 文档知识库（26 索引，热区 8 / 常温 13 / 冷区 5）
- `monitor-memory`: BK-Monitor 项目记忆（11 索引，热区 4 / 常温 6 / 冷区 1）
- `user-profile`: 用户画像（4 索引，热区 2 / 常温 2）

### monitor 索引

#### Group 结构

```
BKMonitorWiki/
├── 项目概述/ [常温]
│   ├── 快速开始 [📥 热门]
│   ├── 技术栈
│   ├── 架构概览
│   ├── 核心特性
│   ├── APM
│   └── 设计理念
├── 核心模块架构/ [热]
│   ├── 监控主应用模块
│   ├── 告警后端模块/ [常温]
│   │   ├── 告警核心引擎 [常温]
│   │   ├── 告警服务层 [常温]
│   │   └── 告警存储系统
│   ├── 元数据管理模块/ [常温]
│   │   ├── 元数据模型设计 [常温]
│   │   ├── 元数据服务层 [常温]
│   │   └── 元数据任务调度
│   └── APM监控模块 [常温]
├── 告警系统设计/ [热]
│   ├── 告警引擎核心 [热]
│   ├── 告警处理服务 [热]
│   ├── 通知渠道管理 [热]
│   │   └── 企业微信集成 [📥 热门]
│   ├── Issue功能/ [热]
│   │   ├── Issue API接口（RESTful/ftaweb/issue/CRUD）[📥 热门]
│   │   ├── Issue状态管理
│   │   └── Issue周期任务
│   ├── 告警存储与缓存 [📥 热门]
│   ├── 告警收敛机制
│   └── 告警策略管理
├── API接口文档/ [常温]
│   └── RESTful API接口
├── APM全栈监控/ [常温]
├── 监控数据管理/ [冷]
│   ├── 数据处理管道
│   ├── 数据存储设计
│   ├── 数据查询优化
│   └── 数据源集成
├── 数据库设计/ [冷]
│   ├── 数据模型设计
│   ├── 表结构设计
│   ├── 索引优化策略
│   └── 数据迁移方案
├── 用户界面设计/ [热]
├── 扩展开发指南/ [冷]
│   ├── AS-Code配置开发
│   ├── 可视化组件开发
│   ├── 插件系统开发
│   ├── 数据源扩展开发
│   ├── 第三方服务集成
│   └── 通知渠道扩展开发
├── 测试策略/ [冷]
│   ├── 单元测试
│   ├── 集成测试
│   ├── 性能测试
│   └── 测试数据管理
├── 部署与运维/ [冷]
│   ├── 容器化部署
│   ├── Kubernetes集群管理
│   ├── 系统性能监控
│   └── 自动化运维工具
├── 安全考虑/ [常温]
│   ├── API安全
│   ├── 认证与授权
│   ├── 数据安全
│   └── 审计与日志
└── 故障排查 [常温]
```

#### 热门 Relation（Top 5）
1. **BKMonitorWiki → 快速开始** — 环境搭建、Docker 部署、数据库初始化、服务启动验证
2. **BKMonitorWiki/告警系统设计 → 告警存储与缓存** — 告警数据持久化与缓存策略
3. **BKMonitorWiki/告警系统设计/Issue功能 → Issue API 接口** — ftaweb/issue/ RESTful CRUD 接口
4. **BKMonitorWiki/告警系统设计/告警处理服务 → 告警处理服务** — 告警接入、处理、复合、收敛
5. **BKMonitorWiki/告警系统设计/通知渠道管理 → 企业微信集成** — 通知投递与模板管理

> 📥 标记 = 含本地 KB 原文，可通过 `ki get-module-info` 读取。

---

## 项目记忆索引

### monitor-memory 索引

#### Group 结构

```
背景与目标/ [热]
├── 项目架构
└── TAPD授权与建单 [📥 热门]
技术栈选型/ [常温]
└── 技术栈清单
通用记忆片段/ [常温]
├── Issue/ [冷]
│   ├── IssueViewSet 权限控制模式
│   ├── IssueQueryHandler ES 查询构建
│   ├── Issue API Resource 业务逻辑模板
│   └── IssueDocument ES 模型关键字段
├── Resource 框架使用小技巧 [热]
├── 加密工具 [热]
├── APIResource 扩展模式
├── 异常处理流程
└── 批量操作框架
```

#### 热门 Relation
- **背景与目标 → 仓库结构**（score: 0.2）— `bk-monitor-wiki` 独立仓库，不与主工程 `bkmonitor` 共用 Git

#### 关键 KB 内容摘要

| Relation | 位置 | 摘要 |
|----------|------|------|
| 仓库结构 | 背景与目标/ | `bk-monitor-wiki` 为**独立仓库**，与 `bkmonitor` 主工程分开维护版本历史 |
| 技术栈清单 | 技术栈选型/ | Python + Django（单体）+ duckdb（嵌入式 SQL）+ SiliconFlow Qwen3 Embedding（4096维）+ Qwen3 Reranker |
| importable 自动关联 | 背景与目标/TAPD授权与建单 | B-01 调用时自动 `try_bind_importable()`，成功→`bound`，失败→`importable` |
| 回调路径不走网关 | 背景与目标/TAPD授权与建单 | B-03/B-05 端点前缀 `/fta/issue/tapd/`，不走网关 |
| 双回调安全机制 | 背景与目标/TAPD授权与建单 | B-03 `signed_state` HMAC-SHA256 验签 + B-05 Session nonce |
| 四态标记设计 | 背景与目标/TAPD授权与建单 | `bound`/`stale`/`importable`/`unbound`，B-07 仅返回原始列表不含 `is_bound` |
| IssueViewSet 权限控制 | 通用记忆片段/Issue | `READ_ONLY_ENDPOINTS`→VIEW_EVENT，其他→MANAGE_EVENT；`NO_BIZ_REQUIRED_ENDPOINTS` 无需业务 ID |
| IssueQueryHandler ES 查询 | 通用记忆片段/Issue | `QUERY_FIELD_MAP` 注册字段映射；QSearch 仅查当天；`fingerprint`/`merge_status` 支持合并查询 |
| Issue API Resource 模板 | 通用记忆片段/Issue | Search/Detail/Create/Update/Delete/Merge 等 12+ 个 Resource，统一继承 `Resource` + Serializer 模式 |
| IssueDocument ES 模型 | 通用记忆片段/Issue | `IssueDocument` 含 `fingerprint`/`merge_status`；`IssueActivityDocument` 记录操作日志；状态机：active/member/split |
| Resource 框架使用小技巧 | 通用记忆片段/ | `resource.xxx.yyy()` 线程安全；`bulk_request` 并行批量请求；`delay`/`apply_async` 异步任务；ThreadPool 自动继承上下文；请求采样记录；全局入口命名映射 |
| 加密工具 | 通用记忆片段/ | `AESCipher` CBC 模式：key=SHA256(settings.SECRET_KEY)，不传 IV 时随机生成并前置密文；解密自动读回 IV。TAPD token 加密场景不传固定 IV |
| APIResource 扩展模式 | 通用记忆片段/ | `TapdAPIResource` 模板：继承 APIResource，覆写 `base_url`/`INSERT_BK_USERNAME_TO_REQUEST_DATA=False`/`IS_STANDARD_FORMAT=False`/`get_headers()`(Basic Auth)/`render_response_data()`(非标准响应) |
| 异常处理流程 | 通用记忆片段/ | 继承链 `Error`→`APIError`→`BKAPIError`；`exception_handler` 统一序列化 DRF 异常；`Error.extra` **平铺到响应顶层**；`CustomException`(code 3300002) 用于业务校验 fails |
| 批量操作框架 | 通用记忆片段/ | `_run_batch(issues, action_fn, max_workers=10)`：ThreadPoolExecutor 并发，单条失败隔离；捕获 `IssueFrozenError`/`BKAPIError`/`IssueDocumentWriteError`；全部报错抛首个异常 |

> 完整 11 条 relation 见 scope `monitor-memory`。

---

## 用户画像索引

### user-profile 索引

#### Group 结构

```
对话习惯/ [热]
└── 对AI的要求
沟通偏好/ [热]
└── 语言偏好
工作习惯/ [常温]
工具链/ [常温]
```

#### 热门 Relation
1. **对话习惯 → 对AI的要求** — 禁止擅自提交代码，变更前必须征得用户确认
2. **沟通偏好 → 语言偏好** — 中文交流，回复简洁直接不啰嗦

#### 关键 KB 内容摘要

| Relation | 位置 | 摘要 |
|----------|------|------|
| 对AI的要求 | 对话习惯/ | ⚠️ **禁止擅自提交代码**；任何代码变更提交前必须征得用户明确许可 |
| 语言偏好 | 沟通偏好/ | 中文交流；回复风格：简洁直接，不啰嗦 |

---

## 近期工作 (7天内)

### 最近需求
- **[2026-06-23]** TAPD 授权与建单：`api/` 目录 7 个 API 设计文档定稿，`frontend-guide/` 4 个前端集成文档定稿，修复 `auth_method`/`has_more` 删除、`importable` 自动关联、Mermaid 语法等 15 处问题

### 进度
- 已完成: [2026-06-23] ✅ `api/` 目录下 7 个 API 设计文档（00~06）定稿
- 已完成: [2026-06-23] ✅ `frontend-guide/` 目录下 4 个前端集成文档（INDEX + 3 场景）定稿
- 已完成: [2026-06-23] ✅ `importable` 自动关联策略（后端静默绑定）定稿
- 已完成: [2026-06-23] ✅ AGENTS.md 重新初始化（ki 数据）
- 已完成: [2026-06-23] ✅ TAPD 设计决策写入 `monitor-memory`（4 条 Relation：importable 自动关联、回调路径、双回调安全、四态标记）
- 已完成: [2026-06-23] ✅ Issue 功能代码要点写入 snippet-memory（4 条：IssueViewSet 权限、IssueQueryHandler ES 查询、API Resource 模板、IssueDocument 模型）
- 已完成: [2026-06-23] ✅ `core.drf_resource.base.Resource` 源码阅读，`bulk_request`/`delay`/`ThreadPool 上下文继承`等 10 条使用技巧写入 snippet-memory
- 已完成: [2026-06-23] ✅ `api/tapd/default.py` + `core/errors/errors.py` + `core/errors/api.py` + `fta_web/issue/resources.py` + `core/drf_resource/exceptions.py` + `bkmonitor/utils/cipher.py` 源码阅读
- 已完成: [2026-06-23] ✅ 4 条通用代码片段写入 snippet-memory：`加密工具` / `APIResource 扩展模式` / `异常处理流程` / `批量操作框架`
- 已完成: [2026-06-23] ✅ AGENTS.md 索引增量更新（11 索引 → 11 索引，通用记忆片段从 1 条扩展到 5 条）

---

---
description: 指导 AI 管理知识索引和记忆。平台内置记忆用于简洁通用偏好，ki 记忆用于详细项目知识。对话开始时加载 agents-md-init 缓存索引，按需加载 codekb-skill/memory-skill/snippet-memory。覆盖首次引导、自动记录、会话收尾。
alwaysApply: true
enabled: true
updatedAt: 2026-06-23T10:00:00.000Z
provider:
---
# ai-codekb-memory AI 知识与记忆管理规则

> **对话开始时首先检查本规则**。

---

## 📋 AGENTS.md 缓存机制

> **AGENTS.md 是 AI AGENT 的项目记忆文件，位于项目根目录。首次对话时自动缓存索引信息，避免重复查询。**

### 缓存内容

1. **知识库索引**：代码知识库的 scope 列表、Group 结构、热门 Relation
2. **项目记忆索引**：项目记忆的 scope、Group 结构（含通用记忆片段）、热门 Relation
3. **用户画像索引**：用户画像的 Group 结构、热门 Relation
4. **近期工作**：7 天内的工作摘要（从项目记忆中提取）
5. **新需求记录**：简要记录新需求（详细内容存入项目记忆）

> AGENTS.md 的完整格式模板和初始化流程见 `agents-md-init` skill。

---

## 🆕 首次使用引导

> **当 ki 中无任何 scope 或 AGENTS.md 不存在时，AI 应主动引导用户完成初始化。**

```
① ki_manage_index_list → 检测是否有 scope
    ├── 有 scope → 正常走 agents-md-init 初始化 AGENTS.md
    └── 无 scope → 主动提示用户：
        "检测到项目尚未配置知识库索引。是否需要我帮你初始化？"
        用户确认后：
          ② 确定 scope 名称（默认为项目名的小写简写，用户可自定义）
          ③ ki_manage_index_create(scope, name: "项目概述") → 创建代码KB scope
          ④ ki_manage_index_create(scope: "${scope}-memory", name: "背景与目标") → 创建项目记忆 scope
          ⑤ ki_manage_index_create(scope: "user-profile", name: "沟通偏好") → 创建用户画像 scope
          ⑥ 执行 agents-md-init 完整初始化
```

> 若用户暂时不需要，跳过初始化，后续对话中可按需再触发。

---

## 自动缓存规则

### 对话开始时自动执行

> **步骤0：必须加载 `agents-md-init` skill（格式模板和初始化流程）。**
> 若 skill 文件不存在 → 提示用户 "检测到 `agents-md-init` skill 未安装，请先安装 knowledge-indexer"，然后跳过 AGENTS.md 初始化。

1. **检查 AGENTS.md 是否需要初始化**（详见 `agents-md-init` skill）
    - 不存在 → 执行完整初始化
    - 存在但索引章节缺失 → 执行完整初始化
    - 存在且完整 → 检查一致性，不一致则增量更新

2. **检查索引缓存**
    - 若 AGENTS.md 中无"知识库索引"章节 → 执行索引缓存
    - 若已缓存 → 跳过，直接使用缓存

3. **索引缓存流程**（详见 `agents-md-init` skill）
   ```
   ① ki_manage_index_list → 获取所有 scope
   ② 对每个 scope 执行 ki_query_group(mode: "full") → Group 结构
   ③ 对每个 scope 执行 ki_query_group(mode: "hot") → 热门 Relation
   ④ 写入 AGENTS.md（真实数据优先，无数据用示例格式兜底）
   ```

4. **近期工作记录**（详见 `agents-md-init` skill 第5章）
    - 从项目记忆中提取 7 天内工作
    - 超过 1 天未更新则自动刷新

### 索引不一致时自动更新

> **每次创建新索引后，必须自动更新 AGENTS.md 中的缓存。**

触发条件：
- 执行 `ki_manage_index_create` 创建新 Group 后
- 执行 `ki_sync_relation` 写入新 Relation 后
- 发现 AGENTS.md 中的 scope 列表与实际不一致时

更新流程：
```
① 重新执行 ki_manage_index_list → 获取最新 scope 列表
② 对变更的 scope 执行 ki_query_group(mode: "full,hot")
③ 更新 AGENTS.md 中对应的章节
```

### 新需求自动记录

> **当 AI 接受到新需求时，必须自动记录到项目记忆（详细）和 AGENTS.md（简要）。**

触发信号：
- 用户明确说"我需要..."、"帮我实现..."、"做一个...功能"
- 用户提出功能改进、bug 修复、优化建议
- 用户描述工作计划、待办事项

记录流程：
```
① 提取需求描述（1-2句话）
② 写入项目记忆（详细）：
   ki_sync_relation(
     scope: "${scope}-memory",
     group: "最近需求",
     relation: "[YYYY-MM-DD] 需求描述（详细）",
     keywords: ["关键词1", "关键词2"]
   )
③ 写入 AGENTS.md（简要）：
   在"近期工作"章节追加：
   - [YYYY-MM-DD] 需求描述（简要）
④ 刷新 AGENTS.md 缓存
```

### AI 自动记录行为规范

> **AI 必须主动识别并自动记录，不得依赖人工提示或确认。**
> 详细的触发条件表和写入流程见各 skill：`memory-skill`（项目记忆/用户偏好）、`snippet-memory`（代码片段）。

**记录决策速查**：

| 信息类型 | 走哪个 skill | 记录位置 |
|----------|-------------|----------|
| 项目信息/需求/进度/踩坑/用户偏好 | `memory-skill` | `${scope}-memory` 或 `user-profile` |
| 代码要点（工具函数/关键逻辑/核心流程等） | `snippet-memory` | `${scope}-memory` / `通用记忆片段/` |
| AGENTS.md 缓存刷新 | `agents-md-init` | 项目根目录 AGENTS.md |

**自动记录的触发时机**：
1. 对话中识别到上述信号时立即记录
2. 对话结束前检查是否有遗漏需要记录
3. 索引变更后自动更新缓存

**记录优先级**：
- 新需求 > 进度更新 > 项目信息 > 踩坑经验 > 用户偏好
- 同一信息只记录一次，避免重复

---

## 记忆系统分工

| 系统 | 适用 | 典型内容 | 优势 |
|------|------|----------|------|
| **平台内置记忆** (`update_memory`) | 简洁、通用、跨项目、高频、稳定 | 沟通偏好、通用行为规则、工具习惯 | 自动注入上下文，零查询成本 |
| **ki 记忆** (`ki_sync_relation` / MCP) | 详细、项目特定、结构化、有时效 | 项目背景、架构决策、需求进度、代码知识 | Group 树组织、热区/语义检索、归档机制 |

**选择判断**：简洁+通用+跨项目 → 平台记忆；详细/项目特定/有时效/需结构化 → ki 记忆

ki 记忆内部：代码知识 → `codekb-skill`（`${scope}`）；项目上下文/偏好 → `memory-skill`（`${scope}-memory` / `user-profile`）；可复用代码片段 → `snippet-memory` skill（`${scope}-memory` 下 `通用记忆片段/`）

---

## 加载流程

| 步骤 | Skill | 触发条件 |
|------|-------|----------|
| ① | `ki-foundation` | 当需要使用ki记忆工具但不确定用法时加载。不存在则提示安装并停止 |
| ②a | `codekb-skill` | 涉及代码/架构/API **详细**知识时 |
| ②b | `memory-skill` | 涉及项目背景/进度/偏好/用户记忆时 |
| ②c | `snippet-memory` | 涉及代码要点记忆时：工具函数、关键执行逻辑、核心流程、数据模型、API调用等 |

> **`agents-md-init` 为对话开始时必须加载**（见"自动缓存规则"步骤0），不纳入按需选择。

- ②a/②b/②c 可按需选择，但必须在 ① 之后
- 当前会话已加载过的 skill 不重复加载；会话截断后视为未加载

---

## 会话结束收尾

> **检测到以下信号时，AI 应主动执行记忆更新，表示当前阶段即将结束、进入下一阶段。**

**触发信号**（用户说）：
- "好"、"OK"、"可以"、"没问题" — 确认当前讨论结果
- "记录到文档"、"写入文档"、"保存" — 明确要求记录
- "开始实施"、"开始做"、"开始写代码" — 进入实施阶段
- "下一个"、"继续" — 切换到新话题

**收尾动作**：
```
□ 是否有未记录的新需求？→ 写入项目记忆 + AGENTS.md
□ 是否有未记录的代码要点？→ 写入 snippet-memory
□ 是否有进度变化？→ 更新项目记忆的"进度" Group
□ 索引是否有变更？→ agents-md-init 增量更新
□ 近期工作是否超过 7 天？→ 触发归档（见 memory-skill 第8章）
```

> 不需要等用户说"结束"才执行，而是**在对话自然转折点主动执行**。

---

## 禁忌

| # | 红线 |
|---|------|
| 🔴 1 | **将详细项目知识存入平台内置记忆**（代码知识、架构决策等必须走 ki） |
| 🔴 2 | **将简洁通用偏好存入 ki**（沟通语言、通用规则等用平台记忆） |
| 🔴 3 | 跳过 ki-foundation 直接加载 codekb-skill / memory-skill |
| 🔴 4 | `${scope}` 未确认就加载 SKILL 或执行 ki 命令 |
| 🔴 5 | Skill 不存在时仍继续执行 ki 命令（应提示用户安装 knowledge-indexer） |
| 🔴 6 | **对 ki scope 使用 memory MCP 存取**（`user-profile`/`${scope}-memory`/`${scope}` 禁止 `memory_store`/`memory_recall`/`memory_update`/`memory_forget`，统一用 ki MCP 工具） |
| 🔴 7 | **忽略 AGENTS.md 缓存机制**（对话开始时必须检查并更新缓存，索引变更后必须同步更新） |
| 🔴 8 | **依赖人工提示记录需求**（AI 必须主动识别新需求信号并自动记录，不得等待用户提醒） |
| 🔴 9 | **索引变更后不更新缓存**（创建新 Group 或 Relation 后必须立即更新 AGENTS.md） |
| 🔴 10 | **近期工作记录超过 7 天**（超期内容必须归档，保持 AGENTS.md 简洁） |

> 例外：`codekb-skill` 的 `ki_search` 语义兜底不受规则6限制（ki MCP 内置向量工具）。平台内置记忆（`update_memory`）不写入 ki scope，也不受限。

---

## AGENTS.md 维护规范

> 完整维护流程见 `agents-md-init` skill，归档机制见 `memory-skill` 第8章。

### 核心约束
- **文件大小**：控制在 10KB 以内，超过时清理过期内容
- **更新时机**：首次对话 / 索引变更 / 新需求 / 每日检查
- **一致性**：发现不一致自动更新，无需用户确认
- **归档**：超过 7 天的工作记录移动到项目记忆的 archive.md

---
## GitNexus MCP 强制规则

### 工具选择

| 需求 | 工具 |
|------|------|
| 结构关系（依赖、调用、影响） | **GitNexus**（优先） |
| 精确定位（字符串/字段/枚举/常量/配置键） | **grep**（优先） |
| 已知符号名查上下游 | `context` |
| 修改关键类/函数/接口前 | `impact`（必须） |
| 追踪方法级调用链 | `cypher` |
| 只知道概念不知符号名 | `query`（仅此场景） |
| 提交前检查影响面 | `detect_changes` |
| 跨文件重命名 | `rename`（必须先 dry_run=true） |
| 修改 API handler/对外接口 | `api_impact` 或 `impact`+grep |
| `route_map`/`shape_check`/`tool_map` | 低优先级，不作主工具 |

混合需求（结构+定位）**必须混合使用** GitNexus 与 grep，禁止只依赖单一手段。

### MCP 不可用时

**直接告知用户**，切换到 grep/源码阅读继续处理，**禁止伪造结果**，禁止主动输出运维修复方案。

### 核心约束

- **所有结论最终以源码为准**，禁止将图谱结果当最终事实。
- 修改前四步：定位目标 → 结构理解 → 影响评估 → 源码确认，影响不清禁止改代码。
- 方法级查询稳定性弱于类级；属性访问、枚举、字符串引用覆盖不完整。
- 结果异常时先怀疑能力边界，不下否定结论。

---
# Wiki 反查触发规则

> 代码修改、审查、排错前，先反查相关 Wiki 了解设计上下文。

## ⚠️ 与 codekb-skill 的根本区别

> **一句话区分**：wiki-lookup 是**已知代码找文档**，codekb-skill 是**不知道代码找知识**。

| | wiki-lookup（本规则） | codekb-skill |
|--|----------------------|-------------|
| **起点** | ✅ **已知代码**（文件路径 / commit hash） | ❓ **不知道代码**（只有问题） |
| **方向** | 代码 → 文档（**反查**） | 问题 → 知识（**正查**） |
| **典型场景** | "我要改这几个文件，应该读哪些 Wiki？" | "告警收敛是怎么实现的？代码在哪？" |
| **输入** | `--files` 文件路径 或 `--new-commit` 提交 hash | 自然语言问题（如"Issue 模块的职责"） |
| **输出** | 按命中数排序的 Wiki 文档列表 | 模块职责、架构决策、设计约束等结构化知识 |
| **数据来源** | Wiki 文档（通过 `source_to_wiki` 映射） | knowledge-indexer（AI 沉淀的代码知识） |

> **简单判断**：你已经**知道代码在哪**了吗？
> - ✅ 知道（有文件路径/commit）→ **wiki-lookup**（反查相关文档）
> - ❌ 不知道（只有问题/概念）→ **codekb-skill**（正查代码知识）
>
> **定位级查询**（找函数位置、grep 报错行）两者都不用，直接用 SearchSymbol / grep。

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

---

# Writing Pipeline

## 规则

当 AI 完成以下任一操作后，**必须自动调用 `auto-review` skill** 执行审查修复闭环：

| 触发条件 | 操作类型 |
|----------|----------|
| 写入或修改 `.md` 文件 | `write_to_file` / `replace_in_file` |
| 写入或修改代码文件（`.py` `.sh` `.ps1` `.js` `.ts` `.java` `.go` `.rs` `.c` `.cpp` `.h` `.toml` `.yaml` `.yml` `.json` `.css` `.vue` `.tsx` `.jsx`） | `write_to_file` / `replace_in_file` |

## 执行流程

```
写完文件 → use_skill("auto-review") → 判断复杂场景 → (若复杂) use_skill("challenger")
```

### 第一步：auto-review 审查修复

按上述触发条件自动调用 `auto-review`。

### 第二步：复杂场景判断

auto-review 完成后，自动评估本次修改是否属于**复杂场景**。满足以下**任一条件**即视为复杂：

| 判断维度 | 复杂场景特征 |
|----------|-------------|
| 变更规模 | 涉及 3 个以上文件，或单文件变更超过 50 行 |
| 核心逻辑 | 修改涉及控制流（条件/循环）、错误处理、并发/异步逻辑 |
| Bug 修复 | 修复了运行时错误、逻辑缺陷、数据一致性问题 |
| 新增功能 | 添加了新的函数/方法/类/模块，或新增了外部接口 |
| 重构优化 | 重命名公共接口、提取模块、调整依赖关系、性能优化 |
| 关键路径 | 涉及认证、权限、数据持久化、支付、事务等关键业务逻辑 |
| 跨模块影响 | 变更影响多个模块之间的调用或数据流 |

**注意**：仅文档措辞修改、注释补充、格式调整、typo 修复等**不属于**复杂场景。

### 第三步：调用 challenger

判定为复杂场景后，**自动调用 `challenger` skill** 进行二次质疑审查：

```
use_skill("challenger")
```

调用时将本次修改的变更内容作为上下文传入，challenger 会根据变更类型（Bug 修复/新增功能/优化）选择对应质疑策略进行深度审查。

## 例外

以下情况跳过整条流水线：
- 用户明确说"不用审查"、"跳过审查"、"skip review"
- 单字符/标点修改

以下情况跳过 challenger（但不跳过 auto-review）：
- 用户明确说"不用质疑"、"跳过 challenger"
- 修改明确属于非复杂场景（见上表）

---
---
# snippet-memory 调用时机

## 何时加载 `snippet-memory` skill

### 必须加载的场景

| 场景 | 触发信号 | 说明 |
|------|----------|------|
| 编码前查询 | AI 准备写代码 | 先查是否有可复用的工具函数或已知流程 |
| 用户问"有没有现成的" | "有没有XX工具"、"XX怎么实现的" | 从通用记忆片段中快速定位 |
| 构建记忆 | "根据这些代码构建记忆"、"把XX记录下来" | 批量或单个录入代码要点 |
| 阅读代码发现要点 | AI 读代码时遇到通用工具/关键流程/重要模式 | 自动记录到对应分类 |

### 不加载的场景（走其他 skill）

| 场景 | 走哪个 | 原因 |
|------|--------|------|
| 模块架构、API设计 | `codekb-skill` | 架构级知识 |
| 项目背景、进度、偏好 | `memory-skill` | 项目上下文 |
| 定位具体文件/符号 | 直接用 grep/SearchSymbol | 定位级查询 |

### 一句话判断

> 问自己：这段信息是"一句话就能说清楚的代码要点（函数/流程/模式）"还是"需要段落描述的架构知识"？
> 前者 → `snippet-memory`，后者 → `codekb-skill`。

---

# url-view-resolver Skill 使用场景

当用户提供了一个 API URL 路径，需要定位该 URL 对应的 Django 视图、处理逻辑或 Resource 类时，使用 `url-view-resolver` skill。

## 使用命令

```bash
/root/bk-monitor/bkmonitor/.venv/bin/python /root/bk-monitor/django-url-view-resolver.py "<目标URL>" "<HTTP方法>"
```

## 使用流程

1. 运行脚本，获取 URL 对应的视图和 Resource 类
2. 从输出中提取「Resource 限定名」（如 `PreviewDutyRulePlanResource`）
3. 搜索该类名，定位到源码文件
4. 阅读 `perform_request` 方法，理解业务逻辑

## 适用场景

- 用户提供了一个 API URL，想知道对应的处理代码
- 需要定位某个接口的 Resource 类以分析业务逻辑
- 排查接口问题时，需要确认请求最终由哪个类处理

## 不适用场景

- 已知 Resource 类名，只需查看其实现 → 直接 grep 搜索类名
- 需要了解 `resource.xxx.yyy` 格式的路径引用 → 使用 `resource-locator` skill

---

# resource-locator Skill 使用场景

当用户在代码中遇到 `resource.xxx.yyy` 或 `api.xxx.yyy` 格式的路径引用，需要定位其对应的 Python Resource 类源码时，使用 `resource-locator` skill。

## 核心转换规则

1. 提取路径最后一段（snake_case 格式）
2. 转换为 PascalCase
3. 添加 `Resource` 后缀

## 转换示例

| 路径引用 | 提取 | PascalCase | 最终类名 |
|----------|------|------------|----------|
| `resource.alert.list_alert_log` | `list_alert_log` | `ListAlertLog` | `ListAlertLogResource` |
| `api.metadata.get_label` | `get_label` | `GetLabel` | `GetLabelResource` |

## 定位流程

1. 转换类名（snake_case → PascalCase + Resource）
2. 全局搜索类定义
    - `resource.` 前缀 → 整个代码库 `bkmonitor/`
    - `api.` 前缀 → `bkmonitor/api/` 目录
3. 查看类实现，阅读 `perform_request` 方法

## 适用场景

- 代码中出现了 `resource.alert.list_alert_log` 这类引用，想知道具体实现
- 需要查看 `api.metadata.get_label` 对应的接口处理类
- 搜索代码定位 Resource 类定义和 `perform_request` 方法

## 注意事项

当用户提供了一个 HTTP URL 路径时，应该优先使用 `url-view-resolver`，而非 `resource-locator`。

