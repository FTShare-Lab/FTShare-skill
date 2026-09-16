#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/holder/stock-ggmx"
_REQUEST_HEADERS = {
    "FTSHARE_API_KEY": os.environ.get("FTSHARE_API_KEY", ""),
    "Content-Type": "application/json",
}


def fetch(params):
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        print("Invalid URL for safe_urlopen", file=sys.stderr)
        raise SystemExit(1)
    request = urllib.request.Request(
        url,
        headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": key},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description="查询董监高持股变动")
    parser.add_argument("--stock-code", dest="stock_code")
    parser.add_argument("--change-direction", dest="change_direction")
    parser.add_argument("--start-date", dest="start_date")
    parser.add_argument("--end-date", dest="end_date")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", dest="page_size", type=int, default=50)
    parser.add_argument("--all", action="store_true", dest="fetch_all")
    args = parser.parse_args()
    if args.page < 1 or not 1 <= args.page_size <= 200:
        parser.error("page 须大于等于 1，page-size 须在 1～200 之间")
    params = {
        "page": 1 if args.fetch_all else args.page,
        "page_size": args.page_size,
    }
    for name in ("stock_code", "change_direction", "start_date", "end_date"):
        value = getattr(args, name)
        if value is not None:
            params[name] = value
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
