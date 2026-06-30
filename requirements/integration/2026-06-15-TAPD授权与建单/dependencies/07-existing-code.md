# 现网已有封装

> 编码前应检查的复用点，避免重复造轮子。

| 现网文件 | 封装内容 | 复用建议 |
|----------|----------|----------|
| `bkmonitor/api/tapd/default.py` -> `TapdAPIResource` | app 级 Basic Auth 客户端，含 `get_granted_workspaces`、`get_workspace_info`、建单资源 | **直接复用** `get_workspace_info` 和 `get_granted_workspaces`；新增接口可复用同一基类 |
| `fta_web/issue/resources.py:1302` -> `ListTapdWorkspaceResource` | 用户态项目列表查询（B-01 前身） | **改名区分**：拆分为 `ListUserVisibleTapdWorkspaceResource`（Bearer）和 `ListGrantedTapdWorkspaceResource`（Basic） |

---

## DEMO 验证脚本

前置条件：

```bash
# 1. 设置环境变量
export TAPD_CLIENT_ID="your_app_id"
export TAPD_CLIENT_SECRET="your_app_secret"
export TAPD_REDIRECT_URI="https://your-callback.com/callback"

# 2. 安装依赖
pip install requests
```

验证脚本模板（`__assets__/verify_tapd_api.py`）：

```python
import os
import base64
import requests

CLIENT_ID = os.environ.get("TAPD_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TAPD_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("请设置 TAPD_CLIENT_ID 和 TAPD_CLIENT_SECRET 环境变量")

# 构造 Basic Auth headers
credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}

# 验证1: get_granted_workspaces
def test_get_granted_workspaces():
    url = "http://apiv2.tapd.woa.com/app_auth/get_granted_workspaces"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get("status") == 1:
            print(f"get_granted_workspaces: {len(data['data']['list'])} 个已授权项目")
            return True
    except Exception as e:
        print(f"get_granted_workspaces 失败: {e}")
        return False

# 验证2: get_workspace_info (需配置一个已知的 workspace_id)
def test_get_workspace_info(workspace_id=""):
    if not workspace_id:
        print("跳过 get_workspace_info（未提供 workspace_id）")
        return True
    url = f"http://apiv2.tapd.woa.com/workspaces/get_workspace_info?workspace_id={workspace_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get("status") == 1:
            print(f"get_workspace_info: {data['data']['Workspace']['name']}")
            return True
    except Exception as e:
        print(f"get_workspace_info 失败: {e}")
        return False

if __name__ == "__main__":
    print("TAPD API 连通性测试")
    test_get_granted_workspaces()
```
