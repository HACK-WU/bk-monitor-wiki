# Skeleton Status — REQ-20260630-001

> design-to-code 骨架生成状态跟踪文件
> 总子需求数: 5 (REQ-01 ~ REQ-05)
> 文件分批数: 1（子需求简单，单批次一次性生成）
> **编码完成时间**: 2026-06-30

---

## 批次 0

### 批次元信息

| 键 | 值 |
|---|---|
| 批次号 | 0 |
| 批次描述 | 全部 5 个子需求一次性生成 + code-implement 填充完成 |
| 目标文件 | 5 个 |
| 状态 | ✅ 已完成 |

### 骨架对应清单（已编码验证）

| 需求项 | 涉及文件 | 状态 |
|---|---|---|
| REQ-01 (S-01) 新增 TapdWorkspaceManualUnbind 模型 | models/tapd.py | ✅ 完成 |
| REQ-01 (S-01) models/__all__ 追加导出 | models/tapd.py | ✅ 完成 |
| REQ-02 (S-01) 状态常量增加 MANUALLY_UNBOUND | constants.py | ✅ 完成 |
| REQ-03 (S-02) UnbindTapdWorkspaceResource 追加 tombstone | resources.py | ✅ 完成 |
| REQ-03 (S-03) _mark_bind_status 四态→五态 | resources.py | ✅ 完成 |
| REQ-03 (S-03) try_bind_importable 增加 tombstone 检查 | utils/tapd.py | ✅ 完成 |
| REQ-04 (S-04) 新增 RebindTapdWorkspaceResource | resources.py | ✅ 完成 |
| REQ-04 (S-05) 新增 RevokeTapdUserAuthResource | resources.py | ✅ 完成 |
| REQ-04 (S-05) views.py 注册新路由 | views.py | ✅ 完成 |
| REQ-05 (S-06) 新增 is_manually_unbound 辅助函数 | utils/tapd.py | ✅ 完成 |

---

## 编码实施验证清单

### 批次 1: utils/tapd.py

| 检查项 | 结果 | 详情 |
|---|---|---|
| `is_manually_unbound()` 从 `return False` 替换为真实 ORM 查询 | ✅ | `TapdWorkspaceManualUnbind.objects.filter(...).exists()` |
| `try_bind_importable()` tombstone guard 清理 TODO 注释 | ✅ | 保留业务注释，删除骨架 TODO |
| TapdWorkspaceManualUnbind 已导入 | ✅ | 已存在 via `from bkmonitor.models import ...` |

### 批次 2: resources.py

| 检查项 | 结果 | 详情 |
|---|---|---|
| `is_manually_unbound` 已导入 | ✅ | 追加到第 55 行 tapd utils import 列表 |
| `get_request_tenant_id` 已导入 | ✅ | 追加到第 35 行 request utils import 列表 |
| `_mark_bind_status()` 新增 `tombstone_ids` 参数 | ✅ | 函数签名 + 调用处均更新 |
| `_mark_bind_status()` 五态逻辑（manually_unbound） | ✅ | `ws_id in tombstone_ids` 判定 |
| 批量 tombstone 查询（N+1 防护） | ✅ | `ListUserTapdWorkspaceResource.perform_request()` loop 外批量查询 |
| S-02 Unbind tombstone 写入 | ✅ | `TapdWorkspaceManualUnbind.objects.get_or_create(...)` → `binding_qs.delete()` |
| S-04 Rebind 完整实现 | ✅ | 验重 → 删 tombstone → Basic Auth 查 info → create binding → return workspace |
| S-05 Revoke 完整实现 | ✅ | get_request_username + get_request_tenant_id → delete_tapd_token |
| 语法正确 | ✅ | `python -m ast.parse` 通过 |
| 所有 S-01~S-06 TODO 清除 | ✅ | `grep` 确认无遗留 |

### 其他文件

| 检查项 | 结果 |
|---|---|
| models/tapd.py S-01 TODO 注释清理 | ✅ |
| constants.py MANUALLY_UNBOUND | ✅ |
| views.py 路由注册 | ✅ |

---

## 全局清单对比（最终验证）

| 序号 | 全局需求 (Sub-REQ) | 实现位置 | 备注 |
|---|---|---|---|
| 1 | REQ-01 S-01 tombstone 模型 | models/tapd.py:45-67 | 含 Meta.unique_together |
| 2 | REQ-01 S-01 __all__ 追加 | models/tapd.py:16 | TapdWorkspaceManualUnbind 已导出 |
| 3 | REQ-02 状态常量增加 | constants.py:773 | MANUALLY_UNBOUND = "manually_unbound" |
| 4 | REQ-03 S-02 Unbind + tombstone | resources.py:2736-2746 | get_or_create + delete（有序） |
| 5 | REQ-03 S-03 _mark_bind_status 五态 | resources.py:2682-2695 | tombstone_ids set 传入，in 判定 |
| 6 | REQ-03 S-03 try_bind_importable tombstone | utils/tapd.py:347-350 | 调用 is_manually_unbound |
| 7 | REQ-04 S-04 RebindTapdWorkspaceResource | resources.py:2766-2812 | 含验重、删 tombstone、查 info、创建 binding |
| 8 | REQ-04 S-05 RevokeTapdUserAuthResource | resources.py:2821-2838 | get_request_username + get_request_tenant_id + delete_tapd_token |
| 9 | REQ-04 S-05 views.py 路由注册 | views.py:201-205 | POST /tapd/unbind_workspace、/tapd/rebind_workspace、/tapd/revoke_auth |
| 10 | REQ-05 S-06 is_manually_unbound | utils/tapd.py:309-319 | ORM filter exists() |

---

## 状态

✅ **编码完成** — 所有批次已填充，所有 TODO 清除，通过语法检查，可进入：
- 数据库迁移（`makemigrations` 生成 TapdWorkspaceManualUnbind 表）
- 前端适配（新增 `manually_unbound` 状态展示 + 重新关联按钮）
- 集成测试
