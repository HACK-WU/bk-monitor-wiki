---
id: REQ-20260729-001
feature: 移动端维度屏蔽支持regex规则
status: 已确认
created: 2026-07-29
updated: 2026-07-29
version: 1
tags: [feat, integration]
depends_on: []
author: AI
document_type: requirement
---

# 移动端维度屏蔽支持 regex 规则

## 一、背景与目标

### 1.1 背景

当前移动端快捷屏蔽（`QuickShield`）仅支持三种屏蔽类型：

- `scope`：按范围屏蔽（实例/IP/节点/动态分组）
- `strategy`：按策略屏蔽
- `event`/`alert`：按告警事件屏蔽，基于告警维度生成精确匹配条件

同时，Web 端的完整屏蔽（`add_shield`）已经支持维度屏蔽（`dimension`），并且 `dimension_conditions` 中支持 `eq`、`neq`、`gte`、`gt`、`lt`、`lte` 等操作符。底层引擎 `ShieldObj` 已经通过 `CONDITION_CLASS_MAP` 支持 `reg`/`nreg`（正则/非正则匹配）。

### 1.2 目标

让移动端快捷屏蔽入口支持按维度创建屏蔽规则，并支持 `regex`/`nregex`（正则/非正则）匹配方式；同时改造告警详情接口 `get_event_detail`，使其能够返回当前告警命中的屏蔽规则摘要信息，供移动端屏蔽详情页展示。

## 二、需求范围

### 2.1 纳入范围

1. 移动端快捷屏蔽新增 `dimension` 类型支持。
2. 维度屏蔽条件支持 `regex`（正则匹配）和 `nregex`（非正则匹配）两种方法。
3. 改造 `weixin/rest/v1/event/get_event_detail` 接口，返回命中屏蔽规则的摘要信息。
4. 展示层补充 `regex`/`nregex` 的友好符号显示。

### 2.2 不纳入范围

1. Web 端完整屏蔽的现有逻辑保持不变（已支持 dimension 类型，但前端未启用 regex）。
2. 屏蔽匹配引擎核心逻辑保持不变（已支持 reg/nreg）。
3. 不新增独立的"屏蔽规则详情"接口，详情数据复用 `get_event_detail` 返回。

## 三、功能需求

### 3.1 移动端快捷屏蔽支持 dimension 类型

#### 3.1.1 接口信息

- **接口**：`POST /weixin/rest/v1/event/quick_shield/`
- **处理类**：`packages/weixin/event/resources.py` 中的 `QuickShield` 资源

#### 3.1.2 请求参数扩展

在现有 `type` 参数基础上新增对 `dimension` 类型的支持；`dimension_config` 参数结构参考 Web 端 `add_shield` 的 `dimension` 类型：

```json
{
  "bk_biz_id": 2,
  "type": "dimension",
  "dimension_config": {
    "dimension_conditions": [
      {
        "key": "bk_target_ip",
        "value": ["10\\.0\\..*"],
        "method": "regex",
        "condition": "and"
      }
    ]
  },
  "begin_time": "2026-07-29 10:00:00",
  "end_time": "2026-07-29 12:00:00",
  "cycle_config": {...},
  "description": "移动端维度正则屏蔽"
}
```

#### 3.1.3 method 取值

| method | 含义 | 引擎侧映射 |
|--------|------|-----------|
| `eq` | 等于 | `EqualCondition` |
| `neq` | 不等于 | `NotEqualCondition` |
| `regex` | 正则匹配 | `RegularCondition` |
| `nregex` | 非正则匹配 | `NotRegularCondition` |

> 注：当前 Web 端完整屏蔽序列化器 `DimensionSerializer` 的 `method` 枚举可能未包含 `regex`/`nregex`，需要同步扩展。

#### 3.1.4 处理流程

1. `QuickShield` 接收移动端请求。
2. 当 `type == "dimension"` 时，调用 `AddShieldResource.handle_dimension` 逻辑构造 `dimension_config`。
3. 生成 `category = "dimension"` 的 `Shield` 记录。

### 3.2 get_event_detail 返回命中规则信息

#### 3.2.1 接口信息

- **接口**：`GET/POST /weixin/rest/v1/event/get_event_detail/`
- **处理类**：`packages/weixin/event/resources.py` 中的 `GetEventDetail` 资源

#### 3.2.2 返回字段扩展

在现有返回结构基础上新增 `shield_info` 字段：

```json
{
  "is_shielded": true,
  "shield_type": "saas_config",
  "shield_info": {
    "id": 123,
    "category": "dimension",
    "description": "移动端维度正则屏蔽",
    "begin_time": "2026-07-29 10:00:00",
    "end_time": "2026-07-29 12:00:00",
    "cycle_config": {...},
    "dimension_config": {
      "dimension_conditions": [...]
    },
    "content": "bk_target_ip regex 10\\.0\\..*"
  }
}
```

#### 3.2.3 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `shield_info.id` | int | 命中的屏蔽规则 ID |
| `shield_info.category` | string | 规则分类：scope/strategy/alert/dimension |
| `shield_info.description` | string | 规则描述 |
| `shield_info.begin_time` | string | 规则开始时间 |
| `shield_info.end_time` | string | 规则结束时间 |
| `shield_info.cycle_config` | object | 周期配置 |
| `shield_info.dimension_config` | object | 规则维度条件 |
| `shield_info.content` | string | 规则内容展示文本，复用 `BaseShieldDisplayManager.get_shield_content` 生成 |

#### 3.2.4 处理流程

1. `GetEventDetail` 获取告警详情后，判断 `alert.is_shielded`。
2. 若已屏蔽，调用 `AlertShieldConfigShielder(alert.to_document())` 获取命中的规则 ID。
3. 查询 `Shield` 模型，组装 `shield_info` 返回。
4. 若未命中任何规则，`shield_info` 为空对象或不返回。

## 四、非功能需求

### 4.1 性能

- `get_event_detail` 增加屏蔽规则匹配查询，需确保在告警详情高频查询场景下性能可控。
- 建议仅在 `is_shielded == true` 时执行命中规则查询。

### 4.2 兼容性

- 保持 `is_shielded` 和 `shield_type` 字段不变，新增 `shield_info` 为可选字段。
- 移动端旧版本未使用 `shield_info` 时不影响功能。

### 4.3 安全性

- `dimension_config` 中的正则表达式仅用于匹配，不允许执行任意代码。
- 移动端接口需保持现有权限校验（`AlertPermissionResource`）。

## 五、影响范围

| 模块 | 文件路径 | 影响说明 |
|------|----------|----------|
| 移动端接口 | `packages/weixin/event/resources.py` | 扩展 `QuickShield` 和 `GetEventDetail` |
| 屏蔽序列化器 | `packages/monitor_web/shield/serializers/` | 扩展 `DimensionSerializer` 的 method 枚举 |
| 屏蔽处理资源 | `packages/monitor_web/shield/resources/backend_resources.py` | 复用 `handle_dimension` |
| 屏蔽展示工具 | `bkmonitor/utils/shield.py` | 补充 regex/nregex 符号映射 |
| 屏蔽匹配引擎 | `alarm_backends/service/converge/shield/shield_obj.py` | 无需改动，已支持 reg/nreg |

## 六、验收标准

### 6.1 功能验收

- [ ] 移动端使用 `type=dimension` 和 `method=regex` 能成功创建屏蔽规则。
- [ ] 创建的规则能在告警处理流程中正确命中/放行目标告警。
- [ ] `get_event_detail` 对已屏蔽告警返回非空 `shield_info`。
- [ ] `shield_info.content` 能正确展示正则规则内容。

### 6.2 回归验收

- [ ] 现有 `scope`/`strategy`/`event` 三种快捷屏蔽类型功能不受影响。
- [ ] Web 端完整屏蔽 `add_shield` 功能不受影响。
- [ ] 未屏蔽告警的 `get_event_detail` 返回结构不变。

## 七、待确认问题

1. 移动端 `QuickShield` 的 `type` 字段是否沿用 `"dimension"`，还是使用其他命名（如 `"regex"`）？
2. `get_event_detail` 是否需要返回命中的**所有**规则，还是仅返回**第一条**命中规则？
3. 屏蔽规则命中多条时，`shield_info` 是否应返回列表？
4. 前端是否需要规则的 `create_user`/`update_user` 等元信息？

## 八、关联资源

- 现有屏蔽接口：`packages/monitor_web/shield/resources/backend_resources.py`
- 屏蔽常量定义：`bkmonitor/constants/shield.py`
- 屏蔽匹配引擎：`alarm_backends/service/converge/shield/shield_obj.py`
- 屏蔽展示工具：`bkmonitor/utils/shield.py`
