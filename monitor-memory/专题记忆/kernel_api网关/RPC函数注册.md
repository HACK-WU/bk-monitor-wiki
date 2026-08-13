---
groupPath: 专题记忆/kernel_api网关
relation: RPC函数注册
exportedAt: "2026-08-13T09:10:59.724Z"
---
kernel_api RPC 函数注册：KernelRPCRegistry 支持装饰器/直接注册/Resource 包装三种注册方式，__meta__ 元协议渐进披露函数列表与 schema，BkmCliOpRegistry 做 op 白名单映射，租户推断按 bk_biz_id/space_uid 等反查注入。全部只读语义。

## 关键类/函数
- 符号: `KernelRPCRegistry.register` / `register_function` / `register_resource` / `list_functions` / `get_function_detail` / `execute`
- 位置: `bkmonitor/kernel_api/rpc/registry.py`
- 符号: `BkmCliOpRegistry` / `inject_bk_tenant_id` / `infer_bk_tenant_id` / `load_builtin_functions`
- 位置: `bkmonitor/kernel_api/rpc/`
- 对外暴露: `KernelRPCResource` / `BkmCliOpCallResource` @ `kernel_api/views/v4/kernel_rpc.py` / `bkm_cli.py`

## 三种注册方式
1. 装饰器注册：`@KernelRPCRegistry.register(...)`（导入期生效）
2. 直接注册：`register_function(func_name, func, ...)`
3. Resource 包装注册：`register_resource(...)`
- admin/bkm_cli/metadata 走装饰器式注册；`load_builtin_functions` 按 `iter_modules` 导入顶层模块，子包需 `__init__.py` 全量 import 成员

## __meta__ 元协议（渐进披露）
- `func_name="__meta__", params.action="list"` → 查可调用函数列表
- `params.action="detail", target_func_name=<函数名>` → 查函数入参 schema
- 正式调用：`func_name=<函数名>, params={...}`
- `__meta__` 为保留函数名，业务函数禁止注册（`register_function` 显式拦截）

## op 白名单（BkmCliOpRegistry）
- op_id → func_name 映射 + 审计元数据，防绕过 func_name 直接调用
- bkm-cli op 不存在时抛 404 `target_not_found`，客户端用 `mapStatusToCode(404)` 映射
- 出口 `BkmCliOpCallResource` 统一 `json.dumps(default=str)` 归一非 JSON-safe 对象（datetime/Decimal）

## 租户推断
- 按 `bk_biz_id` / `space_uid` / `table_id` / `bk_data_id` 等反查租户并注入
- 多租户命中时报「无法根据 xx 反查 bk_tenant_id，命中了多个租户」→ 显式传 `bk_tenant_id`

## 踩坑点
- 新增 RPC 函数不生效：新增函数文件未 import / 未用装饰器注册 → 子包需 `__init__.py` 全量 import 成员
- 报「未找到可调用函数」：先调 `__meta__` action=list 查函数列表确认
- 全部只读语义：bkm-cli 有 AST 只读守卫（`platform_catalog/_lint.py`）