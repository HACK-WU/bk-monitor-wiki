# 已知单元测试失败：采集专家

## 采集配置（列表跨业务守卫）

### bkmonitor/webpack/tests/collector-cross-business.test.cjs:（全部 11 个用例同因失败）

- **执行方式**：`cd bkmonitor/webpack && node --test tests/collector-cross-business.test.cjs`（前置：Node ≥ 20.17.0、`node_modules` 已安装；纯 Node 执行，无网络与浏览器需求）
- **失败时间**：2026-10-13
- **失败原因**：`TypeError: VueRouter is not a constructor`，发生于 `setup()` 的 `new VueRouter({...})`，全部用例未进入业务断言。根因判定为**环境依赖链接漂移**（非用例缺陷）：`webpack/node_modules/vue-router` 被 hoist 为 `vue-router@4.5.1`（Vue 3 版，由 `@blueking/ai-ui-sdk` 的 auto-install peer 引入），而测试面向 Vue 2 生态、期望 `vue-router@3.6.5`（`src/monitor-pc/package.json` 声明 `^3.6.5`；pnpm 存储中已有 3.6.5 安装，未链接到 webpack 根）
- **修复尝试**：将 `require('vue-router')` 临时强制解析到 pnpm 存储中的 `.pnpm/vue-router@3.6.5_vue@2.7.16/node_modules/vue-router` 后 **11/11 通过（907ms）**，证明用例逻辑正确。未落地修复方向（三选一，待决策）：重指向根链接 / 重跑 `pnpm install` 观察 hoisting / 为 `tests/` 补一层 node_modules 映射
- **影响**：修复前跨业务只读守卫（#12736）的回归基线无法在本环境本地执行；同目录另两个采集测试（`collector-detail-back` 5/5、`collector-detail-isolation` 12/12）不受影响，全绿
- **来源**：expert-team 创建期实测（见 `implementation/06-测试.md`「测试可执行性」）

## 已知无关背景（非本专家切面）

`node --test 'tests/**/*.test.cjs'` 全量另有 4 个失败属其它模块（`host-list-page-first-ui.test.cjs`×2、`profiling-explore.test.cjs`×1、`llm-json-display.test.cjs` 文件级×1），与本模块无关，不计入本条。
