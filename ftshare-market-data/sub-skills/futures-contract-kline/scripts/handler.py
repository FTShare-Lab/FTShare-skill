#!/usr/bin/env python3
"""期货行情：期货合约日/周/月/季/年 K 线（GET /api/v1/market/data/futures/kline）"""
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
ENDPOINT = "/api/v1/market/data/futures/kline"

INTERVALS = (
    "daily", "1d",
    "weekly", "1w", "week",
    "monthly", "1mo", "month",
    "quarterly", "1q", "quarter",
    "yearly", "1y", "year",
)

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
    params = {
        "symbol": args.symbol,
        "interval": args.interval,
    }
    if args.start is not None:
        params["start"] = args.start
    if args.end is not None:
        params["end"] = args.end
    if args.limit is not None:
        params["limit"] = args.limit
    return params


def fetch(params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}?{query}",
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
    parser = argparse.ArgumentParser(description="查询期货合约日/周/月/季/年 K 线")
    parser.add_argument("--symbol", required=True,
                        help="期货合约代码，如 A2605.DCE；支持交易所短后缀")
    parser.add_argument("--interval", default="daily", choices=INTERVALS,
                        help="K 线周期，默认 daily；周/月/季/年 K 基于日 K 按北京时间聚合")
    parser.add_argument("--start", type=int, default=None,
                        help="起始时间戳（毫秒，闭区间）；可省略时间范围")
    parser.add_argument("--end", type=int, default=None,
                        help="结束时间戳（毫秒，闭区间）；不能单独传入")
    parser.add_argument("--limit", type=int, default=None,
                        help="返回条数，默认 500；最小值 1，传 0 时按 1 处理")
    args = parser.parse_args()

    if args.end is not None and args.start is None:
        print("--end 不能单独传入，必须与 --start 同时使用", file=sys.stderr)
        raise SystemExit(2)

    print(json.dumps(fetch(build_params(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
