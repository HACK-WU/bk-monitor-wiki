# API字段与UI设计稿对应关系检查报告

> **需求编号**: REQ-20260707-001
> **创建日期**: 2026-07-08
> **关联文档**: [Host页面设计稿](../mockup/host-page-mockup.md)、[前端API文档](frontend-api-wiki.md)

---

## 一、主机列表表格字段对应

| UI设计稿字段 | API返回字段 | 对应状态 | 备注 |
|-------------|------------|----------|------|
| **主机**（主机名或IP） | `display_name` | ✅ 直接对应 | `display_name` 通常为IP或主机名 |
| **内网 IP** | `bk_host_innerip` | ✅ 直接对应 | - |
| **采集状态** | `status` | ⚠️ 需映射 | API返回数值（0=正常，其他=异常），UI需映射为"正常/无数据上报/无Agent" |
| **未恢复的告警** | `alarm_count[].count` | ⚠️ 需聚合 | API返回数组`[{count, level}]`，UI需求和所有告警数量 |
| **CPU 使用率** | `cpu_usage` | ✅ 直接对应 | 百分比数值 |
| **应用内存使用率** | `mem_usage` | ✅ 直接对应 | 百分比数值 |
| **磁盘空间使用率** | `disk_in_use` | ✅ 直接对应 | 百分比数值 |
| **进程** | `component[].display_name` | ⚠️ 需格式化 | API返回组件数组，UI需提取名称并用逗号连接 |

## 二、进程列表字段对应

| UI设计稿字段 | API返回字段 | 对应状态 | 备注 |
|-------------|------------|----------|------|
| **进程名** | `name` | ✅ 直接对应 | - |
| **端口号** | `protocol` + `bindIp` + `port` | ⚠️ 需组合 | UI需显示"协议 IP:端口"格式（如"TCP 0.0.0.0:18000"） |
| **用户** | `user` | ✅ 直接对应 | - |
| **占用CPU** | `cpuUsage` | ✅ 直接对应 | 百分比数值 |
| **常驻内存(RSS)** | `memRss` + `memUsage` | ⚠️ 需组合 | UI需显示"内存量 百分比"格式（如"92 MiB 23%"） |
| **运行时长** | `uptime` | ⚠️ 需转换 | API返回秒数，UI需转换为"天/小时/分钟"格式 |

## 三、主机详情页字段对应

| UI展示内容 | API字段来源 | 对应状态 |
|-----------|------------|----------|
| **基础信息**（IP、主机名、操作系统） | `getHostInfoList` 返回字段 | ✅ 完整 |
| **指标图表**（CPU、内存、磁盘、网络） | `getHostViewsPanels` + `getHostMetricGroupPanelOrder` | ✅ 通过面板配置接口 |
| **进程列表** | `getHostProcessList` | ✅ 字段已补全 |
| **告警事件** | `alarm_count` 字段 | ✅ 可扩展 |

## 四、进程详情页字段对应

| UI展示内容 | API字段来源 | 对应状态 |
|-----------|------------|----------|
| **进程基础信息**（PID、端口、启动命令） | `getHostProcessList` 返回字段 | ✅ 完整 |
| **进程指标图表** | `getProcessViewsPanels` + `getProcessMetricGroupPanelOrder` | ✅ 通过面板配置接口 |
| **进程日志** | 需额外接口 | ⚠️ 当前API未覆盖 |

## 五、需要关注的映射/转换需求

### 1. 采集状态映射
- API `status=0` → UI "🟢正常"
- API `status≠0` 且有component → UI "🔴无数据上报"
- API `status≠0` 且无component → UI "⚫无Agent"

### 2. 告警数量聚合
- 遍历 `alarm_count` 数组，累加所有 `count` 值

### 3. 进程组件格式化
- 从 `component` 数组提取 `display_name`
- 用逗号连接多个进程名

### 4. 端口信息组合
- 格式：`{protocol} {bindIp}:{port}`
- 示例：`TCP 0.0.0.0:18000`

### 5. 内存信息组合
- 格式：`{memRss转换为MiB} {memUsage}%`
- 需要将字节转换为MiB（除以1024*1024）

### 6. 运行时长转换
- 秒 → 天/小时/分钟格式
- 示例：`23040秒` → `5.6 d`

## 六、结论

**大部分字段可直接对应**，但需要前端进行以下处理：
- **4个字段需要映射**：采集状态、告警数量、进程列表、端口信息
- **2个字段需要格式化**：内存信息、运行时长
- **1个字段需要额外接口**：进程日志

**后端API字段完整性**：✅ 满足UI设计稿需求，无需额外字段。

---

## 附录：API接口列表

| 接口名 | 用途 | 状态 |
|--------|------|------|
| `getHostInfoList` | 获取基础主机列表 | ✅ 已存在 |
| `getHostMetricInfoList` | 获取带指标的主机列表 | ✅ 已存在 |
| `getHostTopoTreeByBizId` | 获取主机拓扑树 | ✅ 已存在 |
| `getHostProcessList` | 获取进程列表 | ⚠️ 需补全字段 |
| `getHostViewsPanels` | 获取主机面板配置 | 🆕 需新建 |
| `getProcessViewsPanels` | 获取进程面板配置 | 🆕 需新建 |
| `getHostMetricGroupPanelOrder` | 获取主机指标排序 | 🆕 需新建 |
| `getProcessMetricGroupPanelOrder` | 获取进程指标排序 | 🆕 需新建 |