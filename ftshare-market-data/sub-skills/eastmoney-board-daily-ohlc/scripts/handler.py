#!/usr/bin/env python3
"""查询东财单板块历史 OHLC 数据，支持日期范围过滤与分页"""
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

ENDPOINT = "/api/v1/market/data/eastmoney-board-daily-ohlc"


def fetch_page(board_code: str, page: int, page_size: int, start_date: str = None, end_date: str = None) -> dict:
    params = {"board_code": board_code, "page": page, "page_size": page_size}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
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
    parser = argparse.ArgumentParser(description="查询东财单板块历史 OHLC 数据")
    parser.add_argument("--board_code", required=True, help="板块代码，如 BK1024")
    parser.add_argument("--start_date", default=None, help="起始日期（含），格式 YYYY-MM-DD 或 YYYYMMDD")
    parser.add_argument("--end_date", default=None, help="截止日期（含），格式 YYYY-MM-DD 或 YYYYMMDD")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始）")
    parser.add_argument("--page_size", type=int, default=50, help="每页记录数")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.fetch_all:
        first = fetch_page(args.board_code, 1, args.page_size, args.start_date, args.end_date)
        all_items = list(first.get("items", []))
        total_pages = first.get("total_pages", 1)
        for p in range(2, total_pages + 1):
            page_data = fetch_page(args.board_code, p, args.page_size, args.start_date, args.end_date)
            all_items.extend(page_data.get("items", []))
        result = {
            "items": all_items,
            "total_pages": total_pages,
            "total_items": first.get("total_items", len(all_items)),
        }
    else:
        result = fetch_page(args.board_code, args.page, args.page_size, args.start_date, args.end_date)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
