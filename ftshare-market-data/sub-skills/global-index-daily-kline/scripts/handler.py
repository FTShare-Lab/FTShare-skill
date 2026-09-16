#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/global-index/daily-kline'
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr); raise SystemExit(2)
    return key
def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr); raise SystemExit(1)
    if not isinstance(request, urllib.request.Request): request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    request.add_unredirected_header("Content-Type", "application/json")
    return SAFE_URLOPENER.open(request, timeout=timeout)
def main():
    key = _require_api_key(); parser = argparse.ArgumentParser(description='全球指数日K线')
    parser.add_argument("--secid", required=True)
    parser.add_argument("--start_date")
    parser.add_argument("--end_date")
    parser.add_argument("--limit")
    parser.add_argument("--total", required=False)
    parser.add_argument("--items", required=False)
    parser.add_argument("--name", required=True)
    parser.add_argument("--trade_date", required=True)
    parser.add_argument("--open", required=False)
    parser.add_argument("--close", required=False)
    parser.add_argument("--high", required=False)
    parser.add_argument("--low", required=False)
    parser.add_argument("--volume", required=False)
    parser.add_argument("--amount", required=False)
    parser.add_argument("--amplitude", required=True)
    parser.add_argument("--change_pct", required=False)
    parser.add_argument("--change_amount", required=False)
    parser.add_argument("--turnover", required=False)
    args = parser.parse_args()
    params = {}
    if args.secid is not None: params["secid"] = args.secid
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.limit is not None: params["limit"] = args.limit
    if args.total is not None: params["total"] = args.total
    if args.items is not None: params["items"] = args.items
    if args.name is not None: params["name"] = args.name
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.open is not None: params["open"] = args.open
    if args.close is not None: params["close"] = args.close
    if args.high is not None: params["high"] = args.high
    if args.low is not None: params["low"] = args.low
    if args.volume is not None: params["volume"] = args.volume
    if args.amount is not None: params["amount"] = args.amount
    if args.amplitude is not None: params["amplitude"] = args.amplitude
    if args.change_pct is not None: params["change_pct"] = args.change_pct
    if args.change_amount is not None: params["change_amount"] = args.change_amount
    if args.turnover is not None: params["turnover"] = args.turnover
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    request = urllib.request.Request(BASE_URL + ENDPOINT + query, headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": key, "Content-Type": "application/json", "X-Client-Name": "ft-claw"}, method="GET")
    try:
        with safe_urlopen(request) as response: payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr); raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr); raise SystemExit(1)
if __name__ == "__main__": main()
