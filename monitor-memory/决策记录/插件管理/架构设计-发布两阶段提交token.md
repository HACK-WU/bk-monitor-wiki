---
groupPath: 决策记录/插件管理
relation: 架构设计-发布两阶段提交token
exportedAt: "2026-10-13T12:07:37.824Z"
---
【决策记录｜[推测] 发布两阶段提交 token】
- 分类：架构设计
- 动机：避坑：保存即发布会让未调试/未确认的中间版本直接对外可见
- 决策：[推测] 保存阶段（saveMetric/pluginRegister）只生成新版本并返回 token；发布阶段（releaseCollectorPlugin 携带 token+config_version+info_version）显式执行——只有 release 成功变更才生效；向导步骤2 保存刻意只前进不发布，发布收敛到步骤3
- 背景约束：插件/指标的生成（打包、校验）与发布在后端是两个阶段；前端需要先调试确认后发布的时序
- 被否决方案：无（未找到记录）
- 重新评估触发条件：后端提供原子化保存即发布接口，或现有两阶段语义变更
- 关联代码：saveMetric @ bkmonitor/webpack/src/monitor-api/modules/plugin.js；releaseCollectorPlugin @ modules/model.js；三处同构：step-set-done.vue / metric-dimension-dialog.tsx / indicator-dimension/utils.ts
- 证据来源：无直接证据，基于 saveMetric 返回 {token?, config_version, info_version}、release 消费 token、三处实现同构与 need_upgrade 语义推断