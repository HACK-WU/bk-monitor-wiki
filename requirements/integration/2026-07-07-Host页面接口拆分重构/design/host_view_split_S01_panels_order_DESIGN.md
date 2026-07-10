# S-01: 场景视图接口拆分（Panels / Order）

> **父需求**: REQ-20260707-001
> **子需求编号**: S-01

---

## 1. 术语

| 术语 | 含义 |
|------|------|
| `SceneView` | 场景视图模型，包含 `view_type`、`panels`、`order` 三个核心字段 |
| `get_auto_view_panels` | `HostBuiltinProcessor` 静态方法，入参 `(view_type, builtin_processor, params)`，返回 `(panels, order)` 元组 |
| `view_type` | 场景类型标识，`"host"` 或 `"process"` |

---

## 2. 现状（AS-IS）

### 2.1 现状描述

当前 `GetSceneViewResource` 通过 `HostBuiltinProcessor` 调用 `get_auto_view_panels`，返回完整的视图配置：

```
response = {
    "view_type": "host",
    "panels": [...],  # 图表面板列表
    "order": [...],   # 排序与显隐配置
}
```

**位置**：
- `scene_view/resources/view.py` → `GetSceneViewResource.perform_request()`（第 51-67 行）
- `scene_view/builtin/host.py` → `HostBuiltinProcessor.get_auto_view_panels()`（第 61-81 行）

### 2.2 痛点

- 前端首次加载 Host/Process 页面时，必须同时请求 `panels` + `order`，但实际渲染需要分先后：先 `panels`（决定展示哪些图表），后 `order`（决定排序和显隐）
- 进程详情页的面板配置当前无独立入口，只能通过 `get_scene_view` 传参 `view_type=process` 获取，前端难以缓存

---

## 3. 方案（TO-BE）

### 3.1 方案概述

为 `host` 和 `process` 两个 `view_type` 各新增 2 个 Resource：分别返回 `panels` 和 `order`。底层复用 `get_auto_view_panels`，仅在 `perform_request` 中按字段拆分。

> **性能备注**：4 个 Resource 各自调用 `get_auto_view_panels`（生成 panels + order），仅取其一丢弃另一。`get_auto_view_panels` 内部为静态配置生成（非 DB 查询），开销极低，无需优化。若未来生成成本增高，可考虑合并为 2 个接口（host / process 各一个，同时返回 panels 与 order）。

### 3.2 关键决策点

| 决策 | 选择 | 理由 | 备选方案 | 否决原因 |
|------|------|------|---------|---------|
| 是否复用 `get_auto_view_panels` | 复用，分别取 `[0]`/`[1]` | 零额外逻辑成本，返回结构完全一致 | 重写两个独立方法 | 重复代码，且无必要 |
| HTTP 方法 | POST（与前端 Wiki 对齐） | 前端 Service 层统一使用 POST 传参（body 传递 `bk_biz_id`/`id`） | GET | `get_scene_view` 本身亦为 POST，保持一致性 |
| endpoint 命名 | `get_host_views_panels`/`get_process_views_panels`/`get_host_views_panels_order`/`get_process_views_panels_order` | 与前端 Wiki 严格对齐 | 简写为 `host_panels` | 前端已按全称编码 |

### 3.3 目录结构

```
scene_view/
├── resources/
│   ├── view.py              # [修改] GetSceneViewResource 保持不变
│   └── host.py              # [修改] 新增 4 个 Resource 类
├── views.py                 # [修改] SceneViewViewSet 新增 4 条 ResourceRoute
└── builtin/
    └── host.py              # [复用] get_auto_view_panels 不变
```

---

## 4. 接口设计

### 4.1 对外接口

#### `get_host_views_panels`

| 属性 | 值 |
|------|-----|
| 方法 | POST |
| 路由 | `/scene_view/get_host_views_panels/` |
| Resource | `GetHostViewsPanelsResource` |

**Request**: `SceneViewRequestSerializer`（复用现有）

```json
{
  "bk_biz_id": 2,
  "id": 1
}
```

**Response Demo**:

```json
{
  "code": 200,
  "data": {
    "panels": [
      {"id": "cpu", "title": "CPU", "type": "line"},
      {"id": "mem", "title": "Memory", "type": "line"}
    ]
  },
  "message": "success"
}
```

#### `get_host_views_panels_order`

| 属性 | 值 |
|------|-----|
| 方法 | POST |
| 路由 | `/scene_view/get_host_views_panels_order/` |
| Resource | `GetHostViewsPanelsOrderResource` |

**Response Demo**:

```json
{
  "code": 200,
  "data": {
    "order": [
      {"id": "cpu", "index": 0, "hidden": false},
      {"id": "mem", "index": 1, "hidden": false}
    ]
  },
  "message": "success"
}
```

#### `get_process_views_panels`

| 属性 | 值 |
|------|-----|
| 方法 | POST |
| 路由 | `/scene_view/get_process_views_panels/` |
| Resource | `GetProcessViewsPanelsResource` |

**Response Demo**:

```json
{
  "code": 200,
  "data": {
    "panels": [
      {"id": "proc_cpu", "title": "Process CPU", "type": "line"}
    ]
  },
  "message": "success"
}
```

#### `get_process_views_panels_order`

| 属性 | 值 |
|------|-----|
| 方法 | POST |
| 路由 | `/scene_view/get_process_views_panels_order/` |
| Resource | `GetProcessViewsPanelsOrderResource` |

**Response Demo**:

```json
{
  "code": 200,
  "data": {
    "order": [
      {"id": "proc_cpu", "index": 0, "hidden": false}
    ]
  },
  "message": "success"
}
```

### 4.2 内部协作接口

无新增内部接口。4 个 Resource 均直接调用 `get_auto_view_panels` 并取对应字段。

### 4.3 契约变更声明

| 变更类型 | 接口 | 变更内容 |
|---------|------|---------|
| 新增 | `get_host_views_panels` | 从 `get_scene_view` `host` 视图拆分 panels |
| 新增 | `get_host_views_panels_order` | 从 `get_scene_view` `host` 视图拆分 order |
| 新增 | `get_process_views_panels` | 从 `get_scene_view` `process` 视图拆分 panels |
| 新增 | `get_process_views_panels_order` | 从 `get_scene_view` `process` 视图拆分 order |

---

## 5. 影响范围

| 影响对象 | 影响类型 | 影响描述 | 是否破坏性变更 |
|---------|---------|---------|:----------:|
| `scene_view/resources/host.py` | 文件新增 | 新增 4 个 Resource 类 | 否 |
| `scene_view/views.py` | 接口变更 | `SceneViewViewSet` 新增 4 条路由 | 否 |
| `get_scene_view` | 无影响 | 现有接口行为不变，仅新增拆分入口 | 否 |
