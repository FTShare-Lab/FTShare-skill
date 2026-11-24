#!/usr/bin/env python3
"""期货主力合约映射（GET /api/v1/market/data/futures/dominant-mapping）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/futures/dominant-mapping"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


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


def _parse_date(value, flag):
    try:
        return datetime.strptime(value, "%Y%m%d")
    except ValueError:
        print(f"{flag} 必须为 YYYYMMDD 格式", file=sys.stderr)
        raise SystemExit(2)


def build_params(args):
    params = {"trade_date": args.trade_date}
    if args.rule_version is not None:
        params["rule_version"] = args.rule_version
    return params


def fetch(params):
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{BASE_URL}{ENDPOINT}?{query}"
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
    parser = argparse.ArgumentParser(description="期货主力合约映射：按生效交易日查询各交易所各品种的主力合约")
    parser.add_argument("--trade-date", dest="trade_date", required=True, help="主力映射生效交易日，格式 YYYYMMDD")
    parser.add_argument("--rule-version", dest="rule_version", default=None, help="主力规则版本：v1/v2/v3/v4，默认 v1；区分大小写")
    args = parser.parse_args()

    _parse_date(args.trade_date, "--trade-date")

    print(json.dumps(fetch(build_params(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()