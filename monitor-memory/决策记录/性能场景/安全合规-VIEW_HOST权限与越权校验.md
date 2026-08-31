---
groupPath: 决策记录/性能场景
relation: 安全合规-VIEW_HOST权限与越权校验
exportedAt: "2026-08-31T02:24:08.830Z"
---
【决策记录｜性能场景 列表与查询入口统一 VIEW_HOST 权限，分享场景额外做 host_ids 越权校验（原资产记权限缺失已过期）】
- 分类：安全合规
- 动机：避坑（新版主机查询入口曾缺失主机查看权限校验，commit 24f090ed5e 修复）
- 决策：模块内 PermissionMixin 统一声明读写动作均为 ActionEnum.VIEW_HOST，当前 6 个 ViewSet 全部继承（含 SearchHostInfoViewSet）；分享场景下 validate_scope_host_ids 校验请求的 bk_host_ids 必须是单主机分享 ID 或拓扑分享解析出的主机集合的子集，越权直接抛 ParamsPermissionDeniedError 并回传正确参数
- 背景约束：分享令牌是只读凭证，且只能访问被授权的主机子集；仅靠视图层权限不足以约束具体 host 范围
- 被否决方案：无（未找到相关记录）
- 已知代价：专家资产的 C0 与实现层 02-实现.md 仍记「SearchHostInfoViewSet 未继承 PermissionMixin，无 VIEW_HOST 权限约束」，该条目已过期——2026-08-12 的 commit 24f090ed5e 已补齐，现状 6 个 ViewSet 全部继承
- 重新评估触发条件：新增 ViewSet 时必须继承 PermissionMixin；新增分享形态时必须同步扩展越权校验
- 关联代码：PermissionMixin 与各 ViewSet @ monitor_web/performance/views.py；SearchHostMetricResource.validate_scope_host_ids @ monitor_web/performance/resources.py
- 证据来源：commit 24f090ed5e（修复新版主机查询入口缺失主机查看权限校验）、61b8c009b0（修复主机分享令牌写操作权限与只读态）；代码实现（6 个 ViewSet 均继承 PermissionMixin；validate_scope_host_ids 抛 ParamsPermissionDeniedError）
- 完整上下文：.module-experts/性能场景专家/C5-关键决策.md 决策 10