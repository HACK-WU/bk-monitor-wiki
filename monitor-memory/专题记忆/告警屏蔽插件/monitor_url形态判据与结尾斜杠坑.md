---
groupPath: 专题记忆/告警屏蔽插件
relation: monitor_url形态判据与结尾斜杠坑
exportedAt: "2026-09-21T08:34:05.174Z"
---
- monitor_url 的取值不在代码里（取值机制见 专题记忆/蓝盾插件离线联调），所以跨仓库同步不会携带任何环境信息，同一份代码可配到任意环境
- 仓库内唯一硬编码的域名是 task.json 里 strategy_list 的 optionsConf.url（前端 selector 选项接口，不是 monitor_url）：主仓库 task.json 第 40 行为 https://bk-monitor.apigw.o.woa.com/prod/user/strategy/get_devops_strategy_list/；bkop task.json 第 40 行为 https://bkapi.bkop.woa.com/api/bk-monitor/prod/user/strategy/get_devops_strategy_list/；bksg 因改用 vuex-input 没有该字段，因此无任何域名线索
- 由 selector 地址可反推 monitor_url 形态：网关域名加网关名加 stage 加结尾斜杠，bkop 应为 https://bkapi.bkop.woa.com/api/bk-monitor/prod/
- 结尾斜杠是硬要求：urljoin(monitor_url, "app/shield/add/") 在 monitor_url 不以斜杠结尾时会吞掉 stage 段，表现为打到网关根路径并返回 404
- 现网 monitor_url 实际取值尚未确认：主仓库面向的网关实测 /prod/add_shield/ 返回 404（错误码 1640401 API not found）、/prod/app/shield/add/ 返回 400（1640001 app code cannot be empty，说明资源存在）
- 待确认项：各环境监控是否已支持 end_policy（不支持时 DRF 会静默忽略该字段，插件选项成空壳，用户选了不再通知仍会收到通知）