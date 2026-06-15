---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-15
version: 1
tags: [feat, integration, design, S01]
depends_on: []
author: AI
document_type: design
parent: DESIGN.md
---

# S-01 数据模型设计

> 状态：设计中

---

## ★ 1. 术语

| 术语 | 含义 | 引用 |
|------|------|------|
| `AbstractRecordModel` | bkmonitor 标准抽象模型类，自动提供 `id` / `is_enabled` / `is_deleted` / `create_user` / `create_time` / `update_user` / `update_time` 字段及软删支持 | `bkmonitor/utils/model_manager.py` |
| `RecordModelManager` | `AbstractRecordModel` 的默认 Manager，自动过滤 `is_deleted=True` 的数据；`origin_objects` 提供全量（含已删除）查询 | `bkmonitor/utils/model_manager.py` |
| `TAPD_WORKSPACE_BINDING` | TAPD 项目关联表，存储 space_id 与 tapd_workspace_id 的映射关系 | 本设计 §4b.1 |
| `USER_TAPD_TOKEN` | 用户 TAPD Token 表，存储用户的 access_token 和 refresh_token | 本设计 §4b.1 |
| `upsert` | MySQL 的 INSERT ... ON DUPLICATE KEY UPDATE 语法，实现存在则更新、不存在则插入 | — |

> 共享术语见父文档 §4.3 共享术语速查

---

## ★ 2. 现状（AS-IS）

### 2.1 现状描述

当前蓝鲸监控平台与 TAPD 系统完全独立，无数据交互。用户需要在 TAPD 系统中手动操作，无法在监控平台中直接关联 TAPD 项目或查看授权状态。

### 2.2 痛点

- 痛点 1：用户需要在两个系统间切换，操作繁琐
- 痛点 2：无法在监控平台中统一管理 TAPD 授权状态
- 痛点 3：Token 过期后用户需要手动重新授权，体验差

---

## ★ 3. 方案（TO-BE）

### 3.1 方案概述

设计两个核心数据表：`TapdWorkspaceBinding` 存储项目关联关系，`UserTapdToken` 存储用户 Token。均直接继承 `AbstractRecordModel`（参考 `UserGroup` 等现有模型的做法），自动复用内部约定好的审计字段（`create_user`/`create_time`/`update_user`/`update_time`/`is_enabled`/`is_deleted`）和软删能力，无需重复手写。采用唯一约束保证数据幂等，Token 字段加密存储保障安全。

### 3.2 关键决策点

| 决策 | 选择 | 理由 | 备选方案 | 否决原因 |
|------|------|------|----------|----------|
| Token 存储方式 | 仅 MySQL | 一期不引入 Redis，简化架构 | MySQL + Redis 双层 | 暂不需要高并发缓存优化 |
| Token 加密方案 | Fernet 对称加密 | Django 生态支持，安全性高 | AES-256 | 需要额外依赖，实现复杂 |
| 关联幂等策略 | 唯一约束 + upsert | 数据库层面保证，简单可靠 | 应用层去重 | 并发时可能重复插入 |

### 3.3 行为差异对照表

| 场景 | AS-IS | TO-BE | 影响 |
|------|-------|-------|------|
| 项目关联 | 无关联关系 | 自动关联 TAPD 项目 | 新增功能 |
| Token 存储 | 无 Token 存储 | 加密存储用户 Token | 新增功能 |
| Token 刷新 | 无刷新机制 | 异步刷新 Token | 新增功能 |

---

## ★ 4b. 数据模型

### 4b.1 持久化结构

> **文件位置**：`bkmonitor/bkmonitor/models/tapd.py`（新建文件），并在同目录 `__init__.py` 中加入 `from .tapd import *`

> **继承基类**：`bkmonitor/utils/model_manager.py` → `class AbstractRecordModel(models.Model)`  
> **参考实现**：`bkmonitor/bkmonitor/models/strategy.py` → `class UserGroup(AbstractRecordModel)`  
> **QuerySet 行为**：`objects` 默认过滤已删除记录；`origin_objects` 用于跨表全量查询

```python
# bkmonitor/bkmonitor/models/tapd.py
from django.db import models

from bkmonitor.utils.model_manager import AbstractRecordModel

__all__ = ["TapdWorkspaceBinding", "UserTapdToken"]


class TapdWorkspaceBinding(AbstractRecordModel):
    """TAPD 项目关联表"""
    space_id = models.IntegerField("蓝鲸业务空间ID")
    bk_biz_id = models.IntegerField("蓝鲸CMDB业务ID")
    tapd_workspace_id = models.CharField("TAPD项目ID", max_length=64)
    tapd_workspace_name = models.CharField("TAPD项目名称", max_length=255)
    # creator 由 AbstractRecordModel 的 create_user 自动提供，无需声明

    class Meta:
        db_table = "tapd_workspace_binding"
        unique_together = [("space_id", "tapd_workspace_id")]
        verbose_name = "TAPD项目关联"
        verbose_name_plural = "TAPD项目关联"
        # AbstractRecordModel 自动提供 ordering = ("-create_time",) 等指标


class UserTapdToken(AbstractRecordModel):
    """用户 TAPD Token 表"""
    username = models.CharField("用户username", max_length=128, unique=True, help_text="蓝鲸登录用户名（request.user.username），不是 TAPD 用户名")
    tapd_user_id = models.CharField("TAPD用户ID", max_length=128, blank=True, default="", help_text="TAPD OAuth 返回的 resource.user_id，用于关联 BK 用户与 TAPD 用户身份")
    access_token = models.TextField("TAPD用户态token", help_text="加密存储")
    refresh_token = models.TextField("TAPD刷新token", null=True, blank=True, help_text="加密存储")
    token_type = models.CharField("token类型", max_length=32, default="Bearer")
    expires_at = models.DateTimeField("过期时间")
    refresh_time = models.DateTimeField("上次刷新时间", null=True, blank=True, help_text="最近一次通过refresh_token刷新成功的时间")

    class Meta:
        db_table = "user_tapd_token"
        verbose_name = "用户TAPD Token"
        verbose_name_plural = "用户TAPD Token"
```

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

**`UserTapdToken` 自定义字段说明**：

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `username` | `CharField(128)` | 必填, **唯一** | 用户 username |
| `tapd_user_id` | `CharField(128)` | blank=True, default="" | TAPD OAuth 返回的 `resource.user_id`，用于关联 BK 用户与 TAPD 用户身份；首次授权时写入，后续刷新时不变 |
| `access_token` | `TextField` | 必填 | TAPD 用户态 access_token，**加密存储** |
| `refresh_token` | `TextField` | null=True, blank=True | TAPD 刷新 token，**加密存储**，可选 |
| `token_type` | `CharField(32)` | 默认 `Bearer` | Token 类型 |
| `expires_at` | `DateTimeField` | 必填 | access_token 过期时间 |
| `refresh_time` | `DateTimeField` | null=True, blank=True | 最近一次 refresh_token 刷新成功的时间；**仅刷新成功时更新**，与 `update_time` 解耦，用于防重复刷新判断 |

> 注意：`update_time` 由 `AbstractRecordModel.auto_now` 维护，任何 `save()` 都会更新；`refresh_time` 仅在异步刷新成功时显式更新，避免非刷新操作导致防重刷误判。

**`AbstractRecordModel` 提供的核心能力**：

1. **`save()` 自动审计** — 保存时自动填充 `create_user` / `update_user`（从 `get_global_user()` 获取当前线程用户）
2. **软删支持** — `instance.delete()` 行为：将 `is_deleted=True`、`is_enabled=False`，并记录更新人和更新时间；`instance.delete(hard=True)` 物理删除
3. **默认过滤已删除** — `TapdWorkspaceBinding.objects.all()` 自动附加 `is_deleted=False` 过滤条件，避免查脏数据
4. **全量查询器** — `TapdWorkspaceBinding.origin_objects.all()` 返回含软删记录的全量数据，适用于跨模型级联校验
5. **`TTLCacheManager` 兼容** — 继承后自动支持缓存管理器混合，提高高频查询性能（可选）

### 4b.2 传输/中间结构

```python
# 序列化器定义（仅用于内部数据校验，secret 字段永不对外暴露）
class TapdWorkspaceBindingSerializer(serializers.ModelSerializer):
    """TAPD 项目关联序列化器"""
    class Meta:
        model = TapdWorkspaceBinding
        fields = [
            "id", "space_id", "bk_biz_id",
            "tapd_workspace_id", "tapd_workspace_name",
            "create_user", "create_time", "update_time",
        ]
        read_only_fields = ["id", "create_user", "create_time", "update_time"]


class UserTapdTokenSerializer(serializers.ModelSerializer):
    """用户 TAPD Token 序列化器 —— 不暴露任何 secret 字段"""
    class Meta:
        model = UserTapdToken
        fields = [
            "id", "username", "tapd_user_id", "token_type", "expires_at",
            "is_enabled", "create_time", "update_time",
        ]
        # access_token / refresh_token 不暴露
```

---

## +10. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| 数据库 | 数据变更 | 新增 2 张表 | 否 |
| Django ORM | 接口变更 | 新增 2 个 Model 类 | 否 |
| Migration | 数据变更 | 新增 Migration 文件 | 否 |

---

## +11. 待定问题

| 编号 | 问题 | 影响范围 | 建议决策时间 | 负责人 |
|------|------|---------|------------|--------|
| ~~T-01~~ | ~~Token 加密算法选型~~ | — | ✅ **已解决** | — |
| T-02 | 数据库索引优化策略 | S-01 | 实施阶段 | DBA |
