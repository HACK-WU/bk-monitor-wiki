# GitNexus 配置指南

> 指导如何安装、配置和使用 GitNexus 进行代码分析和嵌入向量化。

## 触发场景

- 用户要求配置 GitNexus 环境
- 用户询问如何安装 GitNexus
- 用户需要设置 GitNexus 的嵌入 API
- 用户想要分析项目代码结构

## 安装 GitNexus

GitNexus 是一个基于 Node.js 的代码分析工具，需要通过 npm 全局安装。

### 前置条件

1. **Node.js 环境**：确保已安装 Node.js 16+ 和 npm
   ```bash
   node --version  # 应显示 v16.x 或更高
   npm --version   # 应显示 8.x 或更高
   ```

2. **全局安装 GitNexus**：
   ```bash
   npm install -g gitnexus
   ```

3. **验证安装**：
   ```bash
   gitnexus --version
   ```

## 环境变量配置

GitNexus 需要配置嵌入 API 的环境变量。这些环境变量可以在 shell 配置文件中设置。

### 获取 API 密钥

1. 访问 [SiliconFlow 控制台](https://cloud.siliconflow.cn/account/ak)
2. 注册或登录账号
3. 创建 API 密钥
4. 复制生成的 API 密钥（格式：`sk-...`）

### Linux/macOS 配置

在 `~/.bashrc`、`~/.zshrc` 或 `~/.profile` 中添加以下内容：

```bash
# GitNexus 嵌入 API 配置
export GITNEXUS_EMBEDDING_URL="https://api.siliconflow.cn"
export GITNEXUS_EMBEDDING_MODEL="Qwen/Qwen3-Embedding-8B"
export GITNEXUS_EMBEDDING_API_KEY="your-api-key-here"
export GITNEXUS_EMBEDDING_DIMS="4096"

# GitNexus 性能配置
export GITNEXUS_WORKER_POOL_SIZE=10
export GITNEXUS_VERBOSE=1
```

### 环境变量说明

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `GITNEXUS_EMBEDDING_URL` | 嵌入 API 服务地址 | `https://api.siliconflow.cn` |
| `GITNEXUS_EMBEDDING_MODEL` | 使用的嵌入模型 | `Qwen/Qwen3-Embedding-8B` |
| `GITNEXUS_EMBEDDING_API_KEY` | API 密钥 | `your-api-key-here` |
| `GITNEXUS_EMBEDDING_DIMS` | 嵌入向量维度 | `4096` |
| `GITNEXUS_WORKER_POOL_SIZE` | 并行工作线程数 | `10` |
| `GITNEXUS_VERBOSE` | 详细输出模式 | `1` (启用) / `0` (禁用) |

## 使用 GitNexus

### 项目分析

进入项目根目录，运行分析命令：

```bash
cd /path/to/your/project
gitnexus analyze --embeddings
```

### 分析选项

| 选项 | 说明 |
|------|------|
| `--embeddings` | 生成代码嵌入向量 |
| `--verbose` | 显示详细分析过程 |