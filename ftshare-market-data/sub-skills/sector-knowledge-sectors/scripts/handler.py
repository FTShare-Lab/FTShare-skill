#!/usr/bin/env python3
"""板块描述列表（GET /api/v3/market/data/sector-knowledge/sectors）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v3/market/data/sector-knowledge/sectors"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}

SECTOR_TYPES = ("industry", "concept", "region", "index_style", "macro_asset")
MARKETS = ("CN", "US", "HK", "KR", "JP", "global")


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


def build_params(args):
    params = {}
    if args.market is not None:
        params["market"] = args.market
    if args.sector_type is not None:
        params["sector_type"] = args.sector_type
    if args.name_keyword is not None:
        params["name_keyword"] = args.name_keyword
    return params


def fetch(params):
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{BASE_URL}{ENDPOINT}" + (f"?{query}" if query else "")
    request = urllib.request.Request(url, headers={**HEADERS, **_REQUEST_HEADERS}, method="GET")
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
    parser = argparse.ArgumentParser(description="板块描述列表：按市场、板块类型和名称关键词筛选板块标准名")
    parser.add_argument("--market", default=None, help="市场过滤：CN/US/HK/KR/JP/global")
    parser.add_argument("--sector-type", dest="sector_type", default=None, help="板块类型过滤：industry/concept/region/index_style/macro_asset")
    parser.add_argument("--name-keyword", dest="name_keyword", default=None, help="板块标准名或别名关键词，最多返回 10 个候选，最长 100 字符")
    args = parser.parse_args()

    if args.market is not None and args.market not in MARKETS:
        print(f"--market 取值须为 {'/'.join(MARKETS)}", file=sys.stderr)
        raise SystemExit(2)
    if args.sector_type is not None and args.sector_type not in SECTOR_TYPES:
        print(f"--sector-type 取值须为 {'/'.join(SECTOR_TYPES)}", file=sys.stderr)
        raise SystemExit(2)

    print(json.dumps(fetch(build_params(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()