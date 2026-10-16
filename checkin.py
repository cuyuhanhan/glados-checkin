import json
import os
import sys
import urllib.request

COOKIE = os.environ.get("GLADOS_COOKIE", "").strip()
if not COOKIE:
    sys.exit("错误: 未设置 GLADOS_COOKIE 环境变量")

BASE = "https://glados.rocks/api/user"


def request(path, payload=None):
    headers = {
        "Cookie": COOKIE if COOKIE.startswith("koa:sess") else f"koa:sess={COOKIE}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://glados.rocks",
        "Referer": "https://glados.rocks/console/checkin",
    }
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    # 签到
    result = request("/checkin", {"token": "glados.network"})
    code = result.get("code")
    message = result.get("message", "")
    if code != 0:
        sys.exit(f"签到失败: code={code}, message={message}")
    print(f"签到结果: {message}")

    # 查询剩余天数
    status = request("/status")
    left_days = status.get("data", {}).get("leftDays", "未知")
    print(f"剩余天数: {left_days}")


if __name__ == "__main__":
    main()
