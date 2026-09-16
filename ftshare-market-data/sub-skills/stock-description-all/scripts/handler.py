#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/stock-description"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {
    "FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"],
    "Content-Type": "application/json",
} if os.environ.get("FTSHARE_API_KEY") else {"Content-Type": "application/json"}


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, method="GET")
    _require_api_key()
    for key, value in _REQUEST_HEADERS.items():
        request.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(request, timeout=timeout)


def main():
    parser = argparse.ArgumentParser(description="查询股票基础信息")
    parser.add_argument("--symbol-id")
    parser.add_argument("--page", type=int)
    parser.add_argument("--page-size", type=int)
    args = parser.parse_args()
    params = {
        "symbol_id": args.symbol_id,
        "page": args.page,
        "page_size": args.page_size,
    }
    query = urllib.parse.urlencode({key: value for key, value in params.items() if value is not None})
    request = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}?{query}" if query else f"{BASE_URL}{ENDPOINT}",
        headers={"X-Client-Name": "ft-claw", "Content-Type": "application/json"},
        method="GET",
    )
    try:
        with safe_urlopen(request) as response:
            payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
