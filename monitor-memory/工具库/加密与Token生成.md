---
groupPath: 工具库
relation: 加密与Token生成
keywords: [加密, AES]
exportedAt: "2026-06-24T12:13:09.586Z"
---
### 加密与安全工具

**文件**: `src/bk_monitor_base/metadata/utils/cipher.py`
- `transform_data_id_to_token()`: 将 data_id 加密为 bk.data.token
  - 格式: `${metric}[salt]${trace}[salt]${log}[salt]${biz}[salt]${app}`
  - 使用 AES 加密（密钥优先级: specify_aes_key > app_secret）
  - 依赖 `bk_monitor_base.infras.cipher.AESCipher`
  - `settings.metadata.bk_data_token_salt` 为分隔盐

**文件**: `src/bk_monitor_base/metadata/utils/dataflow_auth.py`
- 数据流认证工具

**文件**: `src/bk_monitor_base/metadata/utils/version.py`
- 版本号处理工具