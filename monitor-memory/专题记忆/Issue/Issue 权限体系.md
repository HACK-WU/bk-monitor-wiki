---
groupPath: 专题记忆/Issue
relation: Issue 权限体系
exportedAt: "2026-08-13T08:54:33.117Z"
---
Issue 模块权限体系包含 IAM Action 分级、自定义权限校验器和 TAPD 用户态授权三层。只读接口需 VIEW_EVENT，写操作需 MANAGE_EVENT。IssueBusinessActionPermission 处理 bk_biz_id 的三种来源。TAPD 接口额外由 TAPDAuthPermission 校验用户态 token。

## IAM Action
| 接口类型 | IAM Action |
| 只读接口 | VIEW_EVENT |
| 写操作 | MANAGE_EVENT |

## 关键符号
- 符号: `IssueBusinessActionPermission`
- 位置: `bkmonitor/packages/fta_web/issue/views.py`（IssueViewSet 内嵌类）
- 用途: Issue 专用业务权限校验，处理 bk_biz_id 三种来源
  - 批量写操作: body.issues[*].bk_biz_id
  - 查询接口: body.bk_biz_ids 列表
  - 其他接口: request.biz_id（URL/GET/POST/JSON body）
- 对每个业务 ID 分别做 IAM 校验，全部通过才放行

## 无需 bk_biz_id 的接口
- NO_BIZ_REQUIRED_ENDPOINTS: issue/search、issue/top_n、issue/recent_assignees
- TAPD 工作区相关接口仍需 bk_biz_id 作为请求参数

## TAPD 用户态授权
- 符号: `TAPDAuthPermission`
- 位置: `bkmonitor/packages/fta_web/issue/views.py`（IssueViewSet 内嵌类）
- 仅对 TAPD_ENDPOINTS 中的接口生效
- TAPD_ENDPOINTS: tapd/workspace、tapd/user_workspace、tapd/unbind_workspace、tapd/rebind_workspace、issue/get_tapd_fields、issue/search_tapd_items、issue/create_tapd、issue/link_tapd
- tapd/revoke_auth 与 issue/tapd_relations 不在该列表中
- 从 Redis tapd_uat:{tenant}:{user} 读取 token

## 批量操作权限
- _run_batch 框架不额外做权限校验，权限在 Resource 入口校验
- IAM 无 MANAGE_EVENT 权限时整体请求被拦截

## API Gateway 接口
- 位置: `api/issue/default.py`
- 超时 300 秒

## bkm-cli RPC 接口
- 位置: `kernel_api/rpc/functions/bkm_cli/issue.py`
- 4 种只读 operation: detail / list_by_strategy / list_by_fingerprint / list_activities