---
groupPath: 关联关系/外部API集成专题
relation: monitor-module_name-mointor_v3拼写
exportedAt: "2026-08-14T07:53:01.837Z"
---
[强关联] monitor module_name=mointor_v3 拼写陷阱 与调用方入口
强度：必改——改 module_name 拼写时所有调用方入口全变（但这是历史拼写错误，不建议改）
原因：monitor 网关的 module_name 为 mointor_v3（注意拼写 mointor，非 monitor），调用方需用 api.mointor_v3.xxx 而非 api.monitor_v3.xxx

源端（拼写异常）:
- `MonitorAPIGWResource(KernelAPIResource)` @ `bkmonitor/api/monitor/default.py`
- `module_name = mointor_v3` — 历史拼写错误，未修正以保持兼容
- `base_url` 为 bk-monitor 自身网关
- `TIMEOUT = 300`
- 全量 13 类（采集配置/拨测/报表/自定义指标/处理任务/告警经验，均走 `/app/...` apigw 路径）

目标端（调用方）:
- 调用方需用 `api.mointor_v3.xxx` 或走 `resource.monitor`
- 消费方: `alarm_backends/core/cache/models/uptimecheck.py` 等
- 与 metadata（module_name=metadata_v3）同走 KernelAPIResource 自身网关模式