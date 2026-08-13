---
groupPath: 关联关系/kernel_api网关
relation: KernelRPCRegistry-rpc_functions注册
exportedAt: "2026-08-13T09:12:17.185Z"
---
[强关联] KernelRPCRegistry 函数注册 与 rpc/functions/* 实现 + __init__.py 全量 import
强度：必改——新增 RPC 函数必须同时：① 在 rpc/functions/* 用装饰器注册 ② 确保子包 __init__.py 全量 import 成员；漏 import 则函数不生效（load_builtin_functions 按 iter_modules 导入顶层模块）
原因：RPC 函数注册在导入期生效，load_builtin_functions 不会递归扫描子包，子包成员必须在 __init__.py 显式 import 才会被注册到 KernelRPCRegistry

源端（注册中心）：
- `KernelRPCRegistry.register` / `register_function` / `register_resource` @ `bkmonitor/kernel_api/rpc/registry.py`
- `load_builtin_functions`（按 iter_modules 导入顶层模块）@ `bkmonitor/kernel_api/rpc/`
- `BkmCliOpRegistry`（op_id → func_name 白名单映射 + 审计元数据）@ `bkmonitor/kernel_api/rpc/`
- 对外暴露：`KernelRPCResource` / `BkmCliOpCallResource` @ `bkmonitor/kernel_api/views/v4/kernel_rpc.py` / `bkm_cli.py`

目标端（函数实现）：
- `rpc/functions/admin/*`（api_auth_token/cluster_info/es_storage/datasource/storage/space 等运维巡检）@ `bkmonitor/kernel_api/rpc/functions/admin/`
- `rpc/functions/bkm_cli/*`（只读命令/db/es/cache/issue/strategy 巡检）@ `bkmonitor/kernel_api/rpc/functions/bkm_cli/`
- `rpc/functions/{info,biz_scene,metadata}.py`（平台信息）@ `bkmonitor/kernel_api/rpc/functions/`
- 各子包 `__init__.py` 必须 import 全部成员