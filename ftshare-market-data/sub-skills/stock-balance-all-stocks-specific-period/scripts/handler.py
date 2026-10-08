#!/usr/bin/env python3
"""查询指定报告期全市场资产负债表（分页）"""
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

VALID_REPORT_TYPES = ["q1", "q2", "q3", "annual"]


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询指定报告期全市场资产负债表（分页）")
    parser.add_argument("--stock-code", dest="stock_code", default=None,
                        help="股票代码（模式A），如 000001.SZ；存在则查该票所有报告期；不传则按模式B 用 --year + --report-type 查全市场")
    parser.add_argument("--year", type=int, default=None, help="报告所属年度，如 2025（模式B 必填）")
    parser.add_argument("--report-type", default=None, choices=VALID_REPORT_TYPES,
                        help="报告期类型：q1（一季报）/ q2（半年报）/ q3（三季报）/ annual（年报）（模式B 必填）")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页记录数（默认 20）")
    args = parser.parse_args()

    if args.stock_code:
        params = {"stock_code": args.stock_code}
    elif args.year is not None and args.report_type is not None:
        params = {
            "year": args.year,
            "report_type": args.report_type,
            "page": args.page,
            "page_size": args.page_size,
        }
    else:
        parser.error("必须传 --stock-code，或同时传入 --year 和 --report-type")
    url = f"{BASE_URL}/api/v1/market/data/finance/balance?" + urllib.parse.urlencode(params)

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
