#!/usr/bin/env python3
"""查询股票跨日分时行情（GET /api/v4/market/data/stock-intraday）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v4/market/data/stock-intraday"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}

RANGES = ("Today", "FiveDays")


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
    for key, value in _REQUEST_HEADERS.items():
        request.add_unredirected_header(key, value)
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)


def build_query(symbol, range_value, days, ts_ms):
    params = {"symbol": symbol}
    if range_value is not None:
        params["range"] = range_value
    if days is not None:
        params["days"] = days
    if ts_ms is not None:
        params["ts_ms"] = ts_ms
    return params


def main():
    key = _require_api_key()
    parser = argparse.ArgumentParser(description="查询股票跨日分时行情（逐分钟价格、均价、日累计量额）")
    parser.add_argument("--symbol", required=True, help="股票代码，需带市场后缀，如 600000.SH、000001.SZ")
    parser.add_argument("--range", dest="range_value", choices=RANGES, default=None,
                        help="预置区间：Today（当日）/FiveDays（当日及此前 4 个交易日，默认）")
    parser.add_argument("--days", type=int, default=None,
                        help="查询当日及此前 N-1 个交易日，范围 1～5；与 --range 同时传入时以 --days 为准")
    parser.add_argument("--ts-ms", dest="ts_ms", type=int, default=None,
                        help="当日过滤起点（毫秒，包含起点）；不能用于指定历史日期")
    args = parser.parse_args()

    if args.days is not None and not 1 <= args.days <= 5:
        print("--days 须在 1～5 之间", file=sys.stderr)
        raise SystemExit(2)

    params = build_query(args.symbol, args.range_value, args.days, args.ts_ms)
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": key, "X-Client-Name": "ft-claw", "Content-Type": "application/json"},
        method="GET",
    )
    try:
        with safe_urlopen(request) as response:
            print(json.dumps(json.loads(response.read().decode()), ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()