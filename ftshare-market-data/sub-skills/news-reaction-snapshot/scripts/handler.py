#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v3/market/data/news-reaction-snapshot"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"Content-Type": "application/json", "X-Client-Name": "ft-claw"}
LOOKBACK_HOURS = (24, 48)


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
        request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)


def fetch(params):
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="消息量价共振")
    parser.add_argument("--symbol", required=True, help="股票代码，带交易所后缀，如 600519.SH")
    parser.add_argument("--start-date", dest="start_date", required=True, help="起始交易日（含）")
    parser.add_argument("--end-date", dest="end_date", required=True, help="截止交易日（含），跨度不超过 31 天")
    parser.add_argument("--lookback-hours", dest="lookback_hours", type=int, choices=LOOKBACK_HOURS,
                        help="新闻回看窗口（小时），仅 24 或 48；不传返回两套窗口")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1，最大 1000")
    parser.add_argument("--page-size", dest="page_size", type=int, default=50, help="每页条数，默认 50，最大 200")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页返回全部记录")
    args = parser.parse_args()
    if not 1 <= args.page <= 1000 or not 1 <= args.page_size <= 200:
        parser.error("page 须在 1～1000 之间，page-size 须在 1～200 之间")

    base = {"symbol": args.symbol, "start_date": args.start_date, "end_date": args.end_date}
    if args.lookback_hours is not None:
        base["lookback_hours"] = args.lookback_hours

    result = fetch({**base, "page": 1 if args.fetch_all else args.page, "page_size": args.page_size})
    if args.fetch_all:
        data = result.get("data") or {}
        records = list(data.get("records", []))
        for page in range(2, int(data.get("pages", 1)) + 1):
            records.extend((fetch({**base, "page": page, "page_size": args.page_size}).get("data") or {}).get("records", []))
        result["data"] = {**data, "records": records}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
