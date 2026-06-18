---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 已确认
created: 2026-06-17
updated: 2026-06-17
version: 1
tags: [feat, integration]
depends_on: []
author: AI
document_type: review
---

# TAPD 授权方案 — 评审结论（定稿 v1）

> 评审范围：本目录「issue_tapd授权」下 需求报告 / 数据模型与数据流 / S-01~S-07 全部设计文档。
> 评审方式：逐篇审阅 + 与 bk-monitor 现网代码逐项对照核实，多轮收敛后定稿。
> 定稿日期：2026-06-17

---

## 一、总判断

产品流程成立 —— 双层授权链路（用户态 + 应用态）、空间↔workspace 共享关联、查询项目时标记 `is_bound`，方向都对。但原始技术设计**不能直接落地**。

根因不是某几个孤立 bug，而是**设计在未对照现网已有代码的前提下产出**：`bkmonitor/api/tapd/default.py`（已是 app 级 Basic Auth 客户端，含 `get_granted_workspaces` / `get_workspace_info` / 建单资源）和 `bkmonitor/packages/fta_web/issue/resources.py:1302`（已有 workspace 查询），本可回答文档里多处「待确认」。**落地第 0 步：设计与现网代码对账一次。**

下列为定稿结论，详略按重要性。

---

## 二、必须改 / 已锁定的架构决策（最高优先，详述）

### A1. 用户态 token —— AESCipher 加密后写 Redis，不落 DB

用户态 OAuth 的**唯一**用途是冷启动「枚举该用户可见的 TAPD 项目」供挑选；建单 / 查已授权 / 取项目信息全走 app 级 Basic，与它无关。既然产品保留挑选器：

- OAuth 取得 `access_token` → 用 `bkmonitor/bkmonitor/utils/cipher.py` 的 `AESCipher` **加密后写 Redis**。
  - key：`tapd_uat:{bk_tenant_id}:{username}`
  - value（JSON）：`{access_token(密文), tapd_user_id, token_type, expires_at}`
  - **TTL = token 过期时间对齐（约 2h），到期自动淘汰**。
- **实现注意**：实例化时**不要传固定 IV** —— `AESCipher` 源码（`cipher.py:77/87`）在 `iv` 为空时每次生成随机 IV 并前置到密文、解密时从首块读回；传固定 IV（如 `BK_DATA_AES_IV`）会全程复用，CBC 固定 IV 会让相同明文产生相同密文、泄露相等性。故应 `AESCipher(key)`（key 取 `SECRET_KEY`、**不传 iv**）。
- **直接删除**：`UserTapdToken` 表、`refresh_token`、S-07 异步刷新整套。token 过期即重走一次用户态 OAuth（一次廉价重定向）。
- 推论：token 不落 DB ⇒ 持久化数据模型只剩 `TapdWorkspaceBinding` **一张表**；`tapd_user_id` 随 token 进 Redis value，不再有独立表。

### A2. 应用态授权 state —— 签名串烘进 `cb`，验签不验 session（修复 C1：原设计会破坏核心场景）

原设计用 `request.session["tapd_oauth_state_{bk_biz_id}"]` 校验 state。但「非管理员转发安装链接给管理员」是核心场景：管理员在**另一浏览器/账号**完成授权，回调命中的是管理员 session（无发起人 state）→ **必失败**；`tapd_user_id` 一致性校验同理误杀。

- 改为 `signed_state = base64url(json).hmac`，内容含 `bk_tenant_id / space_uid / bk_biz_id / initiator / nonce / expire_at`，**作为 `cb` 回调 URL 自身的 query 参数烘进去**（`cb` 由我们完全控制，必随回调返回；不依赖 TAPD 是否回传自定义 `state`）。回调**只验签 + 验过期**，不碰 session。
- `initiator` 用途是**审计归属**：回调里 `request.user` 是管理员，`AbstractRecordModel.save()` 会把 `create_user` 填成管理员；要记录真实发起人，须从 `signed_state.initiator` 显式写入 `create_user`。
- `nonce` 仅作签名盐：B-03 重放是良性的（upsert 幂等 + 授权由 TAPD 项目管理员把关），不实现「一次性」假承诺。
- 必要性（已核威胁模型）：伪造回调最坏能把攻击者控制的 workspace 绑到受害空间，导致该空间后续建单流向攻击者 TAPD 项目 = 信息泄露，故签名保护是真需求。
- 用户态回调（B-05）是同人同浏览器，可继续用 session 态 state。

### A3. 回调取 workspace 信息 —— 走 app 级 Basic，不用用户态 Bearer（修复 C2：与现网代码冲突）

现网 `TapdAPIResource`（`api/tapd/default.py:20`）对所有 TAPD 调用硬编码 app 级 Basic Auth，`get_workspace_info` 已按此工作。回调操作者可能是管理员、本就拿不到发起人 token。**回调直接复用现成的 Basic `get_workspace_info`**，顺带消除 A2 的身份难题。

---

## 三、数据模型（落地前定，中等）

- **单表 `TapdWorkspaceBinding`**，唯一键 **`(bk_tenant_id, space_uid, tapd_workspace_id)`**。
  - 废弃裸 `space_id` 唯一约束 —— 这是正确性 bug：`space_id` 仅在某 `space_type` 内唯一、非全局唯一，非业务空间还用负数 `bk_biz_id`（见 `metadata/models/space/space.py`）。`space_uid` 为稳定键，`bk_biz_id` 冗余加索引即可。
  - `bk_tenant_id` 对齐仓内多租户惯例（先例 `ApiAuthToken`，`bkmonitor/models/token.py:48,72`）。
- **`bk_biz_id → space_uid` 映射** 从「待确认」提为**前置设计项**（用 `monitor_web/space/resources.py` 的 `get_space_map`），它是回调写表的前置依赖。
- **`is_bound` = 本地 binding × TAPD `get_granted_workspaces` 四态**：

| 本地 binding | TAPD 已授权 | 状态 | 前端语义 |
|:---:|:---:|---|---|
| ✓ | ✓ | `bound` | 已关联 |
| ✓ | ✗ | `stale` | TAPD 侧已解绑，需重关联 |
| ✗ | ✓ | `importable` | TAPD 已装应用，可一键回填本地 |
| ✗ | ✗ | `unbound` | 未关联，可去关联 |

  - 查询 / 建单前用 `get_granted_workspaces` 兜底校验；现网兜底已是 10 并发 fan-out（`issue/resources.py:1302`），需按 space/app 维度加短 TTL 缓存。
- **表名遵循 `bkmonitor/models` 惯例**（裸 snake_case，如 `tapd_workspace_binding`），不加 `bkmonitor_` 前缀、不自定。

---

## 四、模块与接口（承载在 issues 下，中等）

- **全部承载在 `fta_web/issue/`** —— TAPD 是 Issues 的子功能（最终拍板）。授权、项目查询、回调、binding 都在 issue 模块内做清晰内部分层，不新建 `fta_web/tapd/`。
- **两个列表接口必须区分、不可同名**：

| 用途 | 鉴权 | 数据源 | 现状 |
|---|---|---|---|
| 用户可见可挑（冷启动去关联） | 用户态 token（Redis） | TAPD 用户态 API | 新增 |
| app 已授权（日常下拉 + is_bound 兜底源） | app 级 Basic | `get_granted_workspaces` | 现网已有 `ListTapdWorkspaceResource`，**改名区分** |

- **绑定类接口走 `MANAGE_EVENT`**（生成安装链接 / 发起绑定是写语义），不继承只读 `VIEW_EVENT`（参见 `issue/views.py:85` 的读写权限分档）。

---

## 五、后续跟进（本期不做）

- **建单关联模型** `IssueTapdTicketBinding(issue_id, bk_tenant_id, space_uid, workspace_id, ticket_type, ticket_id, ticket_url, status)` —— 下期从 Issue 反查 TAPD 单据时设计，避免补迁移债。

---

## 六、实现期顺手 / 编码前待验证（简列）

- `install_url` 的 `cb=` 整体 urlencode；参数放 query，不放 `#fragment`（fragment 不发服务端）。
- 回调端点：CSRF 豁免、登录态来源、`redirect_uri` 三处（授权时 / 换 token 时 / TAPD 应用配置）严格一致。
- **待验证（外部，不阻塞设计）**：`open_app_install` 的 `cb` 回调结果 `resource` 的具体结构（业界惯例必带结果，结构后续核实）。

---

## 附：发现 — 严重度 — 现网证据 对照

| 编号 | 发现 | 严重度 | 现网证据 / 落点 |
|---|---|:---:|---|
| C1 | session 态 state 破坏「转链接给管理员」 | 🔴 必改 | S-03 §4a；改签名 state 烘进 cb |
| C2 | 回调用用户态 Bearer 取 name，与现网冲突 | 🔴 必改 | `api/tapd/default.py:20`（全 Basic） |
| A1 | token 落 DB + 加密 + 异步刷新 比例失衡 | 🟠 已收敛 | 改 Redis+AESCipher+TTL，删表/删 S-07 |
| M2 | refresh_token 范围：需求说不做、设计在做 | 🟠 已收敛 | 一期删除，三处口径统一 |
| B1 | 唯一键 `space_id` 非全局唯一 | 🟠 必改 | `metadata/models/space/space.py` |
| N1 | 模块边界 / 同名资源冲突 | 🟠 已定 | `issue/resources.py:1302`、`issue/views.py:18` |
| N2 | 缺 `bk_tenant_id`（多租户） | 🟠 已收敛 | `models/token.py:48,72` 等 13 模型 |
| N4 | 绑定接口权限档位过低 | 🟡 | `issue/views.py:85`（VIEW/MANAGE_EVENT） |
| m1 | 加密应复用 AESCipher 而非 Fernet | 🟡 已定 | `utils/cipher.py:67` |
| — | 表名 `bkmonitor_` 前缀建议 | ❌ 否决 | 全仓裸 snake_case，无前缀 |
