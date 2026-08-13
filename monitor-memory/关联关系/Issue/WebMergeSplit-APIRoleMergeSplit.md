---
groupPath: 关联关系/Issue
relation: WebMergeSplit-APIRoleMergeSplit
exportedAt: "2026-08-13T08:56:07.009Z"
---
[强关联] Web 层 MergeIssueResource/SplitIssueResource 与 api role MergeResource/SplitResource
强度：必改——改 api role 的 MergeResource/SplitResource 签名/行为时，Web 层 MergeIssueResource/SplitIssueResource 必须跟着改；反之亦然（双向契约）
原因：Web 层合并/拆分写操作转发到 api role 执行，两层的参数/返回结构/异常处理形成跨角色契约

源端（Web 层）：
- `MergeIssueResource` / `SplitIssueResource` @ `bkmonitor/packages/fta_web/issue/resources.py`
- 接收前端请求，转发到 api role

目标端（api role）：
- `MergeResource` / `SplitResource` @ `kernel_api/views/v4/issue.py`
- 实际执行合并/拆分逻辑，调用 IssueMergeResolver

测试约束:
- 合并/拆分测试需 api 角色（conf.api.development.community），worker/web 角色下会假失败
- 用例同时 import kernel_api.views.v4.issue 与 fta_web.issue.resources