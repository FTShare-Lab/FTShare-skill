#!/usr/bin/env python3
"""查询中国内地（cn）或香港（hk）市场在指定闭区间内的交易日列表"""
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
ENDPOINT = "/api/v1/market/data/time/trading-calendar"


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


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询交易日历")
    parser.add_argument("--market", required=True, help="市场，仅支持 cn 或 hk")
    parser.add_argument("--start_date", type=int, required=True, help="起始日期（含），YYYYMMDD")
    parser.add_argument("--end_date", type=int, required=True, help="截止日期（含），YYYYMMDD")
    args = parser.parse_args()

    if args.market not in ("cn", "hk"):
        print("错误：--market 仅支持 cn 或 hk", file=sys.stderr)
        sys.exit(1)
    if args.end_date < args.start_date:
        print("错误：--start_date 不得晚于 --end_date", file=sys.stderr)
        sys.exit(1)

    qs = urllib.parse.urlencode({"market": args.market, "start_date": args.start_date, "end_date": args.end_date})
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
