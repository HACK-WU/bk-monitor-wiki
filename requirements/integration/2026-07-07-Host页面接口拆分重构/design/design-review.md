---
id: REQ-20260707-001
feature: Host页面接口拆分重构
status: 设计中
updated: 2026-07-09
version: 2
tags: [feat, integration]
document_type: review
---

# 🔍 设计文档评审报告

**需求**: REQ-20260707-001
**评审时间**: 2026-07-09
**评审对象**: `host_view_split_DESIGN.md` + `host_view_split_S01_panels_order_DESIGN.md` + `host_view_split_S02_process_fields_DESIGN.md`
**评审模式**: 增量再审（基于首次评审修复后）

---

## 评审结论

⭕ **有条件通过** — 首次评审发现的 🔴 阻断项已全部修复，当前无阻断问题。

---

## 首次评审问题修复验证

| # | 前次问题 | 严重度 | 状态 | 验证说明 |
|---|---------|:------:|:----:|---------|
| 1 | S-02 §3.2 vs §3.3/§4.2：决策表说一期不改 `Process` 类，但目录结构和数据模型写成了修改 | 🔴 | ✅ 已修复 | §3.1 改为"二期待改造"；§3.3 `api/cmdb/define.py` 标注为"[二期待改]"；§4.2 数据模型改为"二期待办"并明确一期从原始 JSON 取字段 |
| 2 | S-01 §4.1：HTTP 方法未与前端确认 | 🟡 | ✅ 已修复 | §3.2 新增决策点"HTTP 方法 = POST"，说明理由（与前端 Wiki 对齐，body 传参） |
| 3 | S-02 §4.1：`portStatus` 与 `status` 语义区分未说明 | 🟡 | ✅ 已修复 | Response Demo 中增加注释 `// 0=Normal, 1=Abnormal；与 status(ON/OFF/UNKNOWN) 语义不同` |
| 4 | S-02 §6：`None` 值前端展示逻辑未说明 | 🟡 | ✅ 已修复 | 异常处理表格补充"前端展示为 `--` 或 `N/A`"说明 |
| 5 | S-02 §5：`system.proc_port` 查询可合并 | 🟢 | 🟡 维持建议 | 未修复（采纳为可选优化，不阻塞） |
| 6 | S-01 §3.1：计算冗余 | 🟢 | ✅ 已修复 | §3.1 新增性能备注，说明 `get_auto_view_panels` 为静态配置生成，开销极低 |

---

## 剩余建议项（不阻塞）

| # | 维度 | 位置 | 问题描述 | 建议 |
|---|------|------|---------|------|
| 5 | 正确性 | S-02 §5 | `system.proc_port` 的 `proc_exists`（现有 `status`）与 `port_health`（新增 `portStatus`）可合并为单次查询 | 备注优化：portStatus 查询可与现有 get_process_status 合并为单次 system.proc_port 批量查询（Phase 2 可选） |

---

## 评审统计

| 维度 | 🔴 | 🟡 | 🟢 | 合计 |
|------|:--:|:--:|:--:|------|
| 完整性 | 0 | 0 | 0 | 0 |
| 质量 | 0 | 0 | 0 | 0 |
| 正确性 | 0 | 0 | 1 | 1 |
| 一致性 | 0 | 0 | 0 | 0 |
| 体验 | 0 | 0 | 0 | 0 |
| **合计** | **0** | **0** | **1** | **1** |

---

## 下一步

1. 确认设计评审通过 → 推进至 **design-to-code**（生成代码骨架）
2. 编码顺序建议：先 S-01（低风险接口拆分），后 S-02（涉及时序查询）
3. S-02 Phase 1 实施要点：从 `get_process_info` 返回的原始 JSON 直接提取 `start_cmd` 等字段，不等待 `Process` 类改造
