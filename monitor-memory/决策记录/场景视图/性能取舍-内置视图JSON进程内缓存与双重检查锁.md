---
groupPath: 决策记录/场景视图
relation: 性能取舍-内置视图JSON进程内缓存与双重检查锁
exportedAt: "2026-08-31T01:51:34.946Z"
---
【决策记录｜场景视图内置视图 JSON 采用进程内缓存 + 双重检查锁加载】
- 分类：性能取舍
- 动机：优化（APM 场景 34 个 JSON 骨架文件，每次请求读盘加递归国际化翻译成本高）
- 决策：ApmBuiltinProcessor / HostBuiltinProcessor 在类属性 builtin_views 为空时加载一次并缓存；APM 用 threading.Lock 加双重检查，一次性赋值保证原子性；NormalProcessorMixin.load_builtin_views 仍每次重新加载未纳入缓存
- 背景约束：Web 进程多线程并发，首次加载需避免重复读盘；国际化需按请求语言在运行期执行，缓存的是未翻译骨架
- 被否决方案：每次请求重新读盘（NormalProcessorMixin 现状）否决理由为文件多的场景重复 IO 与递归翻译开销大；模块级 _BUILTIN_VIEWS 全局缓存否决理由为变量已声明但从未启用、缓存粒度与失效时机未定
- 已知代价：缓存无失效机制，改 JSON 骨架需重启进程才生效
- 重新评估触发条件：内置视图 JSON 需要不停机热更新；或改了 JSON 不生效的反馈累计 ≥ 2 次
- 关联代码：ApmBuiltinProcessor.load_builtin_views @ scene_view/builtin/apm.py；HostBuiltinProcessor.load_builtin_views @ scene_view/builtin/host.py
- 证据来源：代码注释（apm.py load_builtin_views：双重检查等待锁期间可能已有其他线程完成初始化以减少重复读盘、一次性赋值以确保原子性）；_BUILTIN_VIEWS 声明未使用 @ scene_view/builtin/__init__.py
- 完整上下文：.module-experts/场景视图专家/C5-关键决策.md 决策 3