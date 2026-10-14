---
groupPath: 专题记忆/蓝盾插件离线联调
relation: 离线联调控制台与SDK契约
exportedAt: "2026-09-21T02:55:39.041Z"
---
- 场景：蓝盾（DevOps）流水线插件（task.json + python_atom_sdk）在无插件工作台权限时做离线联调
- 解决方案资产：bk-monitor-wiki/solutions/integration/blueking-devops-atom-offline-debug/SKILL.md，含 scripts/ 三件套副本（--repo 指定插件工程根即可移植）
- 落地位置：bk-monitor-shield/devtools/{offline_console.py 服务, console.html 页面, selfcheck.py 自检}，服务端口 18081，自检 26/26 通过
- 关键结论 1（两个数据面）：optionsConf.url 由蓝盾前台浏览器调用（前端面，受 CORS 约束；无平台权限时它没有消费方）；monitor_url 由插件进程调用（进程面，可本地闭环）
- 关键结论 2（SDK env 契约，python_atom_sdk 1.2.19 源码实证）：get_input() 读 $bk_data_dir/$bk_data_input；get_sensitive_conf(key) 取 input.json 里的 bkSensitiveConfInfo 字段（不是环境变量也不是接口）；BK_CI_START_USER_NAME 等内置变量同源；set_output() 写 $bk_data_dir/$bk_data_output；日志走 stdout 带 ##[level] 前缀；.sdk.json 仅 openapi（构件/通知）调用需要
- 关键结论 3（selector CORS 实测）：真实网关 OPTIONS 预检回 404 API not found、响应无 Access-Control-Allow-Origin、裸 GET 报 user authentication failed（要用户态身份）→ 蓝盾前台大概率拉不到选项；mock 必须正确应答预检并回 ACAO/ACAM/ACAH（含 x-devops-project-id）
- 关键结论 4（告警屏蔽接口契约）：apigw 对外 /app/shield/{add,disable,edit,detail,search}/ → 后端 /api/v4/shield/*（均 appVerifiedRequired=true）；compapi 形态 POST /api/c/compapi/v2/monitor_v3/add_shield/；dimension_conditions[].method 合法枚举 include/exclude/gt/gte/lt/lte/eq/neq/reg/nreg（无 contain/not_contain）；disable 的 id 可传标量（后端 to_internal_value 自动包 list）
- 踩坑：腾讯内网 pypi 源 mirrors.tencent.com/repository/pypi/tencent_pypi/simple/ 是私有窄源（simple 索引仅 python-atom-sdk/qfsclient），第三方包必须加 --index-url https://pypi.org/simple；python-atom-sdk 只有 sdist，构建前需先装 wheel（否则 invalid command bdist_wheel）
- 红线：mock 地址绝不进 task.json 发布物（会随插件市场上架）；input.json/.sdk.json 不提交（.sdk.json 真实环境含凭证）；mock 用 http+内网 IP 会被 https 页面按混合内容拦截，需用 localhost/127.0.0.1
- mock 设计原则：校验必须与真实后端同等宽松（如 bk_biz_id 收数字字符串、bool 收字符串/1、标量 id 自动包列表），否则制造假失败，比不校验更糟
- 被联调插件（bk-monitor-shield）已确认 2 个缺陷、按要求未修：4 处用户输入校验未传 error_code 全落 2199001 PLUGIN_ERROR（而 deal_error 反标 USER_CONFIG_ERROR）；duration 传空串导致 AttributeError 'NoneType' has no attribute 'strftime'