CMDB Process 类构造时丢弃原始字段的问题分析与解决方向。
- 问题: `api.cmdb.get_process` 返回的原始 JSON 包含 `start_cmd`、`bk_start_param_regex`、`create_time`、`last_time` 等字段，但 `Process.__init__` 仅显式接收固定参数，无 `_extra_attr` 兜底存储。
- 符号: `Process.__init__`
- 位置: `bkmonitor/api/cmdb/define.py`
- 后果: 原始 CMDB 字段在构造 `Process` 对象后被直接丢弃，`get_process_info` 无法访问这些字段。
- 涉及字段: `start_cmd`, `bk_start_param_regex`, `create_time`, `last_time`
- 解决方向: 改 `Process.__init__` 增加 `**kwargs` 或 `_extra_attr`，或在 `get_process_info` 中绕过 `Process` 封装直接取原始 JSON。
