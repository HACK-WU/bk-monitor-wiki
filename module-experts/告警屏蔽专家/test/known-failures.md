# 告警屏蔽模块 — 测试已知失败清单

> 记录在**当前开发环境**（稀疏检出 43%、Django 4.2.27、pyenv 3.11.10 + 项目 `.venv`）下运行测试时遇到的失败与规避方式。
> 逐切面标注：哪些失败属于**环境问题**（换环境可消除），哪些属于**测试本身限制**（需要修改测试/代码）。

---

## 1. pytest 启动即失败：filterwarnings 引用不存在的 Warning 类

- **切面**：全部测试（全局级）
- **级别**：🔴 阻塞
- **现象**：

```
ERROR: while parsing the following warning configuration:
  ignore::django.utils.deprecation.RemovedInDjango51Warning
AttributeError: module 'django.utils.deprecation' has no attribute 'RemovedInDjango51Warning'
```

- **根因**：`bkmonitor/pyproject.toml` 的 `[tool.pytest.ini_options] filterwarnings` 引用了 `RemovedInDjango51Warning`，但当前环境 Django 4.2.27 只有到 `RemovedInDjango50Warning` 为止，该属性不存在。pytest 启动解析 warning filter 时直接退出（EXIT=4），**任何** pytest 命令都无法运行。
- **性质**：环境问题（pyproject 配置假设 Django ≥ 5.1）。
- **规避**：加 `--override-ini "filterwarnings="`；或把 pyproject.toml 中该行改为 `ignore::DeprecationWarning` 等 Django 4.2 存在的类。
- **注意**：运行时 Django 4.2.27 本身会发出大量 `RemovedInDjango51Warning`（`index_together` 弃用等），`filterwarnings = ["error"]` 模式下这些 warning 会被升级为 error——这也是默认配置在低版本 Django 下不可用的原因之一。

---

## 2. settings 加载失败：BKAPP_DEPLOY_PLATFORM 为空

- **切面**：全部测试（全局级）
- **级别**：🔴 阻塞
- **现象**：

```
RuntimeError: Environment variable 'BKAPP_DEPLOY_PLATFORM' should not be empty.
```

- **根因**：`pyproject.toml` 用 `env = ["D:BKAPP_DEPLOY_PLATFORM=community", ...]`（pytest-env 的 `D:` = default 语义，仅在变量**未定义**时注入）。当 shell 已导出空字符串 `BKAPP_DEPLOY_PLATFORM=` 时，default 注入不生效。
- **性质**：环境问题。
- **规避**：运行前显式设置：
  ```bash
  export BKAPP_DEPLOY_PLATFORM=community
  export DJANGO_CONF_MODULE=conf.worker.development.community
  export USE_DYNAMIC_SETTINGS=0
  ```

---

## 3. 系统 Python 缺依赖：No module named 'bkcrypto'

- **切面**：全部测试（全局级，若不用 `.venv`）
- **级别**：🔴 阻塞
- **现象**：

```
ModuleNotFoundError: No module named 'bkcrypto'
ImportError: Could not import config 'conf.worker.development.community' ... No module named 'bkcrypto'
```

- **根因**：settings → `config.default` 依赖 `bkcrypto`（bk-monitor-base 依赖链），系统 pyenv Python 未安装该依赖。
- **性质**：环境问题。
- **规避**：使用项目虚拟环境运行：`.venv/bin/python -m pytest ...`。`test_quick_shield.py` 头部注释也说明了这一点："开发环境依赖链（bk_monitor_base → bkcrypto → jinja2）不完整，测试以 Mock 方式隔离所有外部依赖"。

---

## 4. test_add_shield.py：Django app 未注册（收集期失败）

- **切面**：CRUD Resource 测试（`tests/api/fta/test_add_shield.py`）
- **级别**：🟡 环境问题（该文件不在默认 testpaths）
- **现象**：

```
RuntimeError: Model class monitor_web.extend_account.models.UserAccessRecord doesn't declare
an explicit app_label and isn't in an application in INSTALLED_APPS.
```

- **触发链**：`test_add_shield.py` 导入 `fta_web.alert.resources` → `bkmonitor.share` → `monitor_web.models` → `monitor_web.extend_account.models`，其中 `UserAccessRecord` 未被当前 conf 环境（`conf.worker.development.community`）的 INSTALLED_APPS 收录。
- **性质**：环境/配置问题（该文件不在默认 testpaths，属按需运行）。
- **规避**：核对 conf 环境的 INSTALLED_APPS 是否包含 `monitor_web.extend_account`；或在完整部署环境中运行。

---

## 5. test_shield.py：迁移图不一致 + 测试库已存在（DB setup 失败）

- **切面**：引擎层测试（`alarm_backends/tests/service/converge/test_shield.py`）
- **级别**：🔴 阻塞
- **现象**：

```
django.db.migrations.exceptions.NodeNotFoundError: Migration metadata.0252_migrate_custom_ts_data
dependencies reference nonexistent parent node ('monitor_web', '0076_auto_20250408_1522')

Got an error creating the test database: (1007, "Can't create database 'test_bkmonitor_saas'; database exists")
```

- **根因**：
  1. 当前工作区为**稀疏检出（43%）**，`monitor_web` 的 `0076_auto_20250408_1522` 迁移文件缺失，导致迁移图不完整。
  2. 测试库 `test_bkmonitor_saas` 已存在但状态不一致，`create_test_db` 报 1007。
- **性质**：环境问题（完整检出 + 清理测试库后可恢复）。
- **规避**：完整拉取 `monitor_web/migrations/` 迁移文件；删除残留的 `test_bkmonitor_saas` 数据库后重跑。
- **注意**：`alarm_backends/tests/conftest.py` 的 `TestCase.databases = {"default", "monitor_api"}` 要求 MySQL 提供两个测试库，本地运行需配置可写的 DB 账号。

---

## 6. 运行时 DeprecationWarning 噪音

- **切面**：全部测试
- **级别**：🟢 非阻塞
- **现象**：每次运行输出约 49 条 warning（`pipes`/`cgi`/`sre_constants` 的 Python 3.13 deprecation、`index_together`、`USE_DEPRECATED_PYTZ` 等）。
- **性质**：Django 4.2 与依赖库的预期弃用告警，不影响结果。
- **规避**：无需处理；注意默认 `filterwarnings = ["error"]` 会把其中部分升级为 error（见 #1），已通过 `--override-ini "filterwarnings="` 规避。

---

## 结论

- **可稳定运行**：`test_quick_shield.py`（11 用例）、`test_strategy_target_shield.py`（3 用例）——纯单元/纯函数测试，Mock 隔离，验证全绿。
- **当前环境不可运行**：`test_add_shield.py`（app 注册）、`test_shield.py`（迁移图 + 测试库）——均属环境问题，完整环境（全量检出 + 配置 DB）下预期可运行。
- **全局前置**：`--override-ini "filterwarnings="` + 显式环境变量 + `.venv` 是任何 shield 测试在当前工作区运行的前提。
