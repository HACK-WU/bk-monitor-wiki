---
groupPath: 专题记忆/前端专题
relation: TAPD交付流程
exportedAt: "2026-10-19T08:03:15.096Z"
---
【专题记忆｜TAPD + Git/PR 交付流程】
- 职责边界：只做 TAPD + Git/PR 流程编排（识别入口、保护工作区、组织确认、验证交付证据、记录恢复点），不提供编码规范、不承担编码；缺实现方时停在交接门，不自行降级为通用编码
- 四类状态贯穿全程：计划执行 / 等待确认 / 已请求但结果未知 / 已验证成功；发出请求不等于成功，每次外部写入后必须用返回值或重新查询验证；最终摘要逐项复述真实状态，不得把前三类压缩成「已完成」
- 配置驱动：稳定仓库信息存 references/tapd-dev.local.json（gitignored，逐机维护）；加载配置 → 按归一化 remote URL 定位仓库条目；实时事实（remote / host / base / tapd_workspace）每次轻量复核，不一致才提问；纯偏好（branch_convention / commit_convention / tapd_link_format / dev_skill / delivery_mode / head_remote / pr_target_remote）直接信任；写入默认值（default_owner / default_iteration）预填但写前必展示核对；auto_maintain: true 时把新确认值写回并更新 last_verified
- 三类入口：只读分析（只读 TAPD，输出需求摘要 / 验收标准 / 影响面 / 风险 / 待确认项，不写入）；反向建单（无单据，读 git status 与 staged/unstaged diff，展示草稿并确认后才创建）；交付（含续跑与补救，先算 resume_from 首个未完成步骤，从那里开始，已有等价产物复用不重做）
- 主流程：加载配置 → 只读侦察 + 轻量复核（git root/branch/status/remote，验证 base 引用存在）→ 场景路由 → 最小提问（只问配置缺失 / 冲突项与本次任务项）→ 交接开发（dev_skill 从配置取）→ 实现结果只读核对（diff / 范围 / 验收 / 测试证据）→ 交付预览 → 按序执行并逐步验证 → 记录产物与恢复点
- 确认门：优先 AskQuestion（每题至少 2 个选项，自由文本给 2 个兜底 + Other）；不可用时用编号选项文本门，未收到明确确认前状态保持等待确认，禁止建单 / commit / push / 建 PR / 回写；串联指令不得跳门（建单 + 开分支 + commit + PR + 回写仍逐门授权）
- 多 Remote / Fork：origin 是个人 fork（push head），upstream 是上游（PR base）；「创建 PR 到 upstream feat/X」不得解读为 base=develop；必须确认 PR base 分支名 / base 所在 remote / base 是否已存在（git fetch 后验证），不存在时停问「从哪条分支创建」或「改用已有 base」，禁止静默改用 develop
- 交付预览：分支（基于哪个 remote/base，已验证存在或待创建）/ staged 文件清单 / 完整 commit message / push 目标 / PR 行 head_remote:head → pr_target_remote:base / 标题 / 正文 / 回写内容；执行顺序（可选创建 base）→ stage+commit → push → PR/MR → 回写，每步验证；push 前重新验证本地源分支与待推 SHA 未漂移；创建 PR 前再次确认 base 引用仍存在
- PR 正文模板（强制，章节标题与顺序固定）：背景（TAPD 标题 + ID）/ 改动（按模块或路径归纳，来自真实 diff）/ 影响面（对谁有影响，无逻辑变更如实写）/ 测试（- [ ] 清单，未跑项仍列出，不写已通过除非有证据）
- 安全红线：不用 --no-verify；不 force push、不删分支、不改写已发布历史；不静默 stash / reset / checkout；没有工具返回或重新查询到的 PR/MR URL 时不得声称已创建，也不回写虚假链接；GPG/SSH 签名与交互认证交用户；未知托管平台时 push 获批后只做标准 push 并输出手工 PR 材料
- 文档源：blueking-tapd-dev/SKILL.md sha256:f728e71c；references/{config-schema,tapd-mcp,git-delivery,recovery}.md（同步 2026-10-19）
- 检索触发词：TAPD, 反向建单, 分支, commit, push, PR, 回写, 交付预览, resume_from, fork, upstream