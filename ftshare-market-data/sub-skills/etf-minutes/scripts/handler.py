#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v2/market/data/etf_minutes"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}


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


def main():
    key = _require_api_key()
    parser = argparse.ArgumentParser(description="查询 ETF 历史分钟行情")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--interval-value", dest="interval_value", type=int, default=1)
    parser.add_argument("--adjust-kind", dest="adjust_kind")
    parser.add_argument("--since-ts-millis", dest="since_ts_millis", required=True, type=int)
    parser.add_argument("--until-ts-millis", dest="until_ts_millis", required=True, type=int)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    if args.interval_value <= 0 or not 1 <= args.limit <= 1000:
        parser.error("interval-value 须大于 0，limit 须在 1～1000 之间")
    params = {"symbol": args.symbol, "interval_value": args.interval_value,
              "since_ts_millis": args.since_ts_millis, "until_ts_millis": args.until_ts_millis,
              "limit": args.limit}
    if args.adjust_kind is not None:
        params["adjust_kind"] = args.adjust_kind
    request = urllib.request.Request(BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params),
                                     headers={"FTSHARE_API_KEY": key, "X-Client-Name": "ft-claw", "Content-Type": "application/json"}, method="GET")
    try:
        with safe_urlopen(request) as response:
            print(json.dumps(json.loads(response.read().decode()), ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
