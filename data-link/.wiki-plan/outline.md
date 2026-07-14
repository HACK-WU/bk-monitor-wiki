# bkmonitorbeat Wiki 大纲（规划契约）

> Wiki 根目录：`/root/bk-monitor/bk-monitor-wiki/data-link`
> 命名空间：`data-link/bkmonitorbeat`
> 来源代码根：`bkmonitor-datalink/pkg/bkmonitorbeat`
> 拆分粒度：总览 + 子页拆分
> 排除项：test/、docs/、script/、support-files/、`*.md`、`vendor`、`*.pb.go`、`*_test.go`、CI 等噪音（仅分析业务 `.go` 源码）
> 生成日期：2026-07-14

---

## 目录树

```
data-link/bkmonitorbeat/
├── 总览.md                       # 模块定位、整体架构、启动链路、关键技术点
├── 接口与契约层.md               # define/：Task/Scheduler/Beater/Event/Config 接口与公共类型
├── 配置体系.md                   # configs/：全局 Config、BaseTaskParam、各任务配置、并发限制
├── 调度框架.md                   # scheduler/：BaseScheduler + 5 种调度器
├── 采集任务框架.md               # tasks/ 顶层：BaseTask/EventTask/Semaphore/事件封装等公共机制
├── 采集任务分类总览.md           # tasks/ 各采集模块按类别归纳（主机指标/网络探测/进程/日志事件/系统资产）
├── 工具与上报通道.md             # utils/ 工具集 + report/ 命令行上报
└── HTTP服务与多租户.md           # http/ admin 服务 + tenant/ 多租户 dataID 支撑
```

---

## 各页条目

### 1. 总览.md
- **路径**：`bkmonitorbeat/总览.md`
- **引用源文件**：
  - `bkmonitor-datalink/pkg/bkmonitorbeat/main.go`（L69-190 启动链路）
  - `bkmonitor-datalink/pkg/bkmonitorbeat/beater/beater.go`（L117-301 MonitorBeater 与启动）
  - `bkmonitor-datalink/pkg/bkmonitorbeat/define/task.go`（L66-77 Task 接口）
- **章节骨架**：简介 / 项目结构（目录地图）/ 核心组件（beater/configs/define/scheduler/tasks/report/utils/tenant 一句话职责）/ 架构总览（Mermaid：main→beater→configengine→scheduler→task→event→report）/ 启动链路 / 关键技术点（多调度器、并发信号量、热重载、多租户）/ 结论

### 2. 接口与契约层.md
- **路径**：`bkmonitorbeat/接口与契约层.md`
- **引用源文件**：
  - `define/task.go`（L66-77 Task 接口、L17-48 Module 常量、L50-63 状态枚举）
  - `define/beater.go`（L34 Beater 接口、LogConfig、运行状态）
  - `define/config.go`（L58-76 Config/TaskConfig/TaskMetaConfig/ConfigEngine 接口）
  - `define/event.go`（L17 Event 接口）
  - `define/proc.go`（ProcStat/IOStat/CPUStat/MemStat 等进程公共结构）
- **章节骨架**：简介 / 项目结构 / 核心组件（各接口契约）/ 架构总览（契约层如何解耦 beater↔scheduler↔tasks）/ 组件详细分析（Task/Scheduler/Beater/Event/Config 接口逐个说明）/ 依赖关系分析 / 结论

### 3. 配置体系.md
- **路径**：`bkmonitorbeat/配置体系.md`
- **引用源文件**：
  - `configs/config.go`（L71 全局 Config、NewConfig）
  - `configs/basetaskparam.go`（L25 BaseTaskParam、L195 BaseTaskMetaParam 基类字段与清洗）
  - `configs/childconfig.go`（ChildTaskMetaConfig 子任务）
  - `configs/basereport.go`（BasereportConfig 系统指标采集配置代表）
  - 代表：`configs/pingconfig.go`、`configs/tcpconfig.go`、`configs/httpconfig.go`、`configs/processbeat.go`（各任务类型配置）
- **章节骨架**：简介 / 项目结构 / 核心组件（全局 Config、MetaConfig、BaseTaskParam）/ 架构总览（配置如何被 configengine 加载并下发到 task）/ 组件详细分析（基类字段、清洗逻辑、并发限制配置）/ 依赖关系分析 / 结论

### 4. 调度框架.md
- **路径**：`bkmonitorbeat/调度框架.md`
- **引用源文件**：
  - `scheduler/scheduler.go`（L19 BaseScheduler 基类）
  - `scheduler/daemon/scheduler.go`（L53 Daemon 主调度路径）
  - `scheduler/cron/scheduler.go`（cron 周期调度）
  - `scheduler/checker/scheduler.go`（CheckScheduler 一次性检查）
  - `scheduler/keyword/scheduler.go`（日志关键字专用调度）
  - `scheduler/listen/scheduler.go`（常驻监听：trap/metric/kubeevent/dmesg）
- **章节骨架**：简介 / 项目结构 / 核心组件（基类 + 5 调度器）/ 架构总览（schedulerfactory 按模式选择）/ 组件详细分析（每种调度器触发条件与执行模型）/ 依赖关系分析（与 beater 的 KeywordScheduler/ListenScheduler 对应）/ 结论

### 5. 采集任务框架.md
- **路径**：`bkmonitorbeat/采集任务框架.md`
- **引用源文件**：
  - `tasks/task.go`（L24 BaseTask、L120 EventTask、L71 PreRun、L102 PostRun）
  - `tasks/semaphore.go`（Semaphore 接口、DefaultSemaphorePool 并发控制）
  - `tasks/event.go`（Event 构造与封装）
  - `tasks/prom_event.go`（Prometheus 格式事件）
  - `tasks/host_dimension.go`（主机维度注入）
  - `tasks/gatherup.go`（gather_up_beat 汇总）
- **章节骨架**：简介 / 项目结构 / 核心组件（BaseTask/EventTask/Semaphore/事件体系）/ 架构总览（任务如何被 scheduler 驱动、Hook 机制、并发限制）/ 组件详细分析（PreRun/PostRun 生命周期、信号量并发、事件封装与维度）/ 依赖关系分析 / 结论

### 6. 采集任务分类总览.md
- **路径**：`bkmonitorbeat/采集任务分类总览.md`
- **引用源文件**（按类别选代表）：
  - 主机基础指标：`tasks/basereport/basereport.go`（L28 Gather、L134 Run、L208 CollectItem）、`tasks/metricbeat/`、`tasks/static/`、`tasks/selfstats/`
  - 网络探测：`tasks/ping/`、`tasks/tcp/`、`tasks/udp/`、`tasks/http/`
  - 进程采集：`tasks/processbeat/`、`tasks/procstatus/`、`tasks/procconf/`、`tasks/proccustom/`、`tasks/procsync/`、`tasks/procbin/`、`tasks/procsnapshot/`、`tasks/procsnapshot/`
  - 日志与事件：`tasks/keyword/`、`tasks/exceptionbeat/collector/`、`tasks/dmesg/`、`tasks/loginlog/`、`tasks/shellhistory/`、`tasks/trap/`、`tasks/kubeevent/`、`tasks/gatherup.go`
  - 系统资产与配置：`tasks/rpmpackage/`、`tasks/timesync/`、`tasks/cmdb.go`、`tasks/socketsnapshot/`
- **章节骨架**：简介 / 项目结构（按 5 大类分组地图）/ 核心组件（各类采集模块）/ 架构总览（模块名↔Module 常量↔配置类型映射）/ 组件详细分析（每类下列出模块、代表文件、采集内容、产出事件类型）/ 依赖关系分析 / 结论

### 7. 工具与上报通道.md
- **路径**：`bkmonitorbeat/工具与上报通道.md`
- **引用源文件**：
  - `utils/`（原子操作、cgroup、类型转换、解码、文件、hook 管理、正则、pipes、rpm、临时文件、时间等代表文件）
  - `report/`（report.go 命令行 `-report` 上报、sender agent/http 注册）
  - `main.go`（L70 senderhttp.Register、L73-80 DoReport、L139 senderagent.Register）
- **章节骨架**：简介 / 项目结构 / 核心组件（utils 工具集、report 上报）/ 架构总览（report 模式如何独立于 beater 直接发送 message）/ 组件详细分析 / 依赖关系分析 / 结论

### 8. HTTP服务与多租户.md
- **路径**：`bkmonitorbeat/HTTP服务与多租户.md`
- **引用源文件**：
  - `http/`（admin server、debug handler）
  - `tenant/`（多租户 Client、gse agent-message 通信获取 dataID、socket 选项、本地存储）
  - `beater/beater.go`（L54 tcli *tenant.Client、L57-59 三个 Scheduler 字段，体现 tenant 集成）
- **章节骨架**：简介 / 项目结构 / 核心组件（http 调试服务、tenant 多租户）/ 架构总览（多租户如何为每个任务解析 dataID）/ 组件详细分析 / 依赖关系分析 / 结论

---

## 体量评估（Step 5 输入）

- **页面数**：8（> 8 阈值未触发，但源文件数超阈值）
- **去重源文件数**：预计 > 30（触发分批阈值）
- **结论**：启用分批撰写（满足「源文件数 > 30」）

## 分批排期（待用户确认）

| 批次 | 页面 | 预计源文件数 | 顺序依据 |
|------|------|-------------|----------|
| Batch 1（底层契约与框架） | 接口与契约层、配置体系、调度框架 | ~15 | 自底向上：先写解耦契约与调度框架 |
| Batch 2（采集任务核心） | 采集任务框架、采集任务分类总览 | ~20 | 依赖 Batch 1 的接口/调度概念 |
| Batch 3（外围支撑 + 总览） | 工具与上报通道、HTTP服务与多租户、总览 | ~12 | 外围模块 + 收尾总览（需汇总全部） |

> 每批内部用 task-dispatch 并行撰写；每页写完即跑 `wiki_format_check.py --file` 校验；全部批结束后跑 `--wiki-dir` 全量校验。
