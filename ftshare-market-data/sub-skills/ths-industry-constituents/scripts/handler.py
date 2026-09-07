#!/usr/bin/env python3
"""查询同花顺行业成分股列表"""
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



def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询同花顺行业成分股列表")
    parser.add_argument("--industry-code", default=None, help="同花顺行业代码，精确匹配，如 881157")
    parser.add_argument("--industry-name", default=None, help="同花顺行业名称，精确匹配，如 证券")
    parser.add_argument("--stock-code", default=None, help="股票代码，精确匹配，如 600905")
    parser.add_argument("--stock-name", default=None, help="股票名称，精确匹配，如 三峡能源")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=100, help="每页数量，默认 100，最大 1000")
    args = parser.parse_args()

    params = {
        "industry_code": args.industry_code,
        "industry_name": args.industry_name,
        "stock_code": args.stock_code,
        "stock_name": args.stock_name,
        "page": args.page,
        "page_size": args.page_size,
    }
    params = {key: value for key, value in params.items() if value is not None}
    url = f"{BASE_URL}/api/v1/market/data/ths-industry-constituents?" + urllib.parse.urlencode(params)

    try:
        with safe_urlopen(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(body, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
