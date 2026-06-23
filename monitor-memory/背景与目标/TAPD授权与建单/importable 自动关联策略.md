---
groupPath: 背景与目标/TAPD授权与建单
relation: importable 自动关联策略
keywords: [后端静默绑定]
exportedAt: "2026-06-23T07:54:48.108Z"
---
## importable 自动关联策略（后端静默绑定）

### 设计决策
- **`importable` 状态由后端静默自动关联，无需新增前端接口**
- 调用 B-01 接口时，后端对每个 `importable` 项目自动尝试执行 `get_or_create TapdWorkspaceBinding`
- 关联成功 → 状态变为 `bound`（前端显示「已关联」）
- 关联失败 → 仍返回 `importable`（前端显示「去关联」）

### 业务背景
- TAPD 应用安装接口是「全部或部分」授权模式，无法精确控制单个项目权限
- 安装成功意味着「企业和项目的两套权限体系均已具备」，但不能保证当前请求所选的具体项目必然被授权
- 因此需要一种机制区分「权限已开但还需点一下关联」的场景（`importable`）和「完全没有关联过」（`unbound`）

### 前端行为
- 所有非 `bound` 状态（包括 `importable`、`unbound`、`stale`），前端统一显示「去关联」
- 「去关联」点击后调用 B-01 install_url 进行 TAPD 应用态授权

### 代码位置
- 见 B-01 接口实现：`try_bind_importable()` 遍历 items，逐项检测 `tapd_binding_id`
- `TapdWorkspaceBinding` 在 `bkmonitor/issue/models/non_priority/` 下定义