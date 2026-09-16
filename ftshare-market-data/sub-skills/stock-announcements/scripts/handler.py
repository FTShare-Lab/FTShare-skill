#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v2/market/data/announcements/stock-announcements"
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
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)


def main():
    key = _require_api_key()
    parser = argparse.ArgumentParser(description="查询 A 股公告列表")
    parser.add_argument("--stock-code", dest="stock_code")
    parser.add_argument("--start-date", dest="start_date")
    parser.add_argument("--end-date", dest="end_date")
    parser.add_argument("--type", default="stock")
    parser.add_argument("--page", type=int, required=True)
    parser.add_argument("--page-size", dest="page_size", type=int, required=True)
    args = parser.parse_args()
    if not args.stock_code and not args.start_date:
        parser.error("stock-code 与 start-date 至少提供一个")
    if args.type != "stock":
        parser.error("type 当前只支持 stock")
    params = {"type": args.type, "page": args.page, "page_size": args.page_size}
    for name in ("stock_code", "start_date", "end_date"):
        value = getattr(args, name)
        if value is not None:
            params[name] = value
    request = urllib.request.Request(BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params),
                                     headers={"FTSHARE_API_KEY": key, "X-Client-Name": "ft-claw", "Content-Type": "application/json"}, method="GET")
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
