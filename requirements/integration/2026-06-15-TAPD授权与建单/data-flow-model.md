# TAPD 授权与建单 — 数据模型与数据流

> 基于 `requirement.md` 生成，聚焦授权部分的数据建模。

---

## 1. 场景类型

**简单 CRUD** — 单条写入/更新，无并发冲突，单机部署，数据量级低。满足快速通道条件。

---

## 2. 核心实体

| 实体 | 说明 | 来源 | 存储 |
|------|------|------|------|
| **TAPD 项目关联** | space_id 与 tapd_workspace_id 的多对多映射，一次关联全空间共享 | 需求 D-01 | MySQL |
| **用户 TAPD Token** | 用户维度的 TAPD OAuth access_token 存储 | 需求 D-02 | MySQL |

**外部实体（非持久化，参与数据流）**：

| 外部实体 | 说明 |
|----------|------|
| TAPD OAuth 服务 | 用户态/应用态授权、code 换 token |
| TAPD 业务 API | 获取用户项目列表 |
| 前端页面 | 重定向目标 |

---

## 3. ER 图

```mermaid
erDiagram
    AbstractRecordModel ||--o{ TAPD_WORKSPACE_BINDING : "继承"
    AbstractRecordModel ||--o{ USER_TAPD_TOKEN : "继承"

    AbstractRecordModel {
        int id PK
        boolean is_enabled "是否启用，默认true"
        boolean is_deleted "是否删除，默认false"
        varchar create_user "创建人(32)，默认''"
        datetime create_time "创建时间，auto_now_add"
        varchar update_user "最后修改人(32)，默认''"
        datetime update_time "最后修改时间，auto_now"
    }

    TAPD_WORKSPACE_BINDING {
        int space_id "蓝鲸业务空间ID，必填"
        int bk_biz_id "蓝鲸CMDB业务ID，必填"
        varchar tapd_workspace_id "TAPD项目ID(64)，必填"
        varchar tapd_workspace_name "TAPD项目名称(255)，必填"
        # create_user 由 AbstractRecordModel 自动提供，无需声明
    }

    USER_TAPD_TOKEN {
        varchar username "用户username(128)，必填，唯一"
        varchar access_token "TAPD用户态token(512，加密存储)，必填"
        varchar refresh_token "TAPD刷新token(512，加密存储)，可选"
        varchar token_type "token类型(32)，默认Bearer，必填"
        datetime expires_at "过期时间，必填"
        datetime refresh_time "上次刷新时间，可选"
    }
```

> **说明**：两个模型均继承自 `AbstractRecordModel`（定义于 `bkmonitor/utils/model_manager.py`），自动拥有 `id`、`is_enabled`、`is_deleted`、`create_user`、`create_time`、`update_user`、`update_time` 六个标准审计字段。

### 字段清单

#### AbstractRecordModel 基础字段（自动继承）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | int | PK, 自增 | 主键 |
| `is_enabled` | boolean | 默认 `true` | 是否启用 |
| `is_deleted` | boolean | 默认 `false` | 是否删除（软删标记） |
| `create_user` | varchar(32) | 默认 `''` | 创建人 username，由 `save()` 自动填充当前用户 |
| `create_time` | datetime | auto_now_add | 创建时间 |
| `update_user` | varchar(32) | 默认 `''` | 最后修改人，由 `save()` 自动填充当前用户 |
| `update_time` | datetime | auto_now | 最后修改时间 |

> 继承来源：`bkmonitor/utils/model_manager.py` → `class AbstractRecordModel(models.Model)`  
> 配套 Manager：`RecordModelManager`，默认过滤 `is_deleted=True` 的记录；原始查询器为 `origin_objects`

#### TapdWorkspaceBinding（新增表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `space_id` | int | 必填 | 蓝鲸业务空间 ID |
| `bk_biz_id` | int | 必填 | 蓝鲸 CMDB 业务 ID |
| `tapd_workspace_id` | varchar(64) | 必填 | TAPD 项目 ID |
| `tapd_workspace_name` | varchar(255) | 必填 | TAPD 项目名称 |
| `create_user` | varchar(32) | 默认 `''` | 发起关联的用户（AbstractRecordModel 自动审计） |
| `(space_id, tapd_workspace_id)` | - | **唯一约束** | 保证关联幂等 |

> **代码位置**：`bkmonitor/bkmonitor/models/tapd.py` → `class TapdWorkspaceBinding(AbstractRecordModel)`  
> **导出声明**：`__all__` 列表包含该模型，并在 `bkmonitor/bkmonitor/models/__init__.py` 中统一导入

#### UserTapdToken（新增表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `username` | varchar(128) | 必填, **唯一** | 一个用户一条 token 记录 |
| `access_token` | TextField | 必填 | TAPD 用户态 access_token，**加密存储** |
| `refresh_token` | TextField | null=True, blank=True | TAPD 刷新 token，**加密存储** |
| `token_type` | varchar(32) | 默认 `Bearer` | Token 类型 |
| `expires_at` | datetime | 必填 | access_token 过期时间 |
| `refresh_time` | datetime | null=True, blank=True | 最近一次刷新成功时间，防重复刷新专用 |

> **代码位置**：`bkmonitor/bkmonitor/models/tapd.py` → `class UserTapdToken(AbstractRecordModel)`  
> **导出声明**：`__all__` 列表包含该模型，并在 `bkmonitor/bkmonitor/models/__init__.py` 中统一导入

### 设计说明

- **TAPD_WORKSPACE_BINDING**：唯一约束 `(space_id, tapd_workspace_id)` 实现关联幂等，重复授权无副作用
- **USER_TAPD_TOKEN**：`username` 唯一，同一用户重复授权时更新 token（upsert），不新增记录
- **refresh_token**：TAPD 可能不返回 refresh_token（取决于应用配置），字段可选
- **异步刷新策略**：用户访问时触发检查，token 即将过期（剩余 <= 30 分钟）且距上次刷新 >= 5 分钟时，后台异步刷新
- **防重复刷新**：通过 `refresh_time` 字段判断，刷新间隔不低于 5 分钟（`now() - refresh_time >= 5min`）
- **刷新失败处理**：保留原 token 不清除，返回当前 token 仍可使用

### 安全策略

| 项目 | 策略 | 说明 |
|------|------|------|
| `access_token` 存储 | **加密存储** | 使用 Django `cryptography` 库（Fernet 对称加密）或 bkmonitor 现有加密工具，写入时加密、读取时解密 |
| 数据库访问控制 | 最小权限原则 | 仅 bkmonitor_saas 应用账号可访问 `USER_TAPD_TOKEN` 表 |
| 日志脱敏 | `access_token` 禁止明文落日志 | 日志中仅记录 token 前 8 位 + `***` |

### Token 存储方案评估：MySQL 单层高可用策略

> ⚠️ **注意**：以下 Redis 方案为**二期规划**，设计阶段已明确决策「一期仅使用 MySQL，不引入 Redis」。以下评估表保留作为二期参考。

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| **仅 MySQL** | 持久化可靠、事务保证、已有基础设施 | 每次读取需解密、高并发时 DB 压力 | 一期（数据量低、并发低） |
| **仅 Redis** | 读写快、天然支持 TTL 过期 | 重启丢失、需额外持久化方案 | 不推荐（token 需持久化） |
| **MySQL + Redis** | 兼顾持久化与性能、Redis TTL 自动过期 | 架构复杂度增加、需维护一致性 | 二期（高并发时） |

**推荐方案**：一期仅用 MySQL，二期按需引入 Redis 缓存层。

**二期 Redis 缓存策略**：
- **写入**：授权成功后，同时写 MySQL（加密）+ Redis（明文，TTL = token 剩余有效期）
- **读取**：优先读 Redis，未命中则读 MySQL 解密后回填 Redis
- **过期**：Redis TTL 自动淘汰，MySQL 定期清理过期记录
- **一致性**：用户重新授权时，同时更新 MySQL + Redis

### 接口鉴权方案

**说明**：`TAPD_REQUIRED` Permission 为 DRF `BasePermission` 子类，挂载在 `TapdViewSet` 上。请求到达时统一校验用户 `USER_TAPD_TOKEN` 的有效性；无效时抛出 `PermissionDenied(detail={"auth_url": "..."})`，DRF 返回 403 携参，前端拦截后跳转 TAPD 授权页面。Token 校验**不再单独作为接口**，由 Permission 层在请求入口处统一拦截。

| 接口 | 鉴权方式 | 说明 |
|------|----------|------|
| B-01 查询用户 TAPD 项目列表 | **TAPD_REQUIRED + IAM** | `TAPD_REQUIRED` 确保用户已授权 TAPD；`IAM` 校验当前 space 操作权限 |
| B-03 应用态授权回调 | **TAPD 回调签名校验** | 由 TAPD 侧回调，校验请求来源合法性（签名/白名单 IP） |
| B-05 用户态授权回调 | **TAPD 回调** | 由 TAPD 302 重定向回来，携带 code |

---

## 4. 数据流图

### 4.1 用户态授权流程（Token 获取）

```mermaid
flowchart TD
    subgraph 被动授权触发
        A["用户调用业务接口<br/>如 S-04 B-01 查询 TAPD 项目列表"] --> B{"S-06 TAPD_REQUIRED<br/>Permission 拦截"}
        B -->|Token 有效| C[正常执行业务逻辑]
        B -->|Token 不存在 / 已过期| D["PermissionDenied 403<br/>detail.auth_url = generate_auth_url(bk_biz_id)"]
        D --> E[前端拦截 403 提取 auth_url]
    end
    E --> F[前端跳转 TAPD OAuth 授权页]
    F --> G[用户确认授权]
    G --> H["B-05 用户态授权回调<br/>(code, state, resource)"]
    H --> I{B-05.1 验证 state + code 换 token}
    I -->|成功| J[加密 access_token]
    J --> K[upsert USER_TAPD_TOKEN]
    K --> L["302 重定向前端页面<br/>URL参数: ?auth=success"]
    I -->|TAPD API 异常| M[记录错误日志]
    M --> N["302 重定向前端错误页<br/>URL参数: ?auth=error"]
```

**涉及实体**：`USER_TAPD_TOKEN`（写入）

**异常处理**：
- code 无效/过期：返回前端提示「授权失败，请重试」
- TAPD API 不可用：记录错误日志，返回前端提示「服务暂时不可用，请稍后重试」
- 数据库写入失败：事务回滚，返回前端错误提示

### 4.2 应用态授权流程（项目关联）

```mermaid
flowchart TD
    A[TAPD 应用安装] --> B[B-03 应用态授权回调]
    B --> C{校验回调来源合法性}
    C -->|合法| D{业务ID 有效?}
    C -->|非法| ERR1[记录错误日志] --> REDIR_ERR[302 重定向错误页]
    D -->|有效| E[提取 workspace_id / workspace_name]
    D -->|无效| ERR2[记录错误日志] --> REDIR_ERR
    E --> F[upsert TAPD_WORKSPACE_BINDING]
    F -->|成功| G[302 重定向前端页面]
    G --> H["URL 参数携带 ?tapd_bind=success"]
    F -->|DB 写入失败| ERR3[记录错误日志] --> REDIR_ERR
```

**涉及实体**：`TAPD_WORKSPACE_BINDING`（写入）

**异常处理**：
- 业务 ID 无效：302 重定向到前端，URL 带 `?tapd_bind=error&reason=invalid_biz_id`
- 重复回调（幂等）：唯一约束保证 upsert 无副作用，正常返回成功
- 前端状态感知：重定向 URL 携带 `?tapd_bind=success`，前端检测该参数后刷新关联列表

### 4.3 查询用户 TAPD 项目列表

```mermaid
flowchart TD
    A["前端「选择TAPD项目」或「查看已关联项目」"] --> A1["TAPD_REQUIRED Permission 拦截"]
    A1 --> A2{检查 USER_TAPD_TOKEN}
    A2 -->|无记录或已过期| A3["PermissionDenied 403<br/>附带 auth_url<br/>前端跳转授权"]
    A2 -->|有效| B["B-01 查询用户TAPD项目列表接口<br/>(分页, page_size=20)"]
    B --> C[解密 access_token]
    C --> D["调用 TAPD API 获取项目列表"]
    D -->|API 成功| E[按 space_id 查 TAPD_WORKSPACE_BINDING]
    E --> F["合并标记: is_bound=true/false"]
    F --> G[返回带关联状态的项目列表 + install_url]
    D -->|API 权限不足| H["返回「无TAPD项目权限」<br/>前端提示联系管理员"]
    D -->|API 服务异常| I["返回「TAPD服务暂时不可用」<br/>前端提示稍后重试"]
```

**涉及实体**：`USER_TAPD_TOKEN`（读取）、`TAPD_WORKSPACE_BINDING`（读取，比对标记已关联状态）

**异常处理**：
- Token 不存在 / 已过期：`TAPD_REQUIRED` Permission 拦截 → `PermissionDenied(403)` → 前端跳转授权
- TAPD API 超时 / 异常：返回友好错误码，不影响已关联项目展示
- 用户无 TAPD 项目：返回空列表，前端展示「暂无项目」

**说明**：
- `TAPD_REQUIRED` 为 DRF Permission，挂载在 `TapdViewSet` 上，所有请求自动校验
- 查询结果中每个项目携带 `is_bound` 标记，前端不再单独调用「查询已关联项目」接口

### 4.4 异步刷新 Token

```mermaid
flowchart TD
    A["用户访问接口<br/>（如查询项目列表）"] --> B[读取 USER_TAPD_TOKEN]
    B --> C{检查 token 是否即将过期}
    C -->|"未过期且剩余 > 30分钟"| D[正常使用]
    C -->|"即将过期（剩余 <= 30分钟）"| E{检查 refresh_token}
    E -->|无 refresh_token| F[返回 token 即将过期提示]
    E -->|有 refresh_token| G{检查 update_time}
    G -->|"距上次刷新 < 5分钟"| H[跳过刷新，继续使用当前 token]
    G -->|"距上次刷新 >= 5分钟"| I["异步调用 TAPD refresh_token 接口<br/>Basic Auth: client_id:client_secret"]
    I -->|成功| J[加密新 access_token + refresh_token]
    J --> K["更新 USER_TAPD_TOKEN<br/>覆盖 access_token, refresh_token, expires_at"]
    I -->|失败| L[记录错误日志]
    L --> M["保留原 token，返回当前 token 仍可使用"]
```

**涉及实体**：`USER_TAPD_TOKEN`（读取 + 更新）

**触发条件**：
- **用户访问时触发**：用户调用需要 TAPD 权限的接口时（如查询项目列表）
- **Token 即将过期**：`expires_at - now() < 30 分钟`（提前刷新，避免用户感知中断）
- **异步执行**：刷新操作在后台异步执行，不阻塞用户请求

**防重复刷新策略**：
- 检查 `refresh_time` 字段（仅刷新成功时更新此字段，与 `update_time` 解耦）
- 刷新间隔不低于 5 分钟（`now() - refresh_time >= 5min`）
- 使用数据库行锁（`SELECT ... FOR UPDATE`）防止并发刷新

**异常处理**：
- TAPD API 失败：记录错误日志，**保留原 token**，返回当前 token 仍可使用
- refresh_token 无效：记录错误日志，保留原 token（可能是临时问题）
- 数据库更新失败：事务回滚，不影响用户当前请求
- 多次重试失败：token 最终过期后，用户需重新授权

### 数据流总览

```mermaid
flowchart LR
    subgraph 前端
        FE[前端页面]
    end
    subgraph bkmonitor_saas
        SAAS[Django]
    end
    subgraph TAPD
        OAUTH[TAPD OAuth]
        API[TAPD 业务 API]
    end
    subgraph MySQL
        DB1[TAPD_WORKSPACE_BINDING]
        DB2[USER_TAPD_TOKEN]
    end
    FE <-->|API / JSON| SAAS
    SAAS <-->|API / JSON| OAUTH
    SAAS -->|API| API
    SAAS --> DB1
    SAAS --> DB2
```

---

## 5. 数据流汇总

| 流程 | 触发 | 读 | 写 | 外部依赖 | 异常处理 |
|------|------|----|----|----------|----------|
| 用户态授权 | 用户点击授权按钮 | - | `USER_TAPD_TOKEN` | TAPD OAuth | code 无效/token 换失败/DB 写入失败 |
| 应用态授权 | TAPD 回调 | - | `TAPD_WORKSPACE_BINDING` | TAPD 回调 | 业务 ID 无效/重复回调/DB 写入失败 |
| 查询用户 TAPD 项目 | 前端选择 / 查看项目 | `USER_TAPD_TOKEN` + `TAPD_WORKSPACE_BINDING` | - | TAPD 业务 API | Permission 拦截(未授权) / TAPD API 不可用 / 空列表 |
| 异步刷新 Token | 用户访问时触发 | `USER_TAPD_TOKEN` | `USER_TAPD_TOKEN` | TAPD refresh_token 接口 | 无 refresh_token/刷新失败/重复刷新 |

---

## 6. 关键设计决策

1. **存储选型**：MySQL（关系简单、数据量低、需事务保证）
2. **模型基类**：统一继承 `AbstractRecordModel`（`bkmonitor/utils/model_manager.py`），复用内部约定的审计字段与软删逻辑，避免手写重复字段（参考 `UserGroup` 等现有模型的做法）
3. **幂等策略**：唯一约束 + upsert（MySQL `INSERT ... ON DUPLICATE KEY UPDATE`）
4. **Token 管理**：存储 `refresh_token`（TAPD 可能不返回，字段可选），支持异步刷新
5. **防重复刷新**：刷新成功时更新 `refresh_time`；通过判断 `now() - refresh_time >= 5min` 防止并发重复刷新（`refresh_time` 与 `update_time` 分离，避免非刷新操作的审计更新导致误判）
6. **刷新失败处理**：保留原 token 不删除，用户请求不受影响，token 最终过期后再引导重新授权

---

## 7. 待确认项

| # | 内容 | 阶段 | 来源 |
|---|------|------|------|
| 1 | B-03 回调中业务 ID 如何映射到 `space_id` + `bk_biz_id`（查 CMDB？查业务接口？） | 设计 | 初始 |
| 2 | 建单阶段是否需要在 `IssueDocument` 扩展 TAPD 单据关联字段 | 建单需求 | 初始 |
| 3 | `access_token` 加密方案选型：Fernet vs bkmonitor 现有加密工具 | 设计 | 质疑审查 |
| 4 | B-03 回调校验方案：签名校验 vs 白名单 IP | 设计 | 质疑审查 |
| 5 | TAPD 应用是否配置了 refresh_token 权限（决定是否返回 refresh_token） | 设计 | demo 参考 |
| 6 | 异步刷新任务的执行频率和提前量（当前：5分钟检查，提前30分钟刷新） | 设计 | demo 参考 |
