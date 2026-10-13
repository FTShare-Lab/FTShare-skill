#!/usr/bin/env python3
"""查询 A 股代码变更时间线。

无入参，全量返回全部代码变更事件（换码后新代码、换码前旧代码及各启用区间），不分页。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/stk_code_change_timeline"
_REQUEST_HEADERS = {"Content-Type": "application/json"}


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(request):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    return urllib.request.urlopen(request, timeout=30)


def fetch():
    key = _require_api_key()
    url = f"{BASE_URL}{ENDPOINT}"
    try:
        request = urllib.request.Request(
            url,
            headers={"FTSHARE_API_KEY": key, "Content-Type": "application/json"},
            method="GET",
        )
        with safe_urlopen(request) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}", file=sys.stderr)
        raise SystemExit(1)


def main():
    argparse.ArgumentParser(description="查询 A 股代码变更时间线（无参数，全量返回）").parse_args()
    print(json.dumps(fetch(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
