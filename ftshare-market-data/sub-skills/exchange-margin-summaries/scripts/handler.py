#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/exchange-margin-summaries"
_REQUEST_HEADERS = {"X-Client-Name": "ft-claw", "Content-Type": "application/json"}
if os.environ.get("FTSHARE_API_KEY"):
    _REQUEST_HEADERS["FTSHARE_API_KEY"] = os.environ["FTSHARE_API_KEY"]
OPENER = urllib.request.build_opener()


def safe_urlopen(request):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    return OPENER.open(request, timeout=60)


def fetch(
page, page_size, start_date, end_date, exchange=None):
    params = {"start_date": start_date, "end_date": end_date, "page": page, "page_size": page_size}
    if exchange:
        params["exchange"] = exchange
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--exchange")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--all", action="store_true", dest="fetch_all")
    args = parser.parse_args()
    result = fetch(args.page, args.page_size, args.start_date, args.end_date, args.exchange)
    if args.fetch_all:
        records = list(result.get("records", result.get("items", [])))
        pages = result.get("pages", result.get("total_pages", 1))
        for page in range(args.page + 1, pages + 1):
            next_page = fetch(page, args.page_size, args.start_date, args.end_date, args.exchange)
            records.extend(next_page.get("records", next_page.get("items", [])))
        result["records"] = records
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
