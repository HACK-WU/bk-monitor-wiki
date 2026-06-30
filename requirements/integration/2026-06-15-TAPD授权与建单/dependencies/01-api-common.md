# API 通用规范

> 所有 TAPD API v2 接口共享的约定。

---

## 1. 通用响应格式

```json
{
    "status": 1,
    "data": { ... },
    "info": "success"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | integer | 1 = 成功，其他 = 失败 |
| `data` | object | 响应数据体，各接口结构不同 |
| `info` | string | 提示信息 |

> 失败时 `status != 1`，可能伴随更详细的错误信息（详见 [05-error-codes.md](05-error-codes.md)）。

---

## 2. 认证方式

| 认证方式 | 场景 |
|----------|------|
| **Basic Auth** | app 级 API（`get_granted_workspaces`、`get_workspace_info`、建单）；`request_token` 接口本身也使用 Basic Auth |
| **Bearer Token** | 用户态 API（获取用户可见项目列表等） |

**Basic Auth 构造方法**：
```
1. 拼接: client_id + ":" + client_secret
2. BASE64 编码
3. 写入 Header: Authorization: Basic {base64_str}
```

> curl 简写: `curl -u 'client_id:client_secret' URL`

**Bearer Token 使用方法**：
```
Header: Authorization: Bearer {access_token}
```

---

## 3. 通用请求参数（可选）

部分列表接口支持以下分页/过滤参数：

| 字段名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| `limit` | 否 | integer | 返回数量限制，默认 30，最大 200 |
| `page` | 否 | integer | 当前页码，默认 1 |
| `order` | 否 | string | 排序规则，如 `created%20desc` |
| `fields` | 否 | string | 指定返回字段，多个用逗号分隔 |
