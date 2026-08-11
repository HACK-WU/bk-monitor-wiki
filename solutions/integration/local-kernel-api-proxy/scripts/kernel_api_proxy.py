#!/usr/bin/env python3
"""本地 kernel_api 转发代理（本地测试专用，不属于主分支代码）。

背景：web 进程里 api.issue.rename 等调用默认走 APIGW 网关
（BK_COMPONENT_API_URL/api/bk-monitor/{stage}/app/issue/...），本地没有网关导致难以联调。
本脚本把 APIGW 对外路径 /app/* 重写为 kernel_api 路径 /api/v4/*，转发到本地 api 角色进程。

用法：
    python3 kernel_api_proxy.py --listen 18080

配置从项目根目录 .env 自动加载（也可用环境变量，环境变量优先级更高）：
    KERNEL_API_PROXY_TARGET  本地 api 角色进程地址（必填，域名需与鉴权 Host 一致）
    KERNEL_API_PROXY_COOKIE  附加的 Cookie（可选，不设置则不附加）
    --listen                 本地监听端口（默认 18080）

依赖：仅 Python 标准库（http.server / http.client），无需 pip install。
"""
import argparse
import http.client
import http.server
import os
import sys

# APIGW 对外路径前缀 → kernel_api 后端路径前缀
REWRITE_RULES = [
    ("/app/", "/api/v4/"),
]

# 不转发的 hop-by-hop 头
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}

# localhost 强制走 IPv4，避免解析到 ::1 导致 Cannot assign requested address
LOCALHOST_V4 = "127.0.0.1"


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _forward(self, method: str) -> None:
        # 1. 读取请求体
        content_length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(content_length) if content_length else None

        # 2. 重写路径：/app/issue/rename/ -> /api/v4/issue/rename/
        path = self.path
        for src, dst in REWRITE_RULES:
            if path.startswith(src):
                path = dst + path[len(src):]
                break

        # 3. 组装转发请求头（去掉 hop-by-hop）
        headers = {
            k: v
            for k, v in self.headers.items()
            if k.lower() not in HOP_BY_HOP_HEADERS
        }
        if body is not None:
            headers["Content-Length"] = str(len(body))

        # 4. 附加/覆盖 Cookie（配置了 cookie-file 时，统一用配置的，避免本地无会话）
        configured_cookie = self.server.cookie
        if configured_cookie is not None:
            headers["Cookie"] = configured_cookie

        # 5. 转发
        conn = http.client.HTTPConnection(
            self.server.target_host, self.server.target_port, timeout=300
        )
        try:
            conn.request(method, path, body=body, headers=headers)
            resp = conn.getresponse()
            resp_body = resp.read()
        except Exception as e:  # noqa: BLE001 - 本地代理，异常统一返回 502
            self.send_error(
                502,
                message=f"proxy to kernel_api failed: {e} "
                f"(target={self.server.target_host}:{self.server.target_port})",
            )
            return
        finally:
            conn.close()

        # 6. 回传响应
        self.send_response(resp.status)
        for k, v in resp.getheaders():
            if k.lower() not in HOP_BY_HOP_HEADERS:
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(resp_body)))
        self.end_headers()
        self.wfile.write(resp_body)

    do_GET = lambda self: self._forward("GET")  # noqa: E731
    do_POST = lambda self: self._forward("POST")  # noqa: E731
    do_PUT = lambda self: self._forward("PUT")  # noqa: E731
    do_DELETE = lambda self: self._forward("DELETE")  # noqa: E731
    do_PATCH = lambda self: self._forward("PATCH")  # noqa: E731

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[proxy] {self.command} {self.path} -> {fmt % args}\n")


def parse_target(target: str) -> tuple[str, int]:
    target = target.rstrip("/")
    if "://" in target:
        target = target.split("://", 1)[1]
    host, _, port = target.partition(":")
    if host in ("localhost", "::1"):
        host = LOCALHOST_V4
    return host, int(port or 80)


def load_dotenv(env_path: str) -> dict[str, str]:
    """加载 .env 文件（KEY=VALUE 格式，支持 # 注释与引号包裹），不覆盖已存在的环境变量。"""
    loaded: dict[str, str] = {}
    if not os.path.exists(env_path):
        return loaded
    with open(env_path, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            if key not in os.environ:
                os.environ[key] = value
                loaded[key] = value
    return loaded


def main():
    parser = argparse.ArgumentParser(description="本地 kernel_api 转发代理")
    parser.add_argument("--listen", type=int, default=18080, help="本地监听端口（默认 18080）")
    args = parser.parse_args()

    # 从项目根目录 .env 加载配置（脚本位于 devtools/ 下，根目录为其上一层）
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    loaded = load_dotenv(env_path)

    target = os.environ.get("KERNEL_API_PROXY_TARGET")
    if not target:
        sys.exit(
            "KERNEL_API_PROXY_TARGET is not set. Add it to .env or export it, "
            "e.g. KERNEL_API_PROXY_TARGET='http://bkm-dev.paas3-dev.bktencent.com:9000'"
        )

    server = http.server.ThreadingHTTPServer(("0.0.0.0", args.listen), ProxyHandler)
    server.target_host, server.target_port = parse_target(target)
    server.cookie = os.environ.get("KERNEL_API_PROXY_COOKIE")

    print(f"[proxy] .env loaded: {env_path} ({len(loaded)} new vars)")
    print(f"[proxy] listening on :{args.listen} -> {server.target_host}:{server.target_port}")
    print(f"[proxy] rewrite rules: {REWRITE_RULES}")
    print(f"[proxy] cookie: {'configured' if server.cookie else '(none)'}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[proxy] stopped")


if __name__ == "__main__":
    main()
