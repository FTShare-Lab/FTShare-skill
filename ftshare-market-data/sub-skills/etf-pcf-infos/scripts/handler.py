#!/usr/bin/env python3
"""ETF 申赎清单 PCF 汇总信息（GET /api/v2/market/data/etf-pcf/etf-pcf-infos）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v2/market/data/etf-pcf/etf-pcf-infos"

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base_parsed = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base_parsed.scheme or parsed.netloc != base_parsed.netloc:
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


def build_query(args):
    params = {}
    if args.symbol is not None:
        params["symbol"] = args.symbol
    if args.trade_date is not None:
        params["trade_date"] = args.trade_date
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    if args.page is not None:
        params["page"] = args.page
    if args.page_size is not None:
        params["page_size"] = args.page_size
    return params


def fetch(params):
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    req = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}{query}",
        headers={**HEADERS, **_REQUEST_HEADERS},
        method="GET",
    )
    try:
        with safe_urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(
        description="ETF 申赎清单（PCF 汇总信息）：单标的单日 / 全市场单日分页 / 单标的日期区间"
    )
    parser.add_argument("--symbol", default=None, help="ETF 代码，如 510300.SH 或 510300.XSHG")
    parser.add_argument("--trade-date", dest="trade_date", type=int, default=None,
                        help="交易日 YYYYMMDD；单日查询时必填，不能与日期区间同用")
    parser.add_argument("--start-date", dest="start_date", type=int, default=None,
                        help="区间开始日期 YYYYMMDD；须与 --end-date、--symbol 同时提供")
    parser.add_argument("--end-date", dest="end_date", type=int, default=None,
                        help="区间结束日期 YYYYMMDD；须与 --start-date、--symbol 同时提供")
    parser.add_argument("--page", type=int, default=None, help="页码，从 1 开始，默认 1；分页查询有效")
    parser.add_argument("--page-size", dest="page_size", type=int, default=None,
                        help="每页条数，默认 50，最大 500；分页查询有效")
    args = parser.parse_args()

    if args.trade_date is not None and (args.start_date is not None or args.end_date is not None):
        print("--trade-date 不能与 --start-date/--end-date 同时使用", file=sys.stderr)
        raise SystemExit(2)

    print(json.dumps(fetch(build_query(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
