#!/usr/bin/env python3
"""查询指定交易日全部普通 A 股的日 K 快照"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}

def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
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

ENDPOINT = "/api/v1/market/data/stock-candlesticks-daily"


def fetch_page(trade_date: str, page: int, page_size: int) -> dict:
    params = {"trade_date": trade_date, "page": page, "page_size": page_size}
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询指定交易日全部普通 A 股的日 K 快照")
    parser.add_argument("--trade_date", required=True, help="交易日 YYYYMMDD，且必须是交易日")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page_size", type=int, default=200, help="每页数量，默认 200，最大 500")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取当日全部日 K")
    args = parser.parse_args()

    if args.fetch_all:
        first = fetch_page(args.trade_date, 1, args.page_size)
        data = first.get("data") or {}
        records = list(data.get("records", []))
        total_pages = data.get("pages") or 1
        for page in range(2, total_pages + 1):
            page_data = fetch_page(args.trade_date, page, args.page_size)
            records.extend((page_data.get("data") or {}).get("records", []))
        result = {
            "records": records,
            "pages": total_pages,
            "total": data.get("total", len(records)),
        }
    else:
        result = fetch_page(args.trade_date, args.page, args.page_size)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
