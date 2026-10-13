#!/usr/bin/env python3
"""查询单只沪深北 A 股在指定交易日的基础行情、估值、股本及技术面因子。

- symbol 必填，须带交易所后缀（SH/SZ/BJ，兼容 XSHG/XSHE/BJSE）。
- trade_date 选填，格式 YYYYMMDD；不传时按当前日期处理。
- category 选填，用于按分类返回字段；不传返回全部字段。
"""
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

ENDPOINT = "/api/v2/market/data/stock-factor"

CATEGORIES = ["quote", "valuation", "capital", "trend", "momentum", "volatility", "volume", "sentiment"]


def build_params(args):
    params = {"symbol": args.symbol}
    if args.trade_date is not None:
        params["trade_date"] = args.trade_date
    if args.category is not None:
        params["category"] = args.category
    return params


def fetch(params):
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询股票技术面因子")
    parser.add_argument("--symbol", required=True, help="沪深北 A 股代码，须带交易所后缀，如 000001.SZ")
    parser.add_argument("--trade-date", dest="trade_date", default=None, help="目标日期 YYYYMMDD；不传按当前日期处理")
    parser.add_argument("--category", choices=CATEGORIES, default=None, help="返回字段分类；不传返回全部字段")
    args = parser.parse_args()

    result = fetch(build_params(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
