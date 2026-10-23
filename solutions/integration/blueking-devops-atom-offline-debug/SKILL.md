---
name: blueking-devops-atom-offline-debug
description: 在没有蓝盾（DevOps）插件工作台权限的情况下离线联调流水线插件——本地起服务模拟插件编排页、按真实契约 mock 依赖接口（selector 选项接口 + 插件被调用的业务 API）、直接跑插件本体并回显日志；同时规避 selector 的 CORS/预检陷阱与「mock 地址混进 task.json 发布物」的红线。触发词：蓝盾插件联调, 流水线插件本地调试, 插件工作台没权限, task.json 调试, selector 拉不到选项, optionsConf 跨域, python_atom_sdk, get_sensitive_conf, bk-monitor-shield
category: integration
tags: [蓝盾, devops, 流水线插件, atom, task.json, python_atom_sdk, selector, CORS, mock, 离线联调, bk-monitor-shield]
created: 2026-09-21
updated: 2026-09-21
---

# 蓝盾流水线插件离线联调（无平台权限）

## 场景

要开发/维护一个蓝盾（DevOps）流水线插件（`task.json` + `python_atom_sdk`），但：

- **登不上插件工作台**（无权限）→ 用不了官方"测试阶段在线调试"，也拿不到平台的错误提示；
- 插件的 `input.xxx.optionsConf.url`（selector 选项接口）从**浏览器**发跨域请求，天然后置依赖平台侧网关注册；
- 插件本体要调业务 API（本例是监控的告警屏蔽接口），本地没有真实网关。

典型问题：插件参数改了不知道对不对、selector 拉不到选项、插件跑起来到底发了什么请求、构造的请求体是否合规。

本方案用**一个本地 stdlib 服务**同时解决：模拟编排页（渲染 `task.json` 并产出 `input.json`）、mock 依赖接口（按真实契约校验 + 返回）、真跑插件并回显日志。

## 问题

1. **两个数据面必须分清**（最容易走错）：`optionsConf.url` 由**蓝盾前台浏览器**调用（前端面）；插件运行时调的 `monitor_url` 由**插件进程**调用（进程面）。只想调插件逻辑时，前端面根本不用管（`input.json` 里手写值即可）。
2. **selector 的跨域是硬约束**：官方要求第三方 API 先接入蓝鲸网关再配 CORS。实测某真实网关直接拒绝：`OPTIONS` → `404 API not found`、响应无 `Access-Control-Allow-Origin`、裸 GET 报 `user authentication failed`（要用户态身份）→ 蓝盾前台拿不到选项。
3. **SDK 从哪里读数据不明确**：输入、敏感配置（`get_sensitive_conf`）、流水线内置变量的来源都不是文档里一眼可见的。
4. **`task.json` 是发布物**：为调试把 URL 改成 mock，很容易跟着版本上架。

## 解决方案

### 0. 先分清两个数据面

| 面 | 谁发请求 | 不mock 的后果 | 本地可验证性 |
|---|---|---|---|
| 前端面 `optionsConf.url` | 蓝盾前台浏览器 | 下拉框空白（但字段可 `required=false` 兜底） | 只能用 curl 模拟浏览器（预检+GET）自证 CORS 合规 |
| 进程面 `monitor_url`（`.../add_shield/` 等） | 插件进程 | 真打到线上网关 | ✅ 完全可本地闭环 |

> 关键结论：**没有蓝盾权限时，前端面的 mock 没有消费方**（没人会去请求它）——真正立刻有收益的是进程面。

### 1. 环境准备

```bash
cd <plugin-repo>
python3 -m venv .venv && . .venv/bin/activate     # 插件 .gitignore 通常已忽略 .venv/
# 私有源只有内网包，第三方包要走公网 PyPI
pip install --index-url https://pypi.org/simple \
  --extra-index-url https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple/ \
  --trusted-host mirrors.tencent.com python-atom-sdk wheel ply requests
```

实测坑：

- 内网 `mirrors.tencent.com/repository/pypi/tencent_pypi/simple/` 是**私有窄源**，simple 索引里只有 `python-atom-sdk` / `qfsclient`，`ply`/`requests`/`setuptools` 全 404 → **必须同时给 `--index-url https://pypi.org/simple`**。
- `python-atom-sdk` 只有 sdist，构建时报 `invalid command 'bdist_wheel'` → 先装 `wheel`（或 `--no-build-isolation`）。
- 插件若依赖 `ply` 却没写进 `requirements.txt`，本地会直接 ImportError——补上依赖（这也是线上换构建机的隐性风险）。

### 2. 启动（服务 + 页面）

```bash
# 在插件工程内（脚本放 <plugin>/devtools/）
python3 devtools/offline_console.py --listen 18081
# 或用本 solution 的副本，显式指定插件工程根
python3 scripts/offline_console.py --repo /path/to/<plugin-repo> --listen 18081
```

浏览器打开 `http://<host>:18081/`（监听默认 `0.0.0.0`，便于端口转发；页面与脚本必须同目录）。页面按 `task.json` 渲染表单（组件/rely/required/分组），一键生成 `input.json`、真跑插件、回显 stdout / `output.json`、并把服务端收到的请求列出来。

### 3. mock 什么、按什么契约 mock

**前端面**：`GET /mock/strategy-list/?bk_biz_id=xx` 返回网关规范形状，并**正确应答预检**（对照真实网关的 404）：

```json
{"status": 0, "data": [{"optionId": "1540", "optionName": "..."}], "message": ""}
```
响应头需含 `Access-Control-Allow-Origin`（echo Origin 比 `*` 更贴近真实）、`Access-Control-Allow-Methods`（含 OPTIONS）、`Access-Control-Allow-Headers`（**必须含 `x-devops-project-id`**）。

**进程面**：按被调业务接口的真实序列化器校验后返回。以监控告警屏蔽为例（源：`bkmonitor/packages/monitor_web/shield/serializers.py`、`backend_resources.py`）：

| 项 | 契约 |
|---|---|
| 对外路径族 | 蓝鲸网关：`/app/shield/{add,disable,edit,detail,search}/` → 后端 `/api/v4/shield/*`；**ESB compapi**：`POST /api/c/compapi/v2/monitor_v3/add_shield/`；插件常用后缀：`.../add_shield/` |
| 必填字段 | `bk_biz_id`(int) / `category` / `begin_time` / `end_time` / `dimension_config`(非空对象) / `shield_notice`(bool) |
| `category=strategy` | `dimension_config = {id: [int] 必填, level?, scope_type?, target?, dimension_conditions?}` |
| `category=dimension` | `dimension_config = {dimension_conditions 必填}` |
| `dimension_conditions[]` | `{key, value: [str], method?, condition?, name?}`；`method` 合法值 = `include/exclude/gt/gte/lt/lte/eq/neq/reg/nreg`（**无 contain/not_contain**）；`condition` 仅 `or/and` |
| 成功响应 | add → `{"result": true, "data": {"id": N}}`；disable → `{"result": true, "data": "success"}` |
| 失败响应 | `400 + {"result": false, "code": 1640001, "code_name": "INVALID_ARGS", "message": "Parameters error [reason=...]"}` |
| 兼容点 | `disable` 的 `id` 可为标量（后端 `to_internal_value` 自动包成单元素列表） |

> **mock 要与后端同等宽松**（`bk_biz_id` 收数字字符串、bool 收 `"true"/1`、标量 id 自动包列表），否则 mock 会制造"假失败"，比不校验更糟。

### 4. SDK 环境契约（python_atom_sdk 1.2.19 源码实证）

| 项 | 结论 | 来源 |
|---|---|---|
| 输入 | `get_input()` 读 `$bk_data_dir/$bk_data_input`（默认 `./input.json`） | `sdk/input.py:20-28` |
| **敏感配置** | `get_sensitive_conf(key)` 取 **input.json 里的 `bkSensitiveConfInfo` 字段**（不是环境变量、不是接口） | `sdk/__init__.py:95-107` |
| 流水线内置变量 | `BK_CI_START_USER_NAME` / `BK_CI_PIPELINE_UPDATE_USER` / `BK_CI_PIPELINE_CREATE_USER` 等**同样来自 input.json** | `sdk/__init__.py:55-90` |
| 输出 | `set_output()` 写 `$bk_data_dir/$bk_data_output`（默认 `./output.json`），并校验 `status`/`type`/`data` 形状 | `sdk/output.py:69-85` |
| 日志 | `python_atom_sdk.log` → stdout，带 `##[level]` 前缀 | `sdk/bklog.py:40-58` |
| `.sdk.json` | 仅调用 openapi（构件/通知）时才读 `$bk_data_dir/.sdk.json`，业务插件通常不需要 | `sdk/openapi.py:94-101` |

⇒ 本地跑插件只需：

```bash
bk_data_dir=<tmp> bk_data_input=input.json bk_data_output=output.json \
  python -c "from <pkg>.command_line import main; main()"
```
`input.json` 里塞业务入参 + `bkSensitiveConfInfo`（把 `monitor_url` 指向本地 mock）+ 伪造的 `BK_CI_*` 用户变量即可。

### 5. 自检（把"能不能跑"变成断言）

```bash
python3 selfcheck.py --base http://127.0.0.1:18081
```
覆盖：预检 204 + CORS 头、mock 数据形状、三条路径族、契约守门（非法 `method`/缺必填字段必须被拒）、**组件覆盖度与页面实现一致性**、**校验器（required / rule / rely 可见性）**、插件真跑（exit 0 且拿到 mock 返回的 id）、请求日志。本 solution 副本实测 **37/37 通过**。

### 6. 组件覆盖度与校验模式（两个"把经验变成断言"的开关）

**① 组件覆盖度**：页面按 `task.json` 的 `input` 动态渲染（`buildControl` 按 `field.type` 分发），但渲染器只实现了部分组件。服务端维护 `EXPLICIT_TYPES`（有专属渲染）/ `GENERIC_INPUT_TYPES`（与 fallback 等价，如 `vuex-input`）/ `DEGRADED_TYPES`（降级为文本框，如 `time-picker`、`dynamic-parameter*`），页面顶部按 `task.json` 实际用到的类型显示绿/黄提示。
**selfcheck 断言两件事**：`task.json` 用到的类型全部已登记；且**服务端清单与页面里的 `type === "..."` 分支集合逐字一致**（清单靠 grep 页面而来，两边不可能静默漂移）。插件以后新增组件类型会立刻暴露。

**② 校验模式**：
| 模式 | 行为 |
|---|---|
| 宽松（默认） | 不拦截，允许提交非法值——保留"故意喂坏数据看插件怎么反应"的能力（本方案的 2 个插件缺陷就是这么发现的） |
| 严格 | 提交前调 `POST /api/validate`：只校验 **rely 可见**字段的 `required` + `rule`（`alpha/numeric/alpha_dash/alpha_num/min/max/regex`），失败标红并阻止 |

两个语义取舍（**待平台实测校准，别当平台事实**）：① 只校验可见字段（官方未说明隐藏字段是否参与校验）；② `rule.regex` 用**部分匹配**（依据配置规范的示例 `"^[0-9]"` + "以数字开头"；`fullmatch` 会把 `1x` 误判为非法——自检曾因此失败并修正）。

## 关键代码

```python
# offline_console.py 关键点 1：只要与脚本同目录即可服务页面；插件工程根可 --repo 指定
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)          # 默认 <plugin>/devtools/ 的上一级
args = parser.parse_args()
if args.repo:
    REPO_ROOT = os.path.abspath(args.repo)       # 副本放别处运行时必须指定
```

```python
# offline_console.py 关键点 2：真跑插件 = 按 SDK 契约喂 env + 子进程
env.update({"bk_data_dir": data_dir, "bk_data_input": "input.json",
            "bk_data_output": "output.json", "PYTHONPATH": REPO_ROOT})
subprocess.run([venv_python, "-c", "from <pkg>.command_line import main; main()"], env=env)
```

```python
# offline_console.py 关键点 3：一条路由吃下三种真实路径族
if path.endswith(("/add_shield", "/shield/add", "/v4/shield/add")):        return "add_shield"
if path.endswith(("/disable_shield", "/shield/disable", "/v4/shield/disable")): return "disable_shield"
```

## 注意事项（红线优先）

1. 🚩 **mock 地址绝不进发布物**：`task.json` 会随版本发布到插件市场。调试用的 URL 必须可还原（调试分支承载 / 发布前 `git diff` 卡点），`.ci` 的代码扫描不会替你拦。
2. 🚩 **`.sdk.json` / `input.json` 不要提交**：`.sdk.json` 在真实环境含**真实凭证**（误提交需轮换）；把它们加进插件 `.gitignore`。
3. **selector 走的是真实规则，不是"随便一个 URL 都行"**：官方要求接入蓝鲸网关并配 CORS（含 `x-devops-project-id`）；直连 mock 时用 `http://localhost|127.0.0.1`（浏览器视其可信），**内网 IP + http 会被 https 页面按混合内容拦掉**。
4. **不要用 mock 冒充平台事实**：模拟器无法证明蓝盾真实前端的 origin、附加请求头、渲染细节、URL 白名单校验——所有推断都应标注"待平台实测确认"。
5. **`/api/run` 能执行插件逻辑**：仅限受信网络使用，或 `--host 127.0.0.1` 收口。
6. 排查"下拉框拉不到选项"的顺序：先 F12 看请求有没有发出 → 再看是否被预检拦住（OPTIONS 非 2xx）→ 再看是否缺 `Access-Control-Allow-Origin` → 最后看认证（`app_code`/用户态）。
7. **`scripts/` 是快照，不是源**：本 solution 的副本取自 `bk-monitor-shield/devtools/`（2026-09-21）。源目录演进后需手工同步副本，**冲突时以 `devtools/` 为准**；`scripts/logs/` 是运行时产物，可不提交。

## 已验证（2026-09-21）

- 服务实跑 + 自检 **37/37 通过**（含插件真跑：`exit 0`、stdout 有 `##[info]` 日志、mock 端收到完整请求体）。
- 用副本 + `--repo` 从本 solution 目录运行同样 37/37，证明副本可移植。
- 覆盖度自检已能发现"清单漂移"：服务端 `EXPLICIT_TYPES` 与页面 `type === "..."` 分支逐字比对（grep 页面而来），当前一致。
- 同时抓到被联调插件的 2 个真实缺陷（错误码归类反、`duration` 空串崩溃）——**说明"能断言"比"能跑起来"更有价值**。

## 相关资产

- 插件侧工程与资产：`bk-monitor-shield/{task.json, devtools/, docs/蓝盾流水线插件开发速查.md}`
- 平台文档（iWiki）：插件开发快速入门 15008942 / 配置规范 15009001 / 开发规范 15009003 / Python 指引 15009033 / 调试指引 17512739 / 第三方 API 接入蓝鲸网关 15009171
- 姊妹方案：[local-kernel-api-proxy](../local-kernel-api-proxy/SKILL.md)（进程 → 进程转发代理，无浏览器/CORS 面）
