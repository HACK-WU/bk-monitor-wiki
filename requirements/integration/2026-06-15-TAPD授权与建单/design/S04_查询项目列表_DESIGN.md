---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-15
version: 1
tags: [feat, integration, design, S04]
depends_on: [S01, S02]
author: AI
document_type: design
parent: DESIGN.md
---

# S-04 查询项目列表

> 状态：设计中

---

## ★ 1. 术语

| 术语 | 含义 | 引用 |
|------|------|------|
| `is_bound` | 项目是否已关联到当前业务空间 | — |
| `page_size` | 分页大小，默认 20 | — |

---

## ★ 2. 现状（AS-IS）

### 2.1 现状描述

当前蓝鲸监控平台无法查询用户的 TAPD 项目列表。用户需要在 TAPD 系统中查看项目，然后手动在监控平台中配置关联。

### 2.2 痛点

- 痛点 1：用户需要在两个系统间切换，操作繁琐
- 痛点 2：无法在监控平台中查看哪些项目已关联
- 痛点 3：无法批量选择项目进行关联

---

## ★ 3. 方案（TO-BE）

### 3.1 方案概述

实现 B-01 接口，使用用户的 access_token 调用 TAPD API 获取项目列表，然后查询 `TAPD_WORKSPACE_BINDING` 表标记已关联状态，返回带关联状态的项目列表。

### 3.2 关键决策点

| 决策 | 选择 | 理由 | 备选方案 | 否决原因 |
|------|------|------|----------|----------|
| 分页策略 | 默认 page_size=20 | 平衡性能和用户体验 | 不分页 | 数据量大时性能差 |
| 关联状态标记 | 查询后合并 | 简单直接，不影响 TAPD API 调用 | TAPD API 返回时标记 | TAPD API 不支持 |
| Token 过期处理 | 删除过期记录 | 避免无效数据积累 | 保留记录 | 可能导致重复错误 |

### 3.3 行为差异对照表

| 场景 | AS-IS | TO-BE | 影响 |
|------|-------|-------|------|
| 项目查询 | 无查询功能 | 调用 TAPD API 查询 | 新增功能 |
| 关联状态 | 无状态标记 | 自动标记已关联项目 | 新增功能 |
| 分页查询 | 无分页 | 支持分页查询 | 新增功能 |

---

## ★ 4a. 接口设计

### 4a.1 对外接口

#### B-01 查询用户 TAPD 项目列表

```python
class ListTapdWorkspaceResource(Resource):
    """获取已授权的 TAPD 项目（workspace）列表
    
    挂载 `permission_classes = [TAPD_REQUIRED, IAMPermission]`，
    由 `TAPD_REQUIRED` 校验用户是否持有有效 Token（未授权时返回 403 + auth_url），
    `IAMPermission` 校验当前 space 的操作权限。
    """
    
    class RequestSerializer(serializers.Serializer):
        bk_biz_id = serializers.IntegerField(label="蓝鲸业务ID")
        page = serializers.IntegerField(label="页码", default=1)
        page_size = serializers.IntegerField(label="每页数量", default=20)
        include_bound_status = serializers.BooleanField(
            label="是否返回与监控的关联关系",
            default=True,
            help_text="true 时返回 is_bound（需额外查询 TAPD_WORKSPACE_BINDING）；false 时不返回，减少一次数据库查询"
        )
    
    class WorkspaceItemSerializer(serializers.Serializer):
        workspace_id = serializers.CharField(label="项目ID（workspace_id）")
        workspace_name = serializers.CharField(label="项目名称")
        is_bound = serializers.BooleanField(label="是否已关联到当前业务空间", required=False)
    
    class ResponseSerializer(serializers.Serializer):
        total = serializers.IntegerField(label="项目总数")
        items = serializers.ListField(
            label="项目列表",
            child=WorkspaceItemSerializer()
        )
        has_more = serializers.BooleanField(label="是否有更多")
        install_url = serializers.URLField(label="TAPD 项目安装授权URL", required=False)
    
    def perform_request(self, validated_request_data):
        # 1. 读取 USER_TAPD_TOKEN
        # 2. 解密 access_token
        # 3. 检查 token 是否过期
        # 4. 调用 TAPD API 获取用户可访问的 workspace 列表
        # 5. 若 include_bound_status=True：查询 TAPD_WORKSPACE_BINDING 标记关联状态
        # 6. 拼接 install_url（按统一格式 state="{nonce}:{bk_biz_id}" 写入 Session，与 S-02/S-03 共用同一套 Session key 命名规则 `tapd_oauth_state_{bk_biz_id}`）
        # 7. 返回带关联状态的项目列表 + install_url
        pass
```

> **返回信息补充说明**：接口返回的 `items` 中，**每个 workspace 同时携带项目基本信息（`workspace_id`、`workspace_name`）和当前业务空间的关联状态（`is_bound`）**。这种信息聚合方式避免了前端（或后续建单模块）单独调用"查询已关联项目"接口，降低了交互复杂度。

| 接口 | 输入 | 输出 | 异常 |
|------|------|------|------|
| B-01 查询项目列表 | `bk_biz_id, page, page_size` | `total, items(含is_bound), has_more, install_url` | `未授权, token过期, TAPD API异常` |

### 4a.2 内部协作接口

| 接口 | 调用方 | 被调用方 | 说明 |
|------|--------|----------|------|
| `get_user_token()` | B-01 | 数据库操作 | 获取用户 Token |
| `decrypt_token()` | B-01 | 加密模块 | 解密 access_token |
| `call_tapd_api()` | B-01 | TAPD API | 调用 TAPD 获取项目列表 |
| `get_bound_projects()` | B-01 | 数据库操作 | 查询已关联项目 |
| `generate_install_url()` | B-01 | 工具函数 | 按统一格式生成 state="{nonce}:{bk_biz_id}" 并写入 Session，拼接 install_url（与 S-02/S-03 共用同一套 Session key 命名规则） |

### 4a.3 契约变更声明

| 变更类型 | 接口 | 变更内容 | 影响的子需求 |
|---------|------|---------|------------|
| 新增 | B-01 查询项目列表 | 全新接口 | — |

---

## +6. 异常处理

| 场景 | 行为 | 是否对外暴露 |
|------|------|:----------:|
| Token 已过期 | PermissionDenied 403 + auth_url，前端跳转授权（Token 已过期被视为未授权） | 是 |
| TAPD API 权限不足 | 返回「无TAPD项目权限」错误码 | 是 |
| TAPD API 服务异常 | 返回「TAPD服务暂时不可用」错误码 | 是 |
| 用户无 TAPD 项目 | 返回空列表，前端展示「暂无项目」 | 否 |

---

## +10. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| `fta_web/tapd/` | 接口变更 | 新增 1 个 Resource | 否 |
| `urls.py` | 接口变更 | 新增 1 个 URL 路由 | 否 |
| 前端页面 | 行为变更 | 新增项目选择弹窗 | 否 |

---

## +11. 待定问题

| 编号 | 问题 | 影响范围 | 建议决策时间 | 负责人 |
|------|------|---------|------------|--------|
| T-01 | TAPD API 项目列表接口地址和参数 | S-04 | 实施前 | 后端开发 |
| T-02 | TAPD API 分页参数格式 | S-04 | 实施前 | 后端开发 |
| T-03 | 项目列表返回字段映射 | S-04 | 实施前 | 后端开发 |
