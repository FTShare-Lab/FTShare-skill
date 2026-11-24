#!/usr/bin/env python3
"""板块知识检索选项（GET /api/v3/market/data/sector-knowledge/search-options）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v3/market/data/sector-knowledge/search-options"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)


def fetch():
    request = urllib.request.Request(f"{BASE_URL}{ENDPOINT}", headers={**HEADERS, **_REQUEST_HEADERS}, method="GET")
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="板块知识检索选项：返回板块事实与板块洞察的分类、匹配字段及板块类型/市场/排序允许值")
    parser.parse_args()
    print(json.dumps(fetch(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()