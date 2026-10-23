# IpChooserConfig（`bkm-ipchooser`）

> **职责**：IP 选择器 SDK：主机/动态分组/IP(v6) 选择统一 API

> **职责**：IP 选择器 SDK：主机/动态分组/IP(v6) 选择统一 API

- **位置**：`bkm_ipchooser/` · 归属文件 **34** 个 · 约 **3539** 行
- **定义**：`bkm_ipchooser/models.py:1`（django）
- **挂载前缀**：- · 视图/接口入口 **7** 个
- **置信度**：🟢（模块边界来自 apps.py/models.py 声明）

## 依赖关系

- **依赖**（改它要连带看）：`bkm_space`、`bkmonitor`
- **被依赖**（动它会影响）：`monitor_web`

## 数据表（1）

| 表 | 实体 | 引用次数 | 来源 | 证据 |
|----|------|----------|------|------|
| `bkm_ipchooser_ipchooserconfig` ⚠︎默认命名 | IPChooserConfig | 1 | models.Model（定义） | `bkm_ipchooser/models.py:6` |

## 非 HTTP 入口

- **定时任务**：1 处

## 归属文件（34）

- `bkm_ipchooser/models.py`
- `bkm_ipchooser/authentication.py`
- `bkm_ipchooser/types.py`
- `bkm_ipchooser/views.py`
- `bkm_ipchooser/mock_data.py`
- `bkm_ipchooser/exceptions.py`
- `bkm_ipchooser/__init__.py`
- `bkm_ipchooser/urls.py`
- `bkm_ipchooser/constants.py`
- `bkm_ipchooser/apps.py`
- `bkm_ipchooser/config.py`
- `bkm_ipchooser/api.py`
- `bkm_ipchooser/handlers/template_handler.py`
- `bkm_ipchooser/handlers/topo_handler.py`
- `bkm_ipchooser/handlers/__init__.py`
- `bkm_ipchooser/handlers/config_handler.py`
- `bkm_ipchooser/handlers/host_handler.py`
- `bkm_ipchooser/handlers/dynamic_group_handler.py`
- `bkm_ipchooser/handlers/base.py`
- `bkm_ipchooser/query/__init__.py`
- `bkm_ipchooser/query/resource.py`
- `bkm_ipchooser/serializers/template_sers.py`
- `bkm_ipchooser/serializers/__init__.py`
- `bkm_ipchooser/serializers/config_sers.py`
- `bkm_ipchooser/serializers/topo_sers.py`
- `bkm_ipchooser/serializers/dynamic_group_sers.py`
- `bkm_ipchooser/serializers/host_sers.py`
- `bkm_ipchooser/serializers/base.py`
- `bkm_ipchooser/tools/host_tool.py`
- `bkm_ipchooser/tools/topo_tool.py`
- `bkm_ipchooser/tools/__init__.py`
- `bkm_ipchooser/tools/gse_tool.py`
- `bkm_ipchooser/tools/batch_request.py`
- `bkm_ipchooser/tools/translation.py`
