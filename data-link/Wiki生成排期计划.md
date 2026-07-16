<!-- [待审核] AI 自动生成，请人工确认后移除此标记 -->

# data-link 模块 Wiki 生成排期计划

> 适用范围：`bkmonitor-datalink/pkg` 下各模块的 Wiki 文档生成排期。
> 文档风格：概览/核心模型/处理或消费/存储/配置/HTTP指标/工具 等分章，带 `章节来源` 行号引用，并通过 `scripts/wiki_format_check.py` 格式校验。
> 生成时间：2026-07-16

<cite>
**本文引用的目录与脚本**
- [bkmonitor-datalink/pkg](file://bkmonitor-datalink/pkg)
- [bk-monitor-wiki/data-link](file://bk-monitor-wiki/data-link)
- [wiki_format_check.py](file://bk-monitor-wiki/scripts/wiki_format_check.py)
</cite>

## 目录

1. [现状盘点](#现状盘点)
2. [排期计划](#排期计划)
3. [执行约束](#执行约束)
4. [里程碑建议](#里程碑建议)

## 现状盘点

`pkg` 下共 13 个模块，已生成 Wiki 5 个，**未生成 8 个**。

### 已生成 Wiki（5）

| 模块 | 文档数 |
|---|---|
| `bk-log-sidecar` | 10 |
| `bk-monitor-worker` | 10 |
| `bkmonitorbeat` | 9 |
| `collector` | 13 |
| `unify-query` | 31 |

### 未生成 Wiki（8）

| 模块 | .go 文件数 | 角色定位 | 体量 |
|---|---|---|---|
| `transfer` | 490 | 核心：数据采集路由 / ETL / 分发中央枢纽 | 🔴 超大 |
| `influxdb-proxy` | 130 | influxdb 查询 / 写入代理（route / backend / cluster / consul） | 🟠 大 |
| `operator` | 151 | K8s Operator（apis / client / operator 71 文件） | 🟠 大 |
| `libgse` | 62 | GSE beat 框架 SDK（beat / output / processor / gse） | 🟡 中 |
| `ingester` | 62 | 数据接入（poller / processor / datasource / define） | 🟡 中 |
| `utils` | 31 | 公共工具库（host / http / logger / relation / validator …） | 🟢 小 |
| `bkm-ksm-exporter` | 6 | K8s 状态指标 exporter | 🟢 小 |
| `sliwebhook` | 5 | SLI webhook 服务 | 🟢 小 |

**章节来源**
- [bkmonitor-datalink/pkg](file://bkmonitor-datalink/pkg)
- [bk-monitor-wiki/data-link](file://bk-monitor-wiki/data-link)

## 排期计划

按「优先级 + data-link 数据流顺序」分为 3 个阶段。预估文档数基于既有模块的体量经验（如 `bk-monitor-worker` 10 篇、`collector` 13 篇、`unify-query` 31 篇）。

### P1 — 核心数据流（高优先级，建议先启动）

| 模块 | 预估文档数 | 拆分建议 | 顺序依赖 |
|---|---|---|---|
| `transfer` | 15-20 | 按子包拆章：概览/架构、etl、pipeline、storage、consul、bufferpool、define、kafka、elasticsearch、influxdb、shipper、scheduler 等 | 无，首启动 |
| `influxdb-proxy` | 8-10 | 概览/架构、route、backend、cluster、consul、http、transport、common | 紧随 `transfer` |

> 说明：`transfer` 体量远超其它模块（490 个 .go 文件），建议作为单独一大块集中处理；可先交付「概览 + 架构」单章，再逐子包补全，降低单次交付风险。

### P2 — 平台支撑（中优先级，可与 P1 部分并行）

| 模块 | 预估文档数 | 拆分建议 |
|---|---|---|
| `operator` | 8-10 | 概览/架构、apis(CRD)、client、operator 控制器、common、reloader、cmd |
| `ingester` | 5-7 | 概览/架构、poller、processor、datasource、define、http |
| `libgse` | 4-6 | 概览/架构、beat 框架、output、processor、gse SDK |

### P3 — 轻量独立（低优先级，最后收尾）

| 模块 | 预估文档数 | 拆分建议 |
|---|---|---|
| `utils` | 3-5 | 概览 + 子包分组（host/http/logger/relation/validator 等） |
| `bkm-ksm-exporter` | 3-4 | 概览/架构、collectors、exporter |
| `sliwebhook` | 3-4 | 概览/架构、server、config |

**章节来源**
- [bkmonitor-datalink/pkg/transfer](file://bkmonitor-datalink/pkg/transfer)
- [bkmonitor-datalink/pkg/influxdb-proxy](file://bkmonitor-datalink/pkg/influxdb-proxy)
- [bkmonitor-datalink/pkg/operator](file://bkmonitor-datalink/pkg/operator)
- [bkmonitor-datalink/pkg/ingester](file://bkmonitor-datalink/pkg/ingester)
- [bkmonitor-datalink/pkg/libgse](file://bkmonitor-datalink/pkg/libgse)
- [bkmonitor-datalink/pkg/utils](file://bkmonitor-datalink/pkg/utils)
- [bkmonitor-datalink/pkg/bkm-ksm-exporter](file://bkmonitor-datalink/pkg/bkm-ksm-exporter)
- [bkmonitor-datalink/pkg/sliwebhook](file://bkmonitor-datalink/pkg/sliwebhook)

## 执行约束

1. **风格一致**：所有新文档沿用既有系列格式（`<!-- [待审核] -->` 头、`<cite>` 引用、`目录`、`章节来源`/`图表来源` 行号链接）。
2. **格式门禁**：每篇写完后执行 `python3 bk-monitor-wiki/scripts/wiki_format_check.py --file <path> --strict`，确保 0 错误 0 警告。
3. **内容核实**：关键符号、端口、阈值、cron、行号须对照源码核实，不凭空生成。
4. **不主动提交**：按仓库约定，文档生成后不自动 git 提交，入库需人工确认。

**章节来源**
- [wiki_format_check.py](file://bk-monitor-wiki/scripts/wiki_format_check.py#L1-L60)

## 里程碑建议

| 里程碑 | 范围 | 交付物 |
|---|---|---|
| M1 | P1：`transfer` 概览 + `influxdb-proxy` 全量 | transfer 首章 + influxdb-proxy 8-10 篇 |
| M2 | P1：`transfer` 其余子包全量 | transfer 补全至 15-20 篇 |
| M3 | P2：`operator` / `ingester` / `libgse` | 三模块全量 |
| M4 | P3：`utils` / `bkm-ksm-exporter` / `sliwebhook` | 三模块全量，data-link 13 模块 Wiki 全覆盖 |

**章节来源**
- [bkmonitor-datalink/pkg](file://bkmonitor-datalink/pkg)
- [bk-monitor-wiki/data-link](file://bk-monitor-wiki/data-link)
