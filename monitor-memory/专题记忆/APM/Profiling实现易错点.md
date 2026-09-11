---
groupPath: 专题记忆/APM
relation: Profiling实现易错点
exportedAt: "2026-09-07T04:31:42.196Z"
---
APM Profiling 模块（apm_web/profile）四个高代价易错点，改动前务必核对。
- 1. 两条并行管线：页面查询固定 ConverterType.Tree（TreeConverter 直接把 Doris 行建 FunctionTree，绕开 pprof），只有上传解析与导出走 Profile（views.py converter_query 用 Tree；export 用 ConverterType.Profile）。误把 Profile 当页面主链路中间格式会找错调用链。
- 2. 聚合方法是「查表 + 静默回退 SUM」而非语义二分：支持 SUM/AVG/LAST 三值；查表键为 APM_PROFILING_AGG_METHOD_MAPPING（config/default.py），键是 HEAP-SPACE / WALL-TIME / CPU-TIME 这类复合串，未命中静默回退 SUM 不报错；agg_method 入参是自由字符串无 choices 校验（serializers.py），传 typo 也走兜底。新增采样类型忘记加映射会把瞬时量（堆内存）按 SUM 算导致数值虚高。
- 3. 时间单位四套：start/end 微秒；查 Doris 与 dtEventTimeStamp 毫秒；agg_interval 秒（用时 ×1000）；pprof time_nanos 纳秒（毫秒 ×10⁶）。且 serializers.py 的注释（说前端传毫秒需转成秒级）与实现 ×1000×1000、help_text 标注 Second 三者口径不一致。
- 4. 已知不一致与坑：JFR 在 file_type choices 与 InputType 枚举里都有，但 apps.ready() 只注册 DORIS/PERF_SCRIPT/PPROF 三个解析器 → 上传 JFR 必然 PARSING_FAILED；perf/converter.py 残留调试 print；QueryProfileBarGraphResource 对每个时间点发起一次 label 查询（无点数量/并发上限），长周期会打满下游。
- 位置: `bkmonitor/packages/apm_web/profile/`