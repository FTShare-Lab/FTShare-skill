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
ENDPOINT = "/api/v3/market/data/ashare-rating-factor-snapshot"
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


def main():
    _require_api_key()
    parser = argparse.ArgumentParser()
    parser.add_argument("--trade-code", required=True)
    parser.add_argument("--date")
    parser.add_argument("--top-k", type=int)
    args = parser.parse_args()
    params = {"trade_code": args.trade_code}
    if args.date is not None:
        params["date"] = args.date
    if args.top_k is not None:
        params["top_k"] = args.top_k
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    try:
        with safe_urlopen(request) as response:
            result = json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
