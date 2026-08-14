---
groupPath: 关联关系/外部API集成专题
relation: cmsi-8通道-apigw_esb动态切换
exportedAt: "2026-08-14T07:53:01.837Z"
---
[强关联] cmsi 8通道通知 与 apigw/esb 动态切换 + GetMsgType 虚拟通道
强度：必改——改 CMSIBaseResource 的 base_url property 或 GetMsgType 的通道补充逻辑时，所有通知接口的发送路径全变
原因：cmsi 的 base_url 在 apigw/esb/自定义间动态切换，8 种通知通道 + GetMsgType 补虚拟通道

源端（动态基类与通知通道）:
- `CMSIBaseResource` @ `bkmonitor/api/cmsi/default.py`
- `base_url` property: 在 apigw/esb/自定义间动态切换
- 8 种通知通道: `SendMsg`(通用)/`SendWeixin`(微信)/`SendMail`(邮件，内外部用户@tai分流)/`SendSms`(短信)/`SendVoice`(语音)/`SendWecomRobot`/`SendWecomAPP`(企微)/`SendRtx`
- `GetMsgType`: 通知类型查询，补虚拟通道（wxwork-bot/bkchat）

目标端（消费方）:
- `bkmonitor/utils/send.py` — 通知发送工具，消费 `api.cmsi.send_mail` 等
- 各告警通知流程根据 GetMsgType 返回的通道列表选择发送方式