---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Tree 树
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Tree 树】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Data/tree.md
- 导入：import { Tree } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：data: 渲染列表（默认 []）；label: 指定节点标签为节点对象的某个属性值（默认 label）；node-key: 每个树节点用来作为唯一标识的属性，此标识应该是唯一的;如果设置系统会默认自动生成唯一id；children: 子节点 Key, 用于读取子节点（默认 children）；indent: 相邻级节点间的水平缩进，单位为像素（默认 16）；line-height: 设置行高（默认 32）；height: 设置树形组件高度；在设置 virtualRender=true时，请指定高度，避免组件自动计算高度导致多次渲染；level-line: 设置层级连线, 可通过true|false设置默认开启|关闭，也可以直接设置`1px dashed #c3cd（默认 false）
- 事件：node-click: 节点点击事件；node-collapse: 节点收起事件；node-expand: 节点展开事件；node-checked: 节点勾选事件；node-drag-start: 节点拖拽开始事件
- 插槽：#default: 默认自定义节点插槽, #default插槽与 #node插槽二选一即可，两者区别为参数格式不同，其他功能一致；#node: 自定义节点；#nodeType: 节点类型Icon；#nodeAppend: 自定义节点后面的扩展展示
- 方法：handleTreeNodeClick: 节点点击；isNodeChecked: 判定指定节点是否选中；isRootNode: 判定指定节点是否为根节点；isNodeOpened: 判定指定节点是否展开
- 检索触发词：Tree 树, bkui-vue, 组件, tree