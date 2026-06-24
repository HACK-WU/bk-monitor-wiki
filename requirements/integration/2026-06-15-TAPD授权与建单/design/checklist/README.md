# TAPD 授权与建单 — 实施 Checklist

> 设计文档：`2026-06-15-TAPD授权与建单/design/`
> 子需求：S-01 ~ S-04, S-06（S-05 迁移已合并入各子需求，S-07 已删除）
> 生成时间：2026-06-24

---

## 批次总览

| 批次 | 子需求 | 范围 | 条目数 | 前置批次 | 锚点文件 |
|------|--------|------|--------|----------|----------|
| **B01** | S-01 | 数据模型设计 + Redis Token 工具 + 四态定义 | 13 | — | [B01.md](B01.md) |
| **B02** | S-02 | 用户态授权（B-05 回调 + `generate_auth_url` + `validate_state` + RequestTokenResource） | 9 | B01 | [B02.md](B02.md) |
| **B03** | S-03 | 应用态授权（B-03 回调 + `signed_state` 生成/验签 + GetWorkspaceInfoResource + upsert） | 10 | B01, B02 | [B03.md](B03.md) |
| **B04** | S-06 | 授权检查（`TapdRequiredPermission` + `generate_auth_url` 复用 + 异常） | 3 | B01, B02 | [B04.md](B04.md) |
| **B05** | S-04 | 查询项目列表（B-01 用户可见 + B-07 app 已授权 + 四态交叉 + install_url） | 15 | B01 ~ B04 | [B05.md](B05.md) |

> **⚠️ 隐式依赖**：B05 需要 B03（`generate_signed_state` 用于 `install_url`）和 B04（`TAPD_REQUIRED` Permission 挂载于 B-01）完成后才能实施。

---

## 全局约束（父文档 DESIGN.md）

以下约束贯穿所有批次，实施时须逐条检查：

- [ ] 模块路径：TAPD 资源统一承载在 `fta_web/issue/` 下，**不新建 `fta_web/tapd/`** § DESIGN.md §3 代码模块路径
- [ ] 表名：`tapd_workspace_binding`，裸 snake_case，**不加 `bkmonitor_` 前缀** § DESIGN.md §5
- [ ] Token 加密：统一使用 `AESCipher(key=settings.SECRET_KEY)`，**不传 IV** § DESIGN.md §4 / S-01 §4c
- [ ] 空间标识：接口统一使用 `space_uid`（全局唯一），废弃裸 `space_id` § DESIGN.md §4
- [ ] `is_bound` 四态：`bound` / `stale` / `importable` / `unbound`，**非布尔值** § DESIGN.md §4
- [ ] 全局风险缓解：TAPD OAuth 服务不可用 → 错误重试 + 降级提示 § DESIGN.md §4
- [ ] 全局风险缓解：数据库表结构变更 → Migration 版本控制 § DESIGN.md §4

---

## 使用方式

1. 按批次顺序实施（B01 → B02 → B03 & B04 并行 → B05）
2. 每批次完成后更新 `.requirements/integration/2026-06-15-TAPD授权与建单/implement-plan.md`
3. 每批次勾选完成后，用 `git diff --stat` 验证文件变动范围

---

## 设计文档锚点速查

| 锚点 | 文件 | 内容 |
|------|------|------|
| `S01-数据模型` | `S01_数据模型设计_DESIGN.md` | TapdWorkspaceBinding 模型、Redis Token 工具、四态定义 |
| `S02-用户态授权` | `S02_用户态授权_DESIGN.md` | B-05 回调、Session state、RequestTokenResource |
| `S03-应用态授权` | `S03_应用态授权_DESIGN.md` | B-03 回调、signed_state、GetWorkspaceInfoResource |
| `S04-查询项目列表` | `S04_查询项目列表_DESIGN.md` | B-01 / B-07 接口、四态交叉、install_url |
| `S06-授权检查` | `S06_查询授权状态_DESIGN.md` | TapdRequiredPermission、403 + auth_url |
