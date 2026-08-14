---
groupPath: 关联关系/外部API集成专题
relation: grafana-GrafanaApiResource-直连非APIResource
exportedAt: "2026-08-14T07:52:30.763Z"
---
[强关联] grafana GrafanaApiResource 直连模式 与 X-WEBAUTH-USER/X-Grafana-Org-Id 认证头
强度：必改——改 GrafanaApiResource 的 perform_request 或请求头注入时，所有 grafana 接口的认证全变
原因：grafana 直连 settings.GRAFANA_URL（非 APIResource），注入 X-WEBAUTH-USER/X-Grafana-Org-Id 认证头

源端（直连基类）:
- `GrafanaApiResource(Resource)` @ `bkmonitor/api/grafana/default.py`
- 非 `APIResource`——`perform_request` 直连 `settings.GRAFANA_URL`
- 请求头注入: `X-WEBAUTH-USER`（从请求用户取）、`X-Grafana-Org-Id`（需 `with_org_id=True` 的接口带 `org_id` 参数）
- 返回统一信封 `{result, code, message, data}`
- 全量 22 类（组织/仪表盘CRUD/数据源/文件夹/搜索/收藏/组织偏好/用户）

目标端（导出工具与消费）:
- `DashboardExporter` @ `bkmonitor/api/grafana/exporter.py` — 仪表盘模板化导出（$DS_xxx占位符 + __inputs/__requires/datasource_mapping）
- 消费方: `monitor_web/grafana/resources/manage.py`、`monitor_web/as_code/resources.py`、`monitor_web/export_import/import_config.py`