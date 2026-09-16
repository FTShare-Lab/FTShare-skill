#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/eastmoney-us-stock-list"

_REQUEST_HEADERS = {"Content-Type": "application/json"}

def safe_urlopen(request):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    base = urllib.parse.urlparse(BASE_URL)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        print("Invalid URL for safe_urlopen", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    return urllib.request.urlopen(request, timeout=30)

def fetch(params):
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    base = urllib.parse.urlparse(BASE_URL)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        print("Invalid URL for safe_urlopen", file=sys.stderr)
        raise SystemExit(1)
    request = urllib.request.Request(url, headers={"FTSHARE_API_KEY": key, "Content-Type": "application/json"}, method="GET")
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
    parser = argparse.ArgumentParser(description="查询东方财富美股列表")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", dest="page_size", type=int)
    parser.add_argument("--all", action="store_true", dest="fetch_all")
    args = parser.parse_args()
    if args.page < 1 or (args.page_size is not None and args.page_size < 1):
        parser.error("page 和 page-size 必须大于等于 1")
    params = {"page": 1 if args.fetch_all else args.page}
    if args.refresh:
        params["refresh"] = "true"
    if args.page_size is not None:
        params["page_size"] = args.page_size
    result = fetch(params)
    if args.fetch_all:
        data = result.get("data") or {}
        records = list(data.get("records", []))
        for page in range(2, int(data.get("pages", 1)) + 1):
            records.extend((fetch({**params, "page": page}).get("data") or {}).get("records", []))
        result["data"] = {**data, "records": records}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
