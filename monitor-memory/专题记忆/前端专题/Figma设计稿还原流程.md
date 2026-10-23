---
groupPath: 专题记忆/前端专题
relation: Figma设计稿还原流程
exportedAt: "2026-10-19T08:03:15.096Z"
---
【专题记忆｜Figma 设计稿还原流程】
- 边界：仅处理 Vue2/Vue3 + BlueKing 组件生态项目；Figma 生成代码只作结构和视觉参考，组件映射只产生候选，组件 API 必须以与目标项目版本严格匹配的组件 skill reference 为最终依据
- 步骤 0 仓库门禁：进入 Figma 取数或业务代码侦察前，先检查目标仓库 / AGENTS.md / 用户规则是否要求确认分支策略、方案确认、脚本 / dev server / 浏览器自动化授权；未完成门禁先问
- 步骤 1 识别项目与版本：根据 package、锁文件、实际 imports、相邻组件、运行入口确认 Vue2/Vue3、bk-magic-vue / bkui-vue 版本与用法、tdesign-ui / search-select-v3 / date-picker 安装情况、业务封装 / Icon / Theme / i18n / 数据与验证约定；目标目录与 1-2 个同类相邻实现应与 Figma 取数并行；无法确认 Vue 或组件库版本时停止并询问，不按仓库名猜测
- 步骤 2 获取 Figma 数据：从 URL 解析 fileKey 与 nodeId（node-id=1-2 转 1:2）；get_design_context 是结构与设计意图主入口，get_screenshot 做视觉基准，get_metadata 先看大节点层级再下钻，get_variable_defs 读设计变量语义，资源工具拿真实图片或 SVG；大画板先 metadata + 截图读旁注与多态；Code Connect 询问严格按 MCP 原文问用户，同意则走 get_code_connect_suggestions，拒绝则 disableCodeConnect: true 重取，仍失败进入降级
- 上下文降级三级：完整（design_context + screenshot）正常实现；可用（screenshot + metadata 含旁注 / 多态 / Notes）可出方案，缺关键细节再问；不足（仅空节点、无截图、无结构）停止并说明阻塞；认证失败、无权限或降级后仍不足时停止猜测
- 步骤 3 annotations 与状态：除目标节点外检查父级 frame/section、兄弟 variants、annotations、画布说明、红线、示例数据、图层命名；补齐 loading / empty / error / disabled / hover / selected / overflow 等已定义状态；信息缺失或冲突时暂停相关决策并询问
- 步骤 4 组件映射：先读 components.md，再按版本读 component-map-vue2 / vue3、icons.md、theme.md；扩展组件只在目标项目已安装且相邻业务正在使用时成为候选；样式优先对齐同模块稳定实现，不因仓库笼统 Token 规则强行改用 var(--xxx)
- 步骤 5 组件 skill 确认门（固定五路由）：bk-magic-vue / Vue2 → bk-magicbox-vue-components；bkui-vue / Vue3 → bkui-vue-components；@blueking/tdesign-ui → blueking-tdesign-ui；@blueking/search-select-v3 → blueking-search-select-v3；@blueking/date-picker → blueking-date-picker；必须确认 props / events / slots / methods / 类型 / 默认值 / 限制 / 示例后才允许输出组件代码；静态 map 与完整索引都未命中时列出缺口并询问是否允许最小手写，不得凭记忆或安装源码补全 API
- 步骤 5.5 方案确认：非琐碎改动（新页面 / 新侧栏、多步骤流、多状态交互、目录重构）写码前给简短方案并确认，至少含目标目录与文件结构、组件候选映射、交互与状态范围（含明确不做）、数据来源（真实接口 / mock）与是否接入现有页面
- 步骤 6 实现顺序：项目已有业务封装 → 组件 skill 确认的 BlueKing 组件 → 语义 HTML/CSS 布局与业务组合 → 用户明确批准的最小手写组件；不引入设计和项目未要求的依赖 / 抽象 / 状态 / 交互 / 响应式规则
- 步骤 7 验证：逐区域对照截图，按 annotations 与 variants 核对状态与交互；有运行环境且已授权则真实应用验证关键路径；无运行环境则静态自检并列出未验证项，不假装跑通
- 必须停下询问：仓库门禁未完成；Figma 认证失败 / 无权限 / 上下文不足；annotation 与截图或图层冲突；必需状态 / 交互 / 资源 / 响应式断点未定义；无法确认 Vue 或组件库版本；静态 map 与索引均未命中需手写；组件 API / Icon export / Token 无法从可靠来源确认；非琐碎改动未过方案确认门
- 文档源：blueking-figma-dev/SKILL.md sha256:487be99a（同步 2026-10-19）
- 检索触发词：Figma, 设计稿还原, get_design_context, Code Connect, annotations, 组件映射, 视觉验收