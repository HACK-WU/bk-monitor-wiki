进行中：B-01 POST 改造与 signed_state 自包含机制编码已完成，待修复 Review 问题。
- ListUserTapdWorkspaceResource 改为 POST + 新增 redirect_uri_real/verify 参数
- generate_auth_url 改为自包含 signed_state，TAPDAuthPermission 从 POST body 透传参数
- B-05 callback 移除 Session 依赖，改用 verify_signed_state 解析
- 租户/用户名硬编码统一修复
- 待修复: utils/tapd.py 缺失 `import time`（P0），resources.py payload 中 `initiator` 建议统一为 `username`（P1）
