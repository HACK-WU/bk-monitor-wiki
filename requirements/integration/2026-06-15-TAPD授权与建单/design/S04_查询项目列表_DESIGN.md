---
id: REQ-20260615-001
feature: TAPD授权与建单
status: 设计中
created: 2026-06-15
updated: 2026-06-17
version: 2
tags: [feat, integration, design, S04]
depends_on: [S01, S02]
author: AI
document_type: design
parent: DESIGN.md
---

# S-04 查询项目列表

> 状态：已按设计评审结论（v1，2026-06-17）修订。
>
> **评审核心结论**：
> - 两个列表接口**必须区分、不可同名**：
>   - 「用户可见可挑」（冷启动去关联）→ 用户态 token（Redis）+ TAPD 用户态 API
>   - 「app 已授权」（日常下拉 + is_bound 兜底源）→ app 级 Basic + `get_granted_workspaces`
> - `is_bound` 从布尔值改为**四态**（`bound`/`stale`/`importable`/`unbound`）
> - 接口承载在 `fta_web/issue/` 下

---

## ★ 1. 术语

| 术语 | 含义 | 引用 |
|------|------|------|
| `bound` | 本地 binding 存在且 TAPD 已授权 | 本设计 §4b |
| `stale` | 本地 binding 存在但 TAPD 已解绑 | 本设计 §4b |
| `importable` | 本地 binding 不存在但 TAPD 已授权 | 本设计 §4b |
| `unbound` | 本地 binding 不存在且 TAPD 未授权 | 本设计 §4b |
| `page_size` | 分页大小，默认 20 | — |
| `selected_workspace_id` | TAPD 项目 ID，前端填入 `install_url` 的 `#fragment` | — |
| `install_url` | TAPD OAuth 跳转 URL，用于打开项目安装页面 | S-03 §4a |

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

**【评审后重大变更】**：原来只有「B-01 查询用户 TAPD 项目列表」一个接口，现拆分为**两个必须区分、不可同名的接口**：

| 接口 | 用途 | 鉴权 | 数据源 |
|------|------|------|--------|
| **B-01 查询用户可见 TAPD 项目**（改名） | 冷启动去关联时，展示用户有权限的 TAPD 项目 | 用户态 token（Redis 解密） | TAPD 用户态 API |
| **B-07 查询 app 已授权 TAPD 项目**（新增/现网改名） | 日常建单下拉、is_bound 兜底源 | app 级 Basic Auth | `get_granted_workspaces` |

**`is_bound` 从布尔值改为四态**：结合本地 binding 状态和 TAPD `get_granted_workspaces` 返回，给出精确状态。

### 3.2 关键决策点

| 决策 | 选择 | 理由 | 备选方案 | 否决原因 |
|------|------|------|----------|----------|
| 列表接口数量 | **2 个（必须区分）** | N1：避免同名资源冲突，职责清晰 | 1 个接口 | 评审否决 |
| B-01 数据源 | TAPD 用户态 API（Bearer Token） | 冷启动时用户需看到自己有权限的项目 | `get_granted_workspaces` | 只能返回 app 已授权，看不到用户有权限但未授权给 app 的项目 |
| B-07 数据源 | `get_granted_workspaces`（Basic Auth） | 日常下拉只需 app 已授权项目，与该接口职责对齐 | TAPD 用户态 API | 超出职责范围 |
| `is_bound` 语义 | **四态（bound/stale/importable/unbound）** | 精确反映本地 binding 与 TAPD 授权的交叉状态 | 布尔值 | 无法区分 stale/importable |
| 分页策略 | 默认 page_size=20 | 平衡性能和用户体验 | 不分页 | 数据量大时性能差 |

### 3.3 `is_bound` 四态详细定义

| 本地 binding | TAPD `get_granted_workspaces` | 状态 | 前端语义 | 操作 |
|:---:|:---:|---|---|---|
| ✓ | ✓ | `bound` | 已关联 | 可建单/已建单 |
| ✓ | ✗ | `stale` | TAPD 侧已解绑，需重关联 | 标记异常，提示重新关联 |
| ✗ | ✓ | `importable` | TAPD 已装应用，可一键回填本地 | 提供「一键关联」按钮 |
| ✗ | ✗ | `unbound` | 未关联 | 提供「去关联」入口 |

- B-01（用户态列表）：TAPD 用户态 API 返回用户可见项目 → 与本地 binding 交叉 → 返回四态
- B-07（app 已授权列表）：`get_granted_workspaces` 返回 app 已授权 → 与本地 binding 交叉 → 主要返回 `bound`/`importable`

### 3.4 行为差异对照表

| 场景 | AS-IS | TO-BE | 影响 |
|------|-------|-------|------|
| 项目查询 | 无查询功能 | 2 个独立接口，职责清晰 | 新增功能 |
| 关联状态 | 无状态标记 | **四态精确标记** | 新增功能 |
| 分页查询 | 无分页 | 支持分页查询 | 新增功能 |

---

## ★ 4a. 接口设计

### 4a.1 对外接口

#### B-01 查询用户可见 TAPD 项目列表（冷启动去关联）

> **【评审后】接口改名**：原 `ListTapdWorkspaceResource` 改为 `ListUserVisibleTapdWorkspaceResource`，避免与 B-07 同名。

```python
class ListUserVisibleTapdWorkspaceResource(Resource):
    """查询当前用户有权限的 TAPD 项目列表（冷启动去关联用）
    
    挂载 permission_classes = [TAPD_REQUIRED, IAMPermission]，
    由 TAPD_REQUIRED 校验用户是否持有有效 Token（未授权时返回 403 + auth_url），
    IAMPermission 校验当前 space 的操作权限。
    
    数据源：TAPD 用户态 API（Bearer Token，从 Redis 解密获取）。
    """
    
    class RequestSerializer(serializers.Serializer):
        bk_biz_id = serializers.IntegerField(label="蓝鲸业务ID")
        page = serializers.IntegerField(label="页码", default=1)
        page_size = serializers.IntegerField(label="每页数量", default=20)
    
    class WorkspaceItemSerializer(serializers.Serializer):
        workspace_id = serializers.CharField(label="项目ID")
        workspace_name = serializers.CharField(label="项目名称")
        is_bound = serializers.ChoiceField(
            label="关联状态",
            choices=["bound", "stale", "importable", "unbound"]
        )
    
    class ResponseSerializer(serializers.Serializer):
        total = serializers.IntegerField(label="项目总数")
        items = serializers.ListField(
            label="项目列表",
            child=WorkspaceItemSerializer()
        )
        has_more = serializers.BooleanField(label="是否有更多")
        install_url = serializers.CharField(
            label="TAPD 项目安装授权URL模板",
            required=False,
            help_text="占位符 {workspace_id} 由前端替换"
        )
        method = serializers.ChoiceField(
            label="install_url 的请求方式",
            choices=["GET"],
            default="GET",
            required=False
        )
    
    def perform_request(self, validated_request_data):
        # 1. 从 Redis 读取用户 token（tapd_uat:{tenant}:{user}）
        # 2. AESCipher 解密 access_token
        # 3. 检查 token 是否过期（Redis TTL 已保证，但做兜底检查）
        # 4. 调用 TAPD 用户态 API 获取用户可访问的 workspace 列表
        # 5. 查本地 TAPD_WORKSPACE_BINDING（按 bk_tenant_id + space_uid）
        # 6. 调 get_granted_workspaces（app 级 Basic，带短 TTL 缓存）
        # 7. 交叉标记四态 is_bound
        # 8. 【S-03】拼接 install_url：后端预写 open_app_install 固定 URL
        # 9. 返回带四态的项目列表 + install_url
        pass
```

> **Demo API 返回示例**：
> ```json
> {
>   "total": 3,
>   "items": [
>     {
>       "workspace_id": "69990779",
>       "workspace_name": "蓝鲸监控项目",
>       "is_bound": "bound"
>     },
>     {
>       "workspace_id": "69990780",
>       "workspace_name": "TAPD测试项目",
>       "is_bound": "unbound"
>     },
>     {
>       "workspace_id": "69990781",
>       "workspace_name": "运维自动化项目",
>       "is_bound": "stale"
>     }
>   ],
>   "install_url": "https://tapd.woa.com/oauth/open_app_install?client_id=bkmonitor_tapd&test=1&cb=https://monitor.bk.example.com/fta/issue/tapd/app_install_callback/&state=n0nc3#selected_workspace_id={workspace_id}",
>   "method": "GET"
> }
> ```

> **`install_url` 与 `method` 说明**：
> - `install_url` 为 TAPD 应用安装 URL **模板**（`open_app_install`）
> - 后端预写：`client_id`、`test`、`cb`（回跳 URL，URL encode）、`state`（透传参数，TAPD 原样带回回调）
> - 仅 `#selected_workspace_id={workspace_id}` 需要前端替换为实际项目 ID
> - 示例：`https://tapd.woa.com/oauth/open_app_install?client_id=bkmonitor_tapd&test=1&cb=xxx&state=n0nc3#selected_workspace_id=10104091`

| 接口 | 输入 | 输出 | 异常 |
|------|------|------|------|
| B-01 查询用户可见项目 | `bk_biz_id, page, page_size` | `total, items(含四态is_bound), has_more, install_url, method` | `未授权, token过期, TAPD API异常` |

---

#### B-07 查询 app 已授权 TAPD 项目列表（日常下拉）

> **【评审后新增/改名】**：现网已有 `ListTapdWorkspaceResource`（`issue/resources.py:1302`），需**改名区分**。

```python
class ListGrantedTapdWorkspaceResource(Resource):
    """查询 app 级已授权的 TAPD 项目列表（日常建单下拉用）
    
    数据源：get_granted_workspaces（app 级 Basic Auth）
    用途：日常建单时选择 TAPD 项目，无需用户态 OAuth。
    """
    
    class RequestSerializer(serializers.Serializer):
        bk_biz_id = serializers.IntegerField(label="蓝鲸业务ID")
        page = serializers.IntegerField(label="页码", default=1)
        page_size = serializers.IntegerField(label="每页数量", default=20)
    
    class WorkspaceItemSerializer(serializers.Serializer):
        workspace_id = serializers.CharField(label="项目ID")
        workspace_name = serializers.CharField(label="项目名称")
        is_bound = serializers.ChoiceField(
            label="关联状态",
            choices=["bound", "stale", "importable", "unbound"]
        )
    
    class ResponseSerializer(serializers.Serializer):
        total = serializers.IntegerField(label="项目总数")
        items = serializers.ListField(
            label="项目列表",
            child=WorkspaceItemSerializer()
        )
        has_more = serializers.BooleanField(label="是否有更多")
    
    def perform_request(self, validated_request_data):
        # 1. 调用 get_granted_workspaces（app 级 Basic Auth）
        #    按 space/app 维度加短 TTL 缓存（现网已是 10 并发 fan-out）
        # 2. 查本地 TAPD_WORKSPACE_BINDING（按 bk_tenant_id + space_uid）
        # 3. 交叉标记四态 is_bound
        # 4. 返回带四态的项目列表
        pass
```

| 接口 | 输入 | 输出 | 异常 |
|------|------|------|------|
| B-07 查询 app 已授权项目 | `bk_biz_id, page, page_size` | `total, items(含四态is_bound), has_more` | `TAPD API异常` |

### 4a.2 内部协作接口

| 接口 | 调用方 | 被调用方 | 说明 |
|------|--------|----------|------|
| `get_tapd_token()` | B-01 | Redis 操作 | 从 Redis 读取并解密用户 token |
| `call_tapd_user_api()` | B-01 | TAPD API | 用 Bearer Token 调 TAPD 获取用户项目列表 |
| `get_granted_workspaces()` | B-07 | TAPD API | `GET /workspaces/get_granted_workspaces`（Basic Auth） |
| `get_workspace_bindings()` | B-01, B-07 | 数据库操作 | 查询本地 TAPD_WORKSPACE_BINDING |
| `generate_install_url()` | B-01 | 工具函数 | 预写 `open_app_install` URL 模板，含 `#selected_workspace_id` 占位符 |
| `compute_bound_status()` | B-01, B-07 | 工具函数 | 本地 binding × TAPD 授权状态 → 四态 |

### 4a.3 契约变更声明

| 变更类型 | 接口 | 变更内容 | 影响的子需求 |
|---------|------|---------|------------|
| 新增 | B-01 ListUserVisibleTapdWorkspaceResource | 全新接口（改名自原 ListTapdWorkspaceResource） | — |
| 新增 | B-07 ListGrantedTapdWorkspaceResource | 全新接口（app 已授权列表，改名自现网 ListTapdWorkspaceResource） | — |
| 修改 | `is_bound` 字段类型 | `BooleanField` → `ChoiceField`（四态） | B-01, B-07 |

---

## +6. 异常处理

| 场景 | 行为 | 是否对外暴露 |
|------|------|:----------:|
| Token 已过期（B-01） | PermissionDenied 403 + auth_url，前端跳转授权 | 是 |
| TAPD API 权限不足（B-01） | 返回「无TAPD项目权限」错误码 | 是 |
| TAPD API 服务异常 | 返回「TAPD服务暂时不可用」错误码 | 是 |
| 用户无 TAPD 项目 | 返回空列表，前端展示「暂无项目」 | 否 |
| get_granted_workspaces 超时（B-07） | 返回缓存数据或友好错误码 | 是 |

---

## +10. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| `fta_web/issue/` | 接口变更 | 新增 2 个 Resource（B-01、B-07） | 否 |
| `issue/resources.py` | 接口变更 | 现网 `ListTapdWorkspaceResource` 需改名区分 | ⚠️ 注意兼容 |
| `urls.py` | 接口变更 | 新增 2 个 URL 路由 | 否 |
| 前端页面 | 行为变更 | 新增项目选择弹窗，四态展示 | 否 |

---

## +11. 待定问题

| 编号 | 问题 | 影响范围 | 建议决策时间 | 负责人 |
|------|------|---------|------------|--------|
| T-01 | TAPD 用户态 API 项目列表接口地址和参数 | S-04 | 实施前 | 后端开发 |
| T-02 | get_granted_workspaces 短 TTL 缓存策略 | S-04, B-07 | 实施前 | 后端开发 |
| T-03 | `bk_biz_id → space_uid` 映射（get_space_map） | S-04 | 实施前 | 后端开发 |
