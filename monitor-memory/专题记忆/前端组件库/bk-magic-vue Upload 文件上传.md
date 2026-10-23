---
groupPath: 专题记忆/前端组件库
relation: bk-magic-vue Upload 文件上传
exportedAt: "2026-10-19T08:03:17.158Z"
---
【前端组件｜Upload 文件上传】
- 所属组件库：bk-magic-vue；文档源：.codebuddy/skills/bk-magicbox-vue-components/references/upload.md
- 使用：Vue2 全局注册，直接写 <bk-upload>（monitor-pc 的 import-magicbox-ui 统一注册；apm/fta 复用 pc 注册）
- 适用：monitor-pc / apm / fta-solutions（Vue2）
- 属性：theme: 上传组件类型（默认 'draggable'）；accept: 可选的文件类型。theme为 picture时且accept没有配置时，可接受文件文类型为：'image/pn；url: 服务器地址（必传）（默认 0）；header: 请求头 `{ name: " ", value: " " }`；handle-res-code: 处理返回码的函数，默认参数 response，需要返回 true 或 false（默认 true）；multiple: 是否支持多选（默认 true）；name: 后台读取文件的 key（默认 'upload_file'）；size: 限制上传文件体积 `{ maxFileSize: 1, maxImgSize: 1 }`（默认 5(MB)）
- 事件：on-done: 所有文件上传完毕后的事件；on-progress: 文件上传进行时的事件；on-success: 文件上传成功后的事件；on-error: 文件上传失败后的事件；on-exceed: 文件上传个数超出限制后的事件
- 检索触发词：Upload 文件上传, bk-magic-vue, 组件, upload