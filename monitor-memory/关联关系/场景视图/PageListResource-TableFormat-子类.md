---
groupPath: 关联关系/场景视图
relation: PageListResource-TableFormat-子类
exportedAt: "2026-08-13T11:54:56.254Z"
---
[强关联] PageListResource 表格框架 与 TableFormat 子类列表
强度：必改——改 TableFormat 基类的 column/format/get_sort_key/get_filter_key 接口时，所有 15+ 子类必须跟着改；改 PageListResource.get_pagination_data 的流水线步骤时，所有列表子类受影响
原因：PageListResource 依赖子类提供的 get_columns() 返回 TableFormat 子类列表编排流水线（筛选→排序→分页→格式化），TableFormat 接口变更级联影响所有列格式化子类

源端（表格框架）:
- `PageListResource.get_pagination_data(data, params, column_type, skip_sorted)` @ `bkmonitor/packages/monitor_web/scene_view/resources/base.py`
- 流水线: handle_filter → handle_sort → handle_pagination → handle_format
- 子类契约: get_columns(column_type) 返回 TableFormat 子类列表；可选 get_sort_fields/get_filter_fields

目标端（列格式化子类）:
- `TableFormat` / `DefaultTableFormat` @ `bkmonitor/packages/monitor_web/scene_view/table_format.py`
- 15+ 子类: StringTableFormat、LinkTableFormat、TimestampTableFormat、NumberTableFormat、ProgressTableFormat、StatusTableFormat、ScopedSlotsFormat、AliasMappingTableFormat 等
- 每个子类定义自己的 format(row) / get_sort_key(row, reverse) / get_filter_key(row)
- 热点: get_response_columns 遍历全量数据构造筛选项，数据量大时 O(N×列数)