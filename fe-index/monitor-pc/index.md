# monitor-pc 前端接口索引

> 根目录：`/root/bk-monitor/bkmonitor/webpack` · slug：`monitor-pc`
> 范围：`src/monitor-pc/**` + 共享包（monitor-api / monitor-common / monitor-ui / monitor-static / fta-solutions）
> 生成：2026-10-13 @ commit `90a2de6` · 路由条目 172 条（122 条指向页面文件，其余为导航菜单条目，见已知局限 7）· **页面文件 85 个** · 接口 338 个 · 映射 1316 条
> ⚠️ **快照制**：代码变了先跑新鲜度校验（见文末），过期需重建

## 怎么用

1. **改接口前**：查 `apis/{分区}.md` 的「直接调用页面」列，确认要回归哪些页面（🟢/🟡 才算"在用"，🔵 只是候选）
2. **接页面任务**：查 `pages/{分区}.md`，拿到页面文件、用到的接口、直接依赖，再读源码
3. **索引是路标，源码是事实**：命中行的 `file:line` 必须回源码确认

## 置信度（深度）口径

- 🟢 调用点在页面文件自身（156 条）
- 🟡 调用点在直接依赖内（496 条）
- 🔵 调用点在依赖的依赖内，仅"间接候选"（664 条）
- 深度分布：0 → 156 · 1 → 496 · 2 → 664

## 高频直达

| 我要… | 去哪一页 | 证据 |
|---|---|---|
| 改告警策略/事件/屏蔽/分派接口，看哪些页面受影响 | [apis/alarm.md](./apis/alarm.md) | `fta/*`、`strategies/*`、`shield/*` |
| 改采集配置/插件接口 | [apis/collect.md](./apis/collect.md) | `collecting_config/*`、`collector_plugin/*` |
| 改场景视图/性能/主机接口 | [apis/scene.md](./apis/scene.md) | `scene_view/*`、`performance/*` |
| 改拨测接口 | [apis/uptime.md](./apis/uptime.md) | `uptime_check/*` |
| 改查询模板/数据检索接口 | [apis/retrieval.md](./apis/retrieval.md) | `query_template/*`、`data_explorer/*` |
| 改通知方式/告警组/订阅报表接口 | [apis/notice.md](./apis/notice.md) | `notice_group/*`、`user_groups/*`、`report/*` |
| 改通用接口（业务/拓扑/ip 选择器） | [apis/commons.md](./apis/commons.md) | `commons/*`（42 个，跨页共用） |
| 改权限/外部集成/Grafana/AI 设置接口 | [apis/platform.md](./apis/platform.md) | `iam/*`、`external/*`、`grafana/*` |
| 接「告警策略配置」页面任务 | [pages/alarm.md](./pages/alarm.md) | `strategy-config.tsx`（73 接口） |
| 接「采集配置」页面任务 | [pages/collect.md](./pages/collect.md) | `collector-add.vue`（59 接口） |
| 接「主机/性能场景」页面任务 | [pages/scene.md](./pages/scene.md) | `host.tsx`、`performance-wrapper.tsx` |

## 分区索引 · 页面

| 分区 | 文件 | 页面数 | 覆盖内容 |
|---|---|---|---|
| alarm | [pages/alarm.md](./pages/alarm.md) | 11 | 告警策略、事件中心、告警分派（含告警屏蔽/告警中心路由壳） |
| notice | [pages/notice.md](./pages/notice.md) | 9 | 告警组、轮值、订阅报表（含 trace 报表微前端壳） |
| collect | [pages/collect.md](./pages/collect.md) | 7 | 采集配置（插件实例、目标节点、下发状态） |
| scene | [pages/scene.md](./pages/scene.md) | 14 | 场景监控：主机、APM、K8s、性能、RUM、自定义场景 |
| uptime | [pages/uptime.md](./pages/uptime.md) | 4 | 拨测任务与节点 |
| retrieval | [pages/retrieval.md](./pages/retrieval.md) | 8 | 数据检索、事件探索、指标管理、查询模板 |
| custom-report | [pages/custom-report.md](./pages/custom-report.md) | 6 | 自定义事件/指标上报与视图 |
| platform | [pages/platform.md](./pages/platform.md) | 13 | 平台配置、插件管理、AI 设置、Grafana、权限与迁移 |
| shell | [pages/shell.md](./pages/shell.md) | 13 | 微前端壳与通用独立页（分享/异常/导入导出等） |

## 分区索引 · 接口

| 分区 | 文件 | 接口数 | 覆盖内容 |
|---|---|---|---|
| alarm | [apis/alarm.md](./apis/alarm.md) | 100 | 告警策略/事件/屏蔽/分派（fta、strategies、promql_import、shield、event_center） |
| notice | [apis/notice.md](./apis/notice.md) | 28 | 通知方式、告警组、轮值、订阅报表（notice_group、user_groups、report…） |
| collect | [apis/collect.md](./apis/collect.md) | 40 | 采集配置与插件（collecting_config、collector_plugin…） |
| scene | [apis/scene.md](./apis/scene.md) | 45 | 场景视图与性能/K8s/APM/故障（scene_view、performance、k8s…） |
| uptime | [apis/uptime.md](./apis/uptime.md) | 27 | 拨测（uptime_check） |
| retrieval | [apis/retrieval.md](./apis/retrieval.md) | 13 | 查询模板与数据探索（query_template、data_explorer、query-api…） |
| custom-report | [apis/custom-report.md](./apis/custom-report.md) | 11 | 自定义事件/指标上报（custom_metric_report、custom_event_report） |
| commons | [apis/commons.md](./apis/commons.md) | 42 | 通用接口（业务/拓扑/ip 选择器/空间），被多页面共用 |
| platform | [apis/platform.md](./apis/platform.md) | 32 | 权限、外部集成、AI 设置、Grafana、平台开关（iam、external…） |

## 已知局限（本仓库特有，务必先读）

| # | 局限 | 影响 | 处置 |
|---|------|------|------|
| 1 | **微前端壳页面**：`alarm-shield.tsx`、`rotation.tsx`、`new-report.tsx`、`fta.tsx` 用 `@blueking/bk-weweb` 挂载子应用（实现在 `trace` 应用，本轮未索引） | 这些页面在本索引中显示「无接口命中」，**不代表无接口** | 改相关接口时到 `trace` 应用（`src/trace/pages/...`）确认，或另行建 `trace` 索引 |
| 2 | **store/本地封装中转**：`export-import/import-configuration` 的 `-upload` / `-importing` / `-history` 三页接口在父页 `import-configuration.vue` 与 store 中 | 3 个页面无直接命中 | 查 [pages/shell.md](./pages/shell.md) 同分区父页，或查 [apis/commons.md](./apis/commons.md) |
| 3 | **跨应用页面**：`/event-center*`、`/set-meal*` 的路由文件实际在 `src/fta-solutions/pages/` | 由 monitor-pc 路由注册，页面文件属 fta-solutions | 见 [pages/alarm.md](./pages/alarm.md) 中 `src/fta-solutions/...` 行 |
| 4 | **动态 URL / 运行时前缀** | 本轮扫描**无**不可解析插值的接口（0 条 `[待确认]`） | — |
| 5 | **未覆盖**：GraphQL / WebSocket / RPC；`http` 调用经多层自研封装的最终路径 | 此类调用不出现在映射中 | 按封装调用点回源码追 |
| 6 | 深度 2 的 🔵 候选占多数（664/1316） | 反向表可能偏大 | 只作参考；结论用 🟢/🟡 |
| 7 | `router/router-config.ts` 是**导航菜单配置**（`name/icon/path/href`），被路由提取规则识别成 44 条无组件路由条目 | 这批条目不出现在 `pages/` 表（无页面文件），**不影响页面覆盖**；已核查其中仅 `*`、`/fta/intergrations`（仅菜单项）、`/k8s/detail`（已注释）等无真实页面 | 需要菜单→页面映射时另查 `router-config.ts` |

## 新鲜度自检与重建

```bash
# 新鲜度（0 新鲜 / 6 过期 / 7 缺 meta.json）
python3 /root/.codebuddy/skills/frontend-index/scripts/scan_frontend.py \
  --root /root/bk-monitor/bkmonitor/webpack --check --index /root/bk-monitor/bk-monitor-wiki/.fe-index/monitor-pc

# 重建（一条命令 + 重跑标注脚本）
python3 /root/.codebuddy/skills/frontend-index/scripts/scan_frontend.py \
  --root /root/bk-monitor/bkmonitor/webpack --format json --max 5000 --out /root/bk-monitor/bkmonitor/webpack/temp/fe-index-monitor-pc-scan.json
python3 /root/bk-monitor/bkmonitor/webpack/temp/fe-index-monitor-pc-build.py
```
