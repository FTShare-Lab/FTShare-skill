#!/usr/bin/env python3
"""查询百度财经日历。"""
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
ENDPOINT = "/api/v1/market/data/finance/financial-calendar/baidu"


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
    parser = argparse.ArgumentParser(description="查询百度财经日历")
    parser.add_argument("--start-date", required=True, help="开始日期，格式 YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="结束日期，格式 YYYY-MM-DD")
    parser.add_argument(
        "--category",
        choices=("economic", "ipo", "report_time", "trade_reminder"),
        default=None,
        help="可选事件分类",
    )
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始")
    parser.add_argument("--page-size", dest="page_size", type=int, default=50, help="每页条数，最大 200")
    args = parser.parse_args()

    params = {
        "start_date": args.start_date,
        "end_date": args.end_date,
        "category": args.category,
        "page": args.page,
        "page_size": args.page_size,
    }
    query = urllib.parse.urlencode({key: value for key, value in params.items() if value is not None})
    request = urllib.request.Request(f"{BASE_URL}{ENDPOINT}?{query}", method="GET", headers=_REQUEST_HEADERS)

    try:
        with safe_urlopen(request) as response:
            payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
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


if __name__ == "__main__":
    main()
