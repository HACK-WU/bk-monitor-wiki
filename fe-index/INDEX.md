# 索引登记表（.fe-index/）

> 本目录实际位于 `bk-monitor-wiki/.fe-index/`，仓库根 `/root/bk-monitor/.fe-index` 是指向它的**软链接**（两条路径等效）。
> 作为多应用总登记表。涉及下列应用的问题，先查对应入口，再看代码。
> 索引是**快照**，查前先跑新鲜度校验（各端命令见下）。
> 「根目录」列为**绝对路径**（因本目录已不在仓库根下，相对路径会随访问路径漂移，故统一写绝对路径）。

| 应用 | 类型 | slug | 根目录 | 规模 | commit | 生成日期 | 入口 |
|------|------|------|--------|------|--------|----------|------|
| bkmonitor（Django 后端） | backend | bkmonitor | `/root/bk-monitor/bkmonitor` | 模块 24 · 表 286 · 依赖边 125 | `ff89f63` | 2026-10-13 | [bkmonitor/index.md](./bkmonitor/index.md) |
| monitor-pc（监控前端微应用） | frontend | monitor-pc | `/root/bk-monitor/bkmonitor/webpack` | 页面 85 · 接口 338 · 映射 1316 | `90a2de6` | 2026-10-13 | [monitor-pc/index.md](./monitor-pc/index.md) |

## 声明文件

| 端 | 文件 | 关键字段 | 说明 |
|----|------|----------|------|
| backend | `.fe-index/config.json`（本目录） | `root: "/root/bk-monitor/bkmonitor"` · `framework: django` · `exclude: ["webpack/**"]` · `expertsDir`（绝对路径） | **`root` 已改绝对路径**：脚本按「声明文件所在目录」解析相对 root，而本目录不在仓库根下，相对值会被解析成 `bk-monitor-wiki/bkmonitor`（不存在）。上层声明只能「收窄」范围（v2.1.0 起会拒绝放大并提示） |
| frontend | `.fe-index/config.json`（本目录） | `root: "/root/bk-monitor/bkmonitor/webpack"` · routes / pagesDirs / apiDirs / aliases | 同上，`root` 用绝对路径；`aliases` 等内部相对键仍相对 root，不受影响 |

## 重建

技能已迁入项目：`/root/bk-monitor/.codebuddy/skills/backend-index/`（原用户级位置已移除）。

### 后端（三步，顺序错会丢语义标注）

> ⚠️ 索引已不在仓库根下，**所有输出路径必须写绝对路径**（走软链接或 wiki 真实路径都行，指向同一处）。

```bash
cd /root/bk-monitor
SKILL=/root/bk-monitor/.codebuddy/skills/backend-index/scripts/scan_backend.py
CFG=/root/bk-monitor/.fe-index/config.json
IDX=/root/bk-monitor/.fe-index          # 或 /root/bk-monitor/bk-monitor-wiki/.fe-index
# 1) 机器可读扫描结果（必须与 --emit-tree 分开跑：v2.1.0 起两者可并存，但分开更直观）
python3 $SKILL --root /root/bk-monitor/bkmonitor --config $CFG \
  --format json --out bkmonitor/temp/be-index-bkmonitor-scan.json
# 2) 落树（必须绝对路径；相对路径会落到 cwd 下的 .fe-index/）
python3 $SKILL --root /root/bk-monitor/bkmonitor --config $CFG \
  --emit-tree $IDX/bkmonitor
# 3) 语义标注（模块职责 / 专家人工指认 / 未归属 / 前缀口径 / 待确认复核）
python3 bkmonitor/temp/be-index-bkmonitor-build.py
```

### 前端

```bash
cd /root/bk-monitor/bkmonitor/webpack
python3 /root/.codebuddy/skills/frontend-index/scripts/scan_frontend.py --root /root/bk-monitor/bkmonitor/webpack \
  --format json --max 5000 --out temp/fe-index-monitor-pc-scan.json
python3 temp/fe-index-monitor-pc-build.py
```

### 新鲜度校验

```bash
# 后端（v2.1.0 起尊重 meta.exclude：webpack/** 的改动不再误报过期）
python3 /root/bk-monitor/.codebuddy/skills/backend-index/scripts/scan_backend.py \
  --root /root/bk-monitor --check --index /root/bk-monitor/.fe-index/bkmonitor
# 前端
python3 /root/.codebuddy/skills/frontend-index/scripts/scan_frontend.py \
  --root /root/bk-monitor/bkmonitor/webpack --check --index /root/bk-monitor/.fe-index/monitor-pc
```

## 目录位置与软链接

```
/root/bk-monitor/
├── .fe-index -> bk-monitor-wiki/.fe-index   # 软链接，保持旧路径可用
└── bk-monitor-wiki/
    └── .fe-index/                            # 真实位置
```

- 两条访问路径（`/root/bk-monitor/.fe-index/...` 与 `/root/bk-monitor/bk-monitor-wiki/.fe-index/...`）**等效**，实测前后端校验命令均通过。
- `config.json` 的 `root` 已改绝对路径，原因见上「声明文件」表。
- 若软链接失效（如整体搬迁），脚本找不到 `.fe-index/` 时按 skill 约定**逐级向上找 ≤3 层**，仍可命中 wiki 内目录。

## ⚠️ 待清理（遗留，暂未删除）

`bkmonitor/.fe-index/bkmonitor/` 是一棵**用错误 root（`/root/bk-monitor`）生成**的旧树（模块 31 / 表 355 / 未打语义标注），已确认无用：

```bash
rm -rf /root/bk-monitor/bkmonitor/.fe-index
```

## 脚本缺陷状态（backend-index / scan_backend.py）

**7 个缺陷已在 v2.1.0 全部修复**（位置、症状、修法见 `.codebuddy/skills/backend-index/reference.md` §5.3）：

| # | 缺陷 | 验证证据 |
|---|------|----------|
| 1 | 上层声明把 `--root` 放大到祖先目录 | `--root bkmonitor/packages` → 打印「在 --root 之外，已忽略该上层声明」，按 CLI 执行 ✅ |
| 2 | Django `被依赖` 恒为空（类名 vs 导入路径） | 修复后 19/24 模块有被依赖（`bkmonitor ←21`、`drf-resource ←18`、`bkm-space ←15`）✅ |
| 3 | 幽灵表（基类含 model 即算 + 邻居 db_table 窗口） | 表数 318 → **286**（`BaseDictObj`/`CleanRule` 等 32 张假表清零，`*Field` 真模型保留）✅ |
| 4 | `core` 同名歧义（basename 撞车） | 按 `AppConfig.name` 最长前缀匹配；weixin `core` 被依赖 19 → **0**，`core.drf_resource` 独立成边 ✅ |
| 5 | `--check` 不看 `exclude` | A/B 实测：含 exclude → 退出 0（「范围内无变化」）；去掉 exclude → 退出 6 误报 2 个 webpack 文件 ✅ |
| 6 | `--emit-tree` 吞 `--format json --out` | 两者并存时 JSON 与树都写出 ✅ |
| 7 | `expertsDir` 按 cwd 解析 | 声明里的相对路径改按**声明所在目录**解析；绝对路径两条调用路径一致 ✅ |

> 后处理脚本 `bkmonitor/temp/be-index-bkmonitor-build.py` 已同步简化为**纯语义标注**（不再做机械修正）。

## 消费口径速记

| 我要… | 去哪查 |
|-------|--------|
| 改某张后端表，看影响哪些模块 | `bkmonitor/tables.md`（表 → 模块，含引用次数与来源） |
| 改某个后端模块，看影响谁 | `bkmonitor/modules/{slug}.md` 的「被依赖」+ `bkmonitor/index.md` 第 2 节 |
| 后端模块职责 / 挂载前缀 / 未归属代码 | `bkmonitor/index.md` 第 1、6、7 节 |
| 后端接口契约怎么用 | `.module-experts/`（11 个专家包，模块卡里有指针）或 ki `tags=api` |
| 改前端接口，看影响哪些页面 | `monitor-pc/apis/{分区}.md` |
| 接前端页面任务 | `monitor-pc/pages/{分区}.md` |
| 跨端 join（后端接口 → 前端页面） | 后端模块「挂载前缀」× 前端接口路径（后端口径见 `bkmonitor/index.md` 第 7 节） |
