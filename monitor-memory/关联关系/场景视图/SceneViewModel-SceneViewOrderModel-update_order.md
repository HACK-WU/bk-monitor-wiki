---
groupPath: 关联关系/场景视图
relation: SceneViewModel-SceneViewOrderModel-update_order
exportedAt: "2026-08-13T11:54:56.254Z"
---
[强关联] SceneViewModel 视图模型 与 SceneViewOrderModel 排序模型/update_order 并发锁
强度：必改——改 SceneViewOrderModel 唯一键或 config JSON 结构时，SceneViewModel.update_order 必须跟着改；改 update_order 的锁粒度/事务边界，排序逻辑受影响
原因：SceneViewModel.update_order 用 @atomic + select_for_update 锁 SceneViewOrderModel 行，对 config 列表做移除/插入保证并发下顺序一致，排序模型结构变更级联影响所有排序更新操作

源端（视图模型+排序更新）:
- `SceneViewModel` @ `bkmonitor/packages/monitor_web/models/scene_view.py`（唯一键 bk_biz_id+scene_id+type+id，含 mode/variables/panels/order/options JSON 字段）
- `SceneViewModel.update_order` @ `bkmonitor/packages/monitor_web/models/scene_view.py`（@atomic + select_for_update 锁行，移除/插入 config）
- `BulkUpdateSceneViewOrderAndNameResource.perform_request` @ `bkmonitor/packages/monitor_web/scene_view/resources/view.py`（批量更新排序+名称，不在配置中的 ID 追加末尾）

目标端（排序模型）:
- `SceneViewOrderModel` @ `bkmonitor/packages/monitor_web/models/scene_view.py`（唯一键 bk_biz_id+scene_id+type，config JSON 存视图ID有序列表）
- DeleteSceneViewResource 删除视图后同步清理 SceneModel.view_order 中的对应ID
- SceneViewModel.mode 枚举值 auto 与 SceneViewSerializer.mode 值 tile 不一致（跨层高频坑）