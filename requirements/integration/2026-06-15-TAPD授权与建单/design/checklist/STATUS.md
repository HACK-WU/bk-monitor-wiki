# Checklist 实施状态

> 更新规则：每完成一个批次，将对应 status 改为 `done`，并追加完成时间与 commit hash。

| 批次 | 子需求 | 范围 | 条目数 | status | 完成时间 | commit |
|------|--------|------|--------|--------|----------|--------|
| B01 | S-01 | 数据模型设计 + Redis Token 工具 + 四态定义 | 13 | `todo` | — | — |
| B02 | S-02 | 用户态授权（B-05 回调 + generate_auth_url + validate_state + RequestTokenResource） | 9 | `todo` | — | — |
| B03 | S-03 | 应用态授权（B-03 回调 + signed_state 生成/验签 + GetWorkspaceInfoResource + upsert） | 10 | `todo` | — | — |
| B04 | S-06 | 授权检查（TapdRequiredPermission + generate_auth_url 复用 + 异常） | 3 | `todo` | — | — |
| B05 | S-04 | 查询项目列表（B-01 用户可见 + B-07 app 已授权 + 四态交叉 + install_url） | 15 | `todo` | — | — |

## 批次依赖图

```
B01 (S-01 数据模型)
  ├──→ B02 (S-02 用户态授权)
  │      ├──→ B03 (S-03 应用态授权) ─┐
  │      └──→ B04 (S-06 授权检查) ───┤
  │                                   ↓
  └─────────────────────────────────→ B05 (S-04 查询列表)
```

## 全局约束检查清单（所有批次共用）

- [ ] 模块路径：`fta_web/issue/` 下，不新建 `fta_web/tapd/` § DESIGN.md §3
- [ ] 表名：`tapd_workspace_binding`，裸 snake_case § DESIGN.md §5
- [ ] Token 加密：`AESCipher(key=settings.SECRET_KEY)`，不传 IV § DESIGN.md §4
- [ ] 空间标识：接口统一使用 `space_uid` § DESIGN.md §4
- [ ] `is_bound`：四态 `bound/stale/importable/unbound` § DESIGN.md §4
