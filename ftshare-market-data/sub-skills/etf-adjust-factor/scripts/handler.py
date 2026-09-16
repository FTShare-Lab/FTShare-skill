#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/etf-adjust-factor"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}


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
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)


def main():
    key = _require_api_key()
    parser = argparse.ArgumentParser(description="查询 ETF 复权因子")
    parser.add_argument("--symbol")
    parser.add_argument("--trade-date")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()
    if args.page < 1 or not 1 <= args.page_size <= 2000:
        parser.error("page 须 >= 1，page-size 须在 1～2000 之间")
    if bool(args.start_date) != bool(args.end_date):
        parser.error("start-date 与 end-date 必须同时提供")
    if args.start_date and not args.symbol:
        parser.error("区间扫描必须提供 symbol")
    params = {"page": args.page, "page_size": args.page_size}
    for name in ("symbol", "trade_date", "start_date", "end_date"):
        value = getattr(args, name)
        if value:
            params[name] = value
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"FTSHARE_API_KEY": key, "X-Client-Name": "ft-claw", "Content-Type": "application/json"}, method="GET")
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
