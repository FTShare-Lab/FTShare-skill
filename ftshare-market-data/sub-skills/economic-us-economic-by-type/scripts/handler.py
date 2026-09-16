#!/usr/bin/env python3
"""美国经济指标按 type 查询（统一接口）"""
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


VALID_TYPES = [
    "ism-manufacturing",
    "ism-non-manufacturing",
    "nonfarm-payroll",
    "trade-balance",
    "unemployment-rate",
    "ppi-mom",
    "cpi-mom",
    "cpi-yoy",
    "core-cpi-mom",
    "core-cpi-yoy",
    "housing-starts",
    "existing-home-sales",
    "durable-goods-orders-mom",
    "cb-consumer-confidence",
    "gdp-yoy-preliminary",
    "fed-funds-rate-upper",
]


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(
        description="按 type 查询美国经济指标，返回时间序列（前值、现值、发布日期）"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=VALID_TYPES,
        help="指标类型，如 ism-manufacturing, nonfarm-payroll, cpi-mom 等",
    )
    args = parser.parse_args()

    params = {"type": args.type}
    url = f"{BASE_URL}/api/v1/market/data/economic/us-economic?" + urllib.parse.urlencode(params)

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
