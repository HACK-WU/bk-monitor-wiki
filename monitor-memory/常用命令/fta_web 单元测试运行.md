---
groupPath: 常用命令
relation: fta_web 单元测试运行
exportedAt: "2026-09-02T03:57:20.045Z"
---
运行 fta_web（web 层）单元测试必须覆盖 Django 角色为 web，否则模型定义阶段即报错全挂。

- 符号: `cd bkmonitor && DJANGO_CONF_MODULE=conf.web.development.community .venv/bin/pytest packages/fta_web/tests/issue -q`
- 位置: `bkmonitor/pyproject.toml`（pytest env 默认值）+ `bkmonitor/config/role/web.py`（web 角色 INSTALLED_APPS）

## 原因
- pyproject.toml 的 pytest 默认 env 是 worker 角色（`DJANGO_CONF_MODULE=conf.worker.development.community`），worker 的 INSTALLED_APPS **不含 fta_web/monitor_web** → import `fta_web.models.alert` 定义模型时 Django 报 "doesn't declare an explicit app_label / not in INSTALLED_APPS"，整个测试文件全 F（含改动前就存在的用例）
- 默认 `testpaths` 只含 worker 可跑目录（alarm_backends/tests、data_source/tests、metadata/tests），fta_web 测试需显式指定路径
- settings.py 只用 DJANGO_CONF_MODULE 解析出 ROLE，再 import `config.role.{ROLE}`，所以覆盖为 `conf.web.development.community` 即可切换 web 角色（无需 config/web 目录）

## 注意
- 项目 venv 在 `bkmonitor/.venv`（Django 4.2.27）；pyenv 全局 python 的 Django 版本更老，跑 pyproject 的 filterwarnings 会报 RemovedInDjango51Warning 解析错误，须用 .venv 的 pytest
- kernel_api 侧测试（如 kernel_api/tests/test_issue_v4.py）在纯 web/api 角色环境仍无法 import（import 链 transitively 引入 alarm_backends.service.scheduler 的 worker-only 配置），相关用例按文件内既有 skip 约定标记 skip
- 已知无关失败：packages/fta_web/tests/issue/test_issue_trend_contract.py 因 commit 76ad63a988（story 136920675）改掉 use-alarm-table.ts 写法而失败，属既有问题