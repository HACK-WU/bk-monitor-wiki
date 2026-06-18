# 实施排期 — TAPD 授权与建单（REQ-20260615-001）

> 文档版本：v1
> 编制时间：2026-06-18
> 基准：设计评审定稿 v2（2026-06-17）
> 估算模式：1 人天 = 8 小时，基于单人开发

---

## 一、排期总览

| 阶段 | 时间 | 里程碑 | 工作项数 | 预估人天 |
|------|------|--------|---------|---------|
| **Phase 1** | Day 1 | M1：基础设施就绪 | 3 | 2 |
| **Phase 2** | Day 2–3 | M2：OAuth 能力可联调 | 4 | 5 |
| **Phase 3** | Day 4 | M3：API 接口可交付 | 1 | 1 |
| **Phase 4** | Day 5–6 | M4：验收通过 | 2 | 3 |
| **合计** | **6 个工作日** | — | **10** | **11** |

> 不含联调等待时间（TAPD 开放平台白名单审批、应用上架等外部依赖）。

---

## 二、工作项详表

### Phase 1：基础设施（Day 1）

| 编号 | 工作项 | 人天 | 前置依赖 | 说明 |
|------|--------|------|---------|------|
| P1-1 | **Django Model + Migration** | 0.5 | 无 | `TapdWorkspaceBinding` 单表，`space_uid` 全局唯一，裸 snake_case 表名。需确认 `AbstractRecordModel` 的 `create_user` 自动填充行为 |
| P1-2 | **配置项注册** | 0.5 | 无 | `TAPD_CLIENT_ID`、`TAPD_CLIENT_SECRET`、`TAPD_REDIRECT_URI`、`TAPD_OAUTH_BASE_URL`、`TAPD_API_BASE_URL` 注册到 settings / 配置中心 |
| P1-3 | **Redis 工具函数封装** | 1 | P1-2 | `save_tapd_token()`、`get_tapd_token()`、`save_oauth_state()`、`verify_oauth_state()`，封装 AESCipher 加密解密逻辑。关键：`cipher = AESCipher(key=settings.SECRET_KEY)` **不传 iv** |

**Phase 1 交付物：**
- `fta_web/issue/models.py` 新增 `TapdWorkspaceBinding`
- `fta_web/issue/migrations/000x_auto_XXXX.py`
- `fta_web/issue/utils/tapd_token.py`（或同级模块）— Redis 读写工具
- `config/default_settings.py`（或配置中心）— 新增 TAPD 相关配置

**风险点：**
- `bkmonitor/utils/cipher.py` 中 `AESCipher` 实际接口需到源码仓库确认（`code-survey.md §11` 已标注）
- 配置中心白名单需运维配合，可能阻塞 Day 1

---

### Phase 2：核心能力开发（Day 2–3）

| 编号 | 工作项 | 人天 | 前置依赖 | 说明 |
|------|--------|------|---------|------|
| P2-1 | **TapdAPIResource 复用确认** | 0.5 | 无 | 到源码仓库确认现网 `TapdAPIResource` 是否已含 `get_granted_workspaces`；确认 Basic Auth header 构造方式 |
| P2-2 | **B-05 用户态 OAuth 全流程** | 1.5 | P1-3, P2-1 | 授权链接生成（`auth_by=user`, `state=nonce`）→ Redis 存 state → 回调取 code → `request_token` 换 token → AESCipher 加密 → Redis 存 token |
| P2-3 | **B-02/B-03 应用态 OAuth + 回调** | 2 | P1-3, P2-1 | `install_url` 生成（`open_app_install`）→ `signed_state` HMAC-SHA256 签名 → 回调验签 → `get_workspace_info` (Basic Auth) → 创建 `TapdWorkspaceBinding` |
| P2-4 | **B-01/B-07 项目列表查询（四态）** | 1 | P2-1, P1-1 | `ListUserVisibleTapdWorkspaceResource`（Bearer，用户可见）+ `ListGrantedTapdWorkspaceResource`（Basic，app 已授权）→ 交叉判定 `bound/stale/importable/unbound` |

**并行关系：**
- P2-2（用户态）与 P2-3（应用态）**可并行开发**，OAuth flow 独立
- P2-4 依赖 P2-1（TapdAPIResource 确认）和 P1-1（Model 就绪），但可与 P2-2/P2-3 并行到 Day 3

**Phase 2 交付物：**
- `fta_web/issue/resources.py` — 新增 Resource 类（B-01/B-03/B-05/B-07 逻辑）
- `fta_web/issue/services/oauth.py` — OAuth 核心逻辑（可选拆分）
- `fta_web/issue/services/workspace.py` — 四态查询逻辑（可选拆分）

**风险点：**
- `ListTapdWorkspaceResource`（现网 `issue/resources.py:1302`）改名需确认是否影响其他调用方
- 四态查询涉及两次 TAPD API 调用（Bearer + Basic），需加短 TTL 缓存防 429/502
- `get_workspace_info` 404 需处理为 `TAPD_WORKSPACE_NOT_FOUND`

---

### Phase 3：API 接口封装（Day 4）

| 编号 | 工作项 | 人天 | 前置依赖 | 说明 |
|------|--------|------|---------|------|
| P3-1 | **Serializer + Resource + 路由注册** | 1 | Phase 1–2 | `TapdWorkspaceBindingSerializer`、`ListTapdWorkspaceQuerySerializer`、`InstallUrlRequestSerializer`、`TapdOAuthCallbackSerializer` 定义 + 3 个 Resource 类 Meta 配置 + `urls.py` 注册 |

**Phase 3 交付物：**
- `fta_web/issue/serializers.py` — 新增序列化器
- `fta_web/issue/resources.py` — Resource 类完整实现
- `fta_web/issue/urls.py` — `ResourceRoute` 注册 3 个新接口

**接口清单：**

| Endpoint | Method | Resource 类 | 前置 |
|----------|--------|------------|------|
| `/api/v4/issue/get_tapd_workspace_list/` | GET | `GetTapdWorkspaceListResource` | P2-4 |
| `/api/v4/issue/tapd_oauth_callback/` | GET | `TapdOAuthCallbackResource` | P2-2/P2-3 |
| `/api/v4/issue/get_tapd_install_url/` | GET | `GetTapdInstallUrlResource` | P2-3 |

---

### Phase 4：测试与验证（Day 5–6）

| 编号 | 工作项 | 人天 | 前置依赖 | 说明 |
|------|--------|------|---------|------|
| P4-1 | **单元测试** | 1.5 | Phase 1–3 | `TapdWorkspaceBinding` CRUD、OAuth state 签名/验签、AESCipher 加解密、四态判定逻辑、异常分支（过期 code、无效 state、404 workspace） |
| P4-2 | **Demo / TAPD 开放平台联调** | 1.5 | Phase 1–3 | 1) 白名单配置验证（redirect_uri、cb）2) 用户态 OAuth 端到端 3) 应用态 install → 回调 → 绑定 4) 项目列表四态展示 5) 并发/超时/429 场景 |

**测试重点：**

| 场景 | 验证点 |
|------|--------|
| 用户态授权 | 点击授权 → 跳转 TAPD → 同意 → 回调 → Redis 中有加密 token |
| 应用态授权 | 生成 install_url → 管理员安装 → 回调 → DB 中有 binding 记录 |
| 四态查询 | 本地无绑定 + app 未授权 → `unbound`；本地有绑定 + app 已授权 → `bound`；等 |
| 边界 | code 过期（5min）、state 签名篡改、redirect_uri 不匹配 |
| 并发 | 10 并发 fan-out（现网已有模式）加缓存后是否稳定 |

**Phase 4 交付物：**
- `fta_web/issue/tests/test_tapd.py`（或同级）
- 联调报告 / Demo 截图

---

## 三、甘特图

```
Day 1      Day 2      Day 3      Day 4      Day 5      Day 6
|-----------|----------|----------|----------|----------|----------|
  P1-1 +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  P1-2    ▓▓▓▓▓▓▓▓ |
  P1-3    ░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ |

  P2-1    ▓▓▓▓▓▓ |
  P2-2    ░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ |
  P2-3    ░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ |
  P2-4    ░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓ |

  P3-1                           ▓▓▓▓▓▓▓▓▓▓ |

  P4-1                                      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ |
  P4-2                                      ░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ |
                                        ^^^^
                                        联调
                                      (可能等 TAPD 审核)
```

**图例：**
- `▓▓▓▓` 主要工作时间
- `░░░░` 等待/缓冲/联调窗口

---

## 四、里程碑定义

| 里程碑 | 日期 | 验收标准 | 可交付状态 |
|--------|------|---------|----------|
| **M1：基础设施就绪** | Day 1 | Model Migration 可执行；Redis 工具函数 unittest 通过；配置项在环境中可读取 | 可独立验证 |
| **M2：OAuth 能力可联调** | Day 3 | 用户态和应用态 OAuth 链路在本地可跑通（mock TAPD 或直连沙箱）；回调可创建 binding；token 可存取 Redis | 后端可独立联调 |
| **M3：API 接口可交付** | Day 4 | 3 个新接口可通过 curl/Postman 访问；Document 校验通过；swagger（如有）可展示 | 前端可对接 |
| **M4：验收通过** | Day 6 | 单元测试覆盖率 ≥ 80%（核心逻辑）；TAPD 开放平台联调通过；四态查询在各种场景下正确 | 可提测 |

---

## 五、外部依赖与阻塞点

| 依赖 | 阻塞阶段 | 预计等待 | 缓解措施 |
|------|---------|---------|----------|
| **TAPD 应用上架 / 测试应用创建** | 全部联调 | 1–3 个工作日 | 先用测试应用（`test=1`）开发；并行申请正式上架 |
| **redirect_uri / cb 白名单审批** | Phase 4 | 0.5–1 个工作日 | 提前在开发者后台提交；本地用 `localhost` 白名单先做开发 |
| **配置中心新增 TAPD_xxx 变量** | Phase 1 | 0.5 个工作日 | 提前发工单给运维；本地 `.env` 或 `local_settings.py` 先做开发 |
| **IAM 权限配置（如需新增 Action）** | Phase 3 | 1–2 个工作日 | 确认是否复用现有 `VIEW`/`MANAGE` 权限，避免新增 Action |
| **前端页面开发**（并行） | Phase 3–4 | 3–5 人天 | 前端可基于 M2/M3 的 mock API 并行开发 |

---

## 六、人力建议

| 方案 | 人天 | 时长 | 适用场景 |
|------|------|------|---------|
| **A：单人全栈** | 11 | 6 工作日 | 资源紧张，但上下文连续性好 |
| **B：1 后端 + 0.5 前端** | 后端 11 + 前端 4 | 6–8 工作日 | 前端并行，后端完成后前端可继续 |
| **C：1 后端 + 1 前端（全并行）** | 后端 11 + 前端 4 | 6 工作日 | 前端在 M2/M3 介入，整体最快 |

> 推荐 **方案 B 或 C**（前端并行），因前端 install_url 跳转页和项目选择列表与后端 OAuth 流程可高度并行。

---

## 七、风险与预案

| 风险 | 概率 | 影响 | 预案 |
|------|------|------|------|
| `AESCipher` 接口与设计文档不一致 | 中 | P1-3 需重写 | 到源码仓库确认后，若接口不同则适配封装层 |
| `TapdAPIResource` 不含 `get_granted_workspaces` | 低 | P2-1 需新增 | 复用基类新增方法，工作量 +0.5 天 |
| `ListTapdWorkspaceResource` 改名影响其他调用方 | 低 | 回归风险 | 全局搜索引用，确认所有调用方可同步更新 |
| `AbstractRecordModel` 的 `create_user` 自动填充逻辑不同 | 中 | P2-3 中 B-03 回调的 `create_user` 可能被覆盖 | 编码时确认 `save()` 行为；必要时手动覆盖 `create_user` |
| TAPD API 429/502 频繁 | 中 | Phase 4 联调受阻 | 本地缓存（`get_granted_workspaces` TTL 1–5min）、指数退避重试 |
| OAuth 回调超时/丢 state | 低 | 用户体验差 | state 10min TTL + 过期友好提示 + 日志记录 |
