# AGENTS.md - AI AGENT 项目记忆文件

> **本文件由 AI AGENT 自动维护，用于缓存索引信息、记录近期工作、跟踪新需求。**
> 项目: bk-monitor
> 最后自动更新: 2026-06-25

---

## 知识库索引

### Scope 列表
- `monitor`: BK-Monitor Wiki 文档知识库（26 索引，热区 8 / 常温 13 / 冷区 5）
- `monitor-memory`: BK-Monitor 项目记忆（**30 索引**，热区 10 / 常温 16 / 冷区 4）
- `user-profile`: 用户画像（6 索引，热区 2 / 常温 3 / 冷区 1）

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
├── 批量操作框架
├── 空间租户业务ID转换 [📥 热门]
├── 外部API调用模式
├── 内部API暴露模式
├── Resource框架自动发现与使用
├── Django配置加载体系 [📥 热门]
├── Monitor API资源自动暴露到OpenAI
├── 内核API内部Resource复用模式
└── 前端接口与网关接口差异
Resource 框架/ [常温]
API 集成模式/ [常温]
系统配置与异常/ [常温]
开发工具/ [常温]
团队约定/ [常温]
项目历史/ [常温]
当前状态/ [常温]
外部依赖/ [常温]
最近需求/ [常温]
进度/ [常温]
项目踩坑点/ [常温]
项目架构/ [常温]
工具库/ [热]
│   ├── Redis 缓存与分布式锁 [📥 热门]
│   ├── 哈希与一致性哈希 [📥 热门]
│   ├── 时间日期处理工具 [📥 热门]
│   ├── 组件连接工具 [📥 热门]
│   ├── 并发批量与分页 [📥 热门]
│   ├── 加密与Token生成 [📥 热门]
│   ├── 业务空间与租户 [📥 热门]
│   ├── K8S与元数据同步工具 [📥 热门]
│   └── 请求上下文与环境变量 [📥 热门]
常用命令/ [冷]
部署运维/ [冷]
```

#### 热门 Relation
- **背景与目标 → 仓库结构**（score: 0.2）— `bk-monitor-wiki` 独立仓库，不与主工程 `bkmonitor` 共用 Git
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
代码风格/ [常温]
技术背景/ [冷]
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
- **[2026-06-25]** B-01 POST 改造与 signed_state 自包含机制重构：`ListUserTapdWorkspaceResource` 从 GET 改为 POST，body 传递 `bk_biz_id` + `redirect_uri_real` + `redirect_uri_verify`；`generate_auth_url` 改用自包含 signed_state（含 username/tenant_id/exp/redirect_uri）用于 B-05 OAuth 回调，彻底移除 Session 依赖；同步修复 `DEFAULT_TENANT_ID` 硬编码为 `space_uid_to_bk_tenant_id`，修复 `request.user.username` 为 `get_request_username()`
- **[2026-06-24]** 实现 B-04 解绑接口 `UnbindTapdWorkspaceResource`（`POST /fta/issue/tapd/workspace/unbind/`），仅删除本地 `TapdWorkspaceBinding`，补充 API 设计文档 `07-unbind-workspace.md`，更新 `00-api-overview.md` 总览索引
- **[2026-06-24]** 创建 `api-tester` skill（`bk-monitor-wiki/skills/api-tester/`）：在 Django 进程内直调 Resource 类实现自动化接口测试，支持 inspect/dry-run/run 三模式，自动提取 RequestSerializer 参数 schema 与示例
- **[2026-06-24]** 将 `bk_agent_base/metadata/utils`（34 个文件）按分类录入 monitor-memory 工具库：Redis 缓存与分布式锁 / 哈希与一致性哈希 / 时间处理 / 组件连接（Consul/ES） / 并发批量 / 加密 / 空间租户 / K8S元数据同步 / 请求上下文 共 9 条 Relation，均含文件路径、类名、关键方法签名，支持后续代码快速定位
- **[2026-06-23]** TAPD 授权与建单：`api/` 目录 7 个 API 设计文档定稿，`frontend-guide/` 4 个前端集成文档定稿，修复 `auth_method`/`has_more` 删除、`importable` 自动关联、Mermaid 语法等 15 处问题

### 进度
- 进行中: [2026-06-25] 🔄 B-01 POST 改造与 signed_state 自包含机制编码已完成，待修复 Review 问题（`utils/tapd.py` 缺失 `import time`(P0)、`initiator` 建议统一为 `username`(P1)）
- 已完成: [2026-06-25] ✅ B-01 POST 改造 Code Review 完成：确认 redirect_uri 透传逻辑一致、租户/用户名硬编码修复无遗漏，发现 1 P0 + 1 P1
- 已完成: [2026-06-24] ✅ B-04 UnbindTapdWorkspaceResource 实现（`POST /fta/issue/tapd/workspace/unbind/`）+ API 文档 `07-unbind-workspace.md`
- 已完成: [2026-06-24] ✅ `00-api-overview.md` 索引表更新，标记 B-04 为新增接口
- 已完成: [2026-06-24] ✅ `api-tester` skill 交付：`SKILL.md` + `reference.md` + `scripts/api_tester.py`，复用 `url-view-resolver` 的 resolve 机制定位 Resource 类，用 `get_serializer_fields()` 提取参数 schema，`Resource.request()` 直调执行；非 GET 需 `--confirm` 护栏；已通过 inspect 模式实测验证
- 已完成: [2026-06-24] ✅ 补全 monitor-memory 和 user-profile 缺失的 Group 索引（monitor-memory +11, user-profile +2）

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

# url-view-resolver Skill 使用场景

当用户提供了一个 API URL 路径，需要定位该 URL 对应的 Django 视图、处理逻辑或 Resource 类时，使用 `url-view-resolver` skill。

---

# resource-locator Skill 使用场景

当用户在代码中遇到 `resource.xxx.yyy` 或 `api.xxx.yyy` 格式的路径引用，需要定位其对应的 Python Resource 类源码时，使用 `resource-locator` skill。

---
当用户提出一个建议、想法或修改要求时，如果该建议：
- 看起来不合理、存疑
- 或改动范围较大、影响面广
- 或与已有设计/约定可能冲突

**必须先调用 `request-guard` skill 进行质疑检查**，判断其合理性后再决定是否执行修改，不能盲从用户的突发奇想直接动手。

---

# 项目百科全书（`${scope}-memory`）

> **`${scope}-memory` = AI 的项目百科全书。不懂就查，有新发现就写入，维护好它持续提效。**

---

## 1. 判断：该走哪条路

| 信息类型 | 走哪个 | 说明 |
|----------|--------|------|
| 代码要点（函数/流程/工具/模式） | `snippet-memory` → `ki_sync_relation` | 一句话说得清的关键代码信息 |
| 模块架构、API 设计 | `codekb-skill` | 需要段落描述的架构知识 |
| 项目背景、进度、偏好 | `memory-skill` | 项目上下文级信息 |
| 找具体文件/符号 | grep / SearchSymbol | 直接定位，不绕路 |

---

## 2. 写入：该记什么、怎么归类

### 强制要求

**禁止纯文字总结。** 必须包含：

| 必须 | 示例 |
|------|------|
| 文件路径 | `src/utils/hash-ring.ts` |
| 类名/方法名 | `HashRing.getNode(key)` |

> ❌ 废话：*"提供一致性哈希环，支持虚拟节点和二分查找"*
> ✅ 可用：*`src/utils/hash-ring.ts` — `HashRing` 类：`getNode(key: string)` 二分定位、`addNode(addr, weight)` 配权重*

### 归类原则

**禁止全部扔进"通用记忆片段"。** 思考最适合的 Group → 没有则新建 → 实在不行才兜底。

| 内容 | 优先归到 |
|------|----------|
| 工具函数/脚本 | `工具库` |
| 踩坑/注意事项 | `项目踩坑点` |
| 构建/调试命令 | `常用命令` |
| 部署/环境 | `部署运维` |
| 需求记录 | `最近需求` |
| 完成状态 | `进度` |
| 实在无法归类 | `通用记忆片段`（仅兜底） |

```bash
# 通用写入模板（scope 始终用 ${scope}-memory）
ki sync-relation --scope ${scope}-memory --group "目标Group" \
  --relation "标题（需求加日期前缀 [YYYY-MM-DD]）" \
  --module-info "内容（必须含文件路径+类/方法名）" \
  --keywords "关键词1,关键词2"
```

> 需求写入 `最近需求`，进度写入 `进度`。写完记得同步 AGENTS.md（追加 + 删超过 7 天的）。

---

## 3. 查询：疑问排查优先级

| 优先 | 动作 | 命令 |
|------|------|------|
| 1 | 查项目记忆 | `ki_query_group` scope=`${scope}-memory` |
| 2 | 查知识库记忆 | `ki_query_group` scope=`${scope}` |
| 3 | 代码搜索 | grep / SearchSymbol |
| 4 | 语义兜底 | `ki_search` |

---

## 4. 收尾：会话转折点主动执行

**触发信号**：用户说"好/OK/可以"、"记录一下"、"开始写代码"、"下一个"。

```
□ 有新需求？→ ki_sync_relation → 最近需求 + 同步 AGENTS.md
□ 有代码要点？→ ki_sync_relation → 对应 Group
□ 进度变了？→ ki_sync_relation → 进度
□ 索引变了？→ agents-md-init 更新
□ 7 天前的？→ 触发归档
```

---

## 5. 禁忌

| # | 红线 |
|---|------|
| 🔴 | 将代码/架构知识存入平台记忆 → **走 ki** |
| 🔴 | 将通用偏好存入 ki → **走平台记忆** |
| 🔴 | 跳过 ki-foundation 直接用 codekb/memory-skill |
| 🔴 | scope 未确认就执行 ki 命令 |
| 🔴 | 对 ki scope 用 memory MCP（禁止 `memory_store`/`memory_recall` 等） |
| 🔴 | 忽略 AGENTS.md：对话开始必须检查缓存，索引变更必须同步 |
| 🔴 | 等用户提醒才记录：AI 必须**主动识别**并写入 |

---
# 记忆存储位置决策

简洁 + 通用 + 跨项目 + 每次对话都需要 → 平台内置记忆（`update_memory`）
其他一切 → ki 记忆，按内容类型分流：

- 代码要点（函数/流程/模式） → `snippet-memory`
- 模块架构、API 设计 → `codekb-skill`
- 项目背景、进度、偏好 → `memory-skill`

> 详细路由判断见 `project-encyclopedia.md`

- 内置示例："用中文回复"、"不要擅自提交代码"
- ki 示例：工具函数用法、架构决策、踩坑经验、需求记录

禁忌：详细知识禁存内置，简洁偏好禁存 ki。

