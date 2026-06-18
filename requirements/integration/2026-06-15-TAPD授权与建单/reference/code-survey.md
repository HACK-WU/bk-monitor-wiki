# 代码调研：TAPD 授权与建单（REQ-20260615-001）

> 调研来源：记忆系统 ✗ | 知识库 ✗ | 已有文档 ✓ | 代码搜索 ✗（见说明）
> 调研范围：代码路径、架构模式、数据存储、错误处理、安全惯例、API 约定、配置管理

> **重要说明**：当前工作区（`bk-monitor-wiki`）为 **纯文档/知识库型仓库**，不包含 Django 项目源码。设计文档中引用的 `bkmonitor/utils/cipher.py`、`fta_web/issue/resources.py`、`bkmonitor/api/tapd/default.py` 等路径 **不在本仓库中**。本调研基于设计文档、依赖文档和评审报告中的代码引用信息整理，实际开发时需到源码仓库中对照验证。

---

## 1. 相关代码路径

> 以下代码路径来自设计文档 `DESIGN.md` 及子文档中的引用，实际存在于蓝鲸监控主代码仓库中（非本 wiki 仓库）。

| 路径 | 定义/用途 | 在本需求中的角色 |
|------|----------|-----------------|
| `bkmonitor/utils/cipher.py` | `AESCipher` 对称加密类 | **复用**。用户态 token 加密存储（不传固定 IV） |
| `bkmonitor/utils/cipher.py:77/87` | `AESCipher.__init__()` / `encrypt()` | IV 自动生成并前置到密文的实现位置 |
| `bkmonitor/api/tapd/default.py` | `TapdAPIResource` 基类 | **复用**。app 级 Basic Auth，已有 `get_workspace_info`、`get_granted_workspaces`、建单资源 |
| `fta_web/issue/resources.py` | 告警 Issue 相关 Resource | **承载模块**。B-01/B-03/B-07 全部放在此模块下 |
| `fta_web/issue/resources.py:1302` | `ListTapdWorkspaceResource`（现网已有） | **改名拆分**。现为 `ListUserVisibleTapdWorkspaceResource`（Bearer）+ `ListGrantedTapdWorkspaceResource`（Basic） |
| `fta_web/issue/models.py` | 告警 Issue Models（Django ORM） | **新增 `TAPDWorkspaceBinding`**，与现有模型同文件 |
| `fta_web/issue/serializers.py` | DRF Serializer | **新增** `TapdWorkspaceBindingSerializer`、`ListTapdWorkspaceQuerySerializer`、`InstallUrlRequestSerializer` |
| `fta_web/issue/urls.py` | URL 路由配置 | **新增** B-01/B-03/B-07 三个路由 |
| `fta_web/issue/authentication.py` 或 `iam/` | IAM 权限/认证 | `RbacResource`、`IAMBaseAuthentication`、`IAMPermission` 等（设计假定已存在） |
| `bkmonitor/utils/cache.py` 或同类 | `BKMRedisAgent` / Redis 客户端 | **复用**。Token 存取、临时 state 存取 |
| `bkmonitor/exceptions.py` | `ApiException`、`ApiExceptionCode` | **复用**。异常抛出和错误码枚举 |

---

## 2. 架构概览

> 调研来源：已有文档（设计文档）

### 项目架构
- **框架**：Django + Django REST Framework（DRF）或 BlueKing 自定义 Resource 框架
- **模块组织**：`fta_web/issue/` 承载告警 + Issue 功能，本需求全部放在该模块下（评审结论 N1：不新建 `fta_web/tapd/`）
- **API 层**：`Resource` 类模式（非标准 DRF ViewSet），通过 `ResourceRoute` 注册路由
- **数据层**：Django ORM + MySQL；Redis 用于缓存和临时 Token 存储
- **外部 API**：`bkmonitor/api/` 目录下统一封装第三方 API（如 `api/tapd/default.py`）

### 模块关系
```
fta_web/issue/
├── models.py          # 新增 TAPDWorkspaceBinding（与现有 Issue 模型同文件）
├── resources.py       # 新增 B-01/B-03/B-07 Resource 类 + 四态查询逻辑
├── serializers.py     # 新增序列化器
├── urls.py            # 新增路由注册
└── [现有文件]          # RegisterUserResource 等（workspace_id 边界检查逻辑可参考）

bkmonitor/
├── utils/cipher.py    # AESCipher（Token 加密）
├── api/tapd/default.py # TapdAPIResource（app 级 Basic Auth，复用）
├── exceptions.py      # ApiException / ApiExceptionCode（复用）
└── utils/cache.py     # BKMRedisAgent / Redis 封装（复用）
```

---

## 3. 可参考的类似功能

> 调研来源：已有文档（设计文档引用）

### 3.1 `RegisterUserResource` —— workspace_id 边界校验
- **参考价值**：现有的 `workspace_id` 使用限制（硬编码 `if workspace_id > 100` 抛权限异常）体现了本系统对 **多租户 workspace 的边界管控**
- **对本需求的启示**：`TAPDWorkspaceBinding.space_uid` 作为全局唯一键，`space_id` 可能非全局唯一，设计已采纳此约束（评审结论 B1）

### 3.2 `ListTapdWorkspaceResource`（`fta_web/issue/resources.py:1302`）—— 用户态项目列表
- **参考价值**：现网已有通过 Bearer Token 获取用户 TAPD 可见项目的实现
- **对本需求的启示**：
  - 需**改名区分**为 `ListUserVisibleTapdWorkspaceResource`（Bearer，调用 TAPD OAuth 接口）
  - 新增 `ListGrantedTapdWorkspaceResource`（Basic Auth，调用 `get_granted_workspaces`）

### 3.3 `TapdAPIResource`（`bkmonitor/api/tapd/default.py`）—— app 级 Basic Auth 客户端
- **参考价值**：硬编码 `client_id:client_secret` 的 Basic Auth，已封装 `get_workspace_info`、`get_granted_workspaces`
- **对本需求的启示**：回调流程（B-03）直接复用此客户端获取 workspace 信息，不走用户态 Bearer（评审结论 A3）

---

## 4. 技术栈约束

> 调研来源：已有文档（`dependencies/dependencies.md`）

| 组件 | 版本/说明 | 约束 |
|------|----------|------|
| TAPD API | v2 (`apiv2.tapd.woa.com`) | 全响应含外层 `status/data/info`，需防御性解析 |
| TAPD OAuth | 自定义 OAuth（非标准 RFC 6749） | `request_token` 路径非标准 `/token`；code 有效期 5 分钟 |
| Django | 项目已使用 | ORM、settings、管理命令等遵循 Django 惯例 |
| Redis | 项目已使用 | Token 存储 + 临时 state 缓存，TTL 对齐 token 过期（~7200s） |
| AES 加密 | `bkmonitor.utils.cipher.AESCipher` | CBC 模式，key 用 `settings.SECRET_KEY`，**不传固定 IV** |
| HMAC-SHA256 | Python 标准库 `hmac` | 应用态 state 签名 |
| JSON Web Token | 不涉及 | 本需求使用标准 OAuth 2.0 code 换 token |

---

## 5. 数据存储

> 调研来源：已有文档（`S01_数据模型设计_DESIGN.md`）

### 5.1 数据库（MySQL + Django ORM）

**新增表：`tapd_workspace_binding`**（裸 snake_case，不加 `bkmonitor_` 前缀）

```python
# fta_web/issue/models.py（推测模式，基于设计文档）
class TAPDWorkspaceBinding(models.Model):
    id = models.BigAutoField(primary_key=True)
    space_uid = models.CharField(max_length=256, unique=True, help_text="全局唯一空间标识")
    workspace_id = models.CharField(max_length=64, help_text="TAPD 项目/空间 ID")
    workspace_name = models.CharField(max_length=256, help_text="TAPD 项目名称")
    created = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=128, help_text="创建者用户名")
    # 可能继承 AbstractRecordModel，含 create_user/update_user 自动填充
```

**关键约束**：
- `space_uid` 全局唯一（评审结论 B1，`space_id` 非全局唯一）
- 类名 `TAPDWorkspaceBinding`（不是 `TapdWorkspaceBinding`，设计文档如此）

### 5.2 Redis（Token + 临时 state）

| 用途 | Key 格式 | 值内容 | TTL |
|------|---------|--------|-----|
| 用户态 token | `tapd_uat:{bk_tenant_id}:{username}` | AESCipher 加密后的 JSON（含 access_token, expires_at, scope, resource） | 对齐 token 过期时间 |
| 用户态 state | `tapd_uas:{nonce}` | 原始 redirect URL | 10 分钟 |
| 应用态 state | `tapd_aas:{signed_nonce}` | 签名块 + redirect URL | 10 分钟 |

**加密方式**：
```python
from bkmonitor.utils.cipher import AESCipher
cipher = AESCipher(key=settings.SECRET_KEY)  # 不传 iv！
encrypted = cipher.encrypt(plaintext)        # 随机 IV 前置到密文
decrypted = cipher.decrypt(encrypted)        # 自动读回 IV
```

> ⚠️ **实现注意**：`AESCipher` 在 `iv=None` 时自动生成随机 IV 并前置；传固定 IV 会让相同明文产生相同密文（泄露相等性）。

### 5.3 迁移惯例
- Django `makemigrations` + `migrate`
- 表名不加 `bkmonitor_` 前缀（与现网 `fta_web/issue/` 下的其他表保持一致）
- 可能涉及 `000x_auto_XXXX.py` 形式的迁移文件

---

## 6. 错误处理

> 调研来源：已有文档（`S06_API与序列化设计_DESIGN.md`）

### 6.1 异常模式
- 使用 `ApiException`（`bkmonitor/exceptions.py`）作为统一业务异常
- `ApiExceptionCode` 枚举管理错误码（如 `TAPD_OAUTH_ERROR`、`TAPD_WORKSPACE_NOT_FOUND` 等）
- Resource 层 `try...except` 捕获、序列化器 `raise ApiException(...)`

### 6.2 本需求自定义错误码（推测，来自 S06）

| 错误码 | 含义 | 触发场景 |
|--------|------|----------|
| `TAPD_OAUTH_FAILED` | TAPD OAuth 认证失败 | code 无效、超时、scope 不匹配 |
| `TAPD_WORKSPACE_NOT_FOUND` | TAPD 项目不存在 | `get_workspace_info` 返回 404 |
| `TAPD_TOKEN_EXPIRED` | Token 已过期 | 用户态 token 不在 Redis 中 |
| `TAPD_BINDING_EXISTS` | 绑定已存在 | B-03 创建时 `space_uid` 已绑定 |
| `INVALID_STATE` | state 参数无效 | 应用态回调签名验证失败 |
| `INSTALL_ERROR` | 安装 URL 生成失败 | 应用未上架、白名单未配置 |

### 6.3 外部 API 超时/降级
- TAPD API 调用需设置 **3-5 秒超时**
- 超时/异常 return 友好错误提示（不阻断业务，但通知用户）
- 建议指数退避重试 + 本地缓存（如 `get_granted_workspaces` 缓存 1-5 分钟）

---

## 7. 安全惯例

> 调研来源：已有文档（设计文档 + 评审报告）

### 7.1 认证方式
- **App 级**: Basic Auth（`client_id:client_secret` Base64），硬编码在 `TapdAPIResource`
- **用户级**: Bearer Token（OAuth access_token），每个用户独立，存 Redis
- **本系统内部**: IAM RBAC（`RbacResource` + `IAMBaseAuthentication` + `IAMPermission`）

### 7.2 权限模型
- `RbacResource(safe_methods=[ResourceActions.VIEW])` — 查询类接口默认 VIEW 权限
- `ITSMWebAuthentication` / `IAMPermission` — 写操作需校验
- `RegisterUserResource` 中对 `workspace_id > 100` 的硬编码限制 — 本需求也应遵循 workspace 边界管控

### 7.3 敏感配置
- `TAPD_CLIENT_ID` / `TAPD_CLIENT_SECRET` 从 `settings` / 环境变量读取，**禁止硬编码**
- `settings.SECRET_KEY` 用于 AESCipher 加密 key
- 日志中需脱敏（不打印 access_token、client_secret）

### 7.4 OAuth 安全
- `state` 参数防 CSRF（用户态）/ 防篡改（应用态 HMAC-SHA256）
- `redirect_uri` 必须预先在白名单中注册，**不支持通配符**
- code 5 分钟有效期、一次性使用

---

## 8. API 约定

> 调研来源：已有文档（`S06_API与序列化设计_DESIGN.md` + `dependencies/dependencies.md`）

### 8.1 框架风格
- BlueKing 自定义 `Resource` 框架（非标准 DRF ViewSet）
- 通过 `ResourceRoute` 注册路由：`ResourceRoute("POST", GetTapdWorkspaceListResource, endpoint="get_tapd_workspace_list")`
- HTTP Method 枚举：`HTTP_METHOD.GET`、`HTTP_METHOD.POST` 等

### 8.2 请求/响应格式
- 本系统：标准 REST JSON，外层无 `status/data` 包裹（DRF 默认格式）
- TAPD API：外层固定 `{"status": 1, "data": {...}, "info": "success"}`，需防御性解析
- 分页：DRF `PageSerializer` 或自定义 `limit/page` query 参数

### 8.3 本需求新增接口（来自 S06）

| 接口 | Method | Resource 类 | 序列化器 |
|------|--------|------------|---------|
| `/api/v4/issue/get_tapd_workspace_list/` | GET | `GetTapdWorkspaceListResource` | `ListTapdWorkspaceQuerySerializer` (in), `TapdWorkspaceBindingSerializer` (out) |
| `/api/v4/issue/tapd_oauth_callback/` | GET | `TapdOAuthCallbackResource` | `TapdOAuthCallbackSerializer` |
| `/api/v4/issue/get_tapd_install_url/` | GET | `GetTapdInstallUrlResource` | `InstallUrlRequestSerializer` (in), `UrlSerializer` (out) |

---

## 9. 配置管理

> 调研来源：已有文档（`S01_数据模型设计_DESIGN.md` + `dependencies/dependencies.md`）

### 9.1 Django Settings 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `TAPD_CLIENT_ID` | 无 | 应用 ID（from 开放平台） |
| `TAPD_CLIENT_SECRET` | 无 | 应用密钥 |
| `TAPD_OAUTH_BASE_URL` | `https://tapd.woa.com/oauth/` | OAuth 授权页基地址 |
| `TAPD_API_BASE_URL` | `http://apiv2.tapd.woa.com` | API 基地址 |
| `TAPD_REDIRECT_URI` | 无 | OAuth 回调地址（需白名单） |
| `SECRET_KEY` | Django 默认 | AESCipher 加密 key |

### 9.2 配置来源
- 从 Django `settings` 读取（可能来自 `local_settings.py` / 配置中心 / 环境变量）
- 设计文档建议：`settings` 中读取，不要直接在代码中使用 `os.environ`

---

## 10. 代码风格（从设计文档 Python 片段推断）

> 调研来源：已有文档（设计文档代码片段）

| 项 | 风格 |
|----|------|
| 字符串 | f-string 为主 |
| 类名 | `PascalCase`（如 `GetTapdInstallUrlResource`, `TAPDWorkspaceBinding`） |
| 方法/变量 | `snake_case` |
| 模块名 | `snake_case`（如 `resources.py`, `serializers.py`） |
| 常量 | `UPPER_SNAKE_CASE`（如 `TAPD_CLIENT_ID`） |
| 注释风格 | `# 行内注释`，docstring 用 `"""triple quotes"""` |
| 导入排序 | `from xxx import yyy` 在 `import xxx` 之后（Django 惯例） |
| ORM | Django ORM，外键用 `models.ForeignKey()` |
| 事务 | `@transaction.atomic` 上下文管理器 |

---

## 11. 已知源码缺口（需到主代码仓库验证）

| 设计引用 | 本仓库状态 | 验证建议 |
|----------|-----------|----------|
| `bkmonitor/utils/cipher.py` | **不存在** | 确认 `AESCipher` 的 `encrypt()` / `decrypt()` 签名，尤其是 IV 处理方式是否与文档一致 |
| `bkmonitor/api/tapd/default.py` | **不存在** | 确认 `TapdAPIResource` 是否已含 `get_granted_workspaces`；确认 Basic Auth header 构造方式 |
| `fta_web/issue/resources.py` | **不存在** | 确认 `RegisterUserResource` 和 `ListTapdWorkspaceResource` 的实际代码（workspace_id 边界、Bearer 调用方式） |
| `fta_web/issue/models.py` | **不存在** | 确认 `AbstractRecordModel` 的字段和行为（`create_user` 如何自动填充） |
| `bkmonitor/utils/cache.py` | **不存在** | 确认 `BKMRedisAgent`（或同类 Redis 封装）的 API，如 `setex(key, ttl, value)` 接口 |
| `bkmonitor/exceptions.py` | **不存在** | 确认 `ApiException` 构造签名（是否支持 `(code, message)`）|

---

## 12. 调研结论

1. **本仓库为文档型仓库**，实际 Django 源码在主代码仓库中。设计文档已充分引用了源码路径和模式，但编码阶段需到源码仓库对照验证。
2. **核心可复用组件已定位**：`AESCipher`（加密）、`TapdAPIResource`（Basic Auth TAPD 客户端）、`ApiException`（异常）、`BKMRedisAgent`（Redis）。
3. **代码承载于 `fta_web/issue/`**：不新建 `fta_web/tapd/`（评审结论 N1），与现有 `RegisterUserResource`、`ListTapdWorkspaceResource` 同模块。
4. **ORM 风格明确**：Django ORM + 可能的 `AbstractRecordModel` 基类，`space_uid` 全局唯一键。
5. **API 风格明确**：BlueKing Resource 框架（非 DRF ViewSet），`ResourceRoute` 注册，`Meta` 中配置认证/权限类。
6. **安全惯例明确**：IAM RBAC + OAuth state 签名 + AESCipher 随机 IV + 配置中心读取敏感信息。
