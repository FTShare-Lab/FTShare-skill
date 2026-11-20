#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v3/market/data/ashare-rating-factor-snapshot"
_REQUEST_HEADERS = {"X-Client-Name": "ft-claw", "Content-Type": "application/json"}
if os.environ.get("FTSHARE_API_KEY"):
    _REQUEST_HEADERS["FTSHARE_API_KEY"] = os.environ["FTSHARE_API_KEY"]
OPENER = urllib.request.build_opener()


def safe_urlopen(request):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    return OPENER.open(request, timeout=60)


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
    parser = argparse.ArgumentParser(description="查询 A 股相关性快照")
    parser.add_argument("--trade-code", help="目标股票代码；省略时返回当日全市场")
    parser.add_argument("--date", help="快照日期 YYYYMMDD；省略时使用最新交易日")
    parser.add_argument("--top-k", type=int, help="每只股票返回的相关公司数量，默认 10，范围 1–10")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", type=int, default=200, help="每页股票数，默认 200，最大 500")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页取回全部结果")
    args = parser.parse_args()

    if args.page < 1:
        print("--page 必须 >= 1", file=sys.stderr)
        raise SystemExit(2)
    if not 1 <= args.page_size <= 500:
        print("--page-size 必须在 1~500 之间", file=sys.stderr)
        raise SystemExit(2)
    if args.top_k is not None and not 1 <= args.top_k <= 10:
        print("--top-k 必须在 1~10 之间", file=sys.stderr)
        raise SystemExit(2)

    base = {}
    if args.trade_code is not None:
        base["trade_code"] = args.trade_code
    if args.date is not None:
        base["date"] = args.date
    if args.top_k is not None:
        base["top_k"] = args.top_k

    result = fetch({**base, "page": 1 if args.fetch_all else args.page, "page_size": args.page_size})
    if args.fetch_all:
        data = result.get("data") or {}
        records = list(data.get("records", []))
        for page in range(2, int(data.get("pages", 1)) + 1):
            more = fetch({**base, "page": page, "page_size": args.page_size})
            records.extend((more.get("data") or {}).get("records", []))
        result["data"] = {**data, "records": records}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()