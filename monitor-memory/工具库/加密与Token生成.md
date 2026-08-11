加密与安全工具集，提供 data_id 到 bk.data.token 的 AES 加密、数据流认证及版本号处理能力。

将 data_id 加密为 bk.data.token 的 AES 加密工具。
- 符号: `transform_data_id_to_token()`
- 位置: `src/bk_monitor_base/metadata/utils/cipher.py`
- 说明:
  - 格式: `${metric}[salt]${trace}[salt]${log}[salt]${biz}[salt]${app}`
  - 使用 AES 加密（密钥优先级: specify_aes_key > app_secret）
  - 依赖 `bk_monitor_base.infras.cipher.AESCipher`
  - `settings.metadata.bk_data_token_salt` 为分隔盐

数据流认证工具。
- 位置: `src/bk_monitor_base/metadata/utils/dataflow_auth.py`

版本号处理工具。
- 位置: `src/bk_monitor_base/metadata/utils/version.py`
