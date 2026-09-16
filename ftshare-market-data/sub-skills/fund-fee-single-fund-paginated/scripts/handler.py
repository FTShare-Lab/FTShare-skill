#!/usr/bin/env python3
"""基金费率"""
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

ENDPOINT = "/api/v1/market/data/fund/fund-fee"

def build_params(args):
    params = {}
    if args.fund_code is not None:
        params["fund_code"] = args.fund_code
    if args.charge_type is not None:
        params["charge_type"] = args.charge_type
    if args.client_type is not None:
        params["client_type"] = args.client_type
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
    parser = argparse.ArgumentParser(description="基金费率")
    parser.add_argument("--fund_code", required=True, help="基金代码（如 000001 或 000001.OF）")
    parser.add_argument("--charge_type", required=False, help="费率类型：日常申购费/日常赎回费/认购费/管理费/托管费/销售服务费")
    parser.add_argument("--client_type", required=False, help="客户类型：一般/机构/养老金/REITs")
    parser.add_argument("--page", type=int, required=False, help="页码，默认 1")
    parser.add_argument("--page_size", type=int, required=False, help="每页记录数，默认 50，上限 200")
    args = parser.parse_args()

    result = fetch(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
