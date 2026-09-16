#!/usr/bin/env python3
"""查询 A 股十大流通股东。

两种模式：
1) 指定 stock_code：返回该标的全部历史十大流通股东（不分页）。
2) is_last=true：返回所有标的最新一期十大流通股东（分页）。
"""
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

ENDPOINT = "/api/v1/market/data/holder/stock-holder-ften"


def build_params(stock_code, is_last, page, page_size):
    params = {}
    if stock_code:
        params["stock_code"] = stock_code
    if is_last:
        params["is_last"] = "true"
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    return params


def fetch(
stock_code, is_last, page, page_size):
    params = urllib.parse.urlencode(build_params(stock_code, is_last, page, page_size))
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
    parser = argparse.ArgumentParser(description="查询 A 股十大流通股东")
    parser.add_argument(
        "--stock_code",
        help="股票代码，需携带市场后缀，如 603323.SH / 000001.SZ / 833171.BJ；不传时需配合 --is_last",
    )
    parser.add_argument(
        "--is_last",
        action="store_true",
        help="返回所有标的最新一期十大流通股东（分页）",
    )
    parser.add_argument("--page", type=int, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page_size", type=int, help="每页记录数（默认 50）")
    args = parser.parse_args()

    if not args.stock_code and not args.is_last:
        parser.error("需指定 --stock_code 或 --is_last 至少其一")

    result = fetch(args.stock_code, args.is_last, args.page, args.page_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
