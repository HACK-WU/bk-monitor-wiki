# 解决方案索引

> 由 solution-capture 自动维护

## integration

### local-kernel-api-proxy：本地 web 进程 → kernel_api 联调（转发代理）
- **描述**：解决本地联调时 web 角色调用 kernel_api 无法连通的问题，用转发代理 + 环境变量覆盖 base_url，无需真实 APIGW 网关
- **触发关键词**：kernel_api, 本地联调, 转发代理, BKAPP_NEW_MONITOR_API_BASE_URL, api 进程, Cannot assign requested address
- **目录**：integration/local-kernel-api-proxy/

### blueking-devops-atom-offline-debug：蓝盾流水线插件离线联调
- **描述**：解决没有蓝盾平台权限时流水线插件无法调试的问题，通过 mock 依赖接口 + 真跑插件完成离线联调
- **触发关键词**：蓝盾插件, 流水线插件, 插件工作台没权限, task.json 调试, selector 拉不到选项, optionsConf 跨域, python_atom_sdk, get_sensitive_conf, bk-monitor-shield
- **目录**：integration/blueking-devops-atom-offline-debug/

### itsm-v4-integration-config：监控平台对接 ITSM V4 的环境变量配置排查
- **描述**：解决处理套餐「服务名称下拉暂无选项」与「前往IT服务管理中心跳 404」两类问题，根因分别是 BK_ITSM_V4_SYSTEM_ID 静默回退到 APP_CODE、BK_ITSM_V4_HOST 为空导致链接退化为相对路径
- **触发关键词**：ITSM V4, 系统不存在, system_workflow/list, 处理套餐服务名称为空, 前往IT服务管理中心 404, BK_ITSM_V4_SYSTEM_ID, BK_ITSM_V4_HOST, create_itsm_v4_system, BKAPIError 3301001
- **目录**：integration/itsm-v4-integration-config/
