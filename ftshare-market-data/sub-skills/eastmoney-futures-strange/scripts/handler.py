#!/usr/bin/env python3
"""查询东方财富期货龙虎榜面板（成交量/持仓量多空排名等），按交易所/品种/合约/交易日"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/eastmoney-futures-strange"


def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(req_or_url)


def main():
    parser = argparse.ArgumentParser(description="查询东方财富期货龙虎榜面板")
    parser.add_argument("--exchange", required=True, help="交易所代码：shfe/dce/czce/cffex/ine/gfe")
    parser.add_argument("--variety", required=True, help="品种名称，如 多晶硅")
    parser.add_argument("--contract", required=True, help="合约代码，如 ps2609")
    parser.add_argument("--trade_date", required=True, help="交易日 YYYYMMDD")
    args = parser.parse_args()

    params = {
        "exchange": args.exchange,
        "variety": args.variety,
        "contract": args.contract,
        "trade_date": args.trade_date,
    }
    qs = urllib.parse.urlencode(params)
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
