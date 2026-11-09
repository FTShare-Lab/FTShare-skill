#!/usr/bin/env python3
"""查询上海黄金交易所（SGE）现货/延期品种主档全量列表。

- 不传参数返回全部 19 只品种（含已下架）。
- category 可选 spot_full / spot_forward / spot_deferred。
- active_only 传 true 时仅返回活跃品种。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/sge-spot-description-all"
CATEGORIES = ["spot_full", "spot_forward", "spot_deferred"]


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(req_or_url, timeout=30):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    for key, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req_or_url, timeout=timeout)


def build_params(args):
    params = {}
    if args.category is not None:
        params["category"] = args.category
    if args.active_only:
        params["active_only"] = "true"
    return params


def fetch(params):
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    request = urllib.request.Request(
        BASE_URL + ENDPOINT + query,
        headers={**_REQUEST_HEADERS, "X-Client-Name": "ft-claw"},
        method="GET",
    )
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询上金所现货/延期品种主档全量列表")
    parser.add_argument("--category", choices=CATEGORIES, default=None,
                        help="品种分类：spot_full / spot_forward / spot_deferred；不传返回全部分类")
    parser.add_argument("--active-only", dest="active_only", action="store_true",
                        help="仅返回活跃品种（17 只）；不传返回全部（含已下架）")
    args = parser.parse_args()

    result = fetch(build_params(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
