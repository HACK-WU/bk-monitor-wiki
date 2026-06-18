---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-17
version: 2
tags: [feat, integration, design, S01]
depends_on: []
author: AI
document_type: design
parent: DESIGN.md
---

# S-01 数据模型设计

> 状态：已按设计评审结论（v1，2026-06-17）修订。
>
> **评审核心结论**：Token 不落 DB ⇒ 持久化数据模型只剩 `TapdWorkspaceBinding` **一张表**。`UserTapdToken` 表、`refresh_token`、S-07 异步刷新整套已删除。

---

## ★ 1. 术语

| 术语 | 含义 | 引用 |
|------|------|------|
| `AbstractRecordModel` | bkmonitor 标准抽象模型类，自动提供 `id` / `is_enabled` / `is_deleted` / `create_user` / `create_time` / `update_user` / `update_time` 字段及软删支持 | `bkmonitor/utils/model_manager.py` |
| `RecordModelManager` | `AbstractRecordModel` 的默认 Manager，自动过滤 `is_deleted=True` 的数据；`origin_objects` 提供全量（含已删除）查询 | `bkmonitor/utils/model_manager.py` |
| `TapdWorkspaceBinding` | TAPD 项目关联表，存储 space 与 tapd_workspace_id 的映射关系 | 本设计 §4b.1 |
| `bk_tenant_id` | 蓝鲸租户 ID，多租户惯例字段 | 仓内先例：`ApiAuthToken`（`bkmonitor/models/token.py:48,72`） |
| `space_uid` | 蓝鲸空间唯一标识（全局唯一），替代裸 `space_id` | `metadata/models/space/space.py` |
| `upsert` | MySQL 的 INSERT ... ON DUPLICATE KEY UPDATE 语法，实现存在则更新、不存在则插入 | — |

---

## ★ 2. 现状（AS-IS）

### 2.1 现状描述

当前蓝鲸监控平台与 TAPD 系统完全独立，无数据交互。用户需要在 TAPD 系统中手动操作，无法在监控平台中直接关联 TAPD 项目或查看授权状态。

### 2.2 痛点

- 痛点 1：用户需要在两个系统间切换，操作繁琐
- 痛点 2：无法在监控平台中统一管理 TAPD 授权状态
- 痛点 3：关联关系缺乏持久化，无法跨用户共享

---

## ★ 3. 方案（TO-BE）

### 3.1 方案概述

**仅保留一张核心数据表**：`TapdWorkspaceBinding` 存储空间与 TAPD 项目的关联关系。

用户态 token（OAuth access_token）**不落 DB**，改为：**AESCipher 加密后写入 Redis，TTL 对齐 token 过期时间**。Token 过期即重走一次用户态 OAuth（一次廉价重定向），无需持久化存储和刷新机制。

### 3.2 关键决策点

| 决策 | 选择 | 理由 | 备选方案 | 否决原因 |
|------|------|------|----------|----------|
| Token 存储方式 | **Redis + AESCipher 加密 + TTL** | 评审结论 A1：不落 DB，到期自动淘汰，实现简单 | MySQL 持久化 + 异步刷新 | 比例失衡，过度设计 |
| 持久化表数量 | **仅 1 张**（`TapdWorkspaceBinding`） | 评审结论：token 不进 DB，删除 `UserTapdToken` 表 | 2 张表 | 评审否决 |
| 空间主键 | **`space_uid`**（全局唯一） | 评审结论 B1：`space_id` 仅在 `space_type` 内唯一，非全局唯一；非业务空间用负数 `bk_biz_id` | `space_id` | 正确性 bug |
| 多租户字段 | **`bk_tenant_id`** | 对齐仓内 13 个模型惯例（`ApiAuthToken` 等） | 不加 | 多租户合规 |
| 关联幂等策略 | 唯一约束 + upsert | 数据库层面保证，简单可靠 | 应用层去重 | 并发时可能重复插入 |

### 3.3 行为差异对照表

| 场景 | AS-IS | TO-BE | 影响 |
|------|-------|-------|------|
| 项目关联 | 无关联关系 | 自动关联 TAPD 项目 | 新增功能 |
| Token 存储 | 无 Token 存储 | **Redis 加密存储，TTL 自动过期** | 新增功能 |
| Token 刷新 | 无刷新机制 | **过期即重走 OAuth，无刷新** | 简化设计 |
| 数据表 | 无 | **仅 1 张表** | 新增功能 |

---

## ★ 4b. 数据模型

### 4b.1 持久化结构

> **文件位置**：`bkmonitor/bkmonitor/models/tapd.py`（新建文件），并在同目录 `__init__.py` 中加入 `from .tapd import *`
>
> **继承基类**：`bkmonitor/utils/model_manager.py` → `class AbstractRecordModel(models.Model)`
> **参考实现**：`bkmonitor/bkmonitor/models/strategy.py` → `class UserGroup(AbstractRecordModel)`
> **QuerySet 行为**：`objects` 默认过滤已删除记录；`origin_objects` 用于跨表全量查询

```python
# bkmonitor/bkmonitor/models/tapd.py
from django.db import models

from bk_monitor_base.infras.constant import DEFAULT_TENANT_ID
from bkmonitor.utils.model_manager import AbstractRecordModel

__all__ = ["TapdWorkspaceBinding"]


class TapdWorkspaceBinding(AbstractRecordModel):
    """TAPD 项目关联表"""
    bk_tenant_id = models.CharField("蓝鲸租户ID", max_length=64, default=DEFAULT_TENANT_ID)
    space_uid = models.CharField("蓝鲸空间唯一标识", max_length=128)
    bk_biz_id = models.IntegerField("蓝鲸CMDB业务ID", db_index=True)
    tapd_workspace_id = models.CharField("TAPD项目ID", max_length=64)
    tapd_workspace_name = models.CharField("TAPD项目名称", max_length=255)
    # creator 由 AbstractRecordModel 的 create_user 自动提供，无需声明
    # 注意：回调时 request.user 是管理员，create_user 会被填为管理员
    # 真实发起人需 callbacks 从 signed_state.initiator 显式写入

    class Meta:
        db_table = "tapd_workspace_binding"
        unique_together = [("bk_tenant_id", "space_uid", "tapd_workspace_id")]
        verbose_name = "TAPD项目关联"
        verbose_name_plural = "TAPD项目关联"
        # AbstractRecordModel 自动提供 ordering = ("-create_time",) 等指标
```

**关键变更说明（vs 评审前版本）**：

| 项目 | 评审前 | 评审后（定稿） | 原因 |
|------|--------|---------------|------|
| 表数量 | `TapdWorkspaceBinding` + `UserTapdToken`（2 张） | 仅 `TapdWorkspaceBinding`（**1 张**） | A1：token 不落 DB |
| `space_id` 唯一约束 | `unique_together = [("space_id", "tapd_workspace_id")]` | `unique_together = [("bk_tenant_id", "space_uid", "tapd_workspace_id")]` | B1：`space_id` 非全局唯一 |
| 空间标识 | `space_id`（int） | **`space_uid`**（str） + `bk_biz_id` 冗余 | 稳定性 + 查询效率 |
| 多租户 | 无 | **`bk_tenant_id`** | N2：对齐仓内惯例 |
| `UserTapdToken` | 独立表，含 `refresh_token` | **已删除** | A1：Redis 替代 |
| 表名前缀 | `tapd_workspace_binding` | `tapd_workspace_binding`（不变） | 符合全仓裸 snake_case |

**继承自 `AbstractRecordModel` 的自动字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `AutoField` | 自增主键 |
| `is_enabled` | `BooleanField(default=True)` | 是否启用 |
| `is_deleted` | `BooleanField(default=False)` | 是否删除（软删标记） |
| `create_user` | `CharField(max_length=32, default='')` | 创建人，由 `save()` 自动记录当前用户 |
| `create_time` | `DateTimeField(auto_now_add=True)` | 创建时间 |
| `update_user` | `CharField(max_length=32, default='')` | 最后修改人，由 `save()` 自动记录当前用户 |
| `update_time` | `DateTimeField(auto_now=True)` | 最后修改时间 |

> **创建人审计注意**：
> `AbstractRecordModel.save()` 会自动将 `request.user` 填入 `create_user`。但在应用态授权回调（B-03）中，`request.user` 是完成授权的管理员，而非发起关联的普通用户。要记录真实发起人，须从 `signed_state.initiator` 显式覆盖 `create_user`。

### 4b.2 传输/中间结构

```python
# 序列化器定义（仅用于内部数据校验）
class TapdWorkspaceBindingSerializer(serializers.ModelSerializer):
    """TAPD 项目关联序列化器"""
    class Meta:
        model = TapdWorkspaceBinding
        fields = [
            "id", "bk_tenant_id", "space_uid", "bk_biz_id",
            "tapd_workspace_id", "tapd_workspace_name",
            "create_user", "create_time", "update_time",
        ]
        read_only_fields = ["id", "create_user", "create_time", "update_time"]
```

---

## ★ 4c. Redis Token 存储（非持久化）

> **评审结论 A1**：用户态 token 加密后写 Redis，TTL 对齐 token 过期时间，到期自动淘汰。

### Redis Key 设计

| 项 | 值 |
|----|-----|
| Key 格式 | `tapd_uat:{bk_tenant_id}:{username}` |
| Value 格式 | JSON 字符串：`{"access_token": "<密文>", "tapd_user_id": "...", "token_type": "Bearer", "expires_at": <timestamp>}` |
| TTL | 与 token 过期时间对齐（约 2h） |

### 加密方式

```python
from bkmonitor.utils.cipher import AESCipher

cipher = AESCipher(key=settings.SECRET_KEY)  # 不传 iv！
encrypted = cipher.encrypt(access_token)
decrypted = cipher.decrypt(encrypted)
```

> **⚠️ 实现注意**：实例化时**不要传固定 IV**。`AESCipher` 源码（`cipher.py:77/87`）在 `iv` 为空时每次生成随机 IV 并前置到密文、解密时从首块读回。传固定 IV（如 `BK_DATA_AES_IV`）会全程复用，CBC 固定 IV 会让相同明文产生相同密文、泄露相等性。

### Token 读写工具函数

```python
# 伪代码

def save_tapd_token(bk_tenant_id: str, username: str, token_data: dict):
    """加密并写入 Redis，TTL 对齐 expires_at"""
    cipher = AESCipher(key=settings.SECRET_KEY)
    encrypted_token = cipher.encrypt(token_data["access_token"])
    
    value = {
        "access_token": encrypted_token,
        "tapd_user_id": token_data["tapd_user_id"],
        "token_type": token_data.get("token_type", "Bearer"),
        "expires_at": token_data["expires_at"],
    }
    
    ttl = token_data["expires_at"] - int(time.time())
    if ttl <= 0:
        # token 已过期或时钟偏移，视作未授权，不写入 Redis
        return
    redis_client.setex(f"tapd_uat:{bk_tenant_id}:{username}", ttl, json.dumps(value))

def get_tapd_token(bk_tenant_id: str, username: str) -> dict:
    """从 Redis 读取并解密"""
    raw = redis_client.get(f"tapd_uat:{bk_tenant_id}:{username}")
    if not raw:
        return None
    
    data = json.loads(raw)
    cipher = AESCipher(key=settings.SECRET_KEY)
    data["access_token"] = cipher.decrypt(data["access_token"])
    return data
```

---

## ★ 4d. `is_bound` 四态定义

`is_bound` 由 **本地 binding 状态 × TAPD `get_granted_workspaces` 授权状态** 交叉决定：

| 本地 binding | TAPD 已授权 | 状态 | 前端语义 |
|:---:|:---:|---|---|
| ✓ | ✓ | `bound` | 已关联 |
| ✓ | ✗ | `stale` | TAPD 侧已解绑，需重关联 |
| ✗ | ✓ | `importable` | TAPD 已装应用，可一键回填本地 |
| ✗ | ✗ | `unbound` | 未关联，可去关联 |

- 查询 / 建单前用 `get_granted_workspaces` 兜底校验
- 现网兜底已是 10 并发 fan-out（`issue/resources.py:1302`），需按 space/app 维度加短 TTL 缓存

---

## +10. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| 数据库 | 数据变更 | 新增 **1** 张表（`tapd_workspace_binding`） | 否 |
| Django ORM | 接口变更 | 新增 1 个 Model 类 | 否 |
| Migration | 数据变更 | 新增 Migration 文件 | 否 |
| Redis | 新增 | 新增 token 缓存 key（`tapd_uat:*`） | 否 |

---

## +11. 待定问题

| 编号 | 问题 | 影响范围 | 建议决策时间 | 负责人 |
|------|------|---------|------------|--------|
| ~~T-01~~ | ~~Token 存储位置~~ | — | ✅ **已解决** | — |
| ~~T-02~~ | ~~space_id 唯一性~~ | — | ✅ **已解决** | — |
| ~~T-03~~ | ~~refresh_token 是否存储~~ | — | ✅ **已解决** | — |
| T-04 | `bk_biz_id → space_uid` 映射前置依赖（`get_space_map`） | S-01, S-03 | 实施前 | 后端开发 |
