# 接口文档：`list_service_instance_detail`（查询服务实例详情）

> 关联需求：REQ-20260707-001（Host 页面接口拆分重构 · S02 进程字段补全）
> 本文档为**独立接口文档**，仅描述 CMDB `list_service_instance_detail` 接口的契约，不修改其他文档。
> 该接口是 S02「进程列表」CMDB 配置侧字段（bindIp / port / protocol / startCommand / user 等）的唯一数据来源。

---

## 1. 接口概览

| 项 | 说明 |
|----|------|
| 接口名称 | 查询服务实例详情（ListServiceInstanceDetail） |
| 用途 | 按业务/主机查询服务实例及其下的进程实例（进程配置属性 + 端口绑定 + 关联关系） |
| 调用方式 | 蓝鲸 CMDB 组件 API（`client.list_service_instance_detail`） |
| 源码定义 | `bkmonitor/api/cmdb/client.py:178`（`class ListServiceInstanceDetail`） |
| 业务封装 | `bkmonitor/api/cmdb/default.py:600`（`class GetProcess`） |
| 请求方法 | `POST` |

### 1.1 请求路径

| 环境 | 路径 |
|------|------|
| APIGW（云网关） | `/api/v3/findmany/proc/service_instance/details` |
| ESB（内部） | `/list_service_instance_detail/` |

路径由 `ListServiceInstanceDetail.use_apigw()` 自动选择（见 `client.py:184-188`）。

---

## 2. 请求参数

业务侧封装 `GetProcess` 的 `RequestSerializer`（`default.py:605-610`）定义如下：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `bk_biz_id` | int | 是 | 业务 ID |
| `bk_host_id` | int | 否 | 主机 ID；传入时按主机过滤并分页拉取，否则按业务全量拉取 |
| `include_multiple_bind_info` | bool | 否 | 是否返回多个绑定信息，默认 `False` |

> 底层 CMDB 接口为分页接口，`GetProcess` 在传入 `bk_host_id` 时通过 `batch_request(..., limit=500)` 自动翻页；未传 `bk_host_id` 时走 `get_service_instance_by_biz` 全量获取（`default.py:612-621`）。

---

## 3. 响应示例（完整）

```json
{
  "result": true,
  "code": 0,
  "message": "success",
  "permission": null,
  "data": {
    "count": 1,
    "info": [
      {
        "bk_biz_id": 1,
        "id": 49,
        "name": "p1_81",
        "service_template_id": 50,
        "bk_host_id": 11,
        "bk_module_id": 56,
        "creator": "admin",
        "modifier": "admin",
        "create_time": "2019-07-22T09:54:50.906+08:00",
        "last_time": "2019-07-22T09:54:50.906+08:00",
        "bk_supplier_account": "0",
        "service_category_id": 22,
        "process_instances": [
          {
            "process": {
              "proc_num": 0,
              "stop_cmd": "",
              "restart_cmd": "",
              "face_stop_cmd": "",
              "bk_process_id": 43,
              "bk_func_name": "p1",
              "work_path": "",
              "priority": 0,
              "reload_cmd": "",
              "bk_process_name": "p1",
              "pid_file": "",
              "auto_start": false,
              "last_time": "2019-07-22T09:54:50.927+08:00",
              "create_time": "2019-07-22T09:54:50.927+08:00",
              "bk_biz_id": 3,
              "start_cmd": "",
              "user": "",
              "timeout": 0,
              "description": "",
              "bk_supplier_account": "0",
              "bk_start_param_regex": "",
              "bind_info": [
                {
                  "enable": true,
                  "ip": "127.0.0.1",
                  "port": "80",
                  "protocol": "1",
                  "template_row_id": 1234
                }
              ]
            },
            "relation": {
              "bk_biz_id": 1,
              "bk_process_id": 43,
              "service_instance_id": 49,
              "process_template_id": 48,
              "bk_host_id": 11,
              "bk_supplier_account": "0"
            }
          }
        ]
      }
    ]
  }
}
```

---

## 4. 响应参数说明

### 4.1 顶层字段

| 参数名称 | 参数类型 | 描述 |
|----------|----------|------|
| `result` | bool | 请求成功与否。`true`：请求成功；`false`：请求失败 |
| `code` | int | 错误编码。`0` 表示 success，`>0` 表示失败错误 |
| `message` | string | 请求失败返回的错误信息 |
| `permission` | object | 权限信息 |
| `data` | object | 请求返回的数据 |

### 4.2 `data` 字段

| 参数名称 | 参数类型 | 描述 |
|----------|----------|------|
| `count` | int | 总数 |
| `info` | array | 返回结果（服务实例列表） |

### 4.3 `data.info` 字段（服务实例）

| 参数名称 | 参数类型 | 描述 |
|----------|----------|------|
| `id` | integer | 服务实例 ID |
| `name` | string | 服务实例名称 |
| `service_template_id` | int | 服务模板 ID |
| `bk_host_id` | int | 主机 ID |
| `bk_host_innerip` | string | 主机 IP |
| `bk_module_id` | integer | 模块 ID |
| `creator` | string | 创建人 |
| `modifier` | string | 修改人 |
| `create_time` | string | 创建时间 |
| `last_time` | string | 修复时间 |
| `bk_supplier_account` | string | 供应商 ID |
| `service_category_id` | integer | 服务分类 ID |
| `bk_biz_id` | int | 业务 ID |
| `process_instances` | array | 进程实例信息 |

### 4.4 `data.info.process_instances[x].process` 字段（进程实例详情）

| 参数名称 | 参数类型 | 描述 |
|----------|----------|------|
| `auto_start` | bool | 是否自动拉起 |
| `auto_time_gap` | int | 拉起间隔 |
| `bk_biz_id` | int | 业务 id |
| `bk_func_id` | string | 功能 ID |
| `bk_func_name` | string | 进程名称 |
| `bk_process_id` | int | 进程 id |
| `bk_process_name` | string | 进程别名 |
| `bk_start_param_regex` | string | 进程启动参数 |
| `bk_supplier_account` | string | 开发商账号 |
| `create_time` | string | 创建时间 |
| `description` | string | 描述 |
| `face_stop_cmd` | string | 强制停止命令 |
| `last_time` | string | 更新时间 |
| `pid_file` | string | PID 文件路径 |
| `priority` | int | 启动优先级 |
| `proc_num` | int | 启动数量 |
| `reload_cmd` | string | 进程重载命令 |
| `restart_cmd` | string | 重启命令 |
| `start_cmd` | string | 启动命令 |
| `stop_cmd` | string | 停止命令 |
| `timeout` | int | 操作超时时长 |
| `user` | string | 启动用户 |
| `work_path` | string | 工作路径 |
| `bind_info` | object | 绑定信息 |

### 4.5 `data.info.process_instances[x].process.bind_info[n]` 字段（端口绑定）

| 参数名称 | 参数类型 | 描述 |
|----------|----------|------|
| `enable` | bool | 端口是否启用 |
| `ip` | string | 绑定的 ip |
| `port` | string | 绑定的端口 |
| `protocol` | string | 使用的协议 |
| `template_row_id` | int | 实例化使用的模板行索引，进程内唯一 |

### 4.6 `data.info.process_instances[x].relation` 字段（进程实例关联信息）

| 参数名称 | 参数类型 | 描述 |
|----------|----------|------|
| `bk_biz_id` | int | 业务 id |
| `bk_process_id` | int | 进程 id |
| `service_instance_id` | int | 服务实例 id |
| `process_template_id` | int | 进程模版 id |
| `bk_host_id` | int | 主机 id |
| `bk_supplier_account` | string | 供应商账号 |

---

## 5. 与 S02 进程列表字段的映射（参考）

> 详细字段优先级策略见设计文档 `design/S02-process-fields-design-update.md`。此处仅给出本接口到前端 `ProcessItem` 的映射。

| 前端字段 | 本接口来源字段 | 说明 |
|----------|----------------|------|
| `id` | `process.bk_process_id` | 进程配置 ID（非操作系统 PID） |
| `name` | `process.bk_func_name` / `bk_process_name` | 进程名称 |
| `bindIp` | `process.bind_info[].ip` | 绑定 IP |
| `port` | `process.bind_info[].port` | 绑定端口 |
| `protocol` | `process.bind_info[].protocol` | 协议 |
| `startCommand` | `process.start_cmd` | 启动命令 |
| `user` | `process.user` | **启动用户**（CMDB 配置值，运行时实际用户走 TSDB `system.proc.username`） |
| `hostIp` | `bk_host_innerip` / `bk_host_id` 关联 | 主机 IP（示例未回，需确认请求带 fields） |

> ⚠️ **注意**：本接口**不返回**操作系统进程号（PID）、CPU/内存使用率、运行时长、端口健康状态等运行时指标，这些字段需由 TSDB（`system.proc` / `system.proc_port`）单独查询补充。尤其 `pid` 字段前端需要的是操作系统进程号，本接口无法提供，不可用 `bk_process_id` 兜底。

---

## 6. 关键说明

1. **`process.user` 是「启动用户」**：为 CMDB 配置值；与运行时实际运行用户（`system.proc.username`）语义不同，按 S02 设计 CMDB 优先、TSDB 兜底。
2. **分页行为**：底层为分页接口，业务封装已处理翻页（`default.py` 中 `batch_request` / `get_service_instance_by_biz`），上游无需手动翻页。
3. **`bind_info` 多绑定**：一个进程可绑定多个端口，`GetProcess` 会将其展开为多条 `Process` 记录（`default.py:632-637`），前端需按 `bind_info` 数组逐条处理。
