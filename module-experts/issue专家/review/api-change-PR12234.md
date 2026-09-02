# Issue 合并接口变更说明（前端对接版）

> 需求：【issue】主 issue 也能被合并
> 变更核心：放开"主 Issue 不能被合并"的限制。选择一个"已合并过其他 Issue 的主 Issue"作为并入对象时，合并会成功，它原来带的子 Issue 会自动平移挂到新主下，不存在层级嵌套。

## 变更总览

| 接口 | 请求参数 | 返回字段 |
|------|----------|----------|
| 合并 Issue | 无变化 | 新增 `reparented_members` |
| 合并来源列表 | 无变化 | 列表项新增 `via_issue_id` |

行为变化：以前把"已合并过其他 Issue 的主 Issue"传入 `members` 会报错（code 3337108），现在**合法并成功**，同时它名下的子 Issue 一并入组。

---

## 1. 合并 Issue

- **URL**：`POST /fta/issue/issue/merge/`
- **说明**：将若干 Issue 并入一个主 Issue。operator 由后端自动取当前登录用户，无需传。

### 1.1 请求参数（无变化）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| bk_biz_id | int | 是 | 业务 ID |
| main_issue_id | string | 是 | 主 Issue ID（合并目标） |
| members | string[] | 是 | 并入 Issue ID 列表，1~100 个。与 main 重复的会被自动剔除；传"已合并过其他 Issue 的主 Issue"现在也合法 |
| reasons | string[] | 否 | 合并依据，缺省或空数组均合法 |

请求示例：

```json
{
  "bk_biz_id": 123,
  "main_issue_id": "issue_001",
  "members": ["issue_002", "issue_003"],
  "reasons": ["同一故障根因"]
}
```

### 1.2 返回字段

```json
{
  "status": "ok",
  "main_issue_id": "issue_001",
  "members": ["issue_002", "issue_003"],
  "reparented_members": ["issue_010", "issue_011"]
}
```

| 字段 | 类型 | 说明 | 本次变更 |
|------|------|------|----------|
| status | string | 固定 "ok" | 无变化 |
| main_issue_id | string | 合并后的主 Issue ID | 无变化 |
| members | string[] | 本次请求并入的 Issue ID（不含被改挂的） | 无变化 |
| **reparented_members** | string[] | **新增**。随"已合并过其他 Issue 的主"一起平移过来的子 Issue ID 列表。合并后组内子 Issue 总数 = members + reparented_members。普通合并（members 里没有已成组的主）时为空数组 `[]`，此时接口行为与之前完全一致 | ✅ 新增 |

### 1.3 前端交互建议

- `reparented_members` 非空时，建议弹提示告知用户："本次合并同时并入了 N 个来源子 Issue"（例如 issue_003 原本已合并了 issue_010、issue_011，把 issue_003 并入 issue_001 时，issue_010、issue_011 会一并挂到 issue_001 下）。
- 该字段当前前端尚未消费，如需展示请补 TS 类型声明。

---

## 2. 合并来源列表

- **URL**：`GET /fta/issue/issue/merge_sources/`
- **说明**：查询某个主 Issue 的全部合并来源（当前生效的 + 已拆分的历史记录）。

### 2.1 请求参数（无变化，query string）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| bk_biz_id | int | 是 | 业务 ID |
| main_issue_id | string | 是 | 主 Issue ID |

### 2.2 返回字段

```json
{
  "main_issue_id": "issue_001",
  "active_members": [
    {
      "member_issue_id": "issue_011",
      "member_name": "CPU 使用率过高",
      "anomaly_message": "xx 主机 CPU 使用率 95%",
      "merge_reasons": ["同一故障根因"],
      "merge_operator": "zhangsan",
      "merge_time": 1725000000,
      "status": "active",
      "relation_status": "active",
      "member_es_status": "unresolved",
      "via_issue_id": "issue_003"
    }
  ],
  "split_history": [
    {
      "member_issue_id": "issue_020",
      "member_name": "...",
      "anomaly_message": "...",
      "merge_reasons": [],
      "merge_operator": "lisi",
      "merge_time": 1724000000,
      "status": "split",
      "relation_status": "split",
      "member_es_status": "pending_review",
      "via_issue_id": null,
      "split_reasons": ["误合并"],
      "split_operator": "lisi",
      "split_time": 1724500000,
      "split_kind": "manual"
    }
  ]
}
```

**其他字段说明**：

| 字段 | 说明 |
|------|------|
| member_es_status | 成员当前真实状态，取值：`pending_review` / `unresolved` / `resolved` / `archived`。ES 查不到时为 `null`，前端按"已删除"占位渲染 |
| merge_time / split_time / anomaly_message | 时间戳为秒级 Unix 时间；anomaly_message 为成员最新告警描述，查询失败时兜底 `"--"` |
| split_kind（仅 split_history） | 拆分触发类型，新数据固定 `manual`（人工拆分）；历史数据可能为 `by_main_resolve` 等旧值 |
| status / relation_status | 同义双字段，新代码请使用 `relation_status`，`status` 保留一个发布周期后移除 |

### 2.3 新增字段：`via_issue_id`

| 字段 | 出现位置 | 类型 | 含义 |
|------|----------|------|------|
| **via_issue_id** | active_members[*] / split_history[*] | string \| null | 该成员的"上一跳主 Issue"。非空表示：它不是直接并进来的，而是随着某个"已合并过的主"一起被平移挂到当前主下的，字段值就是它原来的主 Issue ID。直接合并进来的成员为 `null`。 |

**使用注意**：

- 这是**纯溯源标签**，只用于展示"来源"（如 tooltip："该 Issue 原挂在 issue_003 下，随其合并平移而来"）。
- `via_issue_id` 指向的 Issue **可能已不在本组**（它的主后来又被拆分走了），前端不得据此假设它仍是本组成员，也不要用它做跳转后的状态判断。

---

## 3. 后端可能报错的信息

### 3.1 错误响应统一结构

所有业务错误返回 HTTP 状态码 + 统一 JSON 结构：

```json
{
  "result": false,
  "code": 3337110,
  "name": "合并组过大",
  "message": "合并后组成员数 120 超过上限 100，请先拆分部分成员再合并",
  "data": null,
  "extra": {
    "business_code": "MERGE_GROUP_TOO_LARGE",
    "current": 0,
    "incoming": 20,
    "carried": 100,
    "limit": 100
  }
}
```

前端建议统一展示 `message`；需要精细分支时用 `code` 或 `extra.business_code`。

### 3.2 本次新增错误

| HTTP | code | business_code | 名称 | message 示例 | 触发条件 | 前端建议 |
|------|------|---------------|------|--------------|----------|----------|
| 409 | 3337110 | MERGE_GROUP_TOO_LARGE | 合并组过大 | 合并后组成员数 {total} 超过上限 {limit}，请先拆分部分成员再合并 | 合并后的组内子 Issue 总数超过平台配置的上限（默认不限，部署方可配置）。extra 中 current=主原有成员数、incoming=本次请求数、carried=改挂平移数、limit=上限 | 直接展示 message，引导用户先拆分 |
| 409 | 3337111 | MERGE_GROUP_INCONSISTENT | 合并组状态不一致 | 以下 Issue 合并关系状态不一致（{reason}），请先修复再合并： {issue_ids_summary} | 被平移的子 Issue 自身状态异常（如已同时挂在目标组下、或自身还带着子 Issue）。extra 中 issue_ids 是问题 Issue 列表，reason 是原因说明（如 already_active_member_of_target / carried_member_has_own_members） | 直接展示 message；这是数据异常，需要运维处理，前端无需特殊重试逻辑 |

### 3.3 不再出现的错误

| code | business_code | 名称 | 说明 |
|------|---------------|------|------|
| 409 / 3337108 | MERGE_MEMBER_IS_ANOTHER_MAIN | 成员 Issue 自身是别的合并组主 | **本次需求放开的限制**。后端不会再返回此错误，前端如有针对 3337108 的分支逻辑可移除 |

### 3.4 既有错误（不变，仍可能出现）

| HTTP | code | business_code | 名称 | message | 触发条件 |
|------|------|---------------|------|---------|----------|
| 400 | 3337101 | MERGE_CROSS_BIZ_FORBIDDEN | 跨业务合并被拒 | 不允许跨业务合并 Issue | main 与 members 不属于同一业务 |
| 409 | 3337102 | MERGE_CONFLICT | 合并冲突 | 待合并的 Issue 已被合并到 #{conflicting_main_issue_id}，请先拆分 | members 中某个 Issue 当前已挂在别的组下 |
| 409 | 3337103 | MERGE_TARGET_IS_MEMBER | 主 Issue 自身被合并 | 目标主 Issue {main_issue_id} 自身已被合并到 #{conflicting_main_issue_id}，请先拆分再作为主 Issue | 选中的目标主本身挂在别的组下 |
| 404 | 3337105 | MERGE_ISSUES_NOT_FOUND | 合并的 Issue 不存在 | 以下 Issue 不存在或业务归属不匹配： {missing_ids} | main 或 members 中的 ID 不存在 |
| 409 | 3337109 | MERGE_FREEZE_VIOLATION | Issue 已被合并冻结 | Issue {issue_id} 已被合并到 #{conflicting_main_issue_id}，请前往主 Issue 操作或先拆分 | 非合并接口：对组内子 Issue 直接做解决/归档/指派等写操作时被冻结守卫拦截 |

补充：错误码 3337106（主 Issue 状态不允许合并）/ 3337107（成员状态不允许合并）已在历史版本废弃，后端不再返回，前端可移除对应分支。

参数校验类错误（HTTP 400，code 为平台通用校验错误，非 3337 段）：

| message | 触发条件 |
|---------|----------|
| members 去重后为空 | members 与 main 完全重复，或剔除重复后为空 |
| 字段必填/格式错误 | members 超过 100 个、ID 格式非法、缺 bk_biz_id 等 |
