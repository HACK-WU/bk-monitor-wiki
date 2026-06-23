---
groupPath: 通用记忆片段
relation: 空间租户业务ID转换
keywords: [space_uid, bk_biz_id, bk_tenant_id, SpaceApi, 转换]
exportedAt: "2026-06-23T09:17:27.665Z"
---
### space_uid ↔ bk_biz_id 转换
- **入口**: `bkm_space.utils`
- **路径**: `bkm_space/utils.py#L8-L57`
- **规则**:
  - `space_uid` 格式：`{space_type}__{space_id}`（如 `bkcc__2`）
  - BKCC 类型（`bk_biz_id >= 0`）：直接互转
  - 非 BKCC（蓝盾/SaaS）：`bk_biz_id = -space.id`（负数）
- **函数**:
  - `space_uid_to_bk_biz_id(space_uid, id=None) -> int` — 非 BKCC 可传自增 id 避免查 API
  - `bk_biz_id_to_space_uid(bk_biz_id) -> str` — 负数时查 API
  - `parse_space_uid(space_uid) -> (space_type, space_id)` — 解析 `bkcc__2`

### bk_biz_id ↔ bk_tenant_id 转换
- **入口**: `bkmonitor.utils.tenant`
- **路径**: `bkmonitor/utils/tenant.py#L27-L69`
- **函数**:
  - `bk_biz_id_to_bk_tenant_id(bk_biz_id: int) -> str` — `lru_cache(maxsize=10000)`
  - `space_uid_to_bk_tenant_id(space_uid: str) -> str` — `lru_cache(maxsize=10000)`
- **特性**: 多租户关闭时返回 `DEFAULT_TENANT_ID`

### SpaceApi 统一查询
- **路径**: `bkm_space/api.py`
- `SpaceApi` 是代理类，实际实现由 `settings.BKM_SPACE_API_CLASS` 配置
- `get_space_detail(space_uid="", bk_biz_id=0) -> Space | None`
- `gen_space_uid(space_type, space_id) -> str`