# api-tester 参考文档

## 参数 schema 类型对照

`param_schema` 中每个字段的 `type` 取值（来自 `core.drf_resource.tools.FieldType`）：

| type | 对应 DRF 字段 | 示例值 |
|------|--------------|--------|
| `String` | CharField / RelatedField 等 | `""` |
| `Integer` | IntegerField | `0` |
| `Number` | DecimalField / FloatField | `0` |
| `Boolean` | BooleanField | `false` |
| `Enum` | ChoiceField / MultipleChoiceField | 第一个 choice |
| `Array` | ListField / ListSerializer | `[]` |
| `Object` | 嵌套 Serializer | `{}` |

每个字段还含：`required`（是否必填）、`name`（字段名）、`source_name`（数据源名）、`description`（label）、`default`（默认值，未设置时为 `empty` 不输出）。

> 注：`read_only` 字段和 `HiddenField` 会被 `get_serializer_fields` 自动跳过，不出现在 schema 中。

## 示例参数生成规则

1. 字段有非空 `default` → 用 `default` 值
2. 无 default → 按 type 生成占位值（见上表"示例值"列）
3. `Array` 若子元素有类型，生成 `[_example_for(子元素)]`（单元素列表）
4. `Object` 递归生成各属性示例

生成的是**占位参数**，仅保证结构合法，业务语义需用户根据 `description` 手动填入真实值。

## 限制：依赖 HTTP 请求上下文的接口

进程内直调 `Resource.request()` 时，没有真实 HTTP 请求对象。`perform_request` 内部若调用以下函数会报错：

| 函数 | 来源 | 说明 |
|------|------|------|
| `get_request_username()` | `bkmonitor.utils.request` | 无请求时返回 None，下游可能因用户为空报错 |
| `get_request_tenant_id()` | `bkmonitor.utils.request` | 同上 |
| `get_request()` | `bkmonitor.utils.request` | `peaceful=True` 返回 None |
| 直接访问 `request.user` / `request.META` | - | AttributeError |

**判断方法**：`run` 模式返回 `result.status=error`，若 `exception_message` 涉及用户/租户/请求对象为空，即属此类限制。

**应对**：
- 这类接口需走真实 HTTP 请求测试
- 或在 `perform_request` 中对 `get_request_username()` 做 None 兜底（属于代码改进，非测试手段）

## 与真实 HTTP 测试的差异

| 维度 | api-tester（进程内直调） | 真实 HTTP |
|------|------------------------|-----------|
| 认证 | 不经过 | 需登录态 cookie |
| 权限 | 不经过 IAM 校验 | 完整权限链 |
| 限流 | 不经过 | 经过 |
| CSRF | 不需要 | POST 需 token |
| 请求上下文 | 无（username/tenant 为空） | 有 |
| 参数校验 | ✅ `RequestSerializer` | ✅ |
| 业务逻辑 | ✅ `perform_request` | ✅ |
| 响应校验 | ✅ `ResponseSerializer` | ✅ |
| 环境成本 | 低（venv python 即可） | 高（需部署+登录态） |

**结论**：api-tester 适合测"业务逻辑正确性"（参数校验+处理+响应），不适合测"访问控制"。

## 常见错误排查

### 1. `env_error: 初始化 Django 环境失败`

- 未用 venv python：改用 `/root/bk-monitor/bkmonitor/.venv/bin/python`
- 项目根路径非默认：设置 `BK_MONITOR_ROOT` 环境变量指向含 `hello.py` 的目录

### 2. `resolve_failed: URL 未匹配到任何视图`

- URL 路径错误，检查是否含 `SITE_URL` 前缀（如 `/o/bk_monitorv3/`）
- 用 `inspect` 模式先确认 URL 可解析

### 3. `resolve_failed: 该视图不是 ResourceViewSet`

- 该接口是标准 DRF ViewSet 或 Django View，不走 Resource 框架，本 skill 不支持
- 这类接口需用 Django Test Client 或真实 HTTP 测试

### 4. `resolve_failed: resource_mapping 中未找到对应 Resource`

- HTTP 方法传错（如把 POST 接口传成 GET）
- 查看 `candidates` 字段，列出该 ViewSet 下所有可用方法+Resource

### 5. `result.status=error` 且异常涉及用户/租户为空

- 属于"依赖 HTTP 请求上下文"限制，见上文

### 6. `confirm_required`

- 非 GET 的 run 未加 `--confirm`，确认后补上该参数重新执行

## 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `BK_MONITOR_ROOT` | 自动向上查找含 `hello.py` 的目录 | 项目根目录，用于初始化 Django 环境 |

## 退出码

| 码 | 含义 |
|----|------|
| 0 | 正常完成 |
| 1 | 用法错误 |
| 2 | Django 环境初始化失败 |
| 3 | URL 解析失败 |
| 4 | 参数 JSON 解析失败 |
| 5 | 非 GET 未确认（被安全拦截） |
