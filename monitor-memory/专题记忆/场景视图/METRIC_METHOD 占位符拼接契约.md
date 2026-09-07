---
groupPath: 专题记忆/场景视图
relation: METRIC_METHOD 占位符拼接契约
exportedAt: "2026-09-04T05:04:18.583Z"
---
进程指标聚合方法占位符拼接机制（2026-09-04 定稿：两级兕底 + 前端实测）：METRIC_METHOD（scene_view/builtin/host.py）中 system.proc 5 指标（cpu_usage_pct/mem_usage_pct/mem_res/mem_virt/fd_num）值为 "${method}_WITHOUT_TIME"（后缀大写与前端选项风格一致；uptime 恒为 MAX），由前端变量插值解析为 MAX_WITHOUT_TIME 等大写变体，查询侧归一为小写 max_without_time，保留 PromQL 风格（不做时间桶聚合）语义的同时让工具栏切换生效。
- 消费点: get_metric_panel @ monitor_web/scene_view/builtin/host.py（method = METRIC_METHOD.get(metric_id, "$method")）
- 兕底: normalize_metric_method @ bkmonitor/data_source/unify_query/functions.py，大小写归一（不区分大小写）+ 两级兕底：① 占位符未解析（含 $，如 "${method}_WITHOUT_TIME"；undefined 前缀为防御性，实测老前端不产生）→ 带 _without_time 后缀兕 sum_without_time（进程指标历史口径），其他兕 sum；② 枚举校验：以 _without_time 结尾但不在 AggMethods 合法枚举内（如拼接产物 distinct_without_time，AggMethods 仅 5 个变体）→ 儕 sum，避免生成 "{method}_over_time" 形态非法查询；均带 warning 日志；兕底产物规范形式保持小写（AggMethods 键名）；消费点在 data_source/__init__.py to_unify_query_config
- 前端实测（webpack/tests/tmp-method-placeholder-resolve.test.cjs，ts-node 直跑真实源码）：新前端 resolveValues/template-srv 与老前端 VariablesService 均能正确拼接四个选项（AVG/SUM/MIN/MAX → *_WITHOUT_TIME）；新前端变量缺失时占位符原样透返（含 $，后端兕底接住）；老前端变量缺失时 method 字段被置 undefined（getVariableValue 返回 null → replaceString isObj=true 提前返 null → transformVariables `v ?? undefined`）→ JSON 下发时字段消失 → 后端 metric.get("method") falsy 跳过聚合分支（与存量 $method 未解析行为一致，非本次引入）
- 关键语义: 分线场景（实例维度在 group_by、组内单 series）下切换 SUM/AVG/MIN/MAX 数值恒等不变，切换仅服务于按维度聚合（收敛实例维度）场景
- 后端测试: packages/fta_web/tests/scene_view/test_builtin_host.py 33 用例（web 角色）