---
groupPath: 专题记忆/前端组件库
relation: bkui-vue Upload 文件上传
exportedAt: "2026-10-19T08:03:17.157Z"
---
【前端组件｜Upload 文件上传】
- 所属组件库：bkui-vue；文档源：.codebuddy/skills/bkui-vue-components/references/Form/upload.md
- 导入：import { Upload } from 'bkui-vue'（Vue3 按需引入，禁止全局 Vue.use）
- 适用：src/trace（Vue3）
- 属性：type: 上传类型。formdata为表单形式上传，文件流包裹在表单数据中。binary为纯文件流传输。（默认 formdata）；theme: 上传组件类型（默认 draggable）；accept: 可选的文件类型。theme为 picture 时且 accept 没有配置时，可接受文件文类型为："image；url: 服务器地址（必传）；header: 请求头 { name: " ", value: " " }；handle-res-code: 处理返回码的函数，默认参数 response，需要返回 true 或 false；multiple: 是否支持多选（默认 true）；name: 后台读取文件的 key（默认 upload_file）
- 事件：done: 所有文件上传完毕后的事件；progress: 文件上传进行时的事件；success: 文件上传成功后的事件；error: 文件上传失败后的事件；exceed: 文件上传个数超出限制后的事件
- 插槽：default: 自定义默认内容；trigger: 触发文件选择框的内容；tip: 提示说明文字；file: 文件列表项内容
- 检索触发词：Upload 文件上传, bkui-vue, 组件, upload