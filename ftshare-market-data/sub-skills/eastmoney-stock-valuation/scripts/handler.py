#!/usr/bin/env python3
"""查询东财个股日估值数据，支持单票、单日、区间查询与分页"""
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

ENDPOINT = "/api/v1/market/data/eastmoney-stock-valuation"


def fetch(
symbol: str = None, trade_date: str = None, start_date: str = None,
          end_date: str = None, page: int = 1, page_size: int = 50) -> dict:
    params = {"page": page, "page_size": page_size}
    if symbol:
        params["symbol"] = symbol
    if trade_date:
        params["trade_date"] = trade_date
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
    parser = argparse.ArgumentParser(description="查询东财个股日估值数据")
    parser.add_argument("--symbol", default=None, help="股票代码，6位数字，如 000001")
    parser.add_argument("--trade_date", default=None, help="交易日，格式 YYYY-MM-DD")
    parser.add_argument("--start_date", default=None, help="区间起始日，格式 YYYY-MM-DD")
    parser.add_argument("--end_date", default=None, help="区间结束日，格式 YYYY-MM-DD")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始，默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页条数（默认 50，最大 500）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.fetch_all:
        first = fetch(args.symbol, args.trade_date, args.start_date, args.end_date, 1, args.page_size)
        data = first.get("data") or {}
        records = list(data.get("records", []))
        total_pages = data.get("pages", 1)
        for p in range(2, total_pages + 1):
            page_data = fetch(args.symbol, args.trade_date, args.start_date, args.end_date, p, args.page_size)
            pdata = page_data.get("data") or {}
            records.extend(pdata.get("records", []))
        result = {
            "code": first.get("code", 0),
            "message": first.get("message", "success"),
            "data": {
                "pageNum": 1,
                "pageSize": args.page_size,
                "total": len(records),
                "pages": 1,
                "records": records,
            },
        }
    else:
        result = fetch(args.symbol, args.trade_date, args.start_date, args.end_date, args.page, args.page_size)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
