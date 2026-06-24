---
groupPath: 最近需求
relation: "[2026-06-24] 补全 monitor-memory 和 user-profile 缺失的 Group 索引"
keywords: [monitor-memory, user-profile, 模板]
exportedAt: "2026-06-24T10:15:09.545Z"
---
用户要求根据模板补全 monitor-memory 和 user-profile 两个 scope 中缺失的 Group。模板定义了 monitor-memory 需要 14 个 Group，user-profile 需要 6 个 Group。通过 ki_manage_index_create 工具创建了 monitor-memory 的 11 个缺失 Group 和 user-profile 的 2 个缺失 Group，并更新了 AGENTS.md 索引缓存。