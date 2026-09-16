#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/hk/stk-ah-comparison"
SAFE_URLOPENER = urllib.request.build_opener()


def require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def fetch(params):
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={"FTSHARE_API_KEY": require_api_key(), "Content-Type": "application/json"},
        method="GET",
    )
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    try:
        with SAFE_URLOPENER.open(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description="查询 AH 股比价")
    parser.add_argument("--hk-code", dest="hk_code")
    parser.add_argument("--ts-code", dest="ts_code")
    parser.add_argument("--trade-date", dest="trade_date", type=int)
    parser.add_argument("--start-date", dest="start_date", type=int)
    parser.add_argument("--end-date", dest="end_date", type=int)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", dest="page_size", type=int, default=50)
    parser.add_argument("--all", action="store_true", dest="fetch_all")
    args = parser.parse_args()
    if args.page < 1 or args.page_size < 1 or args.page_size > 1000:
        parser.error("page 须大于等于 1，page-size 须在 1～1000 之间")
    params = {k: v for k, v in vars(args).items() if k in {
        "hk_code", "ts_code", "trade_date", "start_date", "end_date"
    } and v is not None}
    if args.fetch_all:
        first = fetch({**params, "page": 1, "page_size": args.page_size})
        data = first.get("data") or {}
        records = list(data.get("records", []))
        for page in range(2, int(data.get("pages", 1)) + 1):
            payload = fetch({**params, "page": page, "page_size": args.page_size})
            records.extend((payload.get("data") or {}).get("records", []))
        first["data"] = {**data, "records": records}
        result = first
    else:
        result = fetch({**params, "page": args.page, "page_size": args.page_size})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
