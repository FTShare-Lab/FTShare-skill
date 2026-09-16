#!/usr/bin/env python3
"""查询 A 股市场股权质押汇总。"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


SAFE_URLOPENER = urllib.request.build_opener()
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/pledge/pledge-summary"


def safe_urlopen(req_or_url):
    url = req_or_url.full_url if isinstance(req_or_url, urllib.request.Request) else str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(str(req_or_url), headers=_REQUEST_HEADERS, method="GET")
    if isinstance(req_or_url, urllib.request.Request):
        for key, value in _REQUEST_HEADERS.items():
            req_or_url.add_unredirected_header(key, value)
    else:
        req_or_url = urllib.request.Request(str(req_or_url), headers=_REQUEST_HEADERS, method="GET")
    return SAFE_URLOPENER.open(req_or_url)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询 A 股市场股权质押汇总")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始")
    parser.add_argument("--page-size", dest="page_size", type=int, default=50, help="每页条数，最大 200")
    args = parser.parse_args()

    query = urllib.parse.urlencode({"page": args.page, "page_size": args.page_size})
    request = urllib.request.Request(f"{BASE_URL}{ENDPOINT}?{query}", method="GET", headers=_REQUEST_HEADERS)
    try:
        with safe_urlopen(request) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        body = error.read().decode().strip()
        message = f"HTTP {error.code}"
        if body:
            message += f": {body}"
        print(message, file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        sys.exit(1)

    data = payload.get("data") if isinstance(payload, dict) else None
    records = data.get("records") if isinstance(data, dict) else None
    if not isinstance(records, list):
        print(json.dumps({"error": "unexpected response shape"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
