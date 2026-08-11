# CMDB 与容器资源专家

**一句话职责**：封装 BK-Monitor 对资源与容器监控数据源的调用——CMDB（主机/拓扑/进程）、Kubernetes（K8s 资源聚合）、BCS（容器集群系列：bcs/bcs_cluster_manager/bcs_project/bcs_storage）、节点管理（node_man）。

**负责的模块**：`bkmonitor/api/{cmdb,kubernetes,bcs,bcs_cluster_manager,bcs_project,bcs_storage,node_man}/`。

**何时找这个专家**：
- 查询主机/业务拓扑/进程（`api.cmdb.*`、`resource.cmdb.*`）
- 查询 K8s 集群/节点/Pod/工作负载/监控端点（`api.kubernetes.*`）
- 容器集群管理（bcs_cluster_manager 集群列表、bcs_storage 数据拉取）
- 节点管理/插件订阅/安装（node_man 36 个接口）
- 理解 `batch_request` 分页批量拉取与 `CacheResource` 缓存模式

**契约层就绪**：`C0 + C1` 就绪
**包含的资产**：C0-使用总览 / C1-能力契约；implementation/01-架构 / 02-实现 / 06-测试

**测试状态**：`api/` 目录无测试 → 06-测试 标注「该模块无测试」。

**所属专题**：[外部 API 集成专题](../topic.md)（T0 总览见 [T0-专题总览](../T0-专题总览.md)）
**出处行**：生成日期 2026-08-07，git commit：未提交（工作区）
