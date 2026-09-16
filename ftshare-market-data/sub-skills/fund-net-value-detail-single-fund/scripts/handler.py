#!/usr/bin/env python3
"""基金净值明细"""
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

ENDPOINT = "/api/v1/market/data/fund/fund-net-value"

def build_params(args):
    params = {}
    if args.fund_code is not None:
        params["fund_code"] = args.fund_code
    if args.nav_date is not None:
        params["nav_date"] = args.nav_date
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    if args.page is not None:
        params["page"] = args.page
    if args.page_size is not None:
        params["page_size"] = args.page_size
    return params

def fetch(
args):
    params = urllib.parse.urlencode(build_params(args))
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="基金净值明细")
    parser.add_argument("--fund_code", required=True, help="基金代码")
    parser.add_argument("--nav_date", type=int, required=False, help="净值日期 YYYYMMDD（与 start/end 互斥）")
    parser.add_argument("--start_date", type=int, required=False, help="净值开始日期 YYYYMMDD（需与 end_date 同传）")
    parser.add_argument("--end_date", type=int, required=False, help="净值结束日期 YYYYMMDD")
    parser.add_argument("--page", type=int, required=False, help="页码，默认 1")
    parser.add_argument("--page_size", type=int, required=False, help="每页记录数，默认 50，上限 200")
    args = parser.parse_args()

    result = fetch(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
