---
groupPath: 数据流/告警分派
relation: CSV规则文件
exportedAt: "2026-10-14T03:12:07.452Z"
---
【数据流｜CSV规则文件】
- 实体类型：文件（用户本地；前端导出/导入，不落库）
- 结构：固定 7 列表头（告警组 / 匹配规则 / 通知升级 / 流程 / 等级调整 / 追加标签 / 状态）；条件与通知配置为 JSON 字符串（半角逗号转全角防列错位）；文件名 {组名}-{时间戳}.csv；带 BOM
- 生产方：handleExportChange @ bkmonitor/webpack/src/monitor-pc/pages/alarm-dispatch/alarm-dispatch-config.tsx（downCsvFile 下载）
- 主要消费方：用户（留档/跨组跨环境搬运）；回流 handleImportChange（MonitorImport 读文本到 csvToArr 解析，表头必须逐字一致，逐行还原为 RuleData 追加到表格）
- 业务用途：规则的批量搬运与留档；导入本身不落库，导入行仍需走「调试并生效」整组提交；行级解析错误静默（仅 console.log，源码 // to do 校验）
- 详细流向：见 .module-experts/前端专题/告警分派专家/C4-数据流向与消费.md