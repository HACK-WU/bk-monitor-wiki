---
groupPath: 常用命令
relation: Issue 合并拆分单元测试运行
exportedAt: "2026-09-02T07:18:26.300Z"
---
运行 Issue 合并/拆分执行路径单元测试（alarm_backends/tests/service/fta_action/test_issue_merge.py，含 TestMergeGroupReparent 与批量拆分 TestSplitBatch）必须覆盖 Django 角色为 api。

- 符号: `cd bkmonitor && DJANGO_CONF_MODULE=conf.api.development.community .venv/bin/pytest alarm_backends/tests/service/fta_action/test_issue_merge.py -q`
- 单跑批量拆分用例: 追加 `::TestSplitBatch` 筛选
- 位置: `bkmonitor/pyproject.toml`（pytest env 默认 worker 角色）+ `bkmonitor/config/role/api.py`（api 角色 INSTALLED_APPS 同挂 kernel_api/monitor_web/fta_web/alarm_backends）
- 用法: `SplitResource`/`MergeResource` 来自 `kernel_api.views.v4.issue`，web 层 Resource 来自 `fta_web.issue.resources`，import 链同时需要两端 app，须 api 角色；web 层 serializer 契约测试（packages/fta_web/tests/issue）则用 web 角色（见「fta_web 单元测试运行」条目）
- 注: `kernel_api/tests/test_issue_v4.py` 的 split serializer 用例当前 @skip（跨层 import 耦合），解锁后同样用 api 角色运行