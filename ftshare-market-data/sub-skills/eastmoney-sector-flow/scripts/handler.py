#!/usr/bin/env python3
"""东方财富板块资金流（GET /api/v1/market/data/eastmoney-sector-flow）"""
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
ENDPOINT = "/api/v1/market/data/eastmoney-sector-flow"

BOARD_TYPES = ("industry", "concept", "regional")

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


def build_params(args):
    params = {}
    if args.board_code is not None:
        params["board_code"] = args.board_code
    if args.board_type is not None:
        params["board_type"] = args.board_type
    if args.board_level is not None:
        params["board_level"] = args.board_level
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
    parser = argparse.ArgumentParser(description="东方财富板块（行业/概念/地域）日资金流")
    parser.add_argument("--board-code", dest="board_code", default=None,
                        help="板块代码，如 BK0488")
    parser.add_argument("--board-type", dest="board_type", default=None, choices=BOARD_TYPES,
                        help="板块类型：industry（行业）/concept（概念）/regional（地域）")
    parser.add_argument("--board-level", dest="board_level", type=int, default=None,
                        help="行业层级：1=一级、2=二级、3=三级；不传返回全部层级，仅匹配 industry")
    parser.add_argument("--trade-date", dest="trade_date", default=None, help="交易日 YYYYMMDD")
    parser.add_argument("--start-date", dest="start_date", default=None, help="区间起始日 YYYYMMDD")
    parser.add_argument("--end-date", dest="end_date", default=None, help="区间结束日 YYYYMMDD")
    parser.add_argument("--page", type=int, default=None, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", dest="page_size", type=int, default=None,
                        help="每页条数，默认 50，最大 500")
    args = parser.parse_args()

    print(json.dumps(fetch(build_params(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
