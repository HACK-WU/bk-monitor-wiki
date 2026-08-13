---
groupPath: 专题记忆/场景视图
relation: PageListResource表格框架与TableFormat
exportedAt: "2026-08-13T11:53:38.885Z"
---
PageListResource 是场景视图模块的列表类接口抽象基类，提供分页/排序/筛选/格式化通用流水线。TableFormat 是单列格式化框架，含 15+ 子类定义各自的 format/get_sort_key/get_filter_key。

- 符号: `PageListResource`、`TableFormat`、`DefaultTableFormat`、`get_pagination_data`、`handle_filter`、`handle_sort`、`handle_pagination`、`handle_format`
- 位置: `bkmonitor/packages/monitor_web/scene_view/resources/base.py`、`bkmonitor/packages/monitor_web/scene_view/table_format.py`

流水线编排 get_pagination_data(data, params, column_type, skip_sorted):
1. handle_filter: 筛选——关键字模糊匹配 + filter_dict 精确匹配
2. handle_sort: 排序——cmp_to_key 支持多字段/反向/None 兜底
3. handle_pagination: 分页——page/page_size 切片
4. handle_format: 格式化——deepcopy 每行 + column.format(row)
5. 返回: {columns: list, total: int, data: list}

子类契约:
- 必须实现 get_columns(column_type): 返回 TableFormat 子类列表
- 可选实现 get_sort_fields()/get_filter_fields(): 声明可排序/可筛选字段

TableFormat 基类:
- column(): 输出列元信息字典 {id, name, sortable, disabled, checked, type, width, min_width, filterable, filter_list, actionId, asyncable, props}
- format(row): 格式化单行该列值（基类返回 None，子类必须覆盖）
- get_sort_key(row, reverse): 返回 (sort_value, reverse)
- get_filter_key(row): 返回 {text, value}

TableFormat 子类清单（15+）:
StringTableFormat、StringLabelTableFormat、TimestampTableFormat、TimeTableFormat、LinkTableFormat、SyncTimeLinkTableFormat、ScopedSlotsFormat、AliasMappingTableFormat、LinkListTableFormat、ProgressTableFormat、CustomProgressTableFormat、CustomStringTableFormat、NumberTableFormat、ColorNumberTableFormat、StatusTableFormat、DataStatusTableFormat、DataPointsTableFormat、CollectTableFormat、DictSearchColumnTableFormat、OverviewDataTableFormat、StackLinkTableFormat、StackLinkOverviewDataTableFormat、EndpointListTableFormat、ServiceComponentAdaptLinkFormat

热点路径:
- get_response_columns 遍历全量数据构造筛选项（filterable 列），数据量大时 O(N×列数) 性能下降